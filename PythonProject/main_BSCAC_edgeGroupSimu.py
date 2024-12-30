import copy

import RingCAC_Alg.BitStuffingCAC_Codec as BitStuffingCAC_Codec


########################################################################################################################
######################
#         d1         #
#   d6          d2   #
#         d0         #
#   d5          d3   #
#         d4         #
######################

# Parameters
is_realTSV = (False,  # d0
              True,  # d1
              True,  # d2
              False,  # d3
              False,  # d4
              False,  # d5
              True)  # d6

########################################################################################################################

virtualTSVs_idxList = []
realTSVs_idxList = []
for idx_i in range(0, 7):
    if is_realTSV[idx_i] is True:
        realTSVs_idxList.append(idx_i)
    elif is_realTSV[idx_i] is False:
        virtualTSVs_idxList.append(idx_i)
    else:
        assert False
virtualTSVs_idxTuple = tuple(virtualTSVs_idxList)
realTSVs_idxTuple = tuple(realTSVs_idxList)
n_virtualTSVs = len(virtualTSVs_idxTuple)
n_realTSVs = len(realTSVs_idxTuple)

n_traverseBW = 2 * n_realTSVs
BSCACCodec_instance01 = BitStuffingCAC_Codec.BSCAC_ForHexDyS2C_2CSupFor7bitGroup_Main()
cnt_bitsTransmitted_all = 0
cnt_bitsNotTransmitted_all = 0
cnt_bitsTransmitted_stsv = 0
cnt_bitsNotTransmitted_stsv = 0

for traverse_v in range(0, (2 ** n_traverseBW)):
    traverse_tuple = tuple(bin(traverse_v)[2:].zfill(n_traverseBW))
    gp_lastState_list = []
    gp_dataWaiting_list = []
    gp_lastState_charlist = []
    gp_dataWaiting_charlist = []
    traverse_list_temp = list(traverse_tuple)
    for idx_j in range(0, 7):
        if is_realTSV[idx_j] is False:
            gp_lastState_charlist.append('0')
        elif is_realTSV[idx_j] is True:
            assert len(traverse_list_temp) > 0
            gp_lastState_charlist.append(copy.deepcopy(traverse_list_temp.pop()))
        else:
            assert False
    for idx_j in range(0, 7):
        if is_realTSV[idx_j] is False:
            gp_dataWaiting_charlist.append('0')
        elif is_realTSV[idx_j] is True:
            assert len(traverse_list_temp) > 0
            gp_dataWaiting_charlist.append(copy.deepcopy(traverse_list_temp.pop()))
        else:
            assert False

    assert len(gp_lastState_charlist) == len(gp_dataWaiting_charlist) == 7
    for idx_k in range(0, 7):
        gp_dataWaiting_char_i = gp_dataWaiting_charlist.pop(0)
        gp_lastState_char_i = gp_lastState_charlist.pop(0)
        if gp_dataWaiting_char_i == '0':
            gp_dataWaiting_list.append(0)
        elif gp_dataWaiting_char_i == '1':
            gp_dataWaiting_list.append(1)
        else:
            print("ERROR: Unexpected value {}".format(gp_dataWaiting_char_i))
            assert False

        if gp_lastState_char_i == '0':
            gp_lastState_list.append(0)
        elif gp_lastState_char_i == '1':
            gp_lastState_list.append(1)
        else:
            print("ERROR: Unexpected value {}".format(gp_lastState_char_i))
            assert False


    gp_lastState_tuple = tuple(gp_lastState_list)

    codeword_tuple, n_bitTransmitted, ifTransmitted_tuple = BSCACCodec_instance01.encoder_core(bits_to_be_trans=copy.deepcopy(gp_dataWaiting_list), last_codeword=gp_lastState_tuple)
    cnt_realBitsTransmitted = 0
    cnt_realBitsNotTransmitted = 0
    for idx_j in range(0, 7):
        if is_realTSV[idx_j] is True:
            if ifTransmitted_tuple[idx_j] is True:
                cnt_realBitsTransmitted = cnt_realBitsTransmitted + 1
            elif ifTransmitted_tuple[idx_j] is False:
                cnt_realBitsNotTransmitted = cnt_realBitsNotTransmitted + 1
            else:
                assert False
        else:
            assert is_realTSV[idx_j] is False
            assert codeword_tuple[idx_j] == 0

    cnt_bitsTransmitted_all = cnt_bitsTransmitted_all + cnt_realBitsTransmitted
    cnt_bitsNotTransmitted_all = cnt_bitsNotTransmitted_all + cnt_realBitsNotTransmitted
    cnt_bitsTransmitted_stsv = cnt_bitsTransmitted_stsv + cnt_realBitsTransmitted
    cnt_bitsNotTransmitted_stsv = cnt_bitsNotTransmitted_stsv + cnt_realBitsNotTransmitted
    if is_realTSV[0] is True:
        assert ifTransmitted_tuple[0] is True
        cnt_bitsTransmitted_stsv = cnt_bitsTransmitted_stsv - 1
    print("{} >>> {}---[{}]---> transmitted + {} = {} (STSVs only = {}), blocked + {} = {}".format(traverse_v,
                                                                                                   gp_lastState_tuple,
                                                                                                   gp_dataWaiting_list,
                                                                                                   cnt_realBitsTransmitted,
                                                                                                   cnt_bitsTransmitted_all,
                                                                                                   cnt_bitsTransmitted_stsv,
                                                                                                   cnt_realBitsNotTransmitted,
                                                                                                   cnt_bitsNotTransmitted_all))

print("The probability of STSVs labeled as FREE = {} / {} = {}".format(cnt_bitsTransmitted_stsv,
                                                                       (cnt_bitsTransmitted_stsv + cnt_bitsNotTransmitted_all),
                                                                       (cnt_bitsTransmitted_stsv/(cnt_bitsTransmitted_stsv + cnt_bitsNotTransmitted_all))))



