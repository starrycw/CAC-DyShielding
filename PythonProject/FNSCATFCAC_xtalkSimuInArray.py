import copy
import random

import Evaluation_Tools.array_xtalk_simu
import RingCAC_Alg.Ring2CTransCAC_Codec
import OtherCAC_Alg.IFNSCAC_Codec
import OtherCAC_Alg.FNSCAC_Codec


class FNSCATF_xtalkSimu:
    def __init__(self, instance_id = None):
        self.instance_id = copy.deepcopy(instance_id)
    def codewordMapping_CATF_2x4_in_16x16(self, codeword_tuple):
        '''
        输入16个16-bit的码字，将每个码字组织为2x8的group，映射于16x16的阵列中。
        :param codeword_tuple:
        :return:
        '''
        assert isinstance(codeword_tuple, tuple)
        assert len(codeword_tuple) == 32

        group_rowIdx_init = 0
        group_colId_init = 0

        mappingList = []
        for idx_i in range(0, 16):
            mappingList.append(
                [None, None, None, None,
                 None, None, None, None,
                 None, None, None, None,
                 None, None, None, None]
            )
            assert len(codeword_tuple[idx_i]) == 8

        for codeword_id in range(0, 32):
            # bit 1
            if codeword_tuple[codeword_id][0] == 0:
                mappingList[group_rowIdx_init][group_colId_init] = 0
            elif codeword_tuple[codeword_id][0] == 1:
                mappingList[group_rowIdx_init][group_colId_init] = 1
            else:
                assert False

            # bit 2
            if codeword_tuple[codeword_id][1] == 0:
                mappingList[group_rowIdx_init][group_colId_init + 1] = 0
            elif codeword_tuple[codeword_id][1] == 1:
                mappingList[group_rowIdx_init][group_colId_init + 1] = 1
            else:
                assert False

            # bit 3
            if codeword_tuple[codeword_id][2] == 0:
                mappingList[group_rowIdx_init][group_colId_init + 2] = 0
            elif codeword_tuple[codeword_id][2] == 1:
                mappingList[group_rowIdx_init][group_colId_init + 2] = 1
            else:
                assert False

            # bit 4
            if codeword_tuple[codeword_id][3] == 0:
                mappingList[group_rowIdx_init][group_colId_init + 3] = 0
            elif codeword_tuple[codeword_id][3] == 1:
                mappingList[group_rowIdx_init][group_colId_init + 3] = 1
            else:
                assert False

            # bit 5
            if codeword_tuple[codeword_id][4] == 0:
                mappingList[group_rowIdx_init + 1][group_colId_init + 3] = 0
            elif codeword_tuple[codeword_id][4] == 1:
                mappingList[group_rowIdx_init + 1][group_colId_init + 3] = 1
            else:
                assert False

            # bit 6
            if codeword_tuple[codeword_id][5] == 0:
                mappingList[group_rowIdx_init + 1][group_colId_init + 2] = 0
            elif codeword_tuple[codeword_id][5] == 1:
                mappingList[group_rowIdx_init + 1][group_colId_init + 2] = 1
            else:
                assert False

            # bit 7
            if codeword_tuple[codeword_id][6] == 0:
                mappingList[group_rowIdx_init + 1][group_colId_init + 1] = 0
            elif codeword_tuple[codeword_id][6] == 1:
                mappingList[group_rowIdx_init + 1][group_colId_init + 1] = 1
            else:
                assert False

            # bit 8
            if codeword_tuple[codeword_id][7] == 0:
                mappingList[group_rowIdx_init + 1][group_colId_init] = 0
            elif codeword_tuple[codeword_id][7] == 1:
                mappingList[group_rowIdx_init + 1][group_colId_init] = 1
            else:
                assert False

            group_colId_init = group_colId_init + 4
            if group_colId_init == 16:
                group_colId_init = 0
                group_rowIdx_init = group_rowIdx_init + 2
            else:
                assert group_colId_init in (0, 4, 8, 12)

        assert group_colId_init == 0
        assert group_rowIdx_init == 16

        mappingList_tupleElements = []
        for list_i in mappingList:
            mappingList_tupleElements.append(tuple(copy.deepcopy(list_i)))
        assert len(mappingList_tupleElements) == 16
        mappingTuple = tuple(copy.deepcopy(mappingList_tupleElements))

        return mappingTuple

    def genCodes_FNSCATF_8bitx32(self, lastStates_tuple, value_tuple):
        assert isinstance(lastStates_tuple, tuple)
        assert isinstance(value_tuple, tuple)
        assert len(lastStates_tuple) == 32
        assert len(value_tuple) == 32

        FNSCATFCodec_instance01 = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC_FNSCATF(len_cw=8)

        decValue_upperBound = FNSCATFCodec_instance01.getParam_maxInputLimitation()
        codes_list = []
        for idx_aa in range(0, 32):
            assert value_tuple[idx_aa] <= decValue_upperBound
            assert value_tuple[idx_aa] >= 0
            assert len(lastStates_tuple[idx_aa]) == 8
            code_gen = FNSCATFCodec_instance01.encoder_top(decValue_int=copy.deepcopy(value_tuple[idx_aa]), lastState_tuple=copy.deepcopy(lastStates_tuple[idx_aa]))
            codes_list.append(copy.deepcopy(code_gen))

            decodeResult = FNSCATFCodec_instance01.decoder_top(xorCodeword_tuple=copy.deepcopy(code_gen), lastState_tuple=copy.deepcopy(lastStates_tuple[idx_aa]))
            assert decodeResult == value_tuple[idx_aa]

        codes_tuple = tuple(copy.deepcopy(codes_list))

        return codes_tuple

    def genCodes_FNSFPF_16bitx16(self, value_tuple):
        # assert isinstance(lastStates_tuple, tuple)
        assert isinstance(value_tuple, tuple)
        # assert len(lastStates_tuple) == 16
        assert len(value_tuple) == 16

        FNSCodec_instance01 = OtherCAC_Alg.FNSCAC_Codec.FNSCAC_Codec(n_cw=16)

        decValue_upperBound = FNSCodec_instance01.getParam_maxInputValue()
        codes_list = []

        for idx_aa in range(0, 16):
            assert value_tuple[idx_aa] <= decValue_upperBound
            assert value_tuple[idx_aa] >= 0
            # assert len(lastStates_tuple[idx_aa]) == 8
            # code_gen = FNSCATFCodec_instance01.encoder_top(decValue_int=copy.deepcopy(value_tuple[idx_aa]), lastState_tuple=copy.deepcopy(lastStates_tuple[idx_aa]))
            code_gen = FNSCodec_instance01.encode_FNSFPF(value=copy.deepcopy(value_tuple[idx_aa]), codewordType='int')
            codes_list.append(copy.deepcopy(code_gen))

            decodeResult = FNSCodec_instance01.decoder_FNS(codeword_tuple=copy.deepcopy(code_gen), codewordType='int')
            assert decodeResult == value_tuple[idx_aa]

        codes_tuple = tuple(copy.deepcopy(codes_list))

        return codes_tuple

    def genCodes_FNSFPF_12bitx9(self, value_tuple):
        # assert isinstance(lastStates_tuple, tuple)
        assert isinstance(value_tuple, tuple)
        # assert len(lastStates_tuple) == 16
        assert len(value_tuple) == 12

        FNSCodec_instance01 = OtherCAC_Alg.FNSCAC_Codec.FNSCAC_Codec(n_cw=9)

        decValue_upperBound = FNSCodec_instance01.getParam_maxInputValue()
        codes_list = []

        for idx_aa in range(0, 12):
            assert value_tuple[idx_aa] <= decValue_upperBound
            assert value_tuple[idx_aa] >= 0
            # assert len(lastStates_tuple[idx_aa]) == 8
            # code_gen = FNSCATFCodec_instance01.encoder_top(decValue_int=copy.deepcopy(value_tuple[idx_aa]), lastState_tuple=copy.deepcopy(lastStates_tuple[idx_aa]))
            code_gen = FNSCodec_instance01.encode_FNSFPF(value=copy.deepcopy(value_tuple[idx_aa]), codewordType='int')
            codes_list.append(copy.deepcopy(code_gen))

            decodeResult = FNSCodec_instance01.decoder_FNS(codeword_tuple=copy.deepcopy(code_gen), codewordType='int')
            assert decodeResult == value_tuple[idx_aa]

        codes_tuple = tuple(copy.deepcopy(codes_list))

        return codes_tuple

    def genCodes_FNSFTF_16bitx16(self, value_tuple):
        # assert isinstance(lastStates_tuple, tuple)
        assert isinstance(value_tuple, tuple)
        # assert len(lastStates_tuple) == 16
        assert len(value_tuple) == 16

        FNSCodec_instance01 = OtherCAC_Alg.FNSCAC_Codec.FNSCAC_Codec(n_cw=16)

        decValue_upperBound = FNSCodec_instance01.getParam_maxInputValue()
        codes_list = []

        for idx_aa in range(0, 16):
            assert value_tuple[idx_aa] <= decValue_upperBound
            assert value_tuple[idx_aa] >= 0
            # assert len(lastStates_tuple[idx_aa]) == 8
            # code_gen = FNSCATFCodec_instance01.encoder_top(decValue_int=copy.deepcopy(value_tuple[idx_aa]), lastState_tuple=copy.deepcopy(lastStates_tuple[idx_aa]))
            code_gen = FNSCodec_instance01.encode_FNSFTF(value=copy.deepcopy(value_tuple[idx_aa]), codewordType='int')
            codes_list.append(copy.deepcopy(code_gen))

            decodeResult = FNSCodec_instance01.decoder_FNS(codeword_tuple=copy.deepcopy(code_gen), codewordType='int')
            assert decodeResult == value_tuple[idx_aa]

        codes_tuple = tuple(copy.deepcopy(codes_list))

        return codes_tuple

    def genCodes_FNSFTF_12bitx9(self, value_tuple):
        # assert isinstance(lastStates_tuple, tuple)
        assert isinstance(value_tuple, tuple)
        # assert len(lastStates_tuple) == 16
        assert len(value_tuple) == 12

        FNSCodec_instance01 = OtherCAC_Alg.FNSCAC_Codec.FNSCAC_Codec(n_cw=9)

        decValue_upperBound = FNSCodec_instance01.getParam_maxInputValue()
        codes_list = []

        for idx_aa in range(0, 12):
            assert value_tuple[idx_aa] <= decValue_upperBound
            assert value_tuple[idx_aa] >= 0
            # assert len(lastStates_tuple[idx_aa]) == 8
            # code_gen = FNSCATFCodec_instance01.encoder_top(decValue_int=copy.deepcopy(value_tuple[idx_aa]), lastState_tuple=copy.deepcopy(lastStates_tuple[idx_aa]))
            code_gen = FNSCodec_instance01.encode_FNSFTF(value=copy.deepcopy(value_tuple[idx_aa]), codewordType='int')
            codes_list.append(copy.deepcopy(code_gen))

            decodeResult = FNSCodec_instance01.decoder_FNS(codeword_tuple=copy.deepcopy(code_gen), codewordType='int')
            assert decodeResult == value_tuple[idx_aa]

        codes_tuple = tuple(copy.deepcopy(codes_list))

        return codes_tuple


    def genCodes_IFNSFPF_16bitx16(self, value_tuple):
        # assert isinstance(lastStates_tuple, tuple)
        assert isinstance(value_tuple, tuple)
        # assert len(lastStates_tuple) == 16
        assert len(value_tuple) == 16

        IFNSCodec_instance01 = OtherCAC_Alg.IFNSCAC_Codec.IFNSCAC_Codec(n_cw=16)

        decValue_upperBound = IFNSCodec_instance01.getParam_maxInputValue()
        codes_list = []

        for idx_aa in range(0, 16):
            assert value_tuple[idx_aa] <= decValue_upperBound
            assert value_tuple[idx_aa] >= 0
            # assert len(lastStates_tuple[idx_aa]) == 8
            # code_gen = FNSCATFCodec_instance01.encoder_top(decValue_int=copy.deepcopy(value_tuple[idx_aa]), lastState_tuple=copy.deepcopy(lastStates_tuple[idx_aa]))
            code_gen = IFNSCodec_instance01.encode_IFNS(value=copy.deepcopy(value_tuple[idx_aa]), codewordType='int')
            codes_list.append(copy.deepcopy(code_gen))

            decodeResult = IFNSCodec_instance01.decoder_IFNS(codeword_tuple=copy.deepcopy(code_gen), codewordType='int')
            assert decodeResult == value_tuple[idx_aa]

        codes_tuple = tuple(copy.deepcopy(codes_list))

        return codes_tuple

    def runSimu_16x16Array_FNSCATF8bitx32(self, n_cycle, edgeEffect_rectWeight = 1,
                                          edgeEffect_hexWeight = 1,
                                          edgeEffect_rectPunishment = 0,
                                          edgeEffect_hexPunishment = 0):
        '''

        :param n_cycle:
        :return:
        '''
        codec_instance = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC_FNSCATF(len_cw=8)
        xtalkCalc_instance = Evaluation_Tools.array_xtalk_simu.Array_Xtalk_Calculator(n_row=16, n_col=16)
        cnt_xtalk_rec = {0: 0,
                         0.25: 0,
                         0.5: 0,
                         0.75: 0,
                         1: 0,
                         1.25: 0,
                         1.5: 0,
                         1.75: 0,
                         2: 0,
                         2.25: 0,
                         2.5: 0,
                         2.75: 0,
                         3: 0,
                         3.25: 0,
                         3.5: 0,
                         3.75: 0,
                         4: 0,
                         4.25: 0,
                         4.5: 0,
                         4.75: 0,
                         5: 0,
                         5.25: 0,
                         5.5: 0,
                         5.75: 0,
                         6: 0,
                         6.25: 0,
                         6.5: 0,
                         6.75: 0,
                         7: 0,
                         7.25: 0,
                         7.5: 0,
                         7.75: 0,
                         8: 0,
                         8.25: 0,
                         8.5: 0,
                         8.75: 0,
                         9: 0,
                         9.25: 0,
                         9.5: 0,
                         9.75: 0,
                         10: 0,
                         10.25: 0,
                         10.5: 0,
                         10.75: 0,
                         11: 0,
                         11.25: 0,
                         11.5: 0,
                         11.75: 0,
                         12: 0,
                         'None': 0}

        cnt_xtalk_hex = {0: 0,
                         0.25: 0,
                         0.5: 0,
                         0.75: 0,
                         1: 0,
                         1.25: 0,
                         1.5: 0,
                         1.75: 0,
                         2: 0,
                         2.25: 0,
                         2.5: 0,
                         2.75: 0,
                         3: 0,
                         3.25: 0,
                         3.5: 0,
                         3.75: 0,
                         4: 0,
                         4.25: 0,
                         4.5: 0,
                         4.75: 0,
                         5: 0,
                         5.25: 0,
                         5.5: 0,
                         5.75: 0,
                         6: 0,
                         6.25: 0,
                         6.5: 0,
                         6.75: 0,
                         7: 0,
                         7.25: 0,
                         7.5: 0,
                         7.75: 0,
                         8: 0,
                         8.25: 0,
                         8.5: 0,
                         8.75: 0,
                         9: 0,
                         9.25: 0,
                         9.5: 0,
                         9.75: 0,
                         10: 0,
                         10.25: 0,
                         10.5: 0,
                         10.75: 0,
                         11: 0,
                         11.25: 0,
                         11.5: 0,
                         11.75: 0,
                         12: 0,
                         'None': 0}


        valueIn_upperBound = codec_instance.getParam_maxInputLimitation()

        array_shielding_flags_list = []
        for idx_i in range(0, 16):
            array_shielding_flags_list.append((False, False, False, False,
                                               False, False, False, False,
                                               False, False, False, False,
                                               False, False, False, False))
        array_shielding_flags_tuple = tuple(array_shielding_flags_list)

        lastStates_notMapping_list = []
        for idx_i in range(0, 32):
            lastStates_notMapping_list.append((0, 0, 0, 0, 0, 0, 0, 0))
        lastStates_notMapping_tuple = tuple(lastStates_notMapping_list)

        lastStates_Mapping_list = []
        for idx_i in range(0, 16):
            lastStates_Mapping_list.append((0, 0, 0, 0,
                                               0, 0, 0, 0,
                                               0, 0, 0, 0,
                                               0, 0, 0, 0))
        lastStates_Mapping = tuple(lastStates_Mapping_list)

        for cycle_i in range(0, n_cycle):
            print("-----------------------------")
            print("CYCLE- {}".format(cycle_i))
            currentValueIn_list = []
            for idx_k in range(0, 32):
                genValue_random = random.randint(0, valueIn_upperBound)
                currentValueIn_list.append(copy.deepcopy(genValue_random))
            currentValueIn_tuple = tuple(copy.deepcopy(currentValueIn_list))
            currentCodewords_notMapping = self.genCodes_FNSCATF_8bitx32(lastStates_tuple=copy.deepcopy(lastStates_notMapping_tuple), value_tuple=copy.deepcopy(currentValueIn_tuple))
            currentCodewords_Mapping = self.codewordMapping_CATF_2x4_in_16x16(codeword_tuple=copy.deepcopy(currentCodewords_notMapping))

            print("--- Value IN: {}".format(currentValueIn_tuple))
            print("--- Last Array State: {}".format(lastStates_Mapping))
            print("--- Current Array State: {}".format(currentCodewords_Mapping))

            xtalk_result_rec = xtalkCalc_instance.calc_xtalk_level_rectTopo(array_cw01=copy.deepcopy(lastStates_Mapping),
                                                                            array_cw02=copy.deepcopy(currentCodewords_Mapping),
                                                                            array_shield=copy.deepcopy(array_shielding_flags_tuple),
                                                                            edgeTSVPunishment=copy.deepcopy(edgeEffect_rectPunishment),
                                                                            edgeTSVXtalkZoom=copy.deepcopy(edgeEffect_rectWeight))
            xtalk_cnt_rec = xtalkCalc_instance.xtalk_level_cnt(cw_xtalk_tuple=copy.deepcopy(xtalk_result_rec))
            print("--- xtalk level (Rec): {}".format(xtalk_cnt_rec))
            for dict_key_i in (0, 0.25, 0.5, 0.75,
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
                cnt_xtalk_rec[dict_key_i] = cnt_xtalk_rec[dict_key_i] + xtalk_cnt_rec[dict_key_i]

            xtalk_result_hex = xtalkCalc_instance.calc_xtalk_level_hexTopoA(array_cw01=copy.deepcopy(lastStates_Mapping),
                                                                            array_cw02=copy.deepcopy(currentCodewords_Mapping),
                                                                            array_shield=copy.deepcopy(array_shielding_flags_tuple),
                                                                            edgeTSVPunishment=copy.deepcopy(edgeEffect_hexPunishment),
                                                                            edgeTSVXtalkZoom=copy.deepcopy(edgeEffect_hexWeight))
            xtalk_cnt_hex = xtalkCalc_instance.xtalk_level_cnt(cw_xtalk_tuple=copy.deepcopy(xtalk_result_hex))
            print("---xtalk level (Hex): {}".format(xtalk_cnt_hex))
            for dict_key_i in (0, 0.25, 0.5, 0.75,
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
                cnt_xtalk_hex[dict_key_i] = cnt_xtalk_hex[dict_key_i] + xtalk_cnt_hex[dict_key_i]

            lastStates_notMapping_tuple = copy.deepcopy(currentCodewords_notMapping)
            lastStates_Mapping = copy.deepcopy(currentCodewords_Mapping)

        print("--------------------------------------------------------------------------------------------")
        print("16x16 Array - FNSCATF (2x4)bits_x32")
        print("Result - Rec: {}".format(cnt_xtalk_rec))
        print("Result - Hex: {}".format(cnt_xtalk_hex))




    def runSimu_16x16Array_RowByRow(self, n_cycle, CAC_name, edgeEffect_rectWeight = 1,
                                          edgeEffect_hexWeight = 1,
                                          edgeEffect_rectPunishment = 0,
                                          edgeEffect_hexPunishment = 0):
        '''

        :param n_cycle:
        :return:
        '''



        xtalkCalc_instance = Evaluation_Tools.array_xtalk_simu.Array_Xtalk_Calculator(n_row=16, n_col=16)
        cnt_xtalk_rec = {0: 0,
                         0.25: 0,
                         0.5: 0,
                         0.75: 0,
                         1: 0,
                         1.25: 0,
                         1.5: 0,
                         1.75: 0,
                         2: 0,
                         2.25: 0,
                         2.5: 0,
                         2.75: 0,
                         3: 0,
                         3.25: 0,
                         3.5: 0,
                         3.75: 0,
                         4: 0,
                         4.25: 0,
                         4.5: 0,
                         4.75: 0,
                         5: 0,
                         5.25: 0,
                         5.5: 0,
                         5.75: 0,
                         6: 0,
                         6.25: 0,
                         6.5: 0,
                         6.75: 0,
                         7: 0,
                         7.25: 0,
                         7.5: 0,
                         7.75: 0,
                         8: 0,
                         8.25: 0,
                         8.5: 0,
                         8.75: 0,
                         9: 0,
                         9.25: 0,
                         9.5: 0,
                         9.75: 0,
                         10: 0,
                         10.25: 0,
                         10.5: 0,
                         10.75: 0,
                         11: 0,
                         11.25: 0,
                         11.5: 0,
                         11.75: 0,
                         12: 0,
                         'None': 0}

        cnt_xtalk_hex = {0: 0,
                         0.25: 0,
                         0.5: 0,
                         0.75: 0,
                         1: 0,
                         1.25: 0,
                         1.5: 0,
                         1.75: 0,
                         2: 0,
                         2.25: 0,
                         2.5: 0,
                         2.75: 0,
                         3: 0,
                         3.25: 0,
                         3.5: 0,
                         3.75: 0,
                         4: 0,
                         4.25: 0,
                         4.5: 0,
                         4.75: 0,
                         5: 0,
                         5.25: 0,
                         5.5: 0,
                         5.75: 0,
                         6: 0,
                         6.25: 0,
                         6.5: 0,
                         6.75: 0,
                         7: 0,
                         7.25: 0,
                         7.5: 0,
                         7.75: 0,
                         8: 0,
                         8.25: 0,
                         8.5: 0,
                         8.75: 0,
                         9: 0,
                         9.25: 0,
                         9.5: 0,
                         9.75: 0,
                         10: 0,
                         10.25: 0,
                         10.5: 0,
                         10.75: 0,
                         11: 0,
                         11.25: 0,
                         11.5: 0,
                         11.75: 0,
                         12: 0,
                         'None': 0}




        array_shielding_flags_list = []
        for idx_i in range(0, 16):
            array_shielding_flags_list.append((False, False, False, False,
                                               False, False, False, False,
                                               False, False, False, False,
                                               False, False, False, False))
        array_shielding_flags_tuple = tuple(array_shielding_flags_list)


        lastStates_Mapping_list = []
        for idx_i in range(0, 16):
            lastStates_Mapping_list.append((0, 0, 0, 0,
                                               0, 0, 0, 0,
                                               0, 0, 0, 0,
                                               0, 0, 0, 0))
        lastStates_Mapping = tuple(lastStates_Mapping_list)

        for cycle_i in range(0, n_cycle):
            print("-----------------------------")
            print("CYCLE- {}".format(cycle_i))
            currentValueIn_list = []

            if CAC_name == 'FNS-FPF':
                codec_instance = OtherCAC_Alg.FNSCAC_Codec.FNSCAC_Codec(n_cw=16)
                valueIn_upperBound = codec_instance.getParam_maxInputValue()
                for idx_k in range(0, 16):
                    genValue_random = random.randint(0, valueIn_upperBound)
                    currentValueIn_list.append(copy.deepcopy(genValue_random))
                currentValueIn_tuple = tuple(copy.deepcopy(currentValueIn_list))
                currentCodewords_Mapping = self.genCodes_FNSFPF_16bitx16(value_tuple=copy.deepcopy(currentValueIn_tuple))

            elif CAC_name == 'FNS-FTF':
                codec_instance = OtherCAC_Alg.FNSCAC_Codec.FNSCAC_Codec(n_cw=16)
                valueIn_upperBound = codec_instance.getParam_maxInputValue()
                for idx_k in range(0, 16):
                    genValue_random = random.randint(0, valueIn_upperBound)
                    currentValueIn_list.append(copy.deepcopy(genValue_random))
                currentValueIn_tuple = tuple(copy.deepcopy(currentValueIn_list))
                currentCodewords_Mapping = self.genCodes_FNSFTF_16bitx16(value_tuple=copy.deepcopy(currentValueIn_tuple))

            elif CAC_name == 'IFNS-FPF':
                codec_instance = OtherCAC_Alg.IFNSCAC_Codec.IFNSCAC_Codec(n_cw=16)
                valueIn_upperBound = codec_instance.getParam_maxInputValue()
                for idx_k in range(0, 16):
                    genValue_random = random.randint(0, valueIn_upperBound)
                    currentValueIn_list.append(copy.deepcopy(genValue_random))
                currentValueIn_tuple = tuple(copy.deepcopy(currentValueIn_list))
                currentCodewords_Mapping = self.genCodes_IFNSFPF_16bitx16(value_tuple=copy.deepcopy(currentValueIn_tuple))
            else:
                assert False

            print("--- Value IN: {}".format(currentValueIn_tuple))
            print("--- Last Array State: {}".format(lastStates_Mapping))
            print("--- Current Array State: {}".format(currentCodewords_Mapping))

            xtalk_result_rec = xtalkCalc_instance.calc_xtalk_level_rectTopo(array_cw01=copy.deepcopy(lastStates_Mapping),
                                                                            array_cw02=copy.deepcopy(currentCodewords_Mapping),
                                                                            array_shield=copy.deepcopy(array_shielding_flags_tuple),
                                                                            edgeTSVPunishment=copy.deepcopy(edgeEffect_rectPunishment),
                                                                            edgeTSVXtalkZoom=copy.deepcopy(edgeEffect_rectWeight))
            xtalk_cnt_rec = xtalkCalc_instance.xtalk_level_cnt(cw_xtalk_tuple=copy.deepcopy(xtalk_result_rec))
            print("--- xtalk level (Rec): {}".format(xtalk_cnt_rec))
            for dict_key_i in (0, 0.25, 0.5, 0.75,
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
                cnt_xtalk_rec[dict_key_i] = cnt_xtalk_rec[dict_key_i] + xtalk_cnt_rec[dict_key_i]

            xtalk_result_hex = xtalkCalc_instance.calc_xtalk_level_hexTopoA(array_cw01=copy.deepcopy(lastStates_Mapping),
                                                                            array_cw02=copy.deepcopy(currentCodewords_Mapping),
                                                                            array_shield=copy.deepcopy(array_shielding_flags_tuple),
                                                                            edgeTSVPunishment=copy.deepcopy(edgeEffect_hexPunishment),
                                                                            edgeTSVXtalkZoom=copy.deepcopy(edgeEffect_hexWeight))
            xtalk_cnt_hex = xtalkCalc_instance.xtalk_level_cnt(cw_xtalk_tuple=copy.deepcopy(xtalk_result_hex))
            print("---xtalk level (Hex): {}".format(xtalk_cnt_hex))
            for dict_key_i in (0, 0.25, 0.5, 0.75,
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
                cnt_xtalk_hex[dict_key_i] = cnt_xtalk_hex[dict_key_i] + xtalk_cnt_hex[dict_key_i]

            lastStates_Mapping = copy.deepcopy(currentCodewords_Mapping)

        print("--------------------------------------------------------------------------------------------")
        print("16x16 Array - {} 16bits_x16".format(CAC_name))
        print("Result - Rec: {}".format(cnt_xtalk_rec))
        print("Result - Hex: {}".format(cnt_xtalk_hex))


    def runSimu_12x9HexArray_RowByRow(self, n_cycle, CAC_name, edgeEffect_rectWeight = 1,
                                          edgeEffect_hexWeight = 1,
                                          edgeEffect_rectPunishment = 0,
                                          edgeEffect_hexPunishment = 0):
        '''

        :param n_cycle:
        :return:
        '''



        xtalkCalc_instance = Evaluation_Tools.array_xtalk_simu.Array_Xtalk_Calculator(n_row=12, n_col=9)

        cnt_xtalk_hex = {0: 0,
                         0.25: 0,
                         0.5: 0,
                         0.75: 0,
                         1: 0,
                         1.25: 0,
                         1.5: 0,
                         1.75: 0,
                         2: 0,
                         2.25: 0,
                         2.5: 0,
                         2.75: 0,
                         3: 0,
                         3.25: 0,
                         3.5: 0,
                         3.75: 0,
                         4: 0,
                         4.25: 0,
                         4.5: 0,
                         4.75: 0,
                         5: 0,
                         5.25: 0,
                         5.5: 0,
                         5.75: 0,
                         6: 0,
                         6.25: 0,
                         6.5: 0,
                         6.75: 0,
                         7: 0,
                         7.25: 0,
                         7.5: 0,
                         7.75: 0,
                         8: 0,
                         8.25: 0,
                         8.5: 0,
                         8.75: 0,
                         9: 0,
                         9.25: 0,
                         9.5: 0,
                         9.75: 0,
                         10: 0,
                         10.25: 0,
                         10.5: 0,
                         10.75: 0,
                         11: 0,
                         11.25: 0,
                         11.5: 0,
                         11.75: 0,
                         12: 0,
                         'None': 0}




        array_shielding_flags_list = []
        for idx_i in range(0, 12):
            array_shielding_flags_list.append((False, False, False,
                                               False, False, False,
                                               False, False, False,
                                               False, False, False))
        array_shielding_flags_tuple = tuple(array_shielding_flags_list)


        lastStates_Mapping_list = []
        for idx_i in range(0, 16):
            lastStates_Mapping_list.append((0, 0, 0,
                                            0, 0, 0,
                                            0, 0, 0,
                                            0, 0, 0))
        lastStates_Mapping = tuple(lastStates_Mapping_list)

        for cycle_i in range(0, n_cycle):
            print("-----------------------------")
            print("CYCLE- {}".format(cycle_i))
            currentValueIn_list = []

            if CAC_name == 'FNS-FPF':
                codec_instance = OtherCAC_Alg.FNSCAC_Codec.FNSCAC_Codec(n_cw=9)
                valueIn_upperBound = codec_instance.getParam_maxInputValue()
                for idx_k in range(0, 12):
                    genValue_random = random.randint(0, valueIn_upperBound)
                    currentValueIn_list.append(copy.deepcopy(genValue_random))
                currentValueIn_tuple = tuple(copy.deepcopy(currentValueIn_list))
                currentCodewords_Mapping = self.genCodes_FNSFPF_12bitx9(value_tuple=copy.deepcopy(currentValueIn_tuple))

            elif CAC_name == 'FNS-FTF':
                codec_instance = OtherCAC_Alg.FNSCAC_Codec.FNSCAC_Codec(n_cw=9)
                valueIn_upperBound = codec_instance.getParam_maxInputValue()
                for idx_k in range(0, 12):
                    genValue_random = random.randint(0, valueIn_upperBound)
                    currentValueIn_list.append(copy.deepcopy(genValue_random))
                currentValueIn_tuple = tuple(copy.deepcopy(currentValueIn_list))
                currentCodewords_Mapping = self.genCodes_FNSFTF_12bitx9(value_tuple=copy.deepcopy(currentValueIn_tuple))


            else:
                assert False

            print("--- Value IN: {}".format(currentValueIn_tuple))
            print("--- Last Array State: {}".format(lastStates_Mapping))
            print("--- Current Array State: {}".format(currentCodewords_Mapping))



            xtalk_result_hex = xtalkCalc_instance.calc_xtalk_level_hexTopoA(array_cw01=copy.deepcopy(lastStates_Mapping),
                                                                            array_cw02=copy.deepcopy(currentCodewords_Mapping),
                                                                            array_shield=copy.deepcopy(array_shielding_flags_tuple),
                                                                            edgeTSVPunishment=copy.deepcopy(edgeEffect_hexPunishment),
                                                                            edgeTSVXtalkZoom=copy.deepcopy(edgeEffect_hexWeight))
            xtalk_cnt_hex = xtalkCalc_instance.xtalk_level_cnt(cw_xtalk_tuple=copy.deepcopy(xtalk_result_hex))
            print("---xtalk level (Hex): {}".format(xtalk_cnt_hex))
            for dict_key_i in (0, 0.25, 0.5, 0.75,
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
                cnt_xtalk_hex[dict_key_i] = cnt_xtalk_hex[dict_key_i] + xtalk_cnt_hex[dict_key_i]

            lastStates_Mapping = copy.deepcopy(currentCodewords_Mapping)

        print("--------------------------------------------------------------------------------------------")
        print("12x9 Array - {} 9bits_x12".format(CAC_name))
        print("Result - Hex: {}".format(cnt_xtalk_hex))


    def runSimu_16x16Array_NoCAC(self, n_cycle, edgeEffect_rectWeight = 1,
                                          edgeEffect_hexWeight = 1,
                                          edgeEffect_rectPunishment = 0,
                                          edgeEffect_hexPunishment = 0):
        '''

        :param n_cycle:
        :return:
        '''



        xtalkCalc_instance = Evaluation_Tools.array_xtalk_simu.Array_Xtalk_Calculator(n_row=16, n_col=16)
        cnt_xtalk_rec = {0: 0,
                         0.25: 0,
                         0.5: 0,
                         0.75: 0,
                         1: 0,
                         1.25: 0,
                         1.5: 0,
                         1.75: 0,
                         2: 0,
                         2.25: 0,
                         2.5: 0,
                         2.75: 0,
                         3: 0,
                         3.25: 0,
                         3.5: 0,
                         3.75: 0,
                         4: 0,
                         4.25: 0,
                         4.5: 0,
                         4.75: 0,
                         5: 0,
                         5.25: 0,
                         5.5: 0,
                         5.75: 0,
                         6: 0,
                         6.25: 0,
                         6.5: 0,
                         6.75: 0,
                         7: 0,
                         7.25: 0,
                         7.5: 0,
                         7.75: 0,
                         8: 0,
                         8.25: 0,
                         8.5: 0,
                         8.75: 0,
                         9: 0,
                         9.25: 0,
                         9.5: 0,
                         9.75: 0,
                         10: 0,
                         10.25: 0,
                         10.5: 0,
                         10.75: 0,
                         11: 0,
                         11.25: 0,
                         11.5: 0,
                         11.75: 0,
                         12: 0,
                         'None': 0}

        cnt_xtalk_hex = {0: 0,
                         0.25: 0,
                         0.5: 0,
                         0.75: 0,
                         1: 0,
                         1.25: 0,
                         1.5: 0,
                         1.75: 0,
                         2: 0,
                         2.25: 0,
                         2.5: 0,
                         2.75: 0,
                         3: 0,
                         3.25: 0,
                         3.5: 0,
                         3.75: 0,
                         4: 0,
                         4.25: 0,
                         4.5: 0,
                         4.75: 0,
                         5: 0,
                         5.25: 0,
                         5.5: 0,
                         5.75: 0,
                         6: 0,
                         6.25: 0,
                         6.5: 0,
                         6.75: 0,
                         7: 0,
                         7.25: 0,
                         7.5: 0,
                         7.75: 0,
                         8: 0,
                         8.25: 0,
                         8.5: 0,
                         8.75: 0,
                         9: 0,
                         9.25: 0,
                         9.5: 0,
                         9.75: 0,
                         10: 0,
                         10.25: 0,
                         10.5: 0,
                         10.75: 0,
                         11: 0,
                         11.25: 0,
                         11.5: 0,
                         11.75: 0,
                         12: 0,
                         'None': 0}




        array_shielding_flags_list = []
        for idx_i in range(0, 16):
            array_shielding_flags_list.append((False, False, False, False,
                                               False, False, False, False,
                                               False, False, False, False,
                                               False, False, False, False))
        array_shielding_flags_tuple = tuple(array_shielding_flags_list)


        lastStates_Mapping_list = []
        for idx_i in range(0, 16):
            lastStates_Mapping_list.append((0, 0, 0, 0,
                                               0, 0, 0, 0,
                                               0, 0, 0, 0,
                                               0, 0, 0, 0))
        lastStates_Mapping = tuple(lastStates_Mapping_list)

        for cycle_i in range(0, n_cycle):
            print("-----------------------------")
            print("CYCLE- {}".format(cycle_i))
            currentValueIn_list = []

            currentCodewords_Mapping_list = []
            for idx_mm in range(0, 16):
                currentCodewords_Mapping_list_oneRow = []
                for idx_nn in range(0, 16):
                    currentCodewords_Mapping_list_oneRow.append(random.choice((0, 1)))
                currentCodewords_Mapping_list.append(tuple(copy.deepcopy(currentCodewords_Mapping_list_oneRow)))
            currentCodewords_Mapping = tuple(copy.deepcopy(currentCodewords_Mapping_list))

            # print("--- Value IN: {}".format(currentValueIn_tuple))
            print("--- Last Array State: {}".format(lastStates_Mapping))
            print("--- Current Array State: {}".format(currentCodewords_Mapping))

            xtalk_result_rec = xtalkCalc_instance.calc_xtalk_level_rectTopo(array_cw01=copy.deepcopy(lastStates_Mapping),
                                                                            array_cw02=copy.deepcopy(currentCodewords_Mapping),
                                                                            array_shield=copy.deepcopy(array_shielding_flags_tuple),
                                                                            edgeTSVPunishment=copy.deepcopy(edgeEffect_rectPunishment),
                                                                            edgeTSVXtalkZoom=copy.deepcopy(edgeEffect_rectWeight))
            xtalk_cnt_rec = xtalkCalc_instance.xtalk_level_cnt(cw_xtalk_tuple=copy.deepcopy(xtalk_result_rec))
            print("--- xtalk level (Rec): {}".format(xtalk_cnt_rec))
            for dict_key_i in (0, 0.25, 0.5, 0.75,
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
                cnt_xtalk_rec[dict_key_i] = cnt_xtalk_rec[dict_key_i] + xtalk_cnt_rec[dict_key_i]

            xtalk_result_hex = xtalkCalc_instance.calc_xtalk_level_hexTopoA(array_cw01=copy.deepcopy(lastStates_Mapping),
                                                                            array_cw02=copy.deepcopy(currentCodewords_Mapping),
                                                                            array_shield=copy.deepcopy(array_shielding_flags_tuple),
                                                                            edgeTSVPunishment=copy.deepcopy(edgeEffect_hexPunishment),
                                                                            edgeTSVXtalkZoom=copy.deepcopy(edgeEffect_hexWeight))
            xtalk_cnt_hex = xtalkCalc_instance.xtalk_level_cnt(cw_xtalk_tuple=copy.deepcopy(xtalk_result_hex))
            print("---xtalk level (Hex): {}".format(xtalk_cnt_hex))
            for dict_key_i in (0, 0.25, 0.5, 0.75,
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
                cnt_xtalk_hex[dict_key_i] = cnt_xtalk_hex[dict_key_i] + xtalk_cnt_hex[dict_key_i]

            lastStates_Mapping = copy.deepcopy(currentCodewords_Mapping)

        print("--------------------------------------------------------------------------------------------")
        print("16x16 Array - No CAC")
        print("Result - Rec: {}".format(cnt_xtalk_rec))
        print("Result - Hex: {}".format(cnt_xtalk_hex))

########################################################################################################################
    def runSimu_12x9HexArray_NoCAC(self, n_cycle, edgeEffect_rectWeight = 1,
                                          edgeEffect_hexWeight = 1,
                                          edgeEffect_rectPunishment = 0,
                                          edgeEffect_hexPunishment = 0):
        '''

        :param n_cycle:
        :return:
        '''



        xtalkCalc_instance = Evaluation_Tools.array_xtalk_simu.Array_Xtalk_Calculator(n_row=12, n_col=9)

        cnt_xtalk_hex = {0: 0,
                         0.25: 0,
                         0.5: 0,
                         0.75: 0,
                         1: 0,
                         1.25: 0,
                         1.5: 0,
                         1.75: 0,
                         2: 0,
                         2.25: 0,
                         2.5: 0,
                         2.75: 0,
                         3: 0,
                         3.25: 0,
                         3.5: 0,
                         3.75: 0,
                         4: 0,
                         4.25: 0,
                         4.5: 0,
                         4.75: 0,
                         5: 0,
                         5.25: 0,
                         5.5: 0,
                         5.75: 0,
                         6: 0,
                         6.25: 0,
                         6.5: 0,
                         6.75: 0,
                         7: 0,
                         7.25: 0,
                         7.5: 0,
                         7.75: 0,
                         8: 0,
                         8.25: 0,
                         8.5: 0,
                         8.75: 0,
                         9: 0,
                         9.25: 0,
                         9.5: 0,
                         9.75: 0,
                         10: 0,
                         10.25: 0,
                         10.5: 0,
                         10.75: 0,
                         11: 0,
                         11.25: 0,
                         11.5: 0,
                         11.75: 0,
                         12: 0,
                         'None': 0}




        array_shielding_flags_list = []
        for idx_i in range(0, 12):
            array_shielding_flags_list.append((False, False, False,
                                               False, False, False,
                                               False, False, False,
                                               False, False, False))
        array_shielding_flags_tuple = tuple(array_shielding_flags_list)


        lastStates_Mapping_list = []
        for idx_i in range(0, 16):
            lastStates_Mapping_list.append((0, 0, 0,
                                            0, 0, 0,
                                            0, 0, 0,
                                            0, 0, 0))
        lastStates_Mapping = tuple(lastStates_Mapping_list)

        for cycle_i in range(0, n_cycle):
            print("-----------------------------")
            print("CYCLE- {}".format(cycle_i))
            currentValueIn_list = []

            currentCodewords_Mapping_list = []
            for idx_mm in range(0, 12):
                currentCodewords_Mapping_list_oneRow = []
                for idx_nn in range(0, 9):
                    currentCodewords_Mapping_list_oneRow.append(random.choice((0, 1)))
                currentCodewords_Mapping_list.append(tuple(copy.deepcopy(currentCodewords_Mapping_list_oneRow)))
            currentCodewords_Mapping = tuple(copy.deepcopy(currentCodewords_Mapping_list))

            # print("--- Value IN: {}".format(currentValueIn_tuple))
            print("--- Last Array State: {}".format(lastStates_Mapping))
            print("--- Current Array State: {}".format(currentCodewords_Mapping))



            xtalk_result_hex = xtalkCalc_instance.calc_xtalk_level_hexTopoA(array_cw01=copy.deepcopy(lastStates_Mapping),
                                                                            array_cw02=copy.deepcopy(currentCodewords_Mapping),
                                                                            array_shield=copy.deepcopy(array_shielding_flags_tuple),
                                                                            edgeTSVPunishment=copy.deepcopy(edgeEffect_hexPunishment),
                                                                            edgeTSVXtalkZoom=copy.deepcopy(edgeEffect_hexWeight))
            xtalk_cnt_hex = xtalkCalc_instance.xtalk_level_cnt(cw_xtalk_tuple=copy.deepcopy(xtalk_result_hex))
            print("---xtalk level (Hex): {}".format(xtalk_cnt_hex))
            for dict_key_i in (0, 0.25, 0.5, 0.75,
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
                cnt_xtalk_hex[dict_key_i] = cnt_xtalk_hex[dict_key_i] + xtalk_cnt_hex[dict_key_i]

            lastStates_Mapping = copy.deepcopy(currentCodewords_Mapping)

        print("--------------------------------------------------------------------------------------------")
        print("12x9 Array - No CAC")
        print("Result - Hex: {}".format(cnt_xtalk_hex))



########################################################################################################################
########################################################################################################################
# How to use?
########################################################################################################################
# simu_instance = FNSCATF_xtalkSimu()
# simu_instance.runSimu_16x16Array_FNSCATF8bitx32(n_cycle=1000, edgeEffect_rectWeight=1.35,
#                                                 edgeEffect_hexWeight=1.3,
#                                                 edgeEffect_rectPunishment=1.1,
#                                                 edgeEffect_hexPunishment=0.7)

# simu_instance.runSimu_16x16Array_RowByRow(n_cycle=1000, CAC_name='IFNS-FPF',
#                                           edgeEffect_rectWeight=1.35,
#                                           edgeEffect_hexWeight=1.3,
#                                           edgeEffect_rectPunishment=1.1,
#                                           edgeEffect_hexPunishment=0.7)

# simu_instance.runSimu_16x16Array_NoCAC(n_cycle=1000,
#                                        edgeEffect_rectWeight=1.35,
#                                        edgeEffect_hexWeight=1.3,
#                                        edgeEffect_rectPunishment=1.1,
#                                        edgeEffect_hexPunishment=0.7)









