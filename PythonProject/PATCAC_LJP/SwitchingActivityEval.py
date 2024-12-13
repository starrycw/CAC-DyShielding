import copy
import random

import PATCAC_Codec as PATCAC_Codec
import FNSCAC_Codec as FNSCAC_Codec
import IFNSCAC_Codec as IFNSCAC_Codec

################################################################################
def transBit_count(cw_1, cw_2):
    assert len(cw_1) == len(cw_2)
    cnt_trans = 0
    cnt_rise = 0
    cnt_fall = 0
    for i in range(0, len(cw_1)):
        if (cw_1[i], cw_2[i]) == (0, 1):
            cnt_trans = cnt_trans + 1
            cnt_rise = cnt_rise + 1
        elif (cw_1[i], cw_2[i]) == (1, 0):
            cnt_trans = cnt_trans + 1
            cnt_fall = cnt_fall + 1
        else:
            assert (cw_1[i], cw_2[i]) == (0, 0) or (cw_1[i], cw_2[i]) == (1, 1)

    return cnt_trans, cnt_rise, cnt_fall


################################################################################
def runSimu_FNSFPF(cw_len, n_cycle):
    '''

    :param cw_len:
    :param n_cycle:
    :return:
    '''
    Codec_instance = FNSCAC_Codec.FNSCAC_Codec(n_cw=cw_len)
    maxInput = Codec_instance.getParam_maxInputValue()
    cnt_trans_all = 0
    cnt_rise_all = 0
    cnt_fall_all = 0
    max_nTrans_oneCycle = 0
    max_nRise_oneCycle = 0
    max_nFall_oneCycle = 0
    cw_1 = cw_len * (0,)
    for i in range(0, n_cycle):
        value_random = random.randint(0, maxInput)
        cw_2 = Codec_instance.encode_FNSFPF(value=value_random)
        cnt_trans, cnt_rise, cnt_fall = transBit_count(cw_1=cw_1, cw_2=cw_2)
        cnt_trans_all = cnt_trans_all + cnt_trans
        cnt_rise_all = cnt_rise_all + cnt_rise
        cnt_fall_all = cnt_fall_all + cnt_fall
        if max_nTrans_oneCycle < cnt_trans:
            max_nTrans_oneCycle = cnt_trans
        if max_nRise_oneCycle < cnt_rise:
            max_nRise_oneCycle = cnt_rise
        if max_nFall_oneCycle < cnt_fall:
            max_nFall_oneCycle = cnt_fall
        cw_1 = copy.deepcopy(cw_2)

    return cnt_trans_all, cnt_rise_all, cnt_fall_all, max_nTrans_oneCycle, max_nRise_oneCycle, max_nFall_oneCycle


################################################################################
def runSimu_FNSFTF(cw_len, n_cycle):
    '''

    :param cw_len:
    :param n_cycle:
    :return:
    '''
    Codec_instance = FNSCAC_Codec.FNSCAC_Codec(n_cw=cw_len)
    maxInput = Codec_instance.getParam_maxInputValue()
    cnt_trans_all = 0
    cnt_rise_all = 0
    cnt_fall_all = 0
    max_nTrans_oneCycle = 0
    max_nRise_oneCycle = 0
    max_nFall_oneCycle = 0
    cw_1 = cw_len * (0,)
    for i in range(0, n_cycle):
        value_random = random.randint(0, maxInput)
        cw_2 = Codec_instance.encode_FNSFTF(value=value_random)
        cnt_trans, cnt_rise, cnt_fall = transBit_count(cw_1=cw_1, cw_2=cw_2)
        cnt_trans_all = cnt_trans_all + cnt_trans
        cnt_rise_all = cnt_rise_all + cnt_rise
        cnt_fall_all = cnt_fall_all + cnt_fall
        if max_nTrans_oneCycle < cnt_trans:
            max_nTrans_oneCycle = cnt_trans
        if max_nRise_oneCycle < cnt_rise:
            max_nRise_oneCycle = cnt_rise
        if max_nFall_oneCycle < cnt_fall:
            max_nFall_oneCycle = cnt_fall
        cw_1 = copy.deepcopy(cw_2)

    return cnt_trans_all, cnt_rise_all, cnt_fall_all, max_nTrans_oneCycle, max_nRise_oneCycle, max_nFall_oneCycle


################################################################################
def runSimu_IFNS(cw_len, n_cycle):
    '''

    :param cw_len:
    :param n_cycle:
    :return:
    '''
    Codec_instance = IFNSCAC_Codec.IFNSCAC_Codec(n_cw=cw_len)
    maxInput = Codec_instance.getParam_maxInputValue()
    cnt_trans_all = 0
    cnt_rise_all = 0
    cnt_fall_all = 0
    max_nTrans_oneCycle = 0
    max_nRise_oneCycle = 0
    max_nFall_oneCycle = 0
    cw_1 = cw_len * (0,)
    for i in range(0, n_cycle):
        value_random = random.randint(0, maxInput)
        cw_2 = Codec_instance.encode_IFNS(value=value_random)
        cnt_trans, cnt_rise, cnt_fall = transBit_count(cw_1=cw_1, cw_2=cw_2)
        cnt_trans_all = cnt_trans_all + cnt_trans
        cnt_rise_all = cnt_rise_all + cnt_rise
        cnt_fall_all = cnt_fall_all + cnt_fall
        if max_nTrans_oneCycle < cnt_trans:
            max_nTrans_oneCycle = cnt_trans
        if max_nRise_oneCycle < cnt_rise:
            max_nRise_oneCycle = cnt_rise
        if max_nFall_oneCycle < cnt_fall:
            max_nFall_oneCycle = cnt_fall
        cw_1 = copy.deepcopy(cw_2)

    return cnt_trans_all, cnt_rise_all, cnt_fall_all, max_nTrans_oneCycle, max_nRise_oneCycle, max_nFall_oneCycle

################################################################################
def runSimu_PATCAC(cw_len, n_cycle):
    '''

    :param cw_len:
    :param n_cycle:
    :return:
    '''
    Codec_instance = PATCAC_Codec.PATCAC_Codec(len_cw=cw_len)
    maxInput = Codec_instance.getParam_maxInputLimitation()
    cnt_trans_all = 0
    cnt_rise_all = 0
    cnt_fall_all = 0
    max_nTrans_oneCycle = 0
    max_nRise_oneCycle = 0
    max_nFall_oneCycle = 0
    cw_list = cw_len * [0]
    cw_1 = cw_len * (0,)
    for i in range(0, n_cycle):
        value_random = random.randint(0, maxInput)
        cw_trans = Codec_instance.encode(value=value_random)
        for cwtrans_idx in range(0, cw_len):
            if cw_trans[cwtrans_idx] == 1:
                cw_list[cwtrans_idx] = 1 - cw_list[cwtrans_idx]
            else:
                assert cw_trans[cwtrans_idx] == 0
        cw_2 = tuple(cw_list)
        cnt_trans, cnt_rise, cnt_fall = transBit_count(cw_1=cw_1, cw_2=cw_2)
        cnt_trans_all = cnt_trans_all + cnt_trans
        cnt_rise_all = cnt_rise_all + cnt_rise
        cnt_fall_all = cnt_fall_all + cnt_fall
        if max_nTrans_oneCycle < cnt_trans:
            max_nTrans_oneCycle = cnt_trans
        if max_nRise_oneCycle < cnt_rise:
            max_nRise_oneCycle = cnt_rise
        if max_nFall_oneCycle < cnt_fall:
            max_nFall_oneCycle = cnt_fall
        cw_1 = copy.deepcopy(cw_2)

    return cnt_trans_all, cnt_rise_all, cnt_fall_all, max_nTrans_oneCycle, max_nRise_oneCycle, max_nFall_oneCycle


###################################################################################
###################################################################################
# MAIN
n_cycle = 1000
for cw_len in range(4, 10):
    print("\n---------------------------------------------------------------------------------------------------------------")
    print("Codeword Transition Count - 位宽={}, 周期数={}".format(cw_len, n_cycle))
    # print("--- FNSFPF...")
    simuResult_FNSFPF = runSimu_FNSFPF(cw_len = cw_len, n_cycle = n_cycle)
    # print("--- FNSFPF OK!")
    # print("--- FNSFTF...")
    simuResult_FNSFTF = runSimu_FNSFTF(cw_len = cw_len, n_cycle = n_cycle)
    # print("--- FNSFTF OK!")
    # print("--- IFNS...")
    simuResult_IFNS = runSimu_IFNS(cw_len = cw_len, n_cycle = n_cycle)
    # print("--- IFNS OK!")
    # print("--- FNSCACTF...")
    simuResult_PATCAC = runSimu_PATCAC(cw_len = cw_len, n_cycle = n_cycle)
    # print("--- PATCAC OK!")
    print("---------------------------------------------------------------------------------------------------------------")
    print("[Name]: ([跳变总数], [0->1总数], [1->0总数], [单周期最大0->1总数], [单周期最大跳变总数], [单周期最大1->0总数])")
    # print("---------------------------------------------------------------------------------------------------------------")

    print("FNS-FPF: {}".format(simuResult_FNSFPF))
    print("FNS-FTF: {}".format(simuResult_FNSFTF))
    print("FNS-IFNS: {}".format(simuResult_IFNS))
    print("PAT: {}".format(simuResult_PATCAC))
    print("---------------------------------------------------------------------------------------------------------------")