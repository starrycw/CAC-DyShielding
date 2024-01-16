import copy
import random
import time

import RingCAC_Alg.BitStuffingCAC_Codec

if True: # Testbench for Bit-stuffing CAC class BSCAC_ForHexDyS2C_2CSupFor7bitGroup - V20231223
    Codec01 = RingCAC_Alg.BitStuffingCAC_Codec.BSCAC_ForHexDyS2C_2CSupFor7bitGroup_ver20231224(instance_id=time.time())
    cnt_transmittedDataBits = 0
    cnt_min_nDataProcessed = 7
    cntList_sumStuffingBits = [0, 0, 0, 0, 0, 0, 0]

    cwrand_init = []
    for idx_ii in range(0, 7):
        cwrand_init.append(random.choice((0, 1)))

    cwTuple_last = tuple(cwrand_init)
    for simu_step_idx in range(0, 1000000):
        datarand_new = []
        for idx_ii in range(0, 7):
            datarand_new.append(random.choice((0, 1)))
        dataTuple_in = tuple(datarand_new)

        cwTuple_output, n_dataProcessed, dataList_unprocessed = Codec01.encoder_core(bits_to_be_trans=list(dataTuple_in), last_codeword=cwTuple_last)
        dataTuple_output, flagTuple_stuffingbit = Codec01.decoder_core(codeword_to_be_decode=cwTuple_output, last_codeword=cwTuple_last)

        xtalk_value = Codec01.xtalkCalc(codeword_tuple_last=cwTuple_last, codeword_tuple_current=cwTuple_output)

        # print("Step-{} {} - {}/{} ({}) -> {} ({}) -> {}".format(simu_step_idx, cwTuple_last, dataTuple_in, dataList_unprocessed, n_dataProcessed, cwTuple_output, xtalk_value, dataTuple_output))
        print("Step-{}: dataIn={}, dataUnprocessed={}, n_dataProcessed={}, dataOut={}".format(simu_step_idx, dataTuple_in, dataList_unprocessed, n_dataProcessed, dataTuple_output))
        print("         codeword: {} -> {}, xtalk={}, idxStuffing={}".format(cwTuple_last, cwTuple_output, xtalk_value, flagTuple_stuffingbit))
        assert ( len(dataTuple_output) == n_dataProcessed )
        if cnt_min_nDataProcessed > len(dataTuple_output):
            cnt_min_nDataProcessed = len(dataTuple_output)
        for idx_kk in range(0, n_dataProcessed):
            assert dataTuple_output[idx_kk] == dataTuple_in[idx_kk]

        cwTuple_last = copy.deepcopy(cwTuple_output)
        cnt_transmittedDataBits = cnt_transmittedDataBits + n_dataProcessed

        for idx_stuffing in flagTuple_stuffingbit:
            cntList_sumStuffingBits[idx_stuffing] = cntList_sumStuffingBits[idx_stuffing] + 1

    print("{} / {} = {}".format(cnt_transmittedDataBits, (simu_step_idx + 1), cnt_transmittedDataBits / (simu_step_idx + 1)))
    print("Min length of the data processed in single cycle: {}".format(cnt_min_nDataProcessed))
    print("Stuffing bits count: {}".format(cntList_sumStuffingBits))

