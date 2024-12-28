from copy import deepcopy
import numpy as np
from typing import Callable
import math

import rwmap._frame as frame

import rwmap._util._png_rel as pngrel

def _save_matrix_s(matrix_s:np.ndarray, mat_rect_s:frame.Rectangle, in_matrix_s:np.ndarray, tilerec_s:frame.Rectangle):
    matrix_s[mat_rect_s.i().x():mat_rect_s.e().x(), mat_rect_s.i().y():mat_rect_s.e().y()] = \
        in_matrix_s[tilerec_s.i().x():tilerec_s.e().x(), tilerec_s.i().y():tilerec_s.e().y()]
    
def _save_matrix_exclude0_s(matrix_s:np.ndarray, mat_rect_s:frame.Rectangle, in_matrix_s:np.ndarray, tilerec_s:frame.Rectangle, exclude:int = 0):
    in_matrix_s_now = in_matrix_s[tilerec_s.i().x():tilerec_s.e().x(), tilerec_s.i().y():tilerec_s.e().y()]
    condition = in_matrix_s_now != exclude
    matrix_sn = matrix_s[mat_rect_s.i().x():mat_rect_s.e().x(), mat_rect_s.i().y():mat_rect_s.e().y()]
    matrix_sn[condition] = in_matrix_s_now[condition]



def change_save_matrix_condition(matrix_s:np.ndarray, pos:frame.Coordinate, in_matrix:np.ndarray, tilerec:frame.Rectangle = None)->tuple[frame.Rectangle, np.ndarray, frame.Rectangle]:
        in_matrix_n = deepcopy(in_matrix)
        if tilerec == None:
            tilerec_n = frame.Rectangle(frame.Coordinate(0, 0), frame.Coordinate(in_matrix_n.shape[0], in_matrix_n.shape[1]))
        else:
            tilerec_n = deepcopy(tilerec)
        tilerec_nn = frame.Rectangle.init_ae(
            frame.Coordinate(max(0, tilerec_n.i().x()), max(0, tilerec_n.i().y())), 
            frame.Coordinate(min(in_matrix_n.shape[0], tilerec_n.e().x()), 
                             min(in_matrix_n.shape[1], tilerec_n.e().y()))
        )

        initial_change = tilerec_nn.i() - tilerec_n.i()

        pos_n = frame.Rectangle(pos + initial_change, tilerec_nn.a())

        pos_nn = frame.Rectangle.init_ae(
            frame.Coordinate(max(0, pos_n.i().x()), max(0, pos_n.i().y())), 
            frame.Coordinate(min(matrix_s.shape[0], pos_n.e().x()), 
                             min(matrix_s.shape[1], pos_n.e().y()))
        )
        posi_change = pos_nn.i() - pos_n.i()

        tilerec_nnn = frame.Rectangle(tilerec_nn.i() + posi_change, pos_nn.a())

        if pos_nn.a().x() <= 0 or pos_nn.a().y() <= 0:
             return ()

        return (pos_nn, in_matrix_n, tilerec_nnn)

def save_matrix(matrix_s:np.ndarray, pos:frame.Coordinate, in_matrix:np.ndarray, tilerec:frame.Rectangle = None):
    tuplen = change_save_matrix_condition(matrix_s, pos, in_matrix, tilerec)
    if tuplen == ():
        return
    _save_matrix_s(matrix_s, tuplen[0], tuplen[1], tuplen[2])

def save_matrix_exclude0(matrix_s:np.ndarray, pos:frame.Coordinate, in_matrix:np.ndarray, tilerec:frame.Rectangle = None, exclude = 0):
    tuplen = change_save_matrix_condition(matrix_s, pos, in_matrix, tilerec)
    if tuplen == ():
        return
    _save_matrix_exclude0_s(matrix_s, tuplen[0], tuplen[1], tuplen[2], exclude)

def scale_nparr(matrix_s:np.ndarray, scale_size:frame.Coordinate)->np.ndarray:
    from scipy.ndimage import zoom
    scale_factor = [scale_size.x(), scale_size.y(), 1]
    zoomed_array = zoom(matrix_s, zoom = scale_factor, order = 0, grid_mode = True, mode = 'reflect')
    return zoomed_array

class Bezier(Callable):
    def __init__(self, points:np.ndarray, t:np.ndarray):
        t_matrix = np.ndarray([t.shape[0], t.shape[0]], np.float64)
        for i, tm in np.ndenumerate(t_matrix):
            t_matrix[i] = t[i[1]] ** i[0]

        self._bezier_m = points.transpose() @ np.linalg.inv(t_matrix)

    def __call__(self, t_now:float):
        tn = self._bezier_m.shape[1]
        tl = np.ndarray([tn], np.float64)
        for i in range(tn):
            tl[i] = t_now ** i
        return self._bezier_m @ tl


def cubic_m(points:np.ndarray, t:np.ndarray)->Callable:
    from scipy.interpolate import CubicSpline
    cs = CubicSpline(t, points, bc_type = 'clamped')
    return cs

class Segment(Callable):
    def __init__(self, points:np.ndarray, t_arr:np.ndarray):
        self._points = points.astype(np.float64)
        self._t_arr = t_arr

    def __call__(self, t_now:float):
        for i in range(len(self._t_arr) - 1):
            if t_now >= self._t_arr[i] and t_now <= self._t_arr[i + 1]:
                return (self._points[i] + (t_now - self._t_arr[i]) / (self._t_arr[i + 1] - self._t_arr[i]) * (self._points[i + 1] - self._points[i])).transpose()

def scale_nparr_l(colorl:np.ndarray, colorr:np.ndarray, noisel:list[float], noiser:list[float], delta_l:float, delta_x:float, delta_c:float, scale_size:frame.Coordinate, randseed:int = -1)->np.ndarray:
    colorml = delta_l * (1 - delta_c) * (colorr - colorl) + colorl
    colormr = (delta_c + delta_l * (1 - delta_c)) * (colorr - colorl) + colorl
    points = np.concatenate([colorl.reshape([-1, 1]), colorml.reshape([-1, 1]), colormr.reshape([-1, 1]), colorr.reshape([-1, 1])], axis = 1).transpose()
    points_nc = np.array([0, delta_l * (1 - delta_c), (delta_c + delta_l * (1 - delta_c)), 1])

    t_arr = np.array([0, delta_l * (1 - delta_x), delta_x + delta_l * (1 - delta_x), 1])
    bezier_now = Bezier(points, t_arr)
    cubic_now = cubic_m(points, t_arr)
    segment_now = Segment(points, t_arr)
    nparr_ans = np.ndarray([scale_size.x(), scale_size.y(), colorl.shape[0]], np.uint8)

    isdebug = False
    if isdebug:
        import matplotlib.pyplot as plt
        import pdb;pdb.set_trace()
        num = 1000
        sl = 0
        sr = 1
        for j in range(3):
            plt.figure()
            plt.plot([i / num *(sr - sl) + sl for i in range(num + 1)], [segment_now(i / num *(sr - sl) + sl)[j] for i in range(num + 1)], '-')
            plt.plot(t_arr, points[:, j], '.')
            plt.show()

    dis = np.ndarray((scale_size.x(), scale_size.y()), np.float64)
    done = np.ones((scale_size.x(), scale_size.y()))
    for i in range(scale_size.x()):
        for j in range(scale_size.y()):
            disn = (j + 0.5) / scale_size.y()
            dis[i, j] = disn
            color = segment_now(disn).astype(np.uint8)
            
            nparr_ans[i, j] = color.reshape([1, 1, colorl.shape[0]])

    nparr_ans = pngrel.add_hsv_gaussian_noisel(nparr_ans, [noisel, noiser], [dis, done - dis], randseed = randseed)

    return nparr_ans

def scale_nparr_lt(colorl:np.ndarray, colorr:np.ndarray, noisel:list[float], noiser:list[float], delta_l:float, delta_x:float, delta_c:float, scale_size:frame.Coordinate, randseed:int = -1)->np.ndarray:
    colorml = delta_l * (1 - delta_c) * (colorr - colorl) + colorl
    colormr = (delta_c + delta_l * (1 - delta_c)) * (colorr - colorl) + colorl
    points = np.concatenate([colorl.reshape([-1, 1]), colorml.reshape([-1, 1]), colormr.reshape([-1, 1]), colorr.reshape([-1, 1])], axis = 1).transpose()
    t_arr = np.array([0, delta_l * (1 - delta_x), delta_x + delta_l * (1 - delta_x), 1])
    segment_now = Segment(points, t_arr)
    nparr_ans = np.ndarray([scale_size.x(), scale_size.y(), colorl.shape[0]], np.uint8)

    dis = np.ndarray((scale_size.x(), scale_size.y()), np.float64)
    done = np.ones((scale_size.x(), scale_size.y()))

    for i in range(scale_size.x()):
        for j in range(scale_size.y()):
            disn = np.sqrt((((i + 0.5) / scale_size.x()) ** 2 + ((j + 0.5) / scale_size.y()) ** 2))
            dis[i, j] = disn
            if disn <= 1:
                color = segment_now(disn).astype(np.uint8)
                nparr_ans[i, j] = color.reshape([1, 1, colorl.shape[0]])
            else:
                nparr_ans[i, j] = colorr.reshape([1, 1, colorr.shape[0]])


    nparr_ans = pngrel.add_hsv_gaussian_noisel(nparr_ans, [noisel, noiser], [dis, done - dis], randseed = randseed)

    return nparr_ans

def memory_continuous_nparr(matrix_s:np.ndarray)->np.ndarray:
    if not matrix_s.flags['C_CONTIGUOUS']:
        matrix_s = np.ascontiguousarray(matrix_s)
    return matrix_s

