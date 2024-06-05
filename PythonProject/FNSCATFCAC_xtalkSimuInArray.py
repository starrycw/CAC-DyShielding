import copy

import Evaluation_Tools.array_xtalk_simu
import RingCAC_Alg.Ring2CTransCAC_Codec

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
        assert len(mappingList_tupleElements) == 32
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

    def genCodes_FNSFPF_16bitx16(self, lastStates_tuple, value_tuple):
        #TODO: ^v^




