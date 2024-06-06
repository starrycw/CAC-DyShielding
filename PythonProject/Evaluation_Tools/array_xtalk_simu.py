# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/05/13
# @Author  : c
#
# Version: 20240605

import copy
import math


class Codeword_Xtalk_Calculator:
    def __init__(self):
        assert False

    @staticmethod
    def calculate_codeword_xtalk(codeword_a_tuple, codeword_b_tuple, shielding_tuple):
        '''
        输入码字a以及码字b以及屏蔽标志，计算并统计a->b跳变中的串扰等级。

        :param codeword_a_tuple: 表示码字1的元组，例如 codeword_a_tuple=(0, 1, 1, 0, 1, 0, 0)
        :param codeword_b_tuple: 表示码字1的元组，例如 codeword_b_tuple=(0, 1, 1, 0, 1, 0, 0)
        :param shielding_tuple: 指示哪些位为屏蔽位的元组，1表示屏蔽位，0表示信号位。需要注意：元组大小应与码字元组相同，且屏蔽位在码字元组中必须对应0.
        :return: xtalk_tuple: 各个位的串扰级别，None表示屏蔽位； cnt_level_tuple：统计当前跳变中受到 0C, 1C, 2C, 3C, 4C串扰的信号TSV的个数（忽略屏蔽位）
        '''

        ####################################################
        # function: 计算某个位对其一个相邻位的影响
        def calc_xtalk_default(diff_victim, diff_aggressor):
            assert diff_victim in (-1, 0, 1)
            assert diff_aggressor in (-1, 0, 1)
            xtalk = abs(diff_victim - diff_aggressor)
            return xtalk

        ####################################################

        # Check
        assert isinstance(codeword_a_tuple, tuple)
        assert isinstance(codeword_b_tuple, tuple)
        assert isinstance(shielding_tuple, tuple)
        n = len(codeword_a_tuple)
        assert len(codeword_b_tuple) == n
        assert len(shielding_tuple) == n

        # Vars
        diff_list = [] # 码字对应位差值
        xtalk_list = [] # 串扰级别，考虑屏蔽位


        # diff_list
        for idx in range(0, n):
            a = codeword_a_tuple[idx]
            b = codeword_b_tuple[idx]
            shielding = shielding_tuple[idx]
            if shielding == 1:
                assert a == 0
                assert b == 0
            else:
                assert a in (0, 1)
                assert b in (0, 1)

            diff_list.append(b-a)
            assert len(diff_list) == idx + 1

        diff_tuple = tuple(diff_list)
        # xtalk_list
        for idx in range(0, n):
            if shielding_tuple[idx] == 1:
                xtalk_list.append(None)

            else:
                if idx == 0:
                    xtalk_left = 0
                elif shielding_tuple[idx-1] == 1:
                    xtalk_left = 0
                else:
                    xtalk_left = calc_xtalk_default(diff_victim=diff_tuple[idx], diff_aggressor=diff_tuple[idx-1])

                if idx == n-1:
                    xtalk_right = 0
                elif shielding_tuple[idx+1] == 1:
                    xtalk_right = 0
                else:
                    xtalk_right = calc_xtalk_default(diff_victim=diff_tuple[idx], diff_aggressor=diff_tuple[idx+1])

                xtalk_list.append(xtalk_left + xtalk_right)

            assert len(xtalk_list) == idx + 1

        # 统计
        xtalk_tuple = tuple(xtalk_list)
        cnt_level_list = [0, 0, 0, 0, 0]  # 用于统计当前跳变中受到 0C, 1C, 2C, 3C, 4C串扰的信号TSV的个数（忽略屏蔽位）
        for i in xtalk_tuple:
            if i == 0:
                cnt_level_list[0] = cnt_level_list[0] + 1
            elif i == 1:
                cnt_level_list[1] = cnt_level_list[1] + 1
            elif i == 2:
                cnt_level_list[2] = cnt_level_list[2] + 1
            elif i == 3:
                cnt_level_list[3] = cnt_level_list[3] + 1
            elif i == 4:
                cnt_level_list[4] = cnt_level_list[4] + 1
            else:
                assert i is None

        cnt_level_tuple = tuple(cnt_level_list)

        return xtalk_tuple, cnt_level_tuple


class Array_Xtalk_Calculator:
    def __init__(self, n_row, n_col):
        assert isinstance(n_row, int)
        assert isinstance(n_col, int)
        assert n_row > 2
        assert n_col > 2

        self._n_row = n_row
        self._n_col = n_col

    def get_n_row(self):
        '''
        返回阵列行数
        :return:
        '''
        return self._n_row

    def get_n_col(self):
        '''
        返回阵列列数
        :return:
        '''
        return self._n_col

    def check_array_size(self, array_a):
        '''
        检查二位数组/元组的大小是否与TSV阵列大小相对应，即外层元素数目等于行数，内层元素个数等于列数
        :return: Bool
        '''
        assert isinstance(array_a, tuple) or isinstance(array_a, list)
        if len(array_a) != self.get_n_row():
            return False
        for row_i in array_a:
            assert isinstance(row_i, tuple) or isinstance(row_i, list)
            if len(row_i) != self.get_n_col():
                return False
        return True


    def calc_xtalk_A_to_B(self, diff_victim, diff_aggressor):
        '''
        计算某个位对其一个相邻位的影响。输入分别为受串扰线和施扰线在某次跳变中的差值。
        :param diff_victim:
        :param diff_aggressor:
        :return:
        '''
        assert diff_victim in (-1, 0, 1)
        assert diff_aggressor in (-1, 0, 1)
        xtalk = abs(diff_victim - diff_aggressor)
        return xtalk

    def check_array_idx(self, tsvidx_row, tsvidx_col):
        '''
        检查(tsvidx_row, tsvidx_col)是否为阵列中有效的位置
        :param tsvidx_row:
        :param tsvidx_col:
        :return: Bool
        '''
        assert isinstance(tsvidx_row, int)
        assert isinstance(tsvidx_col, int)
        if tsvidx_row < 0:
            return False
        if tsvidx_row >= self.get_n_row():
            return False
        if tsvidx_col < 0:
            return False
        if tsvidx_col >= self.get_n_col():
            return False
        return True


    def calc_xtalk_level_rectTopo(self, array_cw01, array_cw02, array_shield, edgeTSVXtalkZoom = 1, edgeTSVPunishment = 0):
        '''
        输入t-时刻阵列中传输的码字（array_cw01），t+时刻阵列中传输的码字（array_cw02），以及屏蔽标志位（array_shield），计算阵列中的串扰。

        :param array_cw01: 二维元组，元素为整数0或1，外层索引为行idx，内层索引位列idx。必须与阵列大小相对应。
        :param array_cw02: 二维元组，元素为整数0或1，外层索引为行idx，内层索引位列idx。必须与阵列大小相对应。
        :param array_shield: 二维元组，元素为bool(或整数0或)，True表示设置为屏蔽线，外层索引为行idx，内层索引位列idx。必须与阵列大小相对应。需要注意的是，被标记为屏蔽线的TSV上传输的数据应始终为0！
        :param edgeTSVXtalkZoom: int，默认为1。边缘TSV之间的串扰级别将乘以该数值。
        :param edgeTSVPunishment: int, 默认为0.该数值将被加到每个边缘TSV的串扰级别中。
        :return: cw_xtalk_tuple
        '''

        # Checks
        assert self.check_array_size(array_a=copy.deepcopy(array_cw01))
        assert self.check_array_size(array_a=copy.deepcopy(array_cw02))
        assert self.check_array_size(array_a=copy.deepcopy(array_shield))

        # Convert array_shield
        new_array_shield = []
        for sflags_ii in array_shield:
            new_sflags_row_i = []
            for sflag_iii in sflags_ii:
                if (sflag_iii == 1) or (sflag_iii is True):
                    new_sflags_row_i.append(True)
                elif (sflag_iii == 0) or (sflag_iii is False):
                    new_sflags_row_i.append(False)
                else:
                    print(sflag_iii)
                    assert False
            assert len(new_sflags_row_i) == len(sflags_ii)
            new_array_shield.append(tuple(new_sflags_row_i))
        assert len(new_array_shield) == len(array_shield)
        array_shield = tuple(new_array_shield)

        # Calc diff
        cw_diff_list = []
        for idx_row in range(0, self.get_n_row()):
            row_diff_list = []
            for idx_col in range(0, self.get_n_col()):
                cw01 = array_cw01[idx_row][idx_col]
                cw02 = array_cw02[idx_row][idx_col]
                assert cw01 in (0, 1)
                assert cw02 in (0, 1)
                cwdiff = cw02 - cw01
                row_diff_list.append(cwdiff)
                assert len(row_diff_list) == idx_col + 1
            cw_diff_list.append(tuple(row_diff_list))
            assert len(cw_diff_list) == idx_row + 1
        cw_diff_tuple = tuple(cw_diff_list)

        # Calc xtalk
        # 方法是分别计算：左， 右， 上， 下， 左上， 右下， 右上， 左下 的串扰，然后相加。
        cw_xtalk_list = []
        for idx_row in range(0, self.get_n_row()):
            row_xtalk_list = []
            for idx_col in range(0, self.get_n_col()):
                # 屏蔽线串扰等级为None
                if array_shield[idx_row][idx_col] is True:
                    row_xtalk_list.append(None)
                    assert len(row_xtalk_list) == idx_col + 1
                else:
                    # 左
                    if self.check_array_idx(tsvidx_row=idx_row, tsvidx_col=idx_col - 1) is False:
                        xtalk_a = 0
                    elif array_shield[idx_row][idx_col - 1] is True:
                        xtalk_a = 0
                    else:
                        xtalk_a = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                         diff_aggressor=cw_diff_tuple[idx_row][idx_col - 1])

                    # 右
                    if self.check_array_idx(tsvidx_row=idx_row, tsvidx_col=idx_col + 1) is False:
                        xtalk_d = 0
                    elif array_shield[idx_row][idx_col + 1] is True:
                        xtalk_d = 0
                    else:
                        xtalk_d = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                         diff_aggressor=cw_diff_tuple[idx_row][idx_col + 1])

                    # 上
                    if self.check_array_idx(tsvidx_row=idx_row - 1, tsvidx_col=idx_col) is False:
                        xtalk_w = 0
                    elif array_shield[idx_row - 1][idx_col] is True:
                        xtalk_w = 0
                    else:
                        xtalk_w = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                             diff_aggressor=cw_diff_tuple[idx_row - 1][idx_col])

                    # 下
                    if self.check_array_idx(tsvidx_row=idx_row + 1, tsvidx_col=idx_col) is False:
                        xtalk_s = 0
                    elif array_shield[idx_row + 1][idx_col] is True:
                        xtalk_s = 0
                    else:
                        xtalk_s = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                         diff_aggressor=cw_diff_tuple[idx_row + 1][idx_col])

                    # 左上
                    if self.check_array_idx(tsvidx_row=idx_row - 1, tsvidx_col=idx_col - 1) is False:
                        xtalk_aw = 0
                    elif array_shield[idx_row - 1][idx_col - 1] is True:
                        xtalk_aw = 0
                    else:
                        xtalk_aw = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                         diff_aggressor=cw_diff_tuple[idx_row - 1][idx_col - 1])

                    # 右上
                    if self.check_array_idx(tsvidx_row=idx_row - 1, tsvidx_col=idx_col + 1) is False:
                        xtalk_dw = 0
                    elif array_shield[idx_row - 1][idx_col + 1] is True:
                        xtalk_dw = 0
                    else:
                        xtalk_dw = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                          diff_aggressor=cw_diff_tuple[idx_row - 1][idx_col + 1])

                    # 左下
                    if self.check_array_idx(tsvidx_row=idx_row + 1, tsvidx_col=idx_col - 1) is False:
                        xtalk_as = 0
                    elif array_shield[idx_row + 1][idx_col - 1] is True:
                        xtalk_as = 0
                    else:
                        xtalk_as = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                          diff_aggressor=cw_diff_tuple[idx_row + 1][idx_col - 1])

                    # 右下
                    if self.check_array_idx(tsvidx_row=idx_row + 1, tsvidx_col=idx_col + 1) is False:
                        xtalk_ds = 0
                    elif array_shield[idx_row + 1][idx_col + 1] is True:
                        xtalk_ds = 0
                    else:
                        xtalk_ds = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                          diff_aggressor=cw_diff_tuple[idx_row + 1][idx_col + 1])


                    weight_with_edgeEffect = [1, 1, 1, 1]
                    edgeTSVFlag = False
                    if (idx_row == (self.get_n_row() - 1)) or (idx_row == 0):
                        weight_with_edgeEffect[0] = copy.deepcopy(edgeTSVXtalkZoom)
                        weight_with_edgeEffect[2] = copy.deepcopy(edgeTSVXtalkZoom)
                        edgeTSVFlag = True
                    if (idx_col == (self.get_n_col() - 1)) or (idx_col == 0):
                        weight_with_edgeEffect[1] = copy.deepcopy(edgeTSVXtalkZoom)
                        weight_with_edgeEffect[3] = copy.deepcopy(edgeTSVXtalkZoom)
                        edgeTSVFlag = True



                    xtalk_sum_float = ((xtalk_a * weight_with_edgeEffect[0]) +
                                 (xtalk_w * weight_with_edgeEffect[1]) +
                                 (xtalk_d * weight_with_edgeEffect[2]) +
                                 (xtalk_s * weight_with_edgeEffect[3]) +
                                 ( (xtalk_aw + xtalk_as + xtalk_dw + xtalk_ds) / 4 ))
                    if edgeTSVFlag is True:
                        xtalk_sum_float = xtalk_sum_float + edgeTSVPunishment

                    xtalk_sum = (math.ceil(xtalk_sum_float * 4)) / 4
                    row_xtalk_list.append(xtalk_sum)
                    assert len(row_xtalk_list) == idx_col + 1

            cw_xtalk_list.append(tuple(row_xtalk_list))
            assert len(cw_xtalk_list) == idx_row + 1
        cw_xtalk_tuple = tuple(cw_xtalk_list)

        return cw_xtalk_tuple

    def calc_xtalk_level_hexTopoA(self, array_cw01, array_cw02, array_shield, edgeTSVXtalkZoom = 1, edgeTSVPunishment = 0):
        '''
        输入t-时刻阵列中传输的码字（array_cw01），t+时刻阵列中传输的码字（array_cw02），以及屏蔽标志位（array_shield），计算阵列中的串扰。
        该六边形阵列拓扑是在矩形阵列基础上简单改动而来的：奇数行（或者说是行idx为偶数的行）整体左移一点，然后行之间距离缩小一点。

        :param array_cw01: 二维元组，元素为整数0或1，外层索引为行idx，内层索引位列idx。必须与阵列大小相对应。
        :param array_cw02: 二维元组，元素为整数0或1，外层索引为行idx，内层索引位列idx。必须与阵列大小相对应。
        :param array_shield: 二维元组，元素为bool(或整数0或)，True表示设置为屏蔽线，外层索引为行idx，内层索引位列idx。必须与阵列大小相对应。需要注意的是，被标记为屏蔽线的TSV上传输的数据应始终为0！
        :param edgeTSVXtalkZoom: int，默认为1。边缘TSV之间的串扰级别将乘以该数值。
        :param edgeTSVPunishment: int, 默认为0.该数值将被加到每个边缘TSV的串扰级别中。
        :return: cw_xtalk_tuple
        '''

        # Checks
        assert self.check_array_size(array_a=copy.deepcopy(array_cw01))
        assert self.check_array_size(array_a=copy.deepcopy(array_cw02))
        assert self.check_array_size(array_a=copy.deepcopy(array_shield))

        # Convert array_shield
        new_array_shield = []
        for sflags_ii in array_shield:
            new_sflags_row_i = []
            for sflag_iii in sflags_ii:
                if (sflag_iii == 1) or (sflag_iii is True):
                    new_sflags_row_i.append(True)
                elif (sflag_iii == 0) or (sflag_iii is False):
                    new_sflags_row_i.append(False)
                else:
                    print(sflag_iii)
                    assert False
            assert len(new_sflags_row_i) == len(sflags_ii)
            new_array_shield.append(tuple(new_sflags_row_i))
        assert len(new_array_shield) == len(array_shield)
        array_shield = tuple(new_array_shield)

        # Calc diff
        cw_diff_list = []
        for idx_row in range(0, self.get_n_row()):
            row_diff_list = []
            for idx_col in range(0, self.get_n_col()):
                cw01 = array_cw01[idx_row][idx_col]
                cw02 = array_cw02[idx_row][idx_col]
                assert cw01 in (0, 1)
                assert cw02 in (0, 1)
                cwdiff = cw02 - cw01
                row_diff_list.append(cwdiff)
                assert len(row_diff_list) == idx_col + 1
            cw_diff_list.append(tuple(row_diff_list))
            assert len(cw_diff_list) == idx_row + 1
        cw_diff_tuple = tuple(cw_diff_list)

        # Calc xtalk
        # 方法是分别计算：左， 右， 左上， 左下， 右上， 右下 的串扰，然后相加。
        cw_xtalk_list = []
        for idx_row in range(0, self.get_n_row()):
            row_xtalk_list = []
            for idx_col in range(0, self.get_n_col()):
                # 屏蔽线串扰等级为None
                if array_shield[idx_row][idx_col] is True:
                    row_xtalk_list.append(None)
                    assert len(row_xtalk_list) == idx_col + 1
                else:
                    is_edge_tsv = False
                    # 左
                    if self.check_array_idx(tsvidx_row=idx_row, tsvidx_col=idx_col - 1) is False:
                        xtalk_left = 0
                        is_edge_tsv = True
                    elif array_shield[idx_row][idx_col - 1] is True:
                        xtalk_left = 0
                    else:
                        xtalk_left = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                         diff_aggressor=cw_diff_tuple[idx_row][idx_col - 1])

                    # 右
                    if self.check_array_idx(tsvidx_row=idx_row, tsvidx_col=idx_col + 1) is False:
                        xtalk_right = 0
                        is_edge_tsv = True
                    elif array_shield[idx_row][idx_col + 1] is True:
                        xtalk_right = 0
                    else:
                        xtalk_right = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                         diff_aggressor=cw_diff_tuple[idx_row][idx_col + 1])

                    # 左上、左下、右上、右下的索引
                    if (idx_row % 2 == 0):
                        rowIdx_LU = idx_row - 1
                        colIdx_LU = idx_col - 1

                        rowIdx_RU = idx_row - 1
                        colIdx_RU = idx_col

                        rowIdx_LD = idx_row + 1
                        colIdx_LD = idx_col - 1

                        rowIdx_RD = idx_row + 1
                        colIdx_RD = idx_col

                    elif (idx_row % 2 == 1):
                        rowIdx_LU = idx_row - 1
                        colIdx_LU = idx_col

                        rowIdx_RU = idx_row - 1
                        colIdx_RU = idx_col + 1

                        rowIdx_LD = idx_row + 1
                        colIdx_LD = idx_col

                        rowIdx_RD = idx_row + 1
                        colIdx_RD = idx_col + 1

                    else:
                        assert False

                    # 左上
                    if self.check_array_idx(tsvidx_row=rowIdx_LU, tsvidx_col=colIdx_LU) is False:
                        xtalk_lu = 0
                        is_edge_tsv = True
                    elif array_shield[rowIdx_LU][colIdx_LU] is True:
                        xtalk_lu = 0
                    else:
                        xtalk_lu = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                             diff_aggressor=cw_diff_tuple[rowIdx_LU][colIdx_LU])

                    # 左下
                    if self.check_array_idx(tsvidx_row=rowIdx_LD, tsvidx_col=colIdx_LD) is False:
                        xtalk_ld = 0
                        is_edge_tsv = True
                    elif array_shield[rowIdx_LD][colIdx_LD] is True:
                        xtalk_ld = 0
                    else:
                        xtalk_ld = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                         diff_aggressor=cw_diff_tuple[rowIdx_LD][colIdx_LD])

                    # 右上
                    if self.check_array_idx(tsvidx_row=rowIdx_RU, tsvidx_col=colIdx_RU) is False:
                        xtalk_ru = 0
                        is_edge_tsv = True
                    elif array_shield[rowIdx_RU][colIdx_RU] is True:
                        xtalk_ru = 0
                    else:
                        xtalk_ru = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                         diff_aggressor=cw_diff_tuple[rowIdx_RU][colIdx_RU])

                    # 右下
                    if self.check_array_idx(tsvidx_row=rowIdx_RD, tsvidx_col=colIdx_RD) is False:
                        xtalk_rd = 0
                        is_edge_tsv = True
                    elif array_shield[rowIdx_RD][colIdx_RD] is True:
                        xtalk_rd = 0
                    else:
                        xtalk_rd = self.calc_xtalk_A_to_B(diff_victim=cw_diff_tuple[idx_row][idx_col],
                                                          diff_aggressor=cw_diff_tuple[rowIdx_RD][colIdx_RD])



                    weight_with_edgeEffect = [1, 1, 1, 1, 1, 1]
                    edgeTSVFlag = False
                    if (idx_row == (self.get_n_row() - 1)) or (idx_row == 0):
                        weight_with_edgeEffect[0] = copy.deepcopy(edgeTSVXtalkZoom)
                        weight_with_edgeEffect[1] = copy.deepcopy(edgeTSVXtalkZoom)
                        edgeTSVFlag = True
                    if (idx_col == (self.get_n_col() - 1)) or (idx_col == 0):
                        edgeTSVFlag = True
                        if (idx_row % 2 == 0):
                            weight_with_edgeEffect[2] = copy.deepcopy(edgeTSVXtalkZoom)
                            weight_with_edgeEffect[3] = copy.deepcopy(edgeTSVXtalkZoom)
                        elif (idx_row % 2 == 1):
                            weight_with_edgeEffect[4] = copy.deepcopy(edgeTSVXtalkZoom)
                            weight_with_edgeEffect[5] = copy.deepcopy(edgeTSVXtalkZoom)
                        else:
                            assert False
                    xtalk_sum_float = ((xtalk_left * weight_with_edgeEffect[0]) +
                                 (xtalk_right * weight_with_edgeEffect[1]) +
                                 (xtalk_lu * weight_with_edgeEffect[2]) +
                                 (xtalk_ld * weight_with_edgeEffect[3]) +
                                 (xtalk_ru * weight_with_edgeEffect[4]) +
                                 (xtalk_rd * weight_with_edgeEffect[5]))
                    if edgeTSVFlag is True:
                        xtalk_sum_float = xtalk_sum_float + edgeTSVPunishment


                    xtalk_sum = (math.ceil(xtalk_sum_float * 4)) / 4

                    row_xtalk_list.append(xtalk_sum)
                    assert len(row_xtalk_list) == idx_col + 1

            cw_xtalk_list.append(tuple(row_xtalk_list))
            assert len(cw_xtalk_list) == idx_row + 1
        cw_xtalk_tuple = tuple(cw_xtalk_list)

        return cw_xtalk_tuple

    def xtalk_level_cnt(self, cw_xtalk_tuple):
        '''
        统计各个串扰等级对应的TSV数目
        :param cw_xtalk_tuple:
        :return:
        '''
        cnt_xtalk = {0 : 0,
                     0.25 : 0,
                     0.5 : 0,
                     0.75 : 0,
                     1 : 0,
                     1.25 : 0,
                     1.5 : 0,
                     1.75 : 0,
                     2 : 0,
                     2.25 : 0,
                     2.5 : 0,
                     2.75 : 0,
                     3 : 0,
                     3.25 : 0,
                     3.5 : 0,
                     3.75 : 0,
                     4 : 0,
                     4.25 : 0,
                     4.5 : 0,
                     4.75 : 0,
                     5 : 0,
                     5.25 : 0,
                     5.5 : 0,
                     5.75 : 0,
                     6 : 0,
                     6.25 : 0,
                     6.5 : 0,
                     6.75 : 0,
                     7 : 0,
                     7.25 : 0,
                     7.5 : 0,
                     7.75 : 0,
                     8 : 0,
                     8.25 : 0,
                     8.5 : 0,
                     8.75 : 0,
                     9 : 0,
                     9.25 : 0,
                     9.5 : 0,
                     9.75 : 0,
                     10 : 0,
                     10.25 : 0,
                     10.5 : 0,
                     10.75 : 0,
                     11 : 0,
                     11.25 : 0,
                     11.5 : 0,
                     11.75 : 0,
                     12 : 0,
                     'None' : 0}
        for tuple_ii in cw_xtalk_tuple:
            for level_ii in tuple_ii:
                if level_ii in (0, 0.25, 0.5, 0.75,
                                1, 1.25, 1.5, 1.75,
                                2, 2.25, 2.5, 2.75,
                                3, 3.25, 3.5, 3.75,
                                4, 4.25, 4.5, 4.75,
                                5, 5.25, 5.5, 5.75,
                                6, 6.25, 6.5, 6.75,
                                7, 7.25, 7.5, 7.75,
                                8, 8.25, 8.5, 8.75,
                                9, 9.25, 9.5, 9.75,
                                10, 10.25, 10.5, 10.75,
                                11, 11.25, 11.5, 11.75,
                                12):
                    cnt_xtalk[level_ii] = cnt_xtalk[level_ii] + 1
                else:
                    assert level_ii is None
                    cnt_xtalk['None'] = cnt_xtalk['None'] + 1

        return copy.deepcopy(cnt_xtalk)


