import copy
import random
import time

import RingCAC_Alg.BitStuffingCAC_Codec

if True: # Testbench for Bit-stuffing CAC
    simuStep_max = 10000000
    Codec01 = RingCAC_Alg.BitStuffingCAC_Codec.BSCAC_ForHexDyS2C_2CSupFor7bitGroup_Main(instance_id=time.time())
    cnt_transmittedDataBits = 0
    cnt_transmittedDataBits_signalBitsOnly = 0
    cnt_min_nDataProcessed = 7
    cntList_sumStuffingBits = [0, 0, 0, 0, 0, 0, 0]

    xtalkCntDict_encoded = {0: 0,
                            1: 0,
                            2: 0,
                            3: 0,
                            4: 0,
                            5: 0,
                            6: 0,
                            7: 0,
                            8: 0,
                            9: 0,
                            10: 0,
                            11: 0,
                            12: 0}
    xtalkCntDict_rawData = {0: 0,
                            1: 0,
                            2: 0,
                            3: 0,
                            4: 0,
                            5: 0,
                            6: 0,
                            7: 0,
                            8: 0,
                            9: 0,
                            10: 0,
                            11: 0,
                            12: 0}

    cwrand_init = []
    for idx_ii in range(0, 7):
        cwrand_init.append(random.choice((0, 1)))

    cwTuple_last = tuple(cwrand_init)
    for simu_step_idx in range(0, simuStep_max):
        datarand_new = []
        for idx_ii in range(0, 7):
            datarand_new.append(random.choice((0, 1)))
        dataTuple_in = tuple(datarand_new)

        cwTuple_output, n_dataProcessed, flagList_processed = Codec01.encoder_core(bits_to_be_trans=list(dataTuple_in), last_codeword=cwTuple_last)
        dataTuple_output, flagTuple_stuffingbit = Codec01.decoder_core(codeword_to_be_decode=cwTuple_output, last_codeword=cwTuple_last)

        xtalk_value = Codec01.xtalkCalc(codeword_tuple_last=cwTuple_last, codeword_tuple_current=cwTuple_output)
        xtalk_value_rawData = Codec01.xtalkCalc_noAssert(codeword_tuple_last=cwTuple_last, codeword_tuple_current=dataTuple_in)
        for xtalk_value_iii in xtalk_value[1:]:
            xtalkCntDict_encoded[xtalk_value_iii] = xtalkCntDict_encoded[xtalk_value_iii] + 1
        for xtalk_value_rawData_iii in xtalk_value_rawData[1:]:
            xtalkCntDict_rawData[xtalk_value_rawData_iii] = xtalkCntDict_rawData[xtalk_value_rawData_iii] + 1

        # print("Step-{} {} - {}/{} ({}) -> {} ({}) -> {}".format(simu_step_idx, cwTuple_last, dataTuple_in, dataList_unprocessed, n_dataProcessed, cwTuple_output, xtalk_value, dataTuple_output))
        print("Step-{}: dataIn={}, flagProcessed={}, n_dataProcessed={}, dataOut={}".format(simu_step_idx, dataTuple_in, flagList_processed, n_dataProcessed, dataTuple_output))
        print("         codeword: {} -> {}, xtalk={}, idxStuffing={}".format(cwTuple_last, cwTuple_output, xtalk_value, flagTuple_stuffingbit))
        assert ( len(dataTuple_output) == 7 )
        cnt_nProcessed = 0
        for idx_flagBool_iii in range(0, 7):
            if flagList_processed[idx_flagBool_iii] is False:
                assert dataTuple_output[idx_flagBool_iii] is None
            else:
                assert flagList_processed[idx_flagBool_iii] is True
                assert dataTuple_output[idx_flagBool_iii] in (0, 1)
                assert dataTuple_output[idx_flagBool_iii] == dataTuple_in[idx_flagBool_iii]
                cnt_nProcessed = cnt_nProcessed + 1
        assert cnt_nProcessed == n_dataProcessed
        if cnt_min_nDataProcessed > cnt_nProcessed:
            cnt_min_nDataProcessed = cnt_nProcessed

        cwTuple_last = copy.deepcopy(cwTuple_output)
        cnt_transmittedDataBits = cnt_transmittedDataBits + n_dataProcessed
        assert n_dataProcessed > 1
        cnt_transmittedDataBits_signalBitsOnly = cnt_transmittedDataBits_signalBitsOnly + n_dataProcessed - 1


        for idx_stuffing in flagTuple_stuffingbit:
            cntList_sumStuffingBits[idx_stuffing] = cntList_sumStuffingBits[idx_stuffing] + 1

    print("Coding rate = {} / ({} * 7) = {}".format(cnt_transmittedDataBits, simuStep_max, cnt_transmittedDataBits / (simuStep_max * 7)))
    print("Coding rate (signal bits only) = {} / ({} * 6) = {}".format(cnt_transmittedDataBits_signalBitsOnly, simuStep_max, cnt_transmittedDataBits_signalBitsOnly / (simuStep_max * 6)))
    print("Min length of the data processed in single cycle: {}".format(cnt_min_nDataProcessed))
    print("Stuffing bits count: {}".format(cntList_sumStuffingBits))
    print("xtalk - raw - {}".format(xtalkCntDict_rawData))
    print("xtalk - encoded - {}".format(xtalkCntDict_encoded))
    bitOHEsti_all = 9
    bitOHEsti_trans = (cnt_transmittedDataBits_signalBitsOnly / simuStep_max) + 1
    bitOHEsti_float = (bitOHEsti_all - bitOHEsti_trans) / bitOHEsti_trans
    print("Bit Overhead Estimation: {}".format(bitOHEsti_float))

