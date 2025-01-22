import os
import sys
import argparse
import regex as re

from copy import deepcopy
import numpy as np
from typing import Callable
import time
import math
import subprocess
import warnings
import itertools

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
current_ste_path = os.path.dirname(current_dir_path)
command_dir_path = os.path.dirname(current_ste_path)
package_dir = os.path.dirname(command_dir_path)

sys.path.append(package_dir)

import rwmap as rw
from command._util import *

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)

def generate_permutations(n):
    # 创建一个从 0 到 n-1 的列表
    numbers = list(range(n))
    # 生成全排列
    permutations = list(itertools.permutations(numbers))
    return permutations

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, p):
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP == rootQ:
            return False
        if self.rank[rootP] > self.rank[rootQ]:
            self.parent[rootQ] = rootP
        elif self.rank[rootP] < self.rank[rootQ]:
            self.parent[rootP] = rootQ
        else:
            self.parent[rootQ] = rootP
            self.rank[rootP] += 1
        return True


def random(l:int, r:int):
    return int(np.random.rand() * (r - l) + l)

def random_in_round(size_o:rw.frame.Coordinate, range:float)->rw.frame.Coordinate:
    while True:
        rx = np.random.rand()
        ry = np.random.rand()
        if math.sqrt((2 * rx - 1) ** 2 + (2 * ry - 1) ** 2) <= range:
            return rw.frame.Coordinate(round(rx * size_o.x()), round(ry * size_o.y()))

MAX_GET_RANDOM_NODE = 1

def get_random_node(language, isverbose, ori_node_list:list[rw.frame.Coordinate], node_num:int, min_node_dis:float, size_t:rw.frame.Coordinate, star_range:float)->list[rw.frame.Coordinate]:
    node_list = deepcopy(ori_node_list)

    for i in range(node_num):
        iscycle = True
        time_now = time.time()
        while iscycle:
            node = random_in_round(size_t, star_range)
            iscycle = False
            for node_now in node_list:
                node_dis = (node_now - node).dis()
                if node_dis < min_node_dis:
                    iscycle = True
                    break
            time_end = time.time()
            time_dur = time_end - time_now
            if time_dur >= MAX_GET_RANDOM_NODE:
                standard_out(language, isverbose, f"        Node production failed, reproduction..." + 
                f"|        星系生成失败，重新处理...")
                return None
        node_list.append(node)
    return node_list

def on_segment(p, q, r):
    # 判断点q是否在点p和点r之间的线段上
    if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
        return True
    return False

def orientation(p, q, r):
    # 计算向量pqr的叉乘结果，用来判断pqr的相对位置
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # 共线
    elif val > 0:
        return 1  # 逆时针
    else:
        return 2  # 顺时针

def do_intersect(p1, q1, p2, q2):
    # 判断两条线段p1q1和p2q2是否相交
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # 如果相对位置不同，则线段相交
    if (o1 != o2 and o3 != o4):
        return True

    # 如果一个点在另一条线段上，则线段相交
    if (o1 == 0 and on_segment(p1, p2, q1)) or \
       (o2 == 0 and on_segment(p1, q2, q1)) or \
       (o3 == 0 and on_segment(p2, p1, q2)) or \
       (o4 == 0 and on_segment(p2, q1, q2)):
        return True

    return False

def get_node_edge_mindis(node_list:list[rw.frame.Coordinate], edge_num:int, node_num:int)->list[tuple[int, int]]:
    edge_list = [[(nodei - nodej).dis(), (i, j)] for i, nodei in enumerate(node_list) for j, nodej in enumerate(node_list) if i < j]
    edge_list.sort(key=lambda x: x[0])
    union_now = UnionFind(len(edge_list))
    edge_list_ans = []
    e_now = 0
    edge_list_is = np.zeros(len(edge_list), dtype = np.bool_)
    for i in range(len(edge_list)):
        if e_now >= node_num - 1:
            break

        iscross = False
        for et in edge_list_ans:
            if not (et[0] == edge_list[i][1][0] or et[0] == edge_list[i][1][1] or et[1] == edge_list[i][1][0] or et[1] == edge_list[i][1][1]) and \
                do_intersect(node_list[et[0]].output_tuple(), node_list[et[1]].output_tuple(), 
                            node_list[edge_list[i][1][0]].output_tuple(), 
                            node_list[edge_list[i][1][1]].output_tuple()):
                iscross = True
                break
        if iscross:
            continue

        if union_now.find(edge_list[i][1][0]) != union_now.find(edge_list[i][1][1]):
            edge_list_is[i] = True
            union_now.union(edge_list[i][1][0], edge_list[i][1][1])
            e_now = e_now + 1
            edge_list_ans.append(edge_list[i][1])
    for i in range(len(edge_list)):
        if e_now >= edge_num:
            break

        iscross = False
        for et in edge_list_ans:
            if not (et[0] == edge_list[i][1][0] or et[0] == edge_list[i][1][1] or et[1] == edge_list[i][1][0] or et[1] == edge_list[i][1][1]) and \
                do_intersect(node_list[et[0]].output_tuple(), node_list[et[1]].output_tuple(), 
                            node_list[edge_list[i][1][0]].output_tuple(), 
                            node_list[edge_list[i][1][1]].output_tuple()):
                iscross = True
                break
        if iscross:
            continue

        if edge_list_is[i] == False:
            e_now = e_now + 1
            edge_list_ans.append(edge_list[i][1])
    return edge_list_ans

def write_ftl_edge(nparr:np.ndarray, node1:rw.frame.Coordinate, node2:rw.frame.Coordinate, edge_id:int):
    minx = min(node1.x(), node2.x())
    maxx = max(node1.x(), node2.x())
    miny = min(node1.y(), node2.y())
    maxy = max(node1.y(), node2.y())
    npmx = nparr.shape[0]
    npmy = nparr.shape[1]
    if minx != maxx:
        kn = (node2.y() - node1.y()) / (node2.x() - node1.x())
        for x in range(math.floor(minx), math.ceil(maxx)):
            ny = round((x - node1.x()) * kn + node1.y())
            if x >= 0 and ny >= 0 and x < npmx and ny < npmy:
                nparr[x, ny] = edge_id
    if miny != maxy:
        kn_1 = (node2.x() - node1.x()) / (node2.y() - node1.y())
        for y in range(math.floor(miny), math.ceil(maxy)):
            nx = round((y - node1.y()) * kn_1 + node1.x())
            if nx >= 0 and y >= 0 and nx < npmx and y < npmy:
                nparr[nx, y] = edge_id

def write_ftl_edge_mul(nparr:np.ndarray, node1:rw.frame.Coordinate, node2:rw.frame.Coordinate, edge_id:int, edge_width:float):
    node_sub = node2 - node1
    node_unit = node_sub.vertical().unit()
    node1_n = node1.changetype(np.float64) - node_unit * edge_width
    node2_n = node2.changetype(np.float64) - node_unit * edge_width
    for i in range(math.ceil(2 * edge_width)):
        write_ftl_edge(nparr, node1_n, node2_n, edge_id)
        node1_n = node1_n + node_unit
        node2_n = node2_n + node_unit
    write_ftl_edge(nparr, node1.changetype(np.float64) + node_unit * edge_width, 
                   node2.changetype(np.float64) + node_unit * edge_width, edge_id)

def write_node(node_nparr:np.ndarray, node:rw.frame.Coordinate, node_round:float, node_id:int):
    
    node_round_c = math.ceil(node_round)
    node_c = rw.frame.Coordinate(node_round_c, node_round_c)

    x, y = np.ogrid[:2 * node_round_c, :2 * node_round_c]
    condition = (x - node_c.x()) ** 2 + (y - node_c.y()) ** 2 <= node_round ** 2
    try:
        node_nparr[node.x() - node_round_c:node.x() + node_round_c, 
               node.y() - node_round_c:node.y() + node_round_c][condition] = node_id
    except:
        import pdb;pdb.set_trace()

def get_star_ftl_nparr(node_list:list[rw.frame.Coordinate], edge_list:list[tuple[int, int]], edge_width:float, size_t: rw.frame.Coordinate, node_core:float, node_round:float, node_id:int, edge_id:int):
    ftl_nparr = np.zeros((size_t.x(), size_t.y()), dtype = np.uint32)
    for u, v in edge_list:
        nodeu = node_list[u]
        nodev = node_list[v]
        write_ftl_edge_mul(ftl_nparr, nodeu, nodev, edge_id, edge_width)

    star_nparr = np.zeros((size_t.x(), size_t.y()), dtype = np.uint32)
    for node in node_list:
        write_node(star_nparr, node, node_core, node_id)
        write_node(ftl_nparr, node, node_round, edge_id)

    return (star_nparr, ftl_nparr)

CYCLEVIEWMOD = 200
ISVIEW = False
ISNODE_CHOSE = False

ISIGNORE_NODE = 0.36

def node_edge_move(isdebug, language, isverbose, node_list:list[rw.frame.Coordinate], edge_list:list[tuple[int, int]], 
                   node_force_coe:float, 
                   advise_edge_dis:float, edge_force_coe:float, size_t:rw.frame.Coordinate, 
                   round_force_coe:float, star_range:float, see_range:float, 
                   move_gap:float, friction_coe:float, error_v:float, randseed:int = -1)->list[rw.frame.Coordinate]:
    node_list_ch = [deepcopy(i).changetype(np.float64) for i in node_list]
    node_v_list_ch = [rw.frame.Coordinate(0, 0, np.float64) for i in range(len(node_list_ch))]
    node_isnotconnect = np.zeros((len(node_list), len(node_list)), dtype = np.uint8)
    middle = (size_t / 2).changetype(np.float64)
    iscycle = True
    tnow = 0
    len_n = len(node_list)

    v_friction = (1 - (1 - friction_coe) * move_gap)

    if randseed == -1:
        np.random.seed(int(time.time()))
    else:
        np.random.seed(randseed)
    init_progress()
    while iscycle:
        if ISNODE_CHOSE:
            rd_now = np.random.randint(1, 256)
            node_isconnect = node_isnotconnect < rd_now

        node_a_list_ch = []
        node_a_list_ch_core = []
        node_a_list_ch_edge = []
        node_a_list_ch_node = []
        for i, nch in enumerate(node_list_ch):  
            nch_center = (middle - nch)
            nchun = nch_center.unit()
            rdis = nch_center.dis() / (nch_center / (middle * star_range)).dis() 
            node_a = nchun * round_force_coe * (1 / (rdis -  nch_center.dis()) ** 2 - 1 / rdis ** 2)
            node_a_list_ch_core.append(node_a)
            node_a_list_ch_edge.append(rw.frame.Coordinate(dtype = np.float64))


        for u, v in edge_list:
            nsub = (node_list_ch[v] - node_list_ch[u])
            nsubun = nsub.unit()
            force_now = nsubun * (nsub.dis() - advise_edge_dis) * edge_force_coe
            node_a_list_ch_edge[u] = node_a_list_ch_edge[u] + force_now
            node_a_list_ch_edge[v] = node_a_list_ch_edge[v] - force_now


        node_list_ch_np_j = np.stack([deepcopy(i)._content.reshape((1, 2)) for i in node_list_ch], axis = 1)
        node_list_ch_np_i = node_list_ch_np_j.transpose((1, 0, 2))
        node_list_ch_np_j_m = np.tile(node_list_ch_np_j, (len_n, 1, 1))
        node_list_ch_np_i_m = np.tile(node_list_ch_np_i, (1, len_n, 1))
        node_list_ch_np_i_j_m = node_list_ch_np_i_m - node_list_ch_np_j_m
        node_list_ch_np_dis_m = np.sum(node_list_ch_np_i_j_m**2, axis=2)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            np.seterr(divide='ignore')
            node_list_ch_np_i_j_m_coe = (node_force_coe * node_list_ch_np_i_j_m) / (node_list_ch_np_dis_m[:, :, None] ** (3/2))

        node_list_ch_np_i_sum = -np.sum(np.nan_to_num(node_list_ch_np_i_j_m_coe, copy = False), axis=0)
        for i in range(len_n):
            node_a_list_ch_node.append(rw.frame.Coordinate(node_list_ch_np_i_sum[i, 0], node_list_ch_np_i_sum[i, 1], np.float64))




        for i in range(len_n):
            node_a_list_ch.append(node_a_list_ch_node[i] + \
                                node_a_list_ch_edge[i] + node_a_list_ch_core[i])
            node_v_list_ch[i] = (node_v_list_ch[i] * v_friction + node_a_list_ch[i] * move_gap)

        if tnow % CYCLEVIEWMOD == 0 and ISVIEW:
            
            from matplotlib.patches import FancyArrowPatch
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()

            x = [node.x() for node in node_list_ch]
            y = [node.y() for node in node_list_ch]

            plt_label_list = []

            node_plt = plt.scatter(y, x, s=10, c='blue', alpha=0.5)
            plt_label_list.append([node_plt, 'node'])
            
            for edge in edge_list:
                edge_plt = plt.plot([node_list_ch[edge[0]].y(), node_list_ch[edge[1]].y()], 
                        [node_list_ch[edge[0]].x(), node_list_ch[edge[1]].x()], 
                        c = 'yellow', linestyle = '--')
            plt_label_list.append([edge_plt[0], 'edge'])

            HEAD_WIDTH = 1
            HEAD_LENGTH = 1
            COLOR_A_CORE = 'red'
            COLOR_A_EDGE = '#EEEE55'
            COLOR_A_NODE = 'blue'
            COLOR_A = 'cyan'
            COLOR_V = 'black'
            for i, node in enumerate(node_list_ch):
                node_a_core_plt = plt.arrow(node.y(), node.x(), node_a_list_ch_core[i].y(), 
                          node_a_list_ch_core[i].x(), 
                          head_width=HEAD_WIDTH, head_length=HEAD_LENGTH, 
                          fc=COLOR_A_CORE, ec=COLOR_A_CORE)
                
                node_a_edge_plt = plt.arrow(node.y(), node.x(), node_a_list_ch_edge[i].y(), 
                          node_a_list_ch_edge[i].x(), 
                          head_width=HEAD_WIDTH, head_length=HEAD_LENGTH, \
                          fc=COLOR_A_EDGE, ec=COLOR_A_EDGE)
                node_a_node_plt = plt.arrow(node.y(), node.x(), node_a_list_ch_node[i].y(), 
                          node_a_list_ch_node[i].x(), 
                          head_width=HEAD_WIDTH, head_length=HEAD_LENGTH, 
                          fc=COLOR_A_NODE, ec=COLOR_A_NODE)
                node_a_plt = plt.arrow(node.y(), node.x(), node_a_list_ch[i].y(), 
                          node_a_list_ch[i].x(), 
                          head_width=HEAD_WIDTH, head_length=HEAD_LENGTH, \
                          fc=COLOR_A, ec=COLOR_A)
                node_v_plt = plt.arrow(node.y(), node.x(), node_v_list_ch[i].y(), 
                          node_v_list_ch[i].x(), 
                          head_width=HEAD_WIDTH, head_length=HEAD_LENGTH, 
                          fc=COLOR_V, ec=COLOR_V)\
                          
            def fac_temp(color):
                fac_now = FancyArrowPatch((0, 0), (1, 1), mutation_scale=20, 
                             lw=1, arrowstyle='-|>', color = color)
                return fac_now
            
            plt_label_list.append([fac_temp(COLOR_A_CORE), 'space interation'])
            plt_label_list.append([fac_temp(COLOR_A_EDGE), 'edge interaction'])
            plt_label_list.append([fac_temp(COLOR_A_NODE), 'node interaction'])
            plt_label_list.append([fac_temp(COLOR_A), 'acceleration'])
            plt_label_list.append([fac_temp(COLOR_V), 'velocity'])


            x = np.linspace(-1, 1, 1000)

            y1 = np.sqrt(1 - x ** 2)
            y2 = -np.sqrt(1 - x ** 2)

            xt = x * (size_t.x() / 2 * star_range) + size_t.x() / 2

            yt1 = y1 * (size_t.y() / 2 * star_range) + size_t.y() / 2
            yt2 = y2 * (size_t.y() / 2 * star_range) + size_t.y() / 2

            xs = x * (size_t.x() / 2 * see_range) + size_t.x() / 2

            ys1 = y1 * (size_t.y() / 2 * see_range) + size_t.y() / 2
            ys2 = y2 * (size_t.y() / 2 * see_range) + size_t.y() / 2

            see_edge = plt.plot(ys1, xs, c = 'black', linestyle = '-')
            plt.plot(ys2, xs, c = 'black')

            space_edge = plt.plot(yt1, xt, c = 'red', linestyle = '-')
            plt.plot(yt2, xt, c = 'red')

            plt_label_list.append([space_edge[0], 'space'])
            plt_label_list.append([see_edge[0], 'end'])

            plt.legend([i[0] for i in plt_label_list], [i[1] for i in plt_label_list], loc='upper right')

            plt.xlim(0, size_t.y())
            plt.ylim(0, size_t.x())

            plt.show()
            plt.close()

        tnow = tnow + 1

        iscycle = False

        failure_num = 0
        failure_abs_dis = 0
        max_failure_abs_dis = 0

        for i, n1 in enumerate(node_v_list_ch):
            n1_dis = n1.dis()
            failure_abs_dis = failure_abs_dis + n1_dis
            max_failure_abs_dis = max(n1_dis, max_failure_abs_dis)
            if n1_dis >= error_v:
                failure_num = failure_num + 1
                #print("\t\tfailure:(", i, ")", n1, sep = ' ')
                iscycle = True
            node_list_ch[i] = node_list_ch[i] + n1 * move_gap

        failure_abs_dis = failure_abs_dis / len(node_v_list_ch)
        MAX_FAILURE = 100
        if failure_abs_dis > MAX_FAILURE:
            standard_out(language, isverbose == 1, "|")
            standard_out(language, isverbose, "Star move failure...|        星系移动失败，重新生成...")
            return None
    
        if isverbose == 1:
            ri = max_failure_abs_dis / error_v
            ri = max(ri, 1)

            print_progress_o(language, isverbose == 1, tnow, ri * tnow, 
                            prefix = "        progress: |        进度: ")
        
        if isverbose == 2:
            cycle_str = "        time:(" + f"{tnow * move_gap:.1f}" + ")(failure:" + str(failure_num) + "/" + \
                str(len(node_list_ch)) + ")(>=" + str(error_v) + ")" + "(velocity:" + f"{failure_abs_dis:.3}" + ")" + "|" + \
                    "        时间:(" + f"{tnow * move_gap:.1f}" + ")(可移动点:" + str(failure_num) + "/" + \
                str(len(node_list_ch)) + ")(>=" + str(error_v) + ")" + "(平均速率:" + f"{failure_abs_dis:.3}" + ")"
            standard_out(language, isverbose == 2, cycle_str)

    standard_out(language, isverbose == 1, "|")

    node_list_ch = [node.changetype(np.int32) for node in node_list_ch]
    return node_list_ch
                

MAX_NODE_PRODUCTION_CYCLE = 5
MAX_GRAPH_PRODUCTION_CYCLE = 3
MIN_STAR_RANGE = 0.1

def stellaris_random_node_line(isdebug, language, isverbose, node_edge_minnodedis_num:list[tuple[int, int, int]], node_core:float, node_round:float, 
                               node_id:int, edge_width:float, edge_id:int, 
                               size_t:rw.frame.Coordinate, star_range:float, see_range:float, node_force_coe:float, 
                               advise_edge_dis:float, edge_force_coe:float, round_force_coe:float, 
                               move_gap:float, friction_coe:float, error_v:float, randseed:int = -1)->tuple[np.ndarray, np.ndarray, list[rw.frame.Coordinate], list[rw.frame.Coordinate]]:
    
    is_node_edge = True
    c1 = 0
    while is_node_edge:
        if c1 >= MAX_GRAPH_PRODUCTION_CYCLE:
            standard_error(isdebug, language, "The graph cannot be created.|地图无法生成。", 241)

        node_list = []
        edge_num = 0
        is_node_edge = False
        for i, nem_num in enumerate(node_edge_minnodedis_num):
            node_num = nem_num[0]
            edge_num = edge_num + nem_num[1]
            min_node_dis = nem_num[2]
            real_star_range = star_range - min_node_dis / min(size_t.x(), size_t.y())
            if real_star_range <= MIN_STAR_RANGE:
                standard_error(isdebug, language, "The graph cannot be created.|地图无法生成。", 241)

            iscycle = True
            c2 = 0
            while iscycle:
                if c2 >= MAX_NODE_PRODUCTION_CYCLE:
                    standard_error(isdebug, language, "The movement of stars is abnormal.|星系移动异常。", 242)
                node_list_pre = deepcopy(node_list)
                standard_out(language, isverbose, f'    node/edge cycle({i}):(star:{node_num},FTL:{nem_num[1]})|    星系航道添加循环({i}):(星系:{node_num},FTL航道:{nem_num[1]})')
                standard_out(language, isverbose, f"      Node production..." + 
                                f"|      星系生成...")
                node_list_temp = get_random_node(language, isverbose, node_list, node_num, min_node_dis, size_t, real_star_range)
                
                if node_list_temp == None:
                    is_node_edge = True
                    break
                else:
                    iscycle = False
                node_list = node_list_temp

                standard_out(language, isverbose, f"      Edge production..." + 
                                f"|      FTL航线生成...")
                edge_list = get_node_edge_mindis(node_list, edge_num, node_num)

                standard_out(language, isverbose, f"      Star moving..." + 
                                f"|      星系移动...")
                node_list_temp = node_edge_move(isdebug, language, isverbose, node_list, edge_list, node_force_coe, 
                                        advise_edge_dis, edge_force_coe, size_t, round_force_coe, star_range, 
                                        see_range, move_gap, friction_coe, error_v, randseed)
                if node_list_temp == None:
                    iscycle = True
                    node_list = node_list_pre
                    c2 = c2 + 1
                    continue
                else:
                    iscycle = False
                node_list = node_list_temp

            if is_node_edge:
                break
        
        c1 = c1 + 1
    
    standard_out(language, isverbose, f"    Star, FTL pre-process..." + 
                    f"|      星系航线预绘制...")
    star_nparr, ftl_nparr = get_star_ftl_nparr(node_list, edge_list, edge_width, size_t, node_core, node_round, node_id, edge_id)
    return (star_nparr, ftl_nparr, node_list, edge_list)

EXTERNAL_WIDTH_MAX = 10
EXTERNAL_WIDTH = 0
EXTERNAL_HEIGHT = 0
EXTERNAL_INITIAL = rw.frame.Coordinate(-30, 10)

def get_external_coo():
    EXTERNAL_WIDTH = (EXTERNAL_WIDTH + 1) % EXTERNAL_WIDTH_MAX
    pass

def external_flash_id_tobject(map_now:rw.RWmap, time_initial:int, period:int, fresh_num:int):
    fresh_step = period // fresh_num
    fd_initial = [str(i + time_initial) for i in range(0, period, fresh_step)]
    fd_list = ['fd' + i + '_' + str(period) for i in fd_initial]
    fd_id_list = [f"{fd_cite}.did" for fd_cite in fd_list]
    for i, ini in enumerate(fd_initial):
        tobject_fd = rw.object_useful.Auto("fd." + fd_list[i] + "." + str(ini) + "s." + str(period) + 's', pos = COO(fnow * 80, 20) + half_tile_size)
        fnow = fnow + 1
        map_now.addObject_one(tobject_fd)
    tobject_one_fd = [rw.object_useful.Node(rw.const.COO.SIZE_ZERO, name = fdi) for fdi in fd_id_list]





def stellaris_ogob_add():
    pass


def auto_func():
    parser = argparse.ArgumentParser(
        description='Auto generation of stellaris map.\n' + \
                    '群星地图自动产生。')
    
    parser.add_argument('map_dir', action = "store", metavar = 'path', type=str, 
                        help='The output path of RW map dir.\n' + \
                            '铁锈地图文件的输出文件夹。')
    
    parser.add_argument("-f", "--output_file", 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = False, default = "|", 
                        const = "|", 
                        help = "The output file name of RW map.\n" + \
                               "铁锈地图文件的输出文件名。"
                        )
    
    parser.add_argument("-s", "--scope", 
                        action = "store", metavar = "int", type = int, nargs = "+", 
                        required = False, 
                        help = "The suffix scope of Stellaris RW map.\n" + \
                               "群星产生地图的后缀范围。"
                        )

    parser.add_argument("-y", "--isyes", 
                        action = 'store_true', help = 'Requests are always y.\n' + \
                            "所有输入请求默认为y，继续执行。")
    
    parser.add_argument("-v", "--verbose", type = int, default = 0, const = 1, nargs = "?", action = "store", 
                        required = False, 
                        help = 'Detailed output of the prompt message(0:none, 1:main, 2:detail).\n' + \
                            "提供运行信息(0:无, 1:主要部分, 2:细节)。")

    parser.add_argument("--debug", 
                        action = 'store_true', help = 'Mode of debuging.\n' + \
                            "进入python debug模式。")

    parser.add_argument("--ignorewarning", 
                        action = 'store_true', help = 'Warning would not exit.\n' + \
                            "警告将不会退出。")
    
    parser.add_argument("--language", 
                        action = "store", metavar = "language", type = str, nargs = "?", 
                        required = False, default = "default", 
                        const = "default", 
                        help = "The language of prompt(ch/eg). The language configuration will be stored.(command/config.json)\n" + \
                        "命令行提示的语言(中文(ch),英文(eg))。语言设置将会被存储。(command/config.json)"
                        )

    parser.add_argument('-jv', '--cversion', 
                        action = "store", metavar = "version", type = str, nargs = "?", 
                        required = False, default = '|', const = '|', 
                        help='The version of Stellaris setting(.json).\n' + \
                            '群星属性设置版本(.json)')

    parser.add_argument('-j', '--config', 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = False, default = '|', const = '|', 
                        help='The Stellaris of setting(.json).\n' + \
                            '群星属性设置(.json)')

    parser.add_argument('-r', '--randseed', 
                        action = "store", metavar = "number", type = int, nargs = "?", 
                        required = False, default = -1, const = -1, 
                        help='random seed(default:-1, time as randseed).\n' + \
                            '随机数种子(默认-1 以时间随机)。')


    args = parser.parse_args()

    output_dir = args.map_dir

    output_file = args.output_file

    scope = args.scope

    if len(scope) == 1:
        scope = [scope[0], scope[0]]
    elif len(scope) == 3:
        raise ValueError("dddd")

    isyes = args.isyes

    isverbose = args.verbose

    language = args.language

    ignorewarning = args.ignorewarning

    isdebug = args.debug

    config = args.config

    randseed = args.randseed

    cversion = args.cversion

    if cversion != "|":

        cversion_d = re.findall(r'[a-zA-Z0-9]+', cversion)
        cversion_d = ''.join(cversion_d)
        avd, bvd, cvd = split_first_letter(cversion_d)
        suf = bvd + cvd
        suf = "" if suf == "" else "_" + suf
        cversion_s = "stellaris_" + avd + suf + ".json"
        config = os.path.join(current_dir_path, "json", cversion_s)

    language = input_language(isdebug, language)    

    config_dict = get_config_dict_ex(isdebug, language, config)

    # constant

    ## tileset

    tile_size = rw.frame.Coordinate(20, 20)
    tile_size2 = tile_size * 2
    half_tile_size = tile_size / 2

    star_tileset = "群星地块"

    terrain_name_star = "星系"
    terrain_name_ftl = "FTL航线"
    terrain_name_see = "视域"
    terrain_name_space = "虚空"

    # config start

    standard_out_underline(language, isverbose, "Initialization|初始化")

    config_list = []

    rwmapauto_type = config_get_ex(isdebug, language, config_dict, config_list, "rwmapauto_type", config_code = 100, 
                                  error_id = 169, itype = str, value_set = {"stellaris"})
    
    version = config_get_ex(isdebug, language, config_dict, config_list, "version", config_code = 101, 
                                  error_id = 172, itype = str, value_set = {"1.0"})

    json_version = config_get_ex(isdebug, language, config_dict, config_list, "json_version", config_code = 102, 
                                  error_id = 175, itype = str)

    ## map info
    map_info_dict = config_get_ex(isdebug, language, config_dict, config_list, "map_info", config_code = 103, 
                                  error_id = 177, itype = dict, islist_add = True)

    node_edge_minnodedis_num = config_get_ex(isdebug, language, map_info_dict, config_list, 
                                             "node_edge_minnodedis_num", config_code = 104, 
                                             error_id = 179, itype = list)
    
    for i, ni in enumerate(node_edge_minnodedis_num):
        config_get_ex(isdebug, language, node_edge_minnodedis_num, config_list, i, config_code = 105, 
                      error_id = 181, itype = list, islist_add = True, islist = True, len_max = 3)
        config_list.pop()

    map_size = config_get_ex(isdebug, language, map_info_dict, config_list, "map_size", config_code = 106, 
                             error_id = 184, itype = list, len_max = 2)
    map_size_t = rw.frame.Coordinate(map_size[0], map_size[1])

    team_sum = config_get_ex(isdebug, language, map_info_dict, config_list, "team_sum", config_code = 107, 
                      error_id = 187, itype = int, int_min = 2)

    config_list.pop()

    ## star map

    star_map_dict = config_get_ex(isdebug, language, config_dict, config_list, "star_map", config_code = 108, 
                                  error_id = 190, itype = dict, islist_add = True)

    see_range = config_get_ex(isdebug, language, star_map_dict, config_list, "see_range", config_code = 109, 
                                  error_id = 192, itype = float, int_max = 1, int_min = 0)
    
    star_range = config_get_ex(isdebug, language, star_map_dict, config_list, "star_range", config_code = 110, 
                                  error_id = 196, itype = float, int_max = 1, int_min = 0)

    edge_width = config_get_ex(isdebug, language, star_map_dict, config_list, "edge_width", config_code = 111, 
                                  error_id = 200, itype = float, int_min = 0)
    
    advise_edge_dis = config_get_ex(isdebug, language, star_map_dict, config_list, "advise_edge_dis", 
                                    config_code = 112, 
                                  error_id = 203, itype = int, int_min = 0)

    node_force_coe = config_get_ex(isdebug, language, star_map_dict, config_list, "node_force_coe", 
                                    config_code = 113, 
                                  error_id = 206, itype = int, int_min = 1)

    edge_force_coe = config_get_ex(isdebug, language, star_map_dict, config_list, "edge_force_coe", 
                                    config_code = 114, 
                                  error_id = 209, itype = int, int_min = 1)
    
    round_force_coe = config_get_ex(isdebug, language, star_map_dict, config_list, "round_force_coe", 
                                    config_code = 115, 
                                  error_id = 212, itype = int, int_min = 1)
    node_core = config_get_ex(isdebug, language, star_map_dict, config_list, "node_core", 
                                    config_code = 116, 
                                  error_id = 215, itype = float, int_min = 0)
    node_round = config_get_ex(isdebug, language, star_map_dict, config_list, "node_round", 
                                    config_code = 117, 
                                  error_id = 218, itype = float, int_min = 0)
    edge_width = config_get_ex(isdebug, language, star_map_dict, config_list, "edge_width", 
                                    config_code = 118, 
                                  error_id = 221, itype = float, int_min = 0)

    config_list.pop()

    ## object_info

    object_info = config_get_ex(isdebug, language, config_dict, config_list, "object_info", config_code = 119, 
                                  error_id = 224, itype = dict, islist_add = True)
    
    credit = config_get_ex(isdebug, language, object_info, config_list, "credit", config_code = 120, 
                                  error_id = 226, itype = int, int_min = 0)
    
    config_list.pop()

    ## star_move

    star_move = config_get_ex(isdebug, language, config_dict, config_list, "star_move", config_code = 130, 
                                  error_id = 229, itype = dict, islist_add = True)
    
    move_gap = config_get_ex(isdebug, language, star_move, config_list, "move_gap", config_code = 131, 
                                  error_id = 231, itype = float, int_min = 0)    
    friction_coe = config_get_ex(isdebug, language, star_move, config_list, "friction_coe", config_code = 132, 
                                  error_id = 234, itype = float, int_min = 0, int_max = 1)
    error_v = config_get_ex(isdebug, language, star_move, config_list, "error_v", config_code = 133, 
                                  error_id = 238, itype = float, int_min = 0)
    config_list.pop()

    # config end

    # Calc

    version_now = version + json_version

    star_tileset_mappath = os.path.join(current_dir_path, "tile/群星实验-tr1.tmx")
    template_tileset_mappath = os.path.join(current_dir_path, "tile/ob_template.tmx")
    star_layerauto_js_path = os.path.join(current_dir_path, "tile/stellaris_tile.json")

    zero_coo = rw.frame.Coordinate(0, 0)
    map_size_o = map_size_t.transpose()
    ground_rect = rw.frame.TagRectangle.init_ae(rw.const.NAME.Ground, zero_coo, map_size_t)

    node_num_sum = sum([i[0] for i in node_edge_minnodedis_num])
    edge_num_sum = sum([i[1] for i in node_edge_minnodedis_num])

    standard_out_underline(language, isverbose, f"Map process" + \
                        f"|地图绘制")

    time_all_now = time.time()

    for mi in range(scope[0], scope[1] + 1):
        standard_out(language, isverbose, f"Map process({mi})..." + \
                        f"|地图绘制({mi})...")
        
        time_now = time.time()

        output_file_now = output_file[:-4] + f"-{mi}" + output_file[-4:] if output_file != '|' else f"群星【2-{team_sum}p,城市争夺玩法】(V{version_now})-{mi} by咕咕咕.tmx"
        output_path = os.path.join(output_dir, output_file_now)

        check_input_output_path(isdebug, language, isyes, None, output_path)

        if randseed != -1:
            randseed_now = randseed
            np.random.seed(randseed_now)
        else:
            randseed_now = (int(time.time()) * 3333331) % 998244353
            np.random.seed(randseed_now)
        #

        map_now = rw.RWmap.init_map(size = map_size_o, tile_size = tile_size)

        star_tileset_map = rw.RWmap.init_mapfile(star_tileset_mappath)

        map_now.add_tileset_fromTileSet(star_tileset_map.get_tileset_s(star_tileset))
        map_now.add_layer(rw.const.NAME.Ground)
        map_now.add_layer(rw.const.NAME.Items)
        map_now.add_layer(rw.const.NAME.Units)

        template = rw.RWmap.init_mapfile(template_tileset_mappath)

        map_now.add_objectgroup(rw.const.NAME.Triggers)
        map_now.add_objectgroup(rw.const.NAME.UnitObject)

        standard_out(language, isverbose, "  Star/FTL process...|  星系FTL航线生成...")

        #

        tileset_now = map_now.get_tileset_s(star_tileset)
        terrainid_see = tileset_now.terrainname_to_terrainid(terrain_name_see)
        terrainid_ftl = tileset_now.terrainname_to_terrainid(terrain_name_ftl)
        terrainid_star = tileset_now.terrainname_to_terrainid(terrain_name_star)

        space_c = rw.frame.TagCoordinate.init_xy(star_tileset, 1, 1)
        see_c = rw.frame.TagCoordinate.init_xy(star_tileset, 1, 4)
        ftl_c = rw.frame.TagCoordinate.init_xy(star_tileset, 1, 7)
        star_c = rw.frame.TagCoordinate.init_xy(star_tileset, 4, 7)

        see_g = map_now._tileplace_to_gid(see_c)
        ftl_g = map_now._tileplace_to_gid(ftl_c)
        star_g = map_now._tileplace_to_gid(star_c)

        #

        star_nparr, ftl_nparr, node_list, edge_list = \
        stellaris_random_node_line(isdebug, language, isverbose, 
        node_edge_minnodedis_num, node_core, node_round, star_g, 
        edge_width, ftl_g, map_size_t, star_range, see_range = see_range, 
        node_force_coe = node_force_coe, advise_edge_dis = advise_edge_dis, 
        edge_force_coe = edge_force_coe, round_force_coe = round_force_coe, 
        move_gap = move_gap, friction_coe = friction_coe, error_v = error_v, 
        randseed = randseed_now)

        standard_out(language, isverbose, f"  Space process..." + 
                        f"|  虚空绘制...")
        map_now.addTile_square(ground_rect, space_c)
        
        standard_out(language, isverbose, f"  see process..." + 
                        f"|  视域绘制...")
        space_matrix = np.zeros((map_size_t.x(), map_size_t.y()), dtype = np.uint32)
        x, y = np.ogrid[:space_matrix.shape[0], :space_matrix.shape[1]]
        condition = (2 * (x + 0.5) / map_size_t.x() - 1) ** 2 + (2 * (y + 0.5) / map_size_t.y() - 1) ** 2 <= see_range
        
        space_matrix[condition] = see_g

        layer_ground = map_now.get_layer_s(rw.const.NAME.Ground)
        layer_ground.assigntileid_squarematrix_exclude0(zero_coo, space_matrix)
        
        standard_out(language, isverbose, f"  FTL process..." + 
                        f"|  FTL航线绘制...")
        
        layer_ground.assigntileid_squarematrix_exclude0(zero_coo, ftl_nparr)

        standard_out(language, isverbose, f"  Star process..." + 
                        f"|  星系绘制...")
        
        layer_ground.assigntileid_squarematrix_exclude0(zero_coo, star_nparr)

        standard_out(language, isverbose, "  Triggers process...|  宾语层添加...")

        stellaris_ogob_add()

        for i in template.iterator_object_s(default_re = {"name": TEMPLATE_RE}):
            i.assignDefaultProperty("x", "-200")
            i.assignDefaultProperty("y", "-200")
            map_now.addObject_type(i)

        introText = f"""
欢迎，指挥官。
您已被选中领导我们的文明进入一个未知的新纪元。
在您面前，是无限的可能性。
我们的舰队已经准备好，我们的人民充满希望。
我们将探索星系，寻找新的家园，与未知的文明相遇，或许还会发现古老的秘密。
↓↓↓↓
简要玩法说明：
星系(供应站,激光防御塔)持续提供舰队(导弹舰,战列舰)。
每个玩家开局首都星系是激光防御塔，快速生产导弹舰({CAPITAL_TIME}倍速于普通星系)
首都星系激光防御塔升级后快速生产战列舰。
其他星系为补给站，生产导弹舰。
星系中会随机出现野怪，消灭不会有奖励。
玩家丢失全部建筑就会失败。
↓↓↓↓
地图,地块和程序作者：咕咕咕
地图官方群(城夺社): 699981990
地图版本: {version}
随机种子: {randseed}
↓↓↓↓
该地图由程序生成，星图和玩家分布是随机的。不保证公平性。
房主请勿事先打开地图观看地图来制订策略——被视为作弊行为。
玩家不允许自行选择位置，应当是随机的。
地图允许2p-{team_sum}p的混战,团混和团战。
↓↓↓↓
地图参数信息:
地图大小:({map_size_t.x()}, {map_size_t.y()})
星图属性:(星系:{node_num_sum}, FTL航线:{edge_num_sum})
最大玩家数目:{team_sum}
兵力标准刷新速度:{fresh_time}s
首都刷新倍速:{CAPITAL_TIME}
↓↓↓↓
鸣谢人员:
感谢黑沼帝国,向宠等群友提供的建议。

----2024.12.19----

"""

        for i in template.iterator_object_s(default_re = {"name": "map_info"}):
            i.assignOptionalProperty_text("introText", introText)

        COO = rw.frame.Coordinate
        fnow = 0

        TIME_INITIAL = 25
        fresh_time = 80
        FRESH_NUM = 4
        CAPITAL_TIME = 2

        fresh_step = int(np.ceil(fresh_time / FRESH_NUM))
        fresh_time_cap = int(fresh_time / CAPITAL_TIME)
        fresh_step_cap = int(np.ceil(fresh_time_cap / FRESH_NUM))

        fd_initial = [str(i + TIME_INITIAL) for i in range(0, fresh_time, fresh_step)]
        fd_period = str(fresh_time)
        fd_list = ['fd' + str(i) + '_' + str(fd_period) for i in fd_initial]
        fd_id_list = ['fd' + str(i + 1) for i in range(FRESH_NUM)]
        for i, ini in enumerate(fd_initial):
            tobject_fd = rw.object_useful.Auto("fd." + fd_list[i] + "." + str(ini) + "s." + str(fd_period) + 's', pos = COO(fnow * 80, 20) + half_tile_size)
            fnow = fnow + 1
            map_now.addObject_one(tobject_fd)
        tobject_one_fd = [rw.object_useful.Node(zero_coo, name = fdi) for fdi in fd_id_list]

        fd_bs_initial = [str(i + TIME_INITIAL) for i in range(0, fresh_time_cap, fresh_step_cap)]
        fd_bs_period = str(fresh_time_cap)
        fd_bs_list = ['fd' + str(i) + '_' + str(fd_bs_period) for i in fd_bs_initial]
        fd_bs_id_list = ['fd' + str(i + 1 + FRESH_NUM) for i in range(FRESH_NUM)]
        for i, ini in enumerate(fd_bs_initial):
            tobject_fd = rw.object_useful.Auto("fd." + fd_bs_list[i] + "." + str(ini) + "s." + str(fd_bs_period) + 's', pos = COO(fnow * 80, 20) + half_tile_size)
            fnow = fnow + 1
            map_now.addObject_one(tobject_fd)
        tobject_one_fd_bs = [rw.object_useful.Node(zero_coo, name = fdi) for fdi in fd_bs_id_list]

        fi_initial = ['4']
        fi_list = ['fi' + str(i) for i in fi_initial]
        fi_id_list = ['fi1']
        for i, ini in enumerate(fi_initial):
            tobject_fi = rw.object_useful.Auto("fi." + fi_list[i] + "." + str(ini) + "s", pos = COO(fnow * 80, 20) + half_tile_size)
            fnow = fnow + 1
            map_now.addObject_one(tobject_fi)
        tobject_one_fi = [rw.object_useful.Node(zero_coo, name = fii) for fii in fi_id_list]

        si_time = ['20']
        si_id_list = ['si1']
        for i, ini in enumerate(si_time):
            tobject_si = rw.object_useful.Auto("si.si" + str(ini) + "." + str(ini) + "s", pos = COO(fnow * 80, 20) + half_tile_size)
            fnow = fnow + 1
            map_now.addObject_one(tobject_si)
        tobject_one_si = [rw.object_useful.Node(zero_coo, name = sii) for sii in si_id_list]

        turret_str = ",usu,o,Btl2"
        laser_str = ",uld,W21s"

        ghost_pro_list = [('bs', 0.02, 1), ('bm', 0.05, 1), ('ms', 0.1, 1), ('ms', 0.05, 2), ('ms', 0.02, 4)]

        tmsi = 0
        team_now = 0



        tobject_but_not_list = []

        for ni, node in enumerate(node_list):
            nodelt = node + COO(-2, -2)
            node_c = node.transpose() * tile_size - half_tile_size
            nodelt_c = nodelt.transpose() * tile_size

            nodeq_list = [COO(2, 2), COO(2, -2), COO(-2, 2), COO(-2, -2)]
            nodeq_list = [(node + nodeq).transpose() * tile_size for nodeq in nodeq_list]

            if team_now >= team_sum:
                rand_now = np.random.rand()
                r_ch_now = 0
                for ghost_pro in ghost_pro_list:
                    r_ch_now = r_ch_now + ghost_pro[1]
                    if rand_now < r_ch_now:
                        tobject_ghost = rw.object_useful.Auto("a." + ghost_pro[0] + "." + fi_list[0] + ",t-2")
                        d_list = generate_permutations(len(nodeq_list))
                        for ti in range(ghost_pro[2]):
                            tnq_now = d_list[np.random.randint(0, len(nodeq_list))]
                            map_now.addObject_one(tobject_ghost.offset(nodeq_list[tnq_now]))
                        break

            tmsi = (tmsi + 1) % len(fd_initial)

            if team_now < team_sum:
                tobject_command = rw.object_useful.Auto("", pos = node_c, size = tile_size2)
                tobject_command._otype._optional_properties["team"] = str(team_now)
                tobject_command._otype._optional_properties["unit"] = rw.const.UNIT.commandCenter
                map_now.addObject_one(tobject_command, objectGroup_name = rw.const.NAME.UnitObject)
                tobject_remove = rw.object_useful.UnitRemove(pos = node_c, size = tile_size2, 
                                                            team = team_now, warmup = 2)
                map_now.addObject_one(tobject_remove)
                tobject_but = rw.object_useful.Auto('t' + str(team_now) + laser_str, pos = node_c, 
                                                    size = tile_size2)

                tobject_but_not = rw.object_useful.UnitAdd(pos = node_c, team = -2, warmup = 2,  
                                                        spawnUnits = rw.const.UNIT.laserDefence, 
                                                        size = tile_size2)
                
                tobject_but_not_def_list = [rw.object_useful.UnitAdd(pos = nodeq_now, team = -2, warmup = 2, 
                                                spawnUnits = rw.const.UNIT.missileship, deactiBy_s = [tobject_one_si[0]]) for nodeq_now in nodeq_list]

                tobject_but_not_list.append([tobject_but_not, tobject_but_not_def_list])
                
                map_now.addObject_one(tobject_but)


                for team_oc_now in range(team_sum):
                    
                    td_id = "ctdrw" + str(team_now) + "oc" + str(team_oc_now)
                    teamdetect_now = rw.object_useful.UnitDetect(node_c, tile_size2, name = td_id, 
                                                                team = team_oc_now, minUnits = 1, 
                                                                onlyList = [rw.const.OBJECTOP.onlyBuildings], 
                                                                warmup = 5, reset = 5)

                    map_now.addObject(teamdetect_now)
                    map_now.addObject_one(rw.object_useful.Credit(pos = COO((team_now - team_sum) * 80 - 40, (team_oc_now + 2) * 40), 
                                                                team = team_oc_now, addCredits = credit, reset = 1, 
                                                                actiBy_s = [teamdetect_now]))

            else:
                tobject_but = rw.object_useful.Auto('t' + str(-2) + turret_str, pos = node_c, 
                                                    size = tile_size2)
                map_now.addObject_one(tobject_but)

            nau_id = "nau" + str(ni)

            tobject_nau = rw.object_useful.Basic(node_c, name = nau_id, size = tile_size2, reset = 5)
            tobject_nau_de_list = [
                rw.object_useful.UnitDetect(node_c, tile_size2, team = -1, minUnits = 1, 
                                            onlyList = [rw.const.OBJECTOP.onlyBuildings], warmup = 5, reset = 5, 
                                            alsoacti_s = [tobject_nau]), 
                rw.object_useful.UnitDetect(node_c, tile_size2, team = -2, minUnits = 1, 
                                            onlyList = [rw.const.OBJECTOP.onlyBuildings], warmup = 5, reset = 5, 
                                            alsoacti_s = [tobject_nau]), 
                rw.object_useful.UnitDetect(node_c, tile_size2, maxUnits = 0, 
                                            onlyList = [rw.const.OBJECTOP.onlyBuildings], warmup = 5, reset = 5, 
                                            alsoacti_s = [tobject_nau])
            ]

            for tobject in tobject_nau_de_list:
                map_now.addObject_one(tobject)

            map_now.addObject_one(tobject_nau)

            tmsi_now = 0 if team_now < team_sum else tmsi

            if team_now < team_sum:

                tech2_id_now = "tech2l" + str(team_now)
                tobject_is_tech2 = rw.object_useful.UnitDetect(node_c, tile_size2, name = tech2_id_now, 
                                                            minUnits = 1, unitType = rw.const.UNIT.laserDefence, 
                                                            warmup = 5, reset = 5, id = tech2_id_now, 
                                                            onlyList = [rw.const.OBJECTOP.onlyTechLevel + "2"])
                map_now.addObject_one(tobject_is_tech2)

                tech1_id_now = "tech1l" + str(team_now)
                tobject_is_tech1 = rw.object_useful.UnitDetect(node_c, tile_size2, name = tech1_id_now, 
                                                            minUnits = 1, unitType = rw.const.UNIT.laserDefence, 
                                                            warmup = 5, reset = 5, id = tech1_id_now, 
                                                            onlyList = [rw.const.OBJECTOP.onlyTechLevel + "1"])
                map_now.addObject_one(tobject_is_tech1)

                tobject_ms_now = rw.object_useful.UnitAdd(nodelt_c, -1, rw.const.UNIT.missileship, 
                                                        size = tile_size, warmup = 1, 
                                                        deactiBy_s = [tobject_nau, tobject_one_fd_bs[tmsi_now], tobject_is_tech2])
                map_now.addObject_one(tobject_ms_now)

                tobject_bs_now = rw.object_useful.UnitAdd(nodelt_c, -1, rw.const.UNIT.battleShip, 
                                                        size = tile_size, warmup = 1, 
                                                        deactiBy_s = [tobject_nau, tobject_one_fd_bs[tmsi_now], tobject_is_tech1])

                map_now.addObject_one(tobject_bs_now)

            else:

                tobject_ms_now = rw.object_useful.UnitAdd(nodelt_c, -1, rw.const.UNIT.missileship, 
                                                        size = tile_size, warmup = 1, 
                                                        deactiBy_s = [tobject_nau, tobject_one_fd[tmsi_now]])


                map_now.addObject_one(tobject_ms_now)
            
            team_now = team_now + 1

        tnow = 0
        for i in range(team_sum):
            tobject_builder = rw.object_useful.UnitAdd(COO(tnow * 80, -200) + half_tile_size, tnow, rw.const.UNIT.builder, warmup = 1)
            map_now.addObject_one(tobject_builder, objectGroup_name = rw.const.NAME.Triggers)

            tobject_land = rw.object_useful.UnitAdd(COO(tnow * 80, -300) + half_tile_size, tnow, rw.const.UNIT.landFactory, warmup = 1)
            map_now.addObject_one(tobject_land, objectGroup_name = rw.const.NAME.Triggers)

            check_su_now = "checksup" + str(tnow)
            tobject_checksu = rw.object_useful.UnitDetect(zero_coo, map_size_o * tile_size, name = check_su_now, 
                                                            team = tnow, maxUnits = 0, onlyList = [rw.const.OBJECTOP.onlyBuildings], 
                                                            warmup = 10, id = check_su_now)
            map_now.addObject_one(tobject_checksu)

            tobject_remove_bl = rw.object_useful.UnitRemove(COO(tnow * 80 - 20, -300 - 20) + half_tile_size, rw.frame.Coordinate(60, 100 + 60), 
                                                            warmup = 10, actiBy_s = [tobject_checksu], isalltoacti = True)
            
            map_now.addObject_one(tobject_remove_bl)

            tdetect_now = "tdetect" + str(tnow)
            tobject_tdetect_bl = rw.object_useful.UnitDetect(COO(tnow * 80 - 20, -300 - 20) + half_tile_size, rw.frame.Coordinate(60, 100 + 60), 
                                                            maxUnits = 0, warmup = 1, id = tdetect_now, name = tdetect_now)


            tobject_but_not_list[tnow][0].add_actiBy_s([tobject_tdetect_bl])
            map_now.addObject_one(tobject_but_not_list[tnow][0])

            for buti in range(len(tobject_but_not_list[tnow][1])):
                tobject_but_not_list[tnow][1][buti].add_actiBy_s([tobject_tdetect_bl])
                map_now.addObject_one(tobject_but_not_list[tnow][1][buti])
                

            map_now.addObject_one(tobject_tdetect_bl)

            map_now.addObject_one(rw.object_useful.Credit(pos = COO(tnow * 80, -100), team = tnow, setCredits = 0))
            map_now.addObject_one(rw.object_useful.Credit(pos = COO(tnow * 80, -60), team = tnow, setCredits = 0, warmup = 4))
            
            
            tnow = tnow + 1

        map_now.addObject_one(rw.object_useful.Message(zero_coo, "正在开始新游戏...", textColor = 'green', warmup = 1, delayPerChar = 0.05))
        map_now.addObject_one(rw.object_useful.Message(zero_coo, "欢迎来到群星。", textColor = 'green', warmup = 5, delayPerChar = 0.05))
        map_now.addObject_one(rw.object_useful.Message(zero_coo, "每个玩家有一个首都星系(激光防御塔)。", textColor = 'green', warmup = 9, delayPerChar = 0.05))
        map_now.addObject_one(rw.object_useful.Message(zero_coo, "提示：首都激光防御塔可以升级，升级后可在首都刷新战列舰。", textColor = '#FFC800', warmup = 13, reset = round(2000 / credit), delayPerChar = 0.05))
        map_now.addObject_one(rw.object_useful.Message(zero_coo, "每个星系均可以生产导弹舰。", textColor = 'green', warmup = 17, delayPerChar = 0.05))
        map_now.addObject_one(rw.object_useful.Message(zero_coo, "其他星系可能会出现一些野怪哦，消灭不会有奖励。", textColor = 'green', warmup = 21, delayPerChar = 0.05))
        map_now.addObject_one(rw.object_useful.Message(zero_coo, "前方便是星辰大海，请开始您的征服！", textColor = 'green', warmup = 25, delayPerChar = 0.05))
        map_now.addObject_one(rw.object_useful.Message(zero_coo, "地图官方群(城夺社) : 699981990", textColor = '#00FF66', warmup = 30, reset = round(2000 / credit), delayPerChar = 0.05))
        map_now.addObject_one(rw.object_useful.Message(zero_coo, "地图,地块和程序作者 : 咕咕咕", textColor = '#00FF66', warmup = 32, reset = round(2000 / credit), delayPerChar = 0.05))

        standard_out(language, isverbose, "New RW map is being establishing...|新的铁锈地图正在建立...")

        temp_path = os.path.join(current_dir_path, "tile/stellaris-temp.tmx")
        temp_path_2 = os.path.join(current_dir_path, "tile/stellaris-temp-2.tmx")
        temp_path_3 = os.path.join(current_dir_path, "tile/stellaris-temp-3.tmx")
        temp_path_4 = os.path.join(current_dir_path, "tile/stellaris-temp-4.tmx")

        if isdebug:
            path1 = temp_path
            path2 = temp_path_2
            path3 = temp_path_3
            path4 = temp_path_4
        else:
            path1 = temp_path
            path2 = temp_path
            path3 = temp_path
            path4 = output_path

        tr = map_now.get_objectgroup_s(rw.const.NAME.Triggers)
        tr.change_visible(False)
        output_rwmap(isdebug, language, False, map_now, path1)

        v_str = (["-v"] if isdebug and isverbose else [])
        v2_str = v_str + (["2"] if isdebug and isverbose == 2 else [])
        d_str = (["--debug"] if isdebug else [])
        y_str = (["--isyes"] if isyes else [])
        i_str = (["--ignorewarning"] if ignorewarning else [])
        dyi_str = d_str + y_str + i_str

        og_list = ["python", os.path.join(command_dir_path, "objectgroupauto", "_core.py"), path1, "-o", path2, "-D", "-c"] + v2_str + dyi_str
        la_list = ["python", os.path.join(command_dir_path, "layerauto", "_core.py"), path2, "-o", path3, "-j", star_layerauto_js_path] + v2_str + dyi_str
        ti_list = ["python", os.path.join(command_dir_path, "tsindep", "_core.py"), path3, "-o", path4] + v_str + dyi_str
        try:
            com_og = subprocess.run(og_list)
            if com_og.returncode != 0:
                exit(0)
            com_la = subprocess.run(la_list)
            if com_la.returncode != 0:
                exit(0)
            com_ti = subprocess.run(ti_list)
            if com_ti.returncode != 0:
                exit(0)
        except:
            exit(0)

        standard_out(language, not (isdebug and isverbose), f"RW map output({output_path})" + 
            f"|地图文件导出({output_path})")

        time_end = time.time()
        time_dur = time_end - time_now
        standard_out(language, isverbose, f"  time({mi}):{time_dur:.1f}s|  运行时间({mi}):{time_dur:.1f}s")

    time_all_end = time.time()
    time_all_dur = time_all_end - time_all_now
    standard_out(language, isverbose, f"Total time:{time_all_dur:.1f}s|运行总时间:{time_all_dur:.1f}s")

    if not isdebug:
        try:
            os.remove(temp_path)
            os.remove(temp_path_2)
            os.remove(temp_path_3)
            os.remove(temp_path_4)
        except:
            pass

if __name__ == "__main__":
    auto_func()        

