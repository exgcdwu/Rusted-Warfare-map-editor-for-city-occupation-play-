from copy import deepcopy
import numpy as np

import rwmap._frame as frame

def _save_matrix_s(matrix_s:np.ndarray, mat_rect_s:frame.Rectangle, in_matrix_s:np.ndarray, tilerec_s:frame.Rectangle):
    matrix_s[mat_rect_s.i().x():mat_rect_s.e().x(), mat_rect_s.i().y():mat_rect_s.e().y()] = \
        in_matrix_s[tilerec_s.i().x():tilerec_s.e().x(), tilerec_s.i().y():tilerec_s.e().y()]
    
def _save_matrix_exclude0_s(matrix_s:np.ndarray, mat_rect_s:frame.Rectangle, in_matrix_s:np.ndarray, tilerec_s:frame.Rectangle):
    in_matrix_s_now = in_matrix_s[tilerec_s.i().x():tilerec_s.e().x(), tilerec_s.i().y():tilerec_s.e().y()]
    condition = in_matrix_s_now != 0
    matrix_sn = matrix_s[mat_rect_s.i().x():mat_rect_s.e().x(), mat_rect_s.i().y():mat_rect_s.e().y()]
    matrix_sn[condition] = in_matrix_s_now[condition]



def _change_save_matrix_condition(matrix_s:np.ndarray, pos:frame.Coordinate, in_matrix:np.ndarray, tilerec:frame.Rectangle = None):
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
             return []

        return [matrix_s, pos_nn, in_matrix_n, tilerec_nnn]

def save_matrix(matrix_s:np.ndarray, pos:frame.Coordinate, in_matrix:np.ndarray, tilerec:frame.Rectangle = None):
     listn = _change_save_matrix_condition(matrix_s, pos, in_matrix, tilerec)
     if listn == []:
          return
     _save_matrix_s(listn[0], listn[1], listn[2], listn[3])

def save_matrix_exclude0(matrix_s:np.ndarray, pos:frame.Coordinate, in_matrix:np.ndarray, tilerec:frame.Rectangle = None):
     listn = _change_save_matrix_condition(matrix_s, pos, in_matrix, tilerec)
     if listn == []:
          return
     _save_matrix_exclude0_s(listn[0], listn[1], listn[2], listn[3])


