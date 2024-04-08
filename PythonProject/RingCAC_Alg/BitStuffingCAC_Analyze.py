import copy
import time
import fractions

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import z3 as z3

import RingCAC_Alg.BitStuffingCAC_Codec as BitStuffingCAC_Codec

########################################################################################################################
########################################################################################################################
class _transitionProbabilityMatrix:
    '''
    The transition probability matrix.
    '''
    def __init__(self, n_size: int):
        assert isinstance(n_size, int) and n_size > 1
        self._param_matrixSize = copy.deepcopy(n_size)
        self._init_mainMatrix()

    def __repr__(self):
        matrixCheck_ifpass, matrixCheck_errList = self.checkMatrix()
        matrixInfoStr = "-------\nTransition Probability Matrix\n---Size: {} x {} \n---Matrix Check Pass: {} \n---Errors: {}\n-------\n".format(self.getParam_matrixSize(),
                                                                                                                                          self.getParam_matrixSize(),
                                                                                                                                          matrixCheck_ifpass,
                                                                                                                                          matrixCheck_errList)
        return matrixInfoStr

    def getParam_matrixSize(self):
        return copy.deepcopy(self._param_matrixSize)

    def _init_mainMatrix(self):
        '''
        Initialize / Reset the trans prob matrix.
        :return:
        '''
        self._matrix_main = []
        for row_i in range(0, self.getParam_matrixSize()):
            col_list = self.getParam_matrixSize() * [0]
            self._matrix_main.append(copy.deepcopy(col_list))

    def reset_Matrix(self):
        '''
        Reset
        :return:
        '''
        self._init_mainMatrix()

    def modifyMatrix_singleRow(self, row_index: int, newProbList: list[int, ...]):
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
        self._matrix_main[row_index] = copy.deepcopy(newProbList)

    def getMatrix_all(self):
        return copy.deepcopy(self._matrix_main)

    def getMatrix_oneRow(self, row_idx: int) -> tuple:
        row_list = copy.deepcopy(self._matrix_main[row_idx])
        return tuple(row_list)

    def getMatrix_oneCol(self, col_idx: int) -> tuple:
        col_list = []
        for row_i in range(0, self.getParam_matrixSize()):
            col_list.append(copy.deepcopy(self._matrix_main[row_i][col_idx]))
        return tuple(col_list)

    def showMatrix_main(self, config_zeroValue = -1, config_vmin = -0.05, config_dpi = 500):
        '''
        Show the transProbability Matrix.
        :return:
        '''
        transProbMatrix_float = []
        for row_i in self.getMatrix_all():
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

    def showMatrix_mainTimesN(self, n_int, config_vmin = 0, config_dpi = 500):
        '''
        Show the (transProbability x n) Matrix.
        :return:
        '''
        transCntMatrix = []
        for row_i in self.getMatrix_all():
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


    def checkMatrix(self):
        '''
        Check the trans prob matrix.

        Rules:
        (1) Each the element should be a non-negative value that is no larger than 1.
        (2) The sum result of each row should be 1.

        :return: check_pass, copy.deepcopy(error_list)
        '''
        check_pass = True
        error_list = []
        currentMatrix = self.getMatrix_all()
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


########################################################################################################################
########################################################################################################################
class _transitionCntMatrix(_transitionProbabilityMatrix):
    def __init__(self, n_size):
        super().__init__(n_size=n_size)

    def __repr__(self):
        matrixCheck_ifpass, matrixCheck_errList = self.checkMatrix()
        matrixInfoStr = "-------\nTransition Count Matrix\n---Size: {} x {} \n---Matrix Check Pass: {} \n---Errors: {}\n-------\n".format(self.getParam_matrixSize(),
                                                                                                                                          self.getParam_matrixSize(),
                                                                                                                                          matrixCheck_ifpass,
                                                                                                                                          matrixCheck_errList)
        return matrixInfoStr
    def checkMatrix(self):
        '''
        Check the matrix.

        Rules:
        (1) Each the element should be a non-negative int value.
        (2) All the sum result of each row should be the same.

        :return: check_pass, copy.deepcopy(error_list)
        '''
        check_pass = True
        error_list = []
        currentMatrix = self.getMatrix_all()
        assert len(currentMatrix) == self.getParam_matrixSize()
        sumResults_dict = {}
        for row_idx in range(0, self.getParam_matrixSize()):
            sumValue = 0
            for col_idx in range(0, self.getParam_matrixSize()):
                cnt_i = currentMatrix[row_idx][col_idx]
                if (cnt_i < 0) or (not isinstance(cnt_i, int)):
                    check_pass = False
                    error_list.append("Value{}_{}: {}".format(row_idx, col_idx, cnt_i))
                sumValue  = sumValue + cnt_i
            if (sumValue in sumResults_dict):
                sumResults_dict[sumValue] = sumResults_dict[sumValue] + 1
            else:
                sumResults_dict[sumValue] = 1
        error_list.append(copy.deepcopy(sumResults_dict))
        if len(sumResults_dict) != 1:
            check_pass = False
            error_list.append("RowSUMError")

        return check_pass, copy.deepcopy(error_list)

    def showMatrix_main(self, config_zeroValue = -1, config_vmin = -0.05, config_dpi = 500):
        '''
        Show the transProbability Matrix.
        :return:
        '''
        transCntMatrix_int = []
        for row_i in self.getMatrix_all():
            transCntRow_int = []
            for cntValue_i in row_i:
                transCntRow_int.append(cntValue_i)
            transCntMatrix_int.append(copy.deepcopy(transCntRow_int))
        npMatrix_a = np.array(transCntMatrix_int)

        plt.figure(dpi=config_dpi)
        sns.heatmap(data=npMatrix_a, vmin=config_vmin, annot=False, cmap=plt.get_cmap('Blues'))
        plt.show()


########################################################################################################################
########################################################################################################################
class _Z3Solver_forMuACalc:
    def __init__(self, matrix_B, matrix_Q):
        # Matrix B & matrix Q
        # Matrix Q = Matrix P / 64
        assert len(matrix_B) == 64
        assert len(matrix_Q) == 64
        for idx_ii in range(0, 64):
            assert len(matrix_B[idx_ii]) == 64
            assert len(matrix_Q[idx_ii]) == 64
            for idx_jj in range(0, 64):
                assert isinstance(matrix_Q[idx_ii][idx_jj], int)
                assert matrix_B[idx_ii][idx_jj] in (0, 1)
        self._matrix_B = copy.deepcopy(matrix_B)
        self._matrix_Q = copy.deepcopy(matrix_Q)

        # Z3 solver
        self._solver_main = z3.Solver()

        # var \mu_a
        # Each element in \mu_a is represented by a fraction: Numerator / Denominator.
        # self._var_muA_numeratorList is a 1x64 list (Z3 IntVector) of \mu_a numerators.
        # self._var_muA_denominatorList is a 1x64 list (Z3 IntVector) of \mu_a denominators.
        self._var_muA_numeratorList = z3.IntVector('muA_nu', 64)
        self._var_muA_denominatorList = z3.IntVector('muA_de', 64)

        # var \mu_b
        self._var_muB_numeratorList = z3.IntVector('muB_nu', 64)
        self._var_muB_denominatorList = z3.IntVector('muB_de', 64)

        # var \mu_c
        self._var_muC_numeratorList = z3.IntVector('muC_nu', 64)
        self._var_muC_denominatorList = z3.IntVector('muC_de', 64)

    ####################################################################################################################
    def get_matrixB(self):
        return copy.deepcopy(self._matrix_B)

    ####################################################################################################################
    def get_matrixQ(self):
        return copy.deepcopy(self._matrix_Q)

    ####################################################################################################################
    def _addConstraint_muA2muB(self):
        '''
        Add constraint:
        \mu_a x B = \mu_b
        :return:
        '''
        for idx_i in range(0, 64):
            idx_select = -1
            for idx_k in range(0, 64):
                if self.get_matrixB()[idx_k][idx_i] == 1:
                    assert idx_select == -1
                    idx_select = copy.deepcopy(idx_k)
                else:
                    assert self.get_matrixB()[idx_k][idx_i] == 0
            assert idx_select >= 0
            self._solver_main.add( self._var_muB_denominatorList[idx_i] == self._var_muA_denominatorList[idx_select] )
            self._solver_main.add( self._var_muB_numeratorList[idx_i] == self._var_muA_numeratorList[idx_select] )

    ####################################################################################################################
    def _addConstraint_muBQmuC(self):
        '''
        Add constraint:
        \mu_b x Q = \mu_c
        :return:
        '''
        for idx_i in range(0, 64):
            self._solver_main.add(
                z3.Sum( [self._var_muB_numeratorList[idx_m] * self.get_matrixQ()[idx_m][idx_i] for idx_m in range(0, 64)] )
                == (self._var_muC_numeratorList[idx_i] * 256) )
            self._solver_main.add( self._var_muC_denominatorList[idx_i] == self._var_muB_denominatorList[idx_i] )

    ####################################################################################################################
    def _addConstraint_muCmuA(self):
        '''
        Add Constraint:
        \mu_c == \mu_a
        :return:
        '''
        for idx_i in range(0, 64):
            # self._solver_main.add(
            #     z3.Q(self._var_muC_numeratorList[idx_i], self._var_muC_denominatorList[idx_i])
            #     == z3.Q(self._var_muA_numeratorList[idx_i], self._var_muA_denominatorList[idx_i]) )
            self._solver_main.add(
                (self._var_muC_numeratorList[idx_i] * self._var_muA_denominatorList[idx_i])
                == (self._var_muC_denominatorList[idx_i] * self._var_muA_numeratorList[idx_i]) )

    ####################################################################################################################
    def _addConstraint_muASUM(self):
        '''
        Add Constraint:
        SUM(\mu_a) = 1
        :return:
        '''
        # self._solver_main.add(
        #     z3.Sum( [z3.Q(self._var_muA_numeratorList[idx_m], self._var_muA_denominatorList[idx_m]) for idx_m in range(0, 64)] )
        #     == 1 )

        # self._solver_main.add(
        #     z3.Sum( [(self._var_muA_numeratorList[idx_m] / self._var_muA_denominatorList[idx_m]) for idx_m in range(0, 64)] )
        #     == 1)

        self._solver_main.add(
            z3.Sum( [self._var_muA_numeratorList[idx_m] for idx_m in range(0, 64)] )
            == self._var_muA_denominatorList[0])
        for idx_iii in range(1, 63):
            self._solver_main.add( self._var_muA_denominatorList[idx_iii] == self._var_muA_denominatorList[0] )


    ####################################################################################################################
    def _addConstraint_muASymmetry(self):
        '''
        Add Constraint:
        \mu_a[i] == \mu_a[63-i]
        :return:
        '''
        for idx_i in range(0, 32):
            # self._solver_main.add(
            #     z3.Q(self._var_muA_numeratorList[idx_i], self._var_muA_denominatorList[idx_i])
            #     == z3.Q(self._var_muA_numeratorList[63 - idx_i], self._var_muA_denominatorList[63 - idx_i]) )
            self._solver_main.add( self._var_muA_numeratorList[idx_i] == self._var_muA_numeratorList[63 - idx_i] )
            self._solver_main.add(self._var_muA_denominatorList[idx_i] == self._var_muA_denominatorList[63 - idx_i])

    ####################################################################################################################
    def _addConstraint_others(self):
        '''

        :return:
        '''
        for idx_iii in range(0, 63):
            self._solver_main.add( self._var_muA_denominatorList[idx_iii] > 0 )
            self._solver_main.add( self._var_muA_numeratorList[idx_iii] >= 0 )

    ####################################################################################################################
    def addConstraint(self):

        # \mu_a x B = \mu_b
        self._addConstraint_muA2muB()
        print("Z3Solver: Constraint added - \mu_a x B = \mu_b")

        # \mu_b x Q = \mu_c
        self._addConstraint_muBQmuC()
        print("Z3Solver: Constraint added - \mu_b x Q = \mu_c")

        # \mu_c == \mu_a
        self._addConstraint_muCmuA()
        print("Z3Solver: Constraint added - \mu_c == \mu_a")

        # SUM(\mu_a) = 1
        self._addConstraint_muASUM()
        print("Z3Solver: Constraint added - SUM(\mu_a) = 1")

        # \mu_a[i] == \mu_a[63-i]
        self._addConstraint_muASymmetry()
        print("Z3Solver: Constraint added - \mu_a[i] == \mu_a[63-i]")

        # Others
        self._addConstraint_others()
        print("Z3Solver: Constraint added - Others")

    ####################################################################################################################
    def checkSolver(self):
        '''
        Check if there is a solution.
        :return:
        '''
        print("Check Solver...")
        self._checkResult_ifsat = self._solver_main.check()
        print("Check Solver - Done!")
        print("Result: {}".format(self._checkResult_ifsat))

    def get_ifsat(self):
        return copy.deepcopy(self._checkResult_ifsat)

    ####################################################################################################################
    def getSolutionModel(self):
        '''
        The solution is a model for the set of asserted constraints. A model is an interpretation that makes each asserted constraint true.
        :return:
        '''
        self._solution_model = self._solver_main.model()
        return copy.deepcopy(self._solution_model)










########################################################################################################################
########################################################################################################################
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

    ####################################################################################################################
    def _initialize_codec(self):
        '''
        Initlize codec.
        :return:
        '''
        timestamp_int = int(time.time())
        self._CodecInstance_7bit = BitStuffingCAC_Codec.BSCAC_ForHexDyS2C_2CSupFor7bitGroup_Main(instance_id=timestamp_int)

    ####################################################################################################################
    def _getConfig_msbFirst(self):
        '''
        If msbFirst is True (default), the element with idx=0 in the codeword list is the MSB. Otherwise, it's LSB.
        :return:
        '''
        return copy.deepcopy(self._config_msbFirst)

    ####################################################################################################################
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

    ####################################################################################################################
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

    ####################################################################################################################
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

    ####################################################################################################################
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
            transProbMatrix_top.modifyMatrix_singleRow(row_index=cw_origin_int, newProbList=transProb_list)

        return transProbMatrix_top

    ####################################################################################################################
    def get_transCnt_singleGroup_oneClockPeriod(self):
        '''
        Calculate the transition Cnt of single encoded group (7-bit codeword).
        :return:
        '''
        transCntMatrix_top = _transitionCntMatrix(n_size=(2**7))
        for cw_origin_int in range(0, (2**7)):
            transCnt_list = (2**7) * [0]
            cw_origin_tuple = self.tool_convert_int2BinTuple(input_int=cw_origin_int, n_bit=7, msbFirst=self._getConfig_msbFirst())
            for dataIn_int in range(0, (2**7)):
                dataIn_list = self.tool_convert_int2BinList(input_int=dataIn_int, n_bit=7, msbFirst=self._getConfig_msbFirst())
                cw_new_tuple, temp_n_transmittedBits, temp_unprocessedDataBitsList = self._CodecInstance_7bit.encoder_core(bits_to_be_trans=dataIn_list, last_codeword=cw_origin_tuple)
                cw_new_int = self.tool_convert_binListOrTuple2Int(input_bin_seq=cw_new_tuple, msbFirst=self._getConfig_msbFirst())
                transCnt_list[cw_new_int] = transCnt_list[cw_new_int] + 1
            # transProb_list = []
            # for transCnt_i in transCnt_list:
            #     transProb_list.append(fractions.Fraction(copy.deepcopy(transCnt_i), (2**7)))
            transCntMatrix_top.modifyMatrix_singleRow(row_index=cw_origin_int, newProbList=copy.deepcopy(transCnt_list))

        return transCntMatrix_top

    ####################################################################################################################
    def _calcMuA_subtask_getMatrixB(self):
        '''
        Get the Matrix B.
        :return:
        '''
        matrixAList_transpose = 64 * [None]
        for idx_i in range(0, 64):
            idx_i_binTuple = self.tool_convert_int2BinTuple(input_int=copy.deepcopy(idx_i), n_bit=6, msbFirst=self._getConfig_msbFirst())
            idx_k_binTuple = (copy.deepcopy(idx_i_binTuple[0]),
                              copy.deepcopy(idx_i_binTuple[5]),
                              copy.deepcopy(idx_i_binTuple[2]),
                              copy.deepcopy(idx_i_binTuple[1]),
                              copy.deepcopy(idx_i_binTuple[4]),
                              copy.deepcopy(idx_i_binTuple[3]))
            idx_k = self.tool_convert_binListOrTuple2Int(input_bin_seq=idx_k_binTuple)
            list_a = 64 * [0]
            list_a[idx_k] = 1
            matrixAList_transpose[idx_i] = copy.deepcopy(list_a)

        matrixAList_raw = []
        for idx_row in range(0, 64):
            rowList_a = []
            for idx_col in range(0, 64):
                if matrixAList_transpose[idx_col][idx_row] == 0:
                    rowList_a.append(0)
                elif matrixAList_transpose[idx_col][idx_row] == 1:
                    rowList_a.append(1)
                else:
                    assert False
            matrixAList_raw.append(tuple(copy.deepcopy(rowList_a)))
        matrixATuple_raw = tuple(matrixAList_raw)
        return matrixATuple_raw

    ####################################################################################################################
    def _calcMuA_subtask_getMatrixQ(self):
        '''
        Get the matrix Q (trans count).
        :return:
        '''
        transCntMatrix_top = _transitionCntMatrix(n_size=(2**6))
        for cw_origin_int in range(0, (2**6)):
            transCnt_list = (2**6) * [0]
            cw_origin_tuple_6bit = self.tool_convert_int2BinTuple(input_int=cw_origin_int, n_bit=6, msbFirst=self._getConfig_msbFirst())
            if True:
                cw_origin_tuple_full_0 = (0,
                                          copy.deepcopy(cw_origin_tuple_6bit[0]),
                                          copy.deepcopy(cw_origin_tuple_6bit[1]),
                                          copy.deepcopy(cw_origin_tuple_6bit[2]),
                                          copy.deepcopy(cw_origin_tuple_6bit[3]),
                                          copy.deepcopy(cw_origin_tuple_6bit[4]),
                                          copy.deepcopy(cw_origin_tuple_6bit[5]))
                cw_origin_tuple_full_1 = (1,
                                          copy.deepcopy(cw_origin_tuple_6bit[0]),
                                          copy.deepcopy(cw_origin_tuple_6bit[1]),
                                          copy.deepcopy(cw_origin_tuple_6bit[2]),
                                          copy.deepcopy(cw_origin_tuple_6bit[3]),
                                          copy.deepcopy(cw_origin_tuple_6bit[4]),
                                          copy.deepcopy(cw_origin_tuple_6bit[5]))

            for dataIn_int in range(0, (2**7)):
                dataIn_list = self.tool_convert_int2BinList(input_int=dataIn_int, n_bit=7, msbFirst=self._getConfig_msbFirst())

                cw_new_tuple_0, temp_n_transmittedBits_0, temp_unprocessedDataBitsList_0 = self._CodecInstance_7bit.encoder_core(
                    bits_to_be_trans=dataIn_list,
                    last_codeword=cw_origin_tuple_full_0)
                cw_new_tuple_1, temp_n_transmittedBits_1, temp_unprocessedDataBitsList_1 = self._CodecInstance_7bit.encoder_core(
                    bits_to_be_trans=dataIn_list,
                    last_codeword=cw_origin_tuple_full_1)

                cw_new_int_0 = self.tool_convert_binListOrTuple2Int(input_bin_seq=(cw_new_tuple_0[1],
                                                                                   cw_new_tuple_0[2],
                                                                                   cw_new_tuple_0[3],
                                                                                   cw_new_tuple_0[4],
                                                                                   cw_new_tuple_0[5],
                                                                                   cw_new_tuple_0[6]),
                                                                    msbFirst=self._getConfig_msbFirst())
                transCnt_list[cw_new_int_0] = transCnt_list[cw_new_int_0] + 1

                cw_new_int_1 = self.tool_convert_binListOrTuple2Int(input_bin_seq=(cw_new_tuple_1[1],
                                                                                   cw_new_tuple_1[2],
                                                                                   cw_new_tuple_1[3],
                                                                                   cw_new_tuple_1[4],
                                                                                   cw_new_tuple_1[5],
                                                                                   cw_new_tuple_1[6]),
                                                                    msbFirst=self._getConfig_msbFirst())
                transCnt_list[cw_new_int_1] = transCnt_list[cw_new_int_1] + 1
            # transProb_list = []
            # for transCnt_i in transCnt_list:
            #     transProb_list.append(fractions.Fraction(copy.deepcopy(transCnt_i), (2**7)))
            transCntMatrix_top.modifyMatrix_singleRow(row_index=cw_origin_int, newProbList=copy.deepcopy(transCnt_list))

        return transCntMatrix_top

    ####################################################################################################################
    def calcMuA_main(self):
        '''
        Calc \mu_a
        :return:
        '''

        # Get Matrix B
        param_matrixB = self._calcMuA_subtask_getMatrixB()

        # Get Matrix Q
        param_matrixQ_instance = self._calcMuA_subtask_getMatrixQ()
        param_matrixQ = param_matrixQ_instance.getMatrix_all()

        # Create Z3 solver
        z3Solver_instance = _Z3Solver_forMuACalc(matrix_B=copy.deepcopy(param_matrixB),
                                                 matrix_Q=copy.deepcopy(param_matrixQ))

        # Add Constraint
        z3Solver_instance.addConstraint()

        # Check Solver
        z3Solver_instance.checkSolver()

        # Get Model
        solutionModel_instance = z3Solver_instance.getSolutionModel()
        for modelVar_d in solutionModel_instance.decls():
            print(modelVar_d.name(), solutionModel_instance[modelVar_d])






