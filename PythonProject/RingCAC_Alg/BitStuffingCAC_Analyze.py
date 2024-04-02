import copy
import time
import fractions

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

import RingCAC_Alg.BitStuffingCAC_Codec as BitStuffingCAC_Codec


class _transitionProbabilityMatrix:
    '''
    The transition probability matrix.
    '''
    def __init__(self, n_size: int):
        assert isinstance(n_size, int) and n_size > 1
        self._param_matrixSize = copy.deepcopy(n_size)
        self._init_transProb_matrix()

    def __repr__(self):
        matrixCheck_ifpass, matrixCheck_errList = self.checkMatrix_transProb()
        matrixInfoStr = "-------\nTransition Probability Matrix\n---Size: {} x {} \n---Matrix Check Pass: {} \n---Errors: {}\n-------\n".format(self.getParam_matrixSize(),
                                                                                                                                          self.getParam_matrixSize(),
                                                                                                                                          matrixCheck_ifpass,
                                                                                                                                          matrixCheck_errList)
        return matrixInfoStr

    def getParam_matrixSize(self):
        return copy.deepcopy(self._param_matrixSize)

    def _init_transProb_matrix(self):
        '''
        Initialize / Reset the trans prob matrix.
        :return:
        '''
        self._matrix_transProb = []
        for row_i in range(0, self.getParam_matrixSize()):
            col_list = self.getParam_matrixSize() * [0]
            self._matrix_transProb.append(copy.deepcopy(col_list))

    def reset_Matrix(self):
        '''
        Reset
        :return:
        '''
        self._init_transProb_matrix()

    def modifyMatrix_transProb_singleRow(self, row_index: int, newProbList: list[int, ...]):
        '''
        Replace the one row in the trans prob matrix with a new list.

        The fraction rather than float is recommended to represent the probability!
        Use fractionObj = fractions.Fraction(int_a, int_b) to represent a/b.

        :param row_index:
        :param newProbList:
        :return:
        '''
        assert isinstance(row_index, int) and row_index < self.getParam_matrixSize() and row_index >= 0
        assert isinstance(newProbList, list) and len(newProbList) == self.getParam_matrixSize()
        self._matrix_transProb[row_index] = copy.deepcopy(newProbList)

    def getMatrix_transProb_all(self):
        return copy.deepcopy(self._matrix_transProb)

    def getMatrix_transProb_oneRow(self, row_idx: int) -> tuple:
        row_list = copy.deepcopy(self._matrix_transProb[row_idx])
        return tuple(row_list)

    def getMatrix_transProb_oneCol(self, col_idx: int) -> tuple:
        col_list = []
        for row_i in range(0, self.getParam_matrixSize()):
            col_list.append(copy.deepcopy(self._matrix_transProb[row_i][col_idx]))
        return tuple(col_list)

    def showMatrix_transProb(self, config_zeroValue = -1, config_vmin = -0.05, config_dpi = 500):
        '''
        Show the transProbability Matrix.
        :return:
        '''
        transProbMatrix_float = []
        for row_i in self.getMatrix_transProb_all():
            transProbRow_float = []
            for probValueFrac_i in row_i:
                if probValueFrac_i == 0:
                    transProbRow_float.append(config_zeroValue)
                else:
                    assert probValueFrac_i > 0
                    transProbRow_float.append(float(probValueFrac_i))
            transProbMatrix_float.append(copy.deepcopy(transProbRow_float))
        npMatrix_a = np.array(transProbMatrix_float)

        plt.figure(dpi=config_dpi)
        sns.heatmap(data=npMatrix_a, vmin=config_vmin, annot=False, cmap=plt.get_cmap('Greens'))
        plt.show()

    def showMatrix_transProb_timesN(self, n_int, config_vmin = 0, config_dpi = 500):
        '''
        Show the (transProbability x n) Matrix.
        :return:
        '''
        transCntMatrix = []
        for row_i in self.getMatrix_transProb_all():
            transCntRow = []
            for probValueFrac_i in row_i:
                if probValueFrac_i == 0:
                    transCntRow.append(0)
                else:
                    assert probValueFrac_i > 0
                    transCntRow.append(float(probValueFrac_i * n_int))
            transCntMatrix.append(copy.deepcopy(transCntRow))
        npMatrix_a = np.array(transCntMatrix)

        plt.figure(dpi=config_dpi)
        sns.heatmap(data=npMatrix_a, vmin=config_vmin, annot=True, cmap=plt.get_cmap('Blues'), annot_kws={"size": 7})
        plt.show()


    def checkMatrix_transProb(self):
        '''
        Check the trans prob matrix.

        Rules:
        (1) Each the element should be a non-negative value that is no larger than 1.
        (2) The sum result of each row should be 1.

        :return: check_pass, copy.deepcopy(error_list)
        '''
        check_pass = True
        error_list = []
        currentMatrix = self.getMatrix_transProb_all()
        assert len(currentMatrix) == self.getParam_matrixSize()
        for row_idx in range(0, self.getParam_matrixSize()):
            sumValue = 0
            for col_idx in range(0, self.getParam_matrixSize()):
                prob_i = currentMatrix[row_idx][col_idx]
                if (prob_i < 0) or (prob_i > 1):
                    check_pass = False
                    error_list.append("Value{}_{}: {}".format(row_idx, col_idx, prob_i))
                sumValue  = sumValue + prob_i
            if sumValue != 1:
                check_pass = False
                error_list.append("RowSUM{}: {}".format(row_idx, sumValue))

        # for col_idx in range(0, self.getParam_matrixSize()):
        #     sumValue = 0
        #     for row_idx in range(0, self.getParam_matrixSize()):
        #         prob_i = currentMatrix[row_idx][col_idx]
        #         sumValue = sumValue + prob_i
        #     if sumValue != 1:
        #         check_pass = False
        #         error_list.append("ColSUM{}: {}".format(col_idx, sumValue))

        return check_pass, copy.deepcopy(error_list)







class BitStuffingCAC_Analyze_HexArray:
    def __init__(self, config_msbFirst=True):
        # init the Codec instance
        self._initialize_codec()

        # Params
        # If msbFirst is True (default), the element with idx=0 in the codeword list is the MSB. Otherwise, it's LSB.
        if config_msbFirst is True:
            self._config_msbFirst = True
        else:
            assert config_msbFirst is False
            self._config_msbFirst = False

    def _initialize_codec(self):
        '''
        Initlize codec.
        :return:
        '''
        timestamp_int = int(time.time())
        self._CodecInstance_7bit = BitStuffingCAC_Codec.BSCAC_ForHexDyS2C_2CSupFor7bitGroup_Main(instance_id=timestamp_int)

    def _getConfig_msbFirst(self):
        '''
        If msbFirst is True (default), the element with idx=0 in the codeword list is the MSB. Otherwise, it's LSB.
        :return:
        '''
        return copy.deepcopy(self._config_msbFirst)

    @staticmethod
    def tool_convert_int2BinList(input_int: int, n_bit: int, msbFirst = True) -> list[int, ...]:
        '''
        Convert int to binary list with n_bit elements.
        If msbFirst is True (default), the element with idx=0 in the return list is the MSB. Otherwise, it's LSB.
        Each element in the return list is in {0, 1}.

        :param input_int: int
        :param n_bit: int
        :param msbFirst: bool
        :return:
        '''
        assert isinstance(n_bit, int) and n_bit > 0
        assert isinstance(input_int, int) and input_int >= 0
        assert 2**n_bit > input_int
        bin_str = bin(input_int)[2:].zfill(n_bit)
        bin_list = []
        for char_i in bin_str:
            if char_i == "0":
                bin_list.append(0)
            elif char_i == "1":
                bin_list.append(1)
            else:
                assert False

        if msbFirst is False:
            bin_list.reverse()
        else:
            assert msbFirst is True

        return copy.deepcopy(bin_list)

    @staticmethod
    def tool_convert_int2BinTuple(input_int: int, n_bit: int, msbFirst=True) -> tuple[int, ...]:
        '''
        Convert int to binary tuple with n_bit elements.
        If msbFirst is True (default), the element with idx=0 in the return tuple is the MSB. Otherwise, it's LSB.
        Each element in the return list is in {0, 1}.

        :param input_int: int
        :param n_bit: int
        :param msbFirst: bool
        :return:
        '''
        bin_list = BitStuffingCAC_Analyze_HexArray.tool_convert_int2BinList(input_int=input_int, n_bit=n_bit, msbFirst=msbFirst)
        bin_tuple = tuple(bin_list)
        return copy.deepcopy(bin_tuple)

    @staticmethod
    def tool_convert_binListOrTuple2Int(input_bin_seq, msbFirst=True) -> int:
        '''
        Convert binary sequence (list or tuple) to decimal value (int).
        If msbFirst is True (default), the element with idx=0 in the return tuple is the MSB. Otherwise, it's LSB.
        Each element in the input list/tuple must be in {0, 1}.
        :param input_bin_seq: list or tuple
        :param msbFirst: bool
        :return:
        '''
        assert isinstance(input_bin_seq, list) or isinstance(input_bin_seq, tuple)
        assert len(input_bin_seq) > 0

        binCode_list = list(copy.deepcopy(input_bin_seq))
        if msbFirst is True:
            binCode_list.reverse()
        else:
            assert msbFirst is False

        binWeight_i = 1
        decValue = 0
        for binCode_i in binCode_list:
            assert binCode_i in (0, 1)
            decValue = decValue + (binWeight_i * binCode_i)
            binWeight_i = binWeight_i * 2

        return decValue

    def get_transProb_singleGroup_oneClockPeriod(self):
        '''
        Calculate the transition probability of single encoded group (7-bit codeword).
        :return:
        '''
        transProbMatrix_top = _transitionProbabilityMatrix(n_size=(2**7))
        for cw_origin_int in range(0, (2**7)):
            transCnt_list = (2**7) * [0]
            cw_origin_tuple = self.tool_convert_int2BinTuple(input_int=cw_origin_int, n_bit=7, msbFirst=self._getConfig_msbFirst())
            for dataIn_int in range(0, (2**7)):
                dataIn_list = self.tool_convert_int2BinList(input_int=dataIn_int, n_bit=7, msbFirst=self._getConfig_msbFirst())
                cw_new_tuple, temp_n_transmittedBits, temp_unprocessedDataBitsList = self._CodecInstance_7bit.encoder_core(bits_to_be_trans=dataIn_list, last_codeword=cw_origin_tuple)
                cw_new_int = self.tool_convert_binListOrTuple2Int(input_bin_seq=cw_new_tuple, msbFirst=self._getConfig_msbFirst())
                transCnt_list[cw_new_int] = transCnt_list[cw_new_int] + 1
            transProb_list = []
            for transCnt_i in transCnt_list:
                transProb_list.append(fractions.Fraction(copy.deepcopy(transCnt_i), (2**7)))
            transProbMatrix_top.modifyMatrix_transProb_singleRow(row_index=cw_origin_int, newProbList=transProb_list)

        return transProbMatrix_top





