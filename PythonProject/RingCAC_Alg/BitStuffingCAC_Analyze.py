import copy
import time
import fractions
import random

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import z3 as z3

import PythonProject.RingCAC_Alg.BitStuffingCAC_Codec as BitStuffingCAC_Codec

########################################################################################################################


########################################################################################################################
### class _transitionProbabilityMatrix
########################################################################################################################
###
###
###
########################################################################################################################
class _transitionProbabilityMatrix:
    '''
    The transition probability matrix.
    '''
    def __init__(self, n_size: int):
        assert isinstance(n_size, int) and n_size > 1
        self._param_matrixSize = copy.deepcopy(n_size)
        self._init_mainMatrix()

    ####################################################################################################################
    def __repr__(self):
        matrixCheck_ifpass, matrixCheck_errList = self.checkMatrix()
        matrixInfoStr = ("-------\nTransition Probability Matrix\n"
                         "---Size: {} x {} \n---Matrix Check Pass: {} \n---Errors: {}\n-------\n").format(self.getParam_matrixSize(),
                                                                                                          self.getParam_matrixSize(),
                                                                                                          matrixCheck_ifpass,
                                                                                                          matrixCheck_errList)
        return matrixInfoStr

    ####################################################################################################################
    def getParam_matrixSize(self):
        return copy.deepcopy(self._param_matrixSize)

    ####################################################################################################################
    def _init_mainMatrix(self):
        '''
        Initialize / Reset the trans prob matrix.
        :return:
        '''
        self._matrix_main = []
        for row_i in range(0, self.getParam_matrixSize()):
            col_list = self.getParam_matrixSize() * [0]
            self._matrix_main.append(copy.deepcopy(col_list))

    ####################################################################################################################
    def reset_Matrix(self):
        '''
        Reset
        :return:
        '''
        self._init_mainMatrix()

    ####################################################################################################################
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

    ####################################################################################################################
    def getMatrix_all(self):
        return copy.deepcopy(self._matrix_main)

    ####################################################################################################################
    def getMatrix_oneRow(self, row_idx: int) -> tuple:
        row_list = copy.deepcopy(self._matrix_main[row_idx])
        return tuple(row_list)

    ####################################################################################################################
    def getMatrix_oneCol(self, col_idx: int) -> tuple:
        col_list = []
        for row_i in range(0, self.getParam_matrixSize()):
            col_list.append(copy.deepcopy(self._matrix_main[row_i][col_idx]))
        return tuple(col_list)

    ####################################################################################################################
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

    ####################################################################################################################
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

    ####################################################################################################################
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
### class _transitionCntMatrix <-- (_transitionProbabilityMatrix)
########################################################################################################################
###
###
###
########################################################################################################################
class _transitionCntMatrix(_transitionProbabilityMatrix):
    def __init__(self, n_size):
        super().__init__(n_size=n_size)

    ####################################################################################################################
    def __repr__(self):
        matrixCheck_ifpass, matrixCheck_errList = self.checkMatrix()
        matrixInfoStr = ("-------\nTransition Count Matrix\n"
                         "---Size: {} x {} \n---Matrix Check Pass: {} \n---Errors: {}\n-------\n").format(self.getParam_matrixSize(),
                                                                                                          self.getParam_matrixSize(),
                                                                                                          matrixCheck_ifpass,
                                                                                                          matrixCheck_errList)
        return matrixInfoStr

    ####################################################################################################################
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

    ####################################################################################################################
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
### class _Z3Solver_forMuACalc
########################################################################################################################
###
### ABANDONED!!! DO NOT USE!!!
###
########################################################################################################################
class _Z3Solver_forMuACalc:
    '''
    Z3 Solver for matrix \mu_a calculation & code rate analyze.
    '''
    def __init__(self, matrix_B, matrix_Q):
        ###################################
        # class '_Z3Solver_forMuACalc' has been abandoned!!!
        assert False
        ###################################

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
### class _Z3Solver_forMuACalc_Simplfied_useMatrixBQ
########################################################################################################################
###
###
###
########################################################################################################################
class _Z3Solver_forMuACalc_Simplfied_useMatrixBQ:
    '''
    Z3 Solver for matrix \mu_a calculation & code rate analyze.
    A simplified version:
    (1) Use 'Real' variables to represent the probability, rather than 'Int' / 'Int'.
    (2) Use Matrix BQ to replace Matrix B & Matrix Q, according to the associative law of matrices: (AB)C = A(BC).
    '''
    def __init__(self, matrix_BQ):
        # Matrix BQ = Matrix B times matrix Q
        # Matrix Q = Matrix P * 256
        assert len(matrix_BQ) == 64
        for idx_ii in range(0, 64):
            assert len(matrix_BQ[idx_ii]) == 64
            for idx_jj in range(0, 64):
                assert isinstance(matrix_BQ[idx_ii][idx_jj], int)
        self._matrix_BQ = copy.deepcopy(matrix_BQ)

        # Z3 solver
        self._solver_main = z3.Solver()

        # var \mu_a
        # Each element in \mu_a is represented by a Real var.
        self._var_muA_List = z3.RealVector('muA', 64)

    ####################################################################################################################
    def get_matrixBQ(self):
        return copy.deepcopy(self._matrix_BQ)

    ####################################################################################################################
    def get_var_muAList(self):
        return copy.deepcopy(self._var_muA_List)

    ####################################################################################################################
    def get_solverMain(self):
        return copy.deepcopy(self._solver_main)

    ####################################################################################################################
    def getSolutionModel(self):
        '''
        The solution is a model for the set of asserted constraints. A model is an interpretation that makes each asserted constraint true.
        :return:
        '''
        self._solution_model = self._solver_main.model()
        return copy.deepcopy(self._solution_model)

    ####################################################################################################################
    def modelEvaluate_sumOfMuATimesWeight(self, weightTuple):
        '''
        Calculate the sum of (\muA[i] * weight[i]).
        :param weightTuple:
        :return:
        '''
        assert isinstance(weightTuple, tuple)
        assert len(weightTuple) == (2 ** 6)
        sumResult = self.getSolutionModel().evaluate(
            z3.Sum( [(self._var_muA_List[idx_ei] * weightTuple[idx_ei]) for idx_ei in range(0, 64)] )
        )
        return copy.deepcopy(sumResult)



    ####################################################################################################################
    def _addConstraint_muAmatrixBQmuA(self):
        '''
        Add Constraint:
        \mu_a times matrix BQ = \mu_a
        :return:
        '''
        for idx_i in range(0, 64):
            self._solver_main.add(
                z3.Sum( [(self._var_muA_List[idx_k] * self.get_matrixBQ()[idx_k][idx_i]) for idx_k in range(0, 64)] )
                == (self._var_muA_List[idx_i] * 256)
            )

    ####################################################################################################################
    def _addConstraint_muASUM(self):
        '''
        Add Constraint:
        SUM(\mu_a) == 1
        :return:
        '''
        self._solver_main.add(
            z3.Sum(self._var_muA_List) == z3.RealVal(1)
        )

    ####################################################################################################################
    def _addConstraint_muASymmetry(self):
        '''
        Add Constraint:
        \mu_a[i] == \mu_a[63-i]
        :return:
        '''
        for idx_i in range(0, 32):
            self._solver_main.add(
                self._var_muA_List[idx_i] == self._var_muA_List[63 - idx_i]
            )

    ####################################################################################################################
    def _addConstraint_others(self):
        '''

        :return:
        '''
        for idx_iii in range(0, 63):
            self._solver_main.add( self._var_muA_List[idx_iii] >= 0 )
            self._solver_main.add( self._var_muA_List[idx_iii] <= 1 )

    ####################################################################################################################
    def addConstraint_basic(self):

        # \mu_a x BQ = \mu_a
        self._addConstraint_muAmatrixBQmuA()
        print("Z3Solver: Constraint added - \mu_a x BQ = \mu_a")

        # SUM(\mu_a) = 1
        self._addConstraint_muASUM()
        print("Z3Solver: Constraint added - SUM(\mu_a) = 1")

        # Others
        self._addConstraint_others()
        print("Z3Solver: Constraint added - Others")

    ####################################################################################################################
    def addConstraint_full(self):

        # \mu_a x BQ = \mu_a
        self._addConstraint_muAmatrixBQmuA()
        print("Z3Solver: Constraint added - \mu_a x BQ = \mu_a")

        # SUM(\mu_a) = 1
        self._addConstraint_muASUM()
        print("Z3Solver: Constraint added - SUM(\mu_a) = 1")

        # \mu_a[i] = \mu_a[63-i]
        self._addConstraint_muASymmetry()
        print("Z3Solver: Constraint added - \mu_a[i] = \mu_a[63-i]")

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

    ####################################################################################################################
    def get_ifsat(self):
        '''
        Get the result of the last 'check' - sat or not.
        :return:
        '''
        return copy.deepcopy(self._checkResult_ifsat)

    ####################################################################################################################


########################################################################################################################
### class _Z3Solver_forMuACalc_Simplfied_useMatrixCQ <-- (_Z3Solver_forMuACalc_Simplfied_useMatrixBQ)
########################################################################################################################
###
###
###
########################################################################################################################
class _Z3Solver_forMuACalc_Simplfied_useMatrixCQ(_Z3Solver_forMuACalc_Simplfied_useMatrixBQ):
    '''
    Z3 Solver for matrix \mu_a calculation & code rate analyze.
    A simplified version:
    (1) Use 'Real' variables to represent the probability, rather than 'Int' / 'Int'.
    (2) Use Matrix CQ to replace Matrix B & Matrix Q. Matrix C assumes three pairs of bits are independent of each other.
    '''
    def __init__(self, matrix_C_b16, matrix_C_b32, matrix_C_b54, matrix_Q):
        assert len(matrix_C_b16) == 64
        assert len(matrix_C_b32) == 64
        assert len(matrix_C_b54) == 64
        assert len(matrix_Q) == 64
        for idx_ii in range(0, 64):
            assert len(matrix_C_b16[idx_ii]) == 64
            assert len(matrix_C_b32[idx_ii]) == 64
            assert len(matrix_C_b54[idx_ii]) == 64
            assert len(matrix_Q) == 64
            for idx_kk in range(0, 64):
                assert isinstance(matrix_Q[idx_ii][idx_kk], int)
                assert matrix_Q[idx_ii][idx_kk] >= 0
                assert matrix_C_b16[idx_ii][idx_kk] in (0, 1)
                assert matrix_C_b32[idx_ii][idx_kk] in (0, 1)
                assert matrix_C_b54[idx_ii][idx_kk] in (0, 1)

        self._matrix_C_b16 = copy.deepcopy(matrix_C_b16)
        self._matrix_C_b32 = copy.deepcopy(matrix_C_b32)
        self._matrix_C_b54 = copy.deepcopy(matrix_C_b54)
        self._matrix_Q = copy.deepcopy(matrix_Q)




        # Z3 solver
        self._solver_main = z3.Solver()

        # var \mu_a
        # Each element in \mu_a is represented by a Real var.
        self._var_muA_List = z3.RealVector('muA', 64)

        # var \mu_b
        self._var_muB_List = z3.RealVector('muB', 64)

    ####################################################################################################################
    def get_MatrixC_b16(self):
        return copy.deepcopy(self._matrix_C_b16)

    ####################################################################################################################
    def get_MatrixC_b32(self):
        return copy.deepcopy(self._matrix_C_b32)

    ####################################################################################################################
    def get_MatrixC_b54(self):
        return copy.deepcopy(self._matrix_C_b54)

    ####################################################################################################################
    def get_MatrixQ(self):
        return copy.deepcopy(self._matrix_Q)

    ####################################################################################################################
    def get_matrixBQ(self):
        assert False

    ####################################################################################################################
    def _addConstraint_muAmatrixBQmuA(self):
        assert False

    ####################################################################################################################
    def _addConstraint_muA2muB(self):
        '''
        Add Constraint:
        \mu_a --> \mu_b.
        :return:
        '''
        for idx_i in range(0, 64):
            self._solver_main.add(
                ( (z3.Sum( [(self._var_muA_List[idx_ka] * self.get_MatrixC_b16()[idx_ka][idx_i]) for idx_ka in range(0, 64)] ))
                * (z3.Sum( [(self._var_muA_List[idx_kb] * self.get_MatrixC_b32()[idx_kb][idx_i]) for idx_kb in range(0, 64)] ))
                * (z3.Sum( [(self._var_muA_List[idx_kc] * self.get_MatrixC_b54()[idx_kc][idx_i]) for idx_kc in range(0, 64)] )) )
                == self._var_muB_List[idx_i]
            )

    ####################################################################################################################
    def _addConstraint_muBmatrixQmuA(self):
        '''
        Add Constraint:
        \mu_b times matrix Q = \mu_a
        :return:
        '''
        for idx_i in range(0, 64):
            self._solver_main.add(
                z3.Sum( [(self._var_muB_List[idx_k] * self.get_MatrixQ()[idx_k][idx_i]) for idx_k in range(0, 64)] )
                == (self._var_muA_List[idx_i] * 256)
            )

    ####################################################################################################################
    def addConstraint_basic(self):

        # \mu_a x BQ = \mu_a
        self._addConstraint_muA2muB()
        print("Z3Solver: Constraint added - \mu_a --> \mu_b")

        # \mu_b times matrix Q = \mu_a
        self._addConstraint_muBmatrixQmuA()
        print("Z3Solver: Constraint added - \mu_b times matrix Q = \mu_a")

        # SUM(\mu_a) = 1
        self._addConstraint_muASUM()
        print("Z3Solver: Constraint added - SUM(\mu_a) = 1")

        # Others
        self._addConstraint_others()
        print("Z3Solver: Constraint added - Others")

    ####################################################################################################################
    def addConstraint_full(self):

        # \mu_a x BQ = \mu_a
        self._addConstraint_muA2muB()
        print("Z3Solver: Constraint added - \mu_a --> \mu_b")

        # \mu_b times matrix Q = \mu_a
        self._addConstraint_muBmatrixQmuA()
        print("Z3Solver: Constraint added - \mu_b times matrix Q = \mu_a")

        # SUM(\mu_a) = 1
        self._addConstraint_muASUM()
        print("Z3Solver: Constraint added - SUM(\mu_a) = 1")

        # \mu_a[i] = \mu_a[63-i]
        self._addConstraint_muASymmetry()
        print("Z3Solver: Constraint added - \mu_a[i] = \mu_a[63-i]")

        # Others
        self._addConstraint_others()
        print("Z3Solver: Constraint added - Others")



########################################################################################################################
### class _Z3Solver_forMuACalc_Simplfied_useMatrixCQ <-- (_Z3Solver_forMuACalc_Simplfied_useMatrixBQ)
########################################################################################################################
###
###
###
########################################################################################################################
class _Z3Solver_forMuACalc_Simplfied_useMatrixCQ_ver20241118(_Z3Solver_forMuACalc_Simplfied_useMatrixBQ):
    '''
    Z3 Solver for matrix \mu_a calculation & code rate analyze.
    A simplified version:
    (1) Use 'Real' variables to represent the probability, rather than 'Int' / 'Int'.
    (2) Use Matrix CQ to replace Matrix B & Matrix Q. Matrix C assumes three pairs of bits are independent of each other.

    Changelog: 20241118-
    '''
    def __init__(self, matrix_C_b16, matrix_C_b32, matrix_C_b54, matrix_Q):
        assert len(matrix_C_b16) == 64
        assert len(matrix_C_b32) == 64
        assert len(matrix_C_b54) == 64
        assert len(matrix_Q) == 64
        for idx_ii in range(0, 64):
            assert len(matrix_C_b16[idx_ii]) == 64
            assert len(matrix_C_b32[idx_ii]) == 64
            assert len(matrix_C_b54[idx_ii]) == 64
            assert len(matrix_Q) == 64
            for idx_kk in range(0, 64):
                assert isinstance(matrix_Q[idx_ii][idx_kk], int)
                assert matrix_Q[idx_ii][idx_kk] >= 0
                assert matrix_C_b16[idx_ii][idx_kk] in (0, 1)
                assert matrix_C_b32[idx_ii][idx_kk] in (0, 1)
                assert matrix_C_b54[idx_ii][idx_kk] in (0, 1)

        self._matrix_C_b16 = copy.deepcopy(matrix_C_b16)
        self._matrix_C_b32 = copy.deepcopy(matrix_C_b32)
        self._matrix_C_b54 = copy.deepcopy(matrix_C_b54)
        self._matrix_Q = copy.deepcopy(matrix_Q)




        # Z3 solver
        self._solver_main = z3.Solver()

        # var \mu_a
        # Each element in \mu_a is represented by a Real var.
        self._var_muA_List = z3.RealVector('muA', 64)

        # var \mu_b
        self._var_muB_List = z3.RealVector('muB', 64)

    ####################################################################################################################
    def get_MatrixC_b16(self):
        return copy.deepcopy(self._matrix_C_b16)

    ####################################################################################################################
    def get_MatrixC_b32(self):
        return copy.deepcopy(self._matrix_C_b32)

    ####################################################################################################################
    def get_MatrixC_b54(self):
        return copy.deepcopy(self._matrix_C_b54)

    ####################################################################################################################
    def get_MatrixQ(self):
        return copy.deepcopy(self._matrix_Q)

    ####################################################################################################################
    def get_matrixBQ(self):
        assert False

    ####################################################################################################################
    def _addConstraint_muAmatrixBQmuA(self):
        assert False

    ####################################################################################################################
    def _addConstraint_muA2muB(self):
        '''
        Add Constraint:
        \mu_a --> \mu_b.
        :return:
        '''
        for idx_i in range(0, 64):
            self._solver_main.add(
                ( (z3.Sum( [(self._var_muA_List[idx_ka] * self.get_MatrixC_b16()[idx_ka][idx_i]) for idx_ka in range(0, 64)] ))
                * (z3.Sum( [(self._var_muA_List[idx_kb] * self.get_MatrixC_b32()[idx_kb][idx_i]) for idx_kb in range(0, 64)] ))
                * (z3.Sum( [(self._var_muA_List[idx_kc] * self.get_MatrixC_b54()[idx_kc][idx_i]) for idx_kc in range(0, 64)] )) )
                == self._var_muB_List[idx_i]
            )

    ####################################################################################################################
    def _addConstraint_muBmatrixQmuA(self):
        '''
        Add Constraint:
        \mu_b times matrix Q = \mu_a
        :return:
        '''
        for idx_i in range(0, 64):
            self._solver_main.add(
                z3.Sum( [(self._var_muB_List[idx_k] * self.get_MatrixQ()[idx_k][idx_i]) for idx_k in range(0, 64)] )
                == (self._var_muA_List[idx_i] * 256)
            )

    ####################################################################################################################
    def addConstraint_basic(self):

        # \mu_a x BQ = \mu_a
        self._addConstraint_muA2muB()
        print("Z3Solver: Constraint added - \mu_a --> \mu_b")

        # \mu_b times matrix Q = \mu_a
        self._addConstraint_muBmatrixQmuA()
        print("Z3Solver: Constraint added - \mu_b times matrix Q = \mu_a")

        # SUM(\mu_a) = 1
        self._addConstraint_muASUM()
        print("Z3Solver: Constraint added - SUM(\mu_a) = 1")

        # Others
        self._addConstraint_others()
        print("Z3Solver: Constraint added - Others")

    ####################################################################################################################
    def addConstraint_full(self):

        # \mu_a x BQ = \mu_a
        self._addConstraint_muA2muB()
        print("Z3Solver: Constraint added - \mu_a --> \mu_b")

        # \mu_b times matrix Q = \mu_a
        self._addConstraint_muBmatrixQmuA()
        print("Z3Solver: Constraint added - \mu_b times matrix Q = \mu_a")

        # SUM(\mu_a) = 1
        self._addConstraint_muASUM()
        print("Z3Solver: Constraint added - SUM(\mu_a) = 1")

        # \mu_a[i] = \mu_a[63-i]
        self._addConstraint_muASymmetry()
        print("Z3Solver: Constraint added - \mu_a[i] = \mu_a[63-i]")

        # Others
        self._addConstraint_others()
        print("Z3Solver: Constraint added - Others")







########################################################################################################################
### class BitStuffingCAC_Analyze_HexArray
########################################################################################################################
###
###
###
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
    def get_nBitTransmittedCnt_matrixByOldState_singleGroup_oneClockPeriod(self):
        '''
        Calculate the Cnt of the transmitted bits in single encoded group (7-bit codeword).
        The number of transmitted bits in each "old_state + data_in" case is added up.
        And the weight of each "old_state + data_in" case is 1 instead of the occurrence probability.
        :return: tuple_nBitTransCnt, tuple_minAndMax - tuple_nBitTransCnt is a tuple, in which the idx represents the old state,
                and the value is the sum value of the transmitted data bits in all "old_state(=idx) + data_in(all 0 ~ all 1)" cases.
                tuple_minAndMax is a tuple contains five int value:
                (1) The min number of transmitted data bits in single "old_state + data_in" case;
                (2) The max number of transmitted data bits in single "old_state + data_in" case;
                (3) The min sum value of the number of transmitted data bits of all "old_state" cases;
                (4) The max sum value of the number of transmitted data bits of all "old_state" cases;
                (5) The sum of all the number of transmitted data bits.
        '''
        transCntMatrix_top = _transitionCntMatrix(n_size=(2**7))
        list_nBitTransCnt = []
        allSum_nBitTransCnt = 0
        maxValue_nBitTransCnt_eachOldState = 0
        minValue_nBitTransCnt_eachOldState = (2**7) * 7
        maxValue_nBitTransCnt_eachCase = 0
        minValue_nBitTransCnt_eachCase = 7
        for cw_origin_int in range(0, (2**7)):
            cnt_nBitTrans = 0
            transCnt_list = (2**7) * [0]
            cw_origin_tuple = self.tool_convert_int2BinTuple(input_int=cw_origin_int, n_bit=7, msbFirst=self._getConfig_msbFirst())
            for dataIn_int in range(0, (2**7)):
                dataIn_list = self.tool_convert_int2BinList(input_int=dataIn_int, n_bit=7, msbFirst=self._getConfig_msbFirst())
                cw_new_tuple, caseResult_n_transmittedBits, temp_unprocessedDataBitsList = self._CodecInstance_7bit.encoder_core(bits_to_be_trans=dataIn_list, last_codeword=cw_origin_tuple)
                cw_new_int = self.tool_convert_binListOrTuple2Int(input_bin_seq=cw_new_tuple, msbFirst=self._getConfig_msbFirst())
                transCnt_list[cw_new_int] = transCnt_list[cw_new_int] + 1
                cnt_nBitTrans = cnt_nBitTrans + caseResult_n_transmittedBits
                if maxValue_nBitTransCnt_eachCase < caseResult_n_transmittedBits:
                    maxValue_nBitTransCnt_eachCase = copy.deepcopy(caseResult_n_transmittedBits)
                if minValue_nBitTransCnt_eachCase > caseResult_n_transmittedBits:
                    minValue_nBitTransCnt_eachCase = copy.deepcopy(caseResult_n_transmittedBits)
            # transProb_list = []
            # for transCnt_i in transCnt_list:
            #     transProb_list.append(fractions.Fraction(copy.deepcopy(transCnt_i), (2**7)))
            transCntMatrix_top.modifyMatrix_singleRow(row_index=cw_origin_int, newProbList=copy.deepcopy(transCnt_list))

            list_nBitTransCnt.append(copy.deepcopy(cnt_nBitTrans))

            if maxValue_nBitTransCnt_eachOldState < cnt_nBitTrans:
                maxValue_nBitTransCnt_eachOldState = copy.deepcopy(cnt_nBitTrans)
            if minValue_nBitTransCnt_eachOldState > cnt_nBitTrans:
                minValue_nBitTransCnt_eachOldState = copy.deepcopy(cnt_nBitTrans)

            allSum_nBitTransCnt = allSum_nBitTransCnt + cnt_nBitTrans

        tuple_nBitTransCnt = tuple(copy.deepcopy(list_nBitTransCnt))
        tuple_minAndMax = (copy.deepcopy(minValue_nBitTransCnt_eachCase),
                           copy.deepcopy(maxValue_nBitTransCnt_eachCase),
                           copy.deepcopy(minValue_nBitTransCnt_eachOldState),
                           copy.deepcopy(maxValue_nBitTransCnt_eachOldState),
                           copy.deepcopy(allSum_nBitTransCnt))

        return tuple_nBitTransCnt, tuple_minAndMax

    ####################################################################################################################
    ####################################################################################################################
    # \mu_a calculation & coding rate analyze
    #
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
    # The method 'calcMuA_main' has been abandoned! ####################################################################
    # Use 'calcMuASimplified_main' to calculate \mu_a ! ################################################################
    ####################################################################################################################
    # def calcMuA_main(self):
    #     '''
    #     Calc \mu_a
    #     :return:
    #     '''
    #
    #     # Get Matrix B
    #     param_matrixB = self._calcMuA_subtask_getMatrixB()
    #
    #     # Get Matrix Q
    #     param_matrixQ_instance = self._calcMuA_subtask_getMatrixQ()
    #     param_matrixQ = param_matrixQ_instance.getMatrix_all()
    #
    #     # Create Z3 solver
    #     z3Solver_instance = _Z3Solver_forMuACalc(matrix_B=copy.deepcopy(param_matrixB),
    #                                              matrix_Q=copy.deepcopy(param_matrixQ))
    #
    #     # Add Constraint
    #     z3Solver_instance.addConstraint()
    #
    #     # Check Solver
    #     z3Solver_instance.checkSolver()
    #
    #     # Get Model
    #     solutionModel_instance = z3Solver_instance.getSolutionModel()
    #     for modelVar_d in solutionModel_instance.decls():
    #         print(modelVar_d.name(), solutionModel_instance[modelVar_d])

    ####################################################################################################################
    ####################################################################################################################
    # \mu_a calculation & coding rate analyze - Version 20240410
    #
    ####################################################################################################################
    def _calcMuASimplified_subtask_getMatrixBQ(self):
        '''
        Calc Matrix BQ.
        :return:
        '''
        matrix_B = self._calcMuA_subtask_getMatrixB()
        matrix_Q_instance = self._calcMuA_subtask_getMatrixQ()
        matrix_Q = matrix_Q_instance.getMatrix_all()

        matrix_BQ_list = []

        for idx_row in range(0, 64):
            currentRow_list = []
            for idx_col in range(0, 64):
                currentElement = 0
                for idx_mulsum in range(0, 64):
                    currentElement = currentElement + (matrix_B[idx_row][idx_mulsum] * matrix_Q[idx_mulsum][idx_col])
                    assert ( (matrix_B[idx_row][idx_mulsum] == 0) or (matrix_Q[idx_mulsum][idx_col] == currentElement) )
                currentRow_list.append(copy.deepcopy(currentElement))

            currentRow_tuple = tuple(currentRow_list)
            matrix_BQ_list.append(copy.deepcopy(currentRow_tuple))

        matrix_BQ_tuple = tuple(matrix_BQ_list)

        return matrix_BQ_tuple

    def calcMuASimplified_useMatrixBQ_main(self, constraintSet = 'full'):
        '''
        Calc \mu_a.
        :return:
        '''

        assert constraintSet in ('full', 'basic')

        # Get Matrix BQ
        print("Calculating Matrix BQ...")
        param_matrixBQ = self._calcMuASimplified_subtask_getMatrixBQ()
        assert len(param_matrixBQ) == 64
        if True:
            print("Matrix BQ: ")
            idx_cnt = 0
            for matrixBQ_row_i in param_matrixBQ:
                assert len(matrixBQ_row_i) == 64
                sum_row_i = 0
                for matrixBQ_i in matrixBQ_row_i:
                    sum_row_i = sum_row_i + matrixBQ_i
                assert sum_row_i == 256
                print("Row{}\t - Sum{} - {}".format(idx_cnt, sum_row_i, matrixBQ_row_i))
                idx_cnt = idx_cnt + 1

        print("#######################################################################################################")
        print("#######################################################################################################")
        print("Create Z3-Solver Instance...")
        z3Solver_instance = _Z3Solver_forMuACalc_Simplfied_useMatrixBQ(matrix_BQ=copy.deepcopy(param_matrixBQ))
        print("Add Constraint ({})...".format(constraintSet))
        if constraintSet == 'full':
            z3Solver_instance.addConstraint_full()
        elif constraintSet == 'basic':
            z3Solver_instance.addConstraint_basic()

        z3Solver_instance.checkSolver()

        solutionModel_instance = z3Solver_instance.getSolutionModel()
        for modelVar_d in solutionModel_instance.decls():
            print(modelVar_d.name(), '=\t', solutionModel_instance[modelVar_d])


        # print("###### {}".format(solutionModel_instance.evaluate( z3.Sum([z3Solver_instance.get_var_muAList()[idx_sss] for idx_sss in range(0, 32)]) )))
        return z3Solver_instance


    ####################################################################################################################
    def _calcMuA_subtask_getMatrixC(self):
        '''
        Get the Matrix C.
        :return:
        '''
        # cMatrix_bits16 = []
        # cMatrix_bits32 = []
        # cMatrix_bits54 = []
        #
        # for idx_codeword in range(0, 64):
        #     cList_bits16 = [0, 0, 0,
        #                     0]  # [ (bits[0,5] == 00 ?), (bits[0,5] == 01 ?), (bits[0,5] == 10 ?), (bits[0,5] == 11 ?) ]
        #     cList_bits32 = [0, 0, 0,
        #                     0]  # [ (bits[2,1] == 00 ?), (bits[2,1] == 01 ?), (bits[2,1] == 10 ?), (bits[2,1] == 11 ?) ]
        #     cList_bits54 = [0, 0, 0,
        #                     0]  # [ (bits[4,3] == 00 ?), (bits[4,3] == 01 ?), (bits[4,3] == 10 ?), (bits[4,3] == 11 ?) ]
        #
        #     cw_binTuple = self.tool_convert_int2BinTuple(input_int=copy.deepcopy(idx_codeword), n_bit=6, msbFirst=self._getConfig_msbFirst())
        #
        #     if (cw_binTuple[0] == 0 and cw_binTuple[5] == 0):
        #         cList_bits16[0] = 1
        #     elif (cw_binTuple[0] == 0 and cw_binTuple[5] == 1):
        #         cList_bits16[1] = 1
        #     elif (cw_binTuple[0] == 1 and cw_binTuple[5] == 0):
        #         cList_bits16[2] = 1
        #     elif (cw_binTuple[0] == 1 and cw_binTuple[5] == 1):
        #         cList_bits16[3] = 1
        #     else:
        #         assert False
        #
        #     if (cw_binTuple[2] == 0 and cw_binTuple[1] == 0):
        #         cList_bits32[0] = 1
        #     elif (cw_binTuple[2] == 0 and cw_binTuple[1] == 1):
        #         cList_bits32[1] = 1
        #     elif (cw_binTuple[2] == 1 and cw_binTuple[1] == 0):
        #         cList_bits32[2] = 1
        #     elif (cw_binTuple[2] == 1 and cw_binTuple[1] == 1):
        #         cList_bits32[3] = 1
        #     else:
        #         assert False
        #
        #     if (cw_binTuple[4] == 0 and cw_binTuple[3] == 0):
        #         cList_bits54[0] = 1
        #     elif (cw_binTuple[4] == 0 and cw_binTuple[3] == 1):
        #         cList_bits54[1] = 1
        #     elif (cw_binTuple[4] == 1 and cw_binTuple[3] == 0):
        #         cList_bits54[2] = 1
        #     elif (cw_binTuple[4] == 1 and cw_binTuple[3] == 1):
        #         cList_bits54[3] = 1
        #     else:
        #         assert False
        #
        #     cTuple_bits16 = tuple(cList_bits16)
        #     cTuple_bits32 = tuple(cList_bits32)
        #     cTuple_bits54 = tuple(cList_bits54)
        #
        #     cMatrix_bits16.append(copy.deepcopy(cTuple_bits16))
        #     cMatrix_bits32.append(copy.deepcopy(cTuple_bits32))
        #     cMatrix_bits54.append(copy.deepcopy(cTuple_bits54))


        matrixC_A_tr = []
        matrixC_B_tr = []
        matrixC_C_tr = []


        for idx_ii in range(0, 64):
            matrixATr_rowList = []
            matrixBTr_rowList = []
            matrixCTr_rowList = []
            idx_ii_binTuple = self.tool_convert_int2BinTuple(input_int=copy.deepcopy(idx_ii),
                                                             n_bit=6,
                                                             msbFirst=self._getConfig_msbFirst())

            for idx_state_i in range(0, 64):
                idx_state_i_binTuple = self.tool_convert_int2BinTuple(input_int=copy.deepcopy(idx_state_i),
                                                                      n_bit=6,
                                                                      msbFirst=self._getConfig_msbFirst())
                if ((idx_ii_binTuple[0] == idx_state_i_binTuple[0]) and (idx_ii_binTuple[1] == idx_state_i_binTuple[5])):
                    matrixATr_rowList.append(1)
                else:
                    matrixATr_rowList.append(0)

                if ((idx_ii_binTuple[2] == idx_state_i_binTuple[2]) and (idx_ii_binTuple[3] == idx_state_i_binTuple[1])):
                    matrixBTr_rowList.append(1)
                else:
                    matrixBTr_rowList.append(0)

                if ((idx_ii_binTuple[4] == idx_state_i_binTuple[4]) and (idx_ii_binTuple[5] == idx_state_i_binTuple[3])):
                    matrixCTr_rowList.append(1)
                else:
                    matrixCTr_rowList.append(0)

            matrixC_A_tr.append(copy.deepcopy(matrixATr_rowList))
            matrixC_B_tr.append(copy.deepcopy(matrixBTr_rowList))
            matrixC_C_tr.append(copy.deepcopy(matrixCTr_rowList))

        matrixC_A = []
        matrixC_B = []
        matrixC_C = []
        for idx_row_i in range(0, 64):
            matrixCA_rowList = []
            matrixCB_rowList = []
            matrixCC_rowList = []
            for idx_col_i in range(0, 64):
                matrixCA_rowList.append(copy.deepcopy(matrixC_A_tr[idx_col_i][idx_row_i]))
                matrixCB_rowList.append(copy.deepcopy(matrixC_B_tr[idx_col_i][idx_row_i]))
                matrixCC_rowList.append(copy.deepcopy(matrixC_C_tr[idx_col_i][idx_row_i]))

            matrixCA_rowTuple = tuple(matrixCA_rowList)
            matrixCB_rowTuple = tuple(matrixCB_rowList)
            matrixCC_rowTuple = tuple(matrixCC_rowList)

            matrixC_A.append(copy.deepcopy(matrixCA_rowTuple))
            matrixC_B.append(copy.deepcopy(matrixCB_rowTuple))
            matrixC_C.append(copy.deepcopy(matrixCC_rowTuple))

        matrixC_A_tuple = tuple(matrixC_A)
        matrixC_B_tuple = tuple(matrixC_B)
        matrixC_C_tuple = tuple(matrixC_C)

        return matrixC_A_tuple, matrixC_B_tuple, matrixC_C_tuple













    def calcMuASimplified_useMatrixCQ_main(self, constraintSet = 'full'):
        '''
        Calc \mu_a.
        :return:
        '''

        assert constraintSet in ('full', 'basic')

        # Get Matrix C
        print("Calculating Matrix C...")
        param_matrixC_A, param_matrixC_B, param_matrixC_C = self._calcMuA_subtask_getMatrixC()
        assert len(param_matrixC_A) == 64
        assert len(param_matrixC_B) == 64
        assert len(param_matrixC_C) == 64
        print("Matrix C-A, Matrix C-B &  Matrix C-C: ")
        for idx_i in range(0, 64):
            print("Row{}\t{}\t{}\t{}".format(idx_i, param_matrixC_A[idx_i], param_matrixC_B[idx_i], param_matrixC_C[idx_i]))

        # Get Matrix Q
        print("Calculating Matrix Q...")
        param_matrixQ_instance = self._calcMuA_subtask_getMatrixQ()
        param_matrixQ = param_matrixQ_instance.getMatrix_all()
        assert len(param_matrixQ) == 64
        print("Matrix Q: ")
        for idx_i in range(0, 64):
            print("Row{}\t{}".format(idx_i, param_matrixQ[idx_i]))


        print("#######################################################################################################")
        print("#######################################################################################################")
        print("Create Z3-Solver Instance...")
        z3Solver_instance = _Z3Solver_forMuACalc_Simplfied_useMatrixCQ(matrix_C_b16=copy.deepcopy(param_matrixC_A),
                                                                       matrix_C_b32=copy.deepcopy(param_matrixC_B),
                                                                       matrix_C_b54=copy.deepcopy(param_matrixC_C),
                                                                       matrix_Q=copy.deepcopy(param_matrixQ))
        print("Add Constraint ({})...".format(constraintSet))
        if constraintSet == 'full':
            z3Solver_instance.addConstraint_full()
        elif constraintSet == 'basic':
            z3Solver_instance.addConstraint_basic()

        z3Solver_instance.checkSolver()

        solutionModel_instance = z3Solver_instance.getSolutionModel()
        for modelVar_d in solutionModel_instance.decls():
            print(modelVar_d.name(), '=\t', solutionModel_instance[modelVar_d])

        return z3Solver_instance







########################################################################################################################
### class BitStuffingCAC_Simulation_HexArray
########################################################################################################################
###
###
###
########################################################################################################################
class BitStuffingCAC_Simulation_HexArray:
    def __init__(self, arrayType, additionParamsTuple = None):
        self._flag_arrayLocked = False
        self._initialize_codec()

        if arrayType == "Hex_RegularA_9x6":
            self._createHexArray_regularA_9x6()
        elif arrayType == 'Hex_RegularA_12x6':
            self._createHexArray_regularA_12x6()
        elif arrayType == 'Hex_RegularB_11x9':
            self._createHexArray_regularB_11x9()
        elif arrayType == 'Hex_RegularA_12x9':
            self._createHexArray_regularA_12x9()
        elif arrayType == 'Hex_RegularA_13x9':
            self._createHexArray_regularA_13x9()
        elif arrayType == 'Hex_RegularA_18x9':
            self._createHexArray_regularA_18x9()
        elif arrayType == 'Hex_RegularA_18x12':
            self._createHexArray_regularA_18x12()
        elif arrayType == 'HexArrayAuto_regularA_6m_x_3n':
            assert isinstance(additionParamsTuple, tuple)
            assert len(additionParamsTuple) == 2
            self._createHexArrayAuto_regularA_6m_x_3n(m=copy.deepcopy(additionParamsTuple[0]),
                                                      n=copy.deepcopy(additionParamsTuple[1]))

        else:
            assert False

        self.resetCurrentState()
        self._check_dyShieldingTopo()


    ####################################################################################################################
    def resetCurrentState(self):
        self._stateList_signalBits_current = copy.deepcopy(self._stateList_signalBits_init)
        self._stateList_dyShieldingType1_current = copy.deepcopy(self._stateList_dyShieldingType1_init)
        self._stateList_dyShieldingType2_current = copy.deepcopy(self._stateList_dyShieldingType2_init)
        self._stateList_dyShieldingType3_current = copy.deepcopy(self._stateList_dyShieldingType3_init)




    ####################################################################################################################
    def _initialize_codec(self):
        timestamp_int = int(time.time())
        self._codecInstance_BSCAC_7bit = BitStuffingCAC_Codec.BSCAC_ForHexDyS2C_2CSupFor7bitGroup_Main(instance_id=copy.deepcopy(timestamp_int))

    ####################################################################################################################
    def get_dyShieldingType1_topoTuple(self):
        return copy.deepcopy(self._topoTuple_dyShieldingType1)

    ####################################################################################################################
    def get_dyShieldingType2_topoTuple(self):
        return copy.deepcopy(self._topoTuple_dyShieldingType2)

    ####################################################################################################################
    def get_dyShieldingType3_topoTuple(self):
        return copy.deepcopy(self._topoTuple_dyShieldingType3)

    ####################################################################################################################
    def get_dyShieldingType1_unconstraintBitsTuple(self):
        return copy.deepcopy(self._unconstraintBitsTuple_dyShieldingType1)

    ####################################################################################################################
    def get_dyShieldingType2_unconstraintBitsTuple(self):
        return copy.deepcopy(self._unconstraintBitsTuple_dyShieldingType2)

    ####################################################################################################################
    def get_dyShieldingType3_unconstraintBitsTuple(self):
        return copy.deepcopy(self._unconstraintBitsTuple_dyShieldingType3)

    ####################################################################################################################
    def get_dyShieldingType1_initState(self):
        return copy.deepcopy(self._stateList_dyShieldingType1_init)

    ####################################################################################################################
    def get_dyShieldingType2_initState(self):
        return copy.deepcopy(self._stateList_dyShieldingType2_init)

    ####################################################################################################################
    def get_dyShieldingType3_initState(self):
        return copy.deepcopy(self._stateList_dyShieldingType3_init)

    ####################################################################################################################
    def get_dyShieldingType1_currentState(self):
        return copy.deepcopy(self._stateList_dyShieldingType1_current)

    ####################################################################################################################
    def get_dyShieldingType2_currentState(self):
        return copy.deepcopy(self._stateList_dyShieldingType2_current)

    ####################################################################################################################
    def get_dyShieldingType3_currentState(self):
        return copy.deepcopy(self._stateList_dyShieldingType3_current)

    ####################################################################################################################
    def get_nDyShType1_notVirtual(self):
        '''

        :return:
        '''
        return copy.deepcopy(self._arrayTopo_nDySh1_notVirtual)

    ####################################################################################################################
    def get_nDyShType2_notVirtual(self):
        '''

        :return:
        '''
        return copy.deepcopy(self._arrayTopo_nDySh2_notVirtual)

    ####################################################################################################################
    def get_nDyShType3_notVirtual(self):
        '''

        :return:
        '''
        return copy.deepcopy(self._arrayTopo_nDySh3_notVirtual)

    ####################################################################################################################
    def updateState_dyShieldingType1(self, newState_list):
        '''
        Update the state of the dyShieldingType1.
        The element \in {0, 1, None},
        in which 'None' represents 'No Change'.
        The state of virtual bit CANNOT be modified!
        :param newState_list:
        :return:
        '''
        assert isinstance(newState_list, list)
        oldState_list = self.get_dyShieldingType1_currentState()
        newState_list_copy = copy.deepcopy(newState_list)
        assert len(newState_list_copy) == len(oldState_list)

        for idx_state_i in range(0, len(oldState_list)):
            if newState_list_copy[idx_state_i] is None:
                newState_list_copy[idx_state_i] = copy.deepcopy(oldState_list[idx_state_i])
            else:
                assert newState_list_copy[idx_state_i] in (0, 1)
                assert oldState_list[idx_state_i] in (0, 1)


        self._stateList_dyShieldingType1_current = copy.deepcopy(newState_list_copy)


    ####################################################################################################################
    def updateState_dyShieldingType2(self, newState_list):
        '''
        Update the state of the dyShieldingType2.
        The element \in {0, 1, None},
        in which 'None' represents 'No Change'.
        The state of virtual bit CANNOT be modified!
        :param newState_list:
        :return:
        '''
        assert isinstance(newState_list, list)
        oldState_list = self.get_dyShieldingType2_currentState()
        newState_list_copy = copy.deepcopy(newState_list)
        assert len(newState_list_copy) == len(oldState_list)

        for idx_state_i in range(0, len(oldState_list)):
            if newState_list_copy[idx_state_i] is None:
                newState_list_copy[idx_state_i] = copy.deepcopy(oldState_list[idx_state_i])
            else:
                assert newState_list_copy[idx_state_i] in (0, 1)
                assert oldState_list[idx_state_i] in (0, 1)

        self._stateList_dyShieldingType2_current = copy.deepcopy(newState_list_copy)

    ####################################################################################################################
    def updateState_dyShieldingType3(self, newState_list):
        '''
        Update the state of the dyShieldingType3.
        The element \in {0, 1, None},
        in which 'None' represents 'No Change'.
        The state of virtual bit CANNOT be modified!
        :param newState_list:
        :return:
        '''
        assert isinstance(newState_list, list)
        oldState_list = self.get_dyShieldingType3_currentState()
        newState_list_copy = copy.deepcopy(newState_list)
        assert len(newState_list_copy) == len(oldState_list)

        for idx_state_i in range(0, len(oldState_list)):
            if newState_list_copy[idx_state_i] is None:
                newState_list_copy[idx_state_i] = copy.deepcopy(oldState_list[idx_state_i])
            else:
                assert newState_list_copy[idx_state_i] in (0, 1)
                assert oldState_list[idx_state_i] in (0, 1)

        self._stateList_dyShieldingType3_current = copy.deepcopy(newState_list_copy)

    ####################################################################################################################
    def get_signalBits_initState(self):
        return copy.deepcopy(self._stateList_signalBits_init)

    ####################################################################################################################
    def get_signalBits_currentState(self):
        return copy.deepcopy(self._stateList_signalBits_current)

    ####################################################################################################################
    def updateState_signalBits(self, newState_list):
        '''
        Update the state of the signal bits.
        The element \in {0, 1, None},
        in which 'None' represents 'No Change'.
        :param newState_list:
        :return:
        '''
        assert isinstance(newState_list, list)
        oldState_list = self.get_signalBits_currentState()
        newState_list_copy = copy.deepcopy(newState_list)
        assert len(newState_list_copy) == len(oldState_list)

        for idx_state_i in range(0, len(oldState_list)):
            if newState_list_copy[idx_state_i] is None:
                newState_list_copy[idx_state_i] = copy.deepcopy(oldState_list[idx_state_i])
            else:
                assert idx_state_i in (0, 1)

        self._stateList_signalBits_current = copy.deepcopy(newState_list_copy)

    ####################################################################################################################
    def updateState_signalBits_modifySingleBit(self, bitIdx, bitNewState):
        '''
        Update the state of ONE signal bit.
        The element \in {0, 1, None},
        in which 'None' represents 'No Change'.
        :param bitIdx:
        :param bitNewState:
        :return:
        '''
        assert isinstance(bitIdx, int)
        assert bitIdx >= 0
        assert self.get_signalBits_currentState()[bitIdx] in (0, 1)
        if bitNewState in (0, 1):
            self._stateList_signalBits_current[bitIdx] = copy.deepcopy(bitNewState)
        else:
            assert bitNewState is None


    ####################################################################################################################
    def get_state_virtualBit(self):
        return copy.deepcopy(self._state_virtualBit)

    ####################################################################################################################
    def _check_dyShieldingTopo(self):
        '''
        Make sure the state lists and topo tuples are defined completely and correctly.

        :return:
        '''
        signal_currentState = self.get_signalBits_initState()

        for typeX in (1, 2, 3):
            # Type 1
            if typeX == 1:
                dyshTypeX_currentStates = self.get_dyShieldingType1_initState()
                dyshTypeX_topoTuple = self.get_dyShieldingType1_topoTuple()
                dyshTypeX_unconstraintBits = self.get_dyShieldingType1_unconstraintBitsTuple()

            # Type 2
            elif typeX == 2:
                dyshTypeX_currentStates = self.get_dyShieldingType2_initState()
                dyshTypeX_topoTuple = self.get_dyShieldingType2_topoTuple()
                dyshTypeX_unconstraintBits = self.get_dyShieldingType2_unconstraintBitsTuple()

            # Type 3
            elif typeX == 3:
                dyshTypeX_currentStates = self.get_dyShieldingType3_initState()
                dyshTypeX_topoTuple = self.get_dyShieldingType3_topoTuple()
                dyshTypeX_unconstraintBits = self.get_dyShieldingType3_unconstraintBitsTuple()

            else:
                assert False

            assert len(dyshTypeX_currentStates) == len(dyshTypeX_topoTuple)

            boolList_traverseSignalBits = len(signal_currentState) * [False]

            for topoTuple_i in dyshTypeX_topoTuple:
                assert len(topoTuple_i) == 6
                for bitIdx_iii in topoTuple_i:
                    if isinstance(bitIdx_iii, int):
                        assert bitIdx_iii >= 0
                        assert bitIdx_iii < len(signal_currentState)
                        assert boolList_traverseSignalBits[bitIdx_iii] is False
                        boolList_traverseSignalBits[bitIdx_iii] = True
                    else:
                        assert bitIdx_iii is None
            for bitIdx_iii in dyshTypeX_unconstraintBits:
                assert bitIdx_iii >= 0
                assert bitIdx_iii < len(signal_currentState)
                assert boolList_traverseSignalBits[bitIdx_iii] is False
                boolList_traverseSignalBits[bitIdx_iii] = True

            for bool_i in boolList_traverseSignalBits:
                assert bool_i is True

        # Virtual dysh must be at the tail of list
        dyshType1_currentStates = self.get_dyShieldingType1_currentState()
        dyshType2_currentStates = self.get_dyShieldingType2_currentState()
        dyshType3_currentStates = self.get_dyShieldingType3_currentState()

        dyshType1_initStates = self.get_dyShieldingType1_initState()
        dyshType2_initStates = self.get_dyShieldingType2_initState()
        dyshType3_initStates = self.get_dyShieldingType3_initState()

        assert len(dyshType1_currentStates) == len(dyshType1_initStates)
        assert len(dyshType2_currentStates) == len(dyshType2_initStates)
        assert len(dyshType3_currentStates) == len(dyshType3_initStates)
        for idx_check_temp_iii in range(0, len(dyshType1_currentStates)):
            assert dyshType1_currentStates[idx_check_temp_iii] == dyshType1_initStates[idx_check_temp_iii]
            if idx_check_temp_iii < self.get_nDyShType1_notVirtual():
                assert dyshType1_currentStates[idx_check_temp_iii] in (0, 1)
            else:
                assert dyshType1_currentStates[idx_check_temp_iii] is None

        for idx_check_temp_iii in range(0, len(dyshType2_currentStates)):
            assert dyshType2_currentStates[idx_check_temp_iii] == dyshType2_initStates[idx_check_temp_iii]
            if idx_check_temp_iii < self.get_nDyShType2_notVirtual():
                assert dyshType2_currentStates[idx_check_temp_iii] in (0, 1)
            else:
                assert dyshType2_currentStates[idx_check_temp_iii] is None

        for idx_check_temp_iii in range(0, len(dyshType3_currentStates)):
            assert dyshType3_currentStates[idx_check_temp_iii] == dyshType3_initStates[idx_check_temp_iii]
            if idx_check_temp_iii < self.get_nDyShType3_notVirtual():
                assert dyshType3_currentStates[idx_check_temp_iii] in (0, 1)
            else:
                assert dyshType3_currentStates[idx_check_temp_iii] is None

    ####################################################################################################################
    ####################################################################################################################
    # Array

    ####################################################################################################################
    def _createHexArray_regularA_9x6(self):
        '''
        See " ./Docs/BitStuffingCAC_Arrays/ "

        :param n_shieldingRow:
        :param n_shieldingCol:
        :return:
        '''
        assert self._flag_arrayLocked is False
        self._flag_arrayLocked = True

        # State of virtual bit
        self._state_virtualBit = 0

        # Init states of signal bits
        # State: 0 / 1
        self._stateList_signalBits_init = 18 * [0]

        # self._stateList_signalBits_current = 36 * [0]

        # Init states of dy-shielding bits (including the virtual dy-shielding bits)
        # The virtual bits MUST be at the TAIL of the tuple !!!
        # The state of virtual bits MUST be 'None' !!!
        # State: 0 /1 /None
        self._stateList_dyShieldingType1_init = 3 * [0]
        self._stateList_dyShieldingType2_init = 3 * [0]
        self._stateList_dyShieldingType3_init = 3 * [0]

        self._arrayTopo_nDySh1_notVirtual = 3
        self._arrayTopo_nDySh2_notVirtual = 3
        self._arrayTopo_nDySh3_notVirtual = 3

        # self._stateList_dyShieldingType1_current = 6 * [0]
        # self._stateList_dyShieldingType2_current = 6 * [0]
        # self._stateList_dyShieldingType3_current = 6 * [0]

        # The adjacent bits of each dy-shielding bit, and the bits that are unconstrained.
        # The element are the idx of signal bits.
        # The idx of virtual bits MUST be 'None' !!!
        # The adjacent bits tuple of each dy-shielding bit MUST be ranked by encoding order !!!
        # The order of each encoding circle are specified by the figures in " ./Docs/BitStuffingCAC_Arrays/xxx.png ".
        self._topoTuple_dyShieldingType1 = ((4, 1, 0, None, 6, 7),
                                            (None, 3, 2, 5, 8, 9),
                                            (14, 11, 10, 13, 16, 17))
        self._unconstraintBitsTuple_dyShieldingType1 = (12, 15)

        self._topoTuple_dyShieldingType2 = ((4, 5, 2, None, None, 1),
                                            (12, 13, 10, 7, 6, None),
                                            (14, 15, None, 9, 8, 11))
        self._unconstraintBitsTuple_dyShieldingType2 = (0, 3, 16, 17)

        self._topoTuple_dyShieldingType3 = ((4, 7, 10, 11, 8, 5),
                                            (12, None, None, None, 16, 13),
                                            (14, 17, None, None, None, 15))
        self._unconstraintBitsTuple_dyShieldingType3 = (0, 1, 2, 3, 6, 9)

    ####################################################################################################################
    def _createHexArray_regularA_12x6(self):
        '''
        See " ./Docs/BitStuffingCAC_Arrays/ "

        :param n_shieldingRow:
        :param n_shieldingCol:
        :return:
        '''
        assert self._flag_arrayLocked is False
        self._flag_arrayLocked = True

        # State of virtual bit
        self._state_virtualBit = 0

        # Init states of signal bits
        # State: 0 / 1
        self._stateList_signalBits_init = 24 * [0]

        # self._stateList_signalBits_current = 36 * [0]

        # Init states of dy-shielding bits (including the virtual dy-shielding bits)
        # The virtual bits MUST be at the TAIL of the tuple !!!
        # The state of virtual bits MUST be 'None' !!!
        # State: 0 /1 /None
        self._stateList_dyShieldingType1_init = 4 * [0]
        self._stateList_dyShieldingType2_init = 4 * [0]
        self._stateList_dyShieldingType3_init = 4 * [0]

        self._arrayTopo_nDySh1_notVirtual = 4
        self._arrayTopo_nDySh2_notVirtual = 4
        self._arrayTopo_nDySh3_notVirtual = 4

        # self._stateList_dyShieldingType1_current = 6 * [0]
        # self._stateList_dyShieldingType2_current = 6 * [0]
        # self._stateList_dyShieldingType3_current = 6 * [0]

        # The adjacent bits of each dy-shielding bit, and the bits that are unconstrained.
        # The element are the idx of signal bits.
        # The idx of virtual bits MUST be 'None' !!!
        # The adjacent bits tuple of each dy-shielding bit MUST be ranked by encoding order !!!
        # The order of each encoding circle are specified by the figures in " ./Docs/BitStuffingCAC_Arrays/xxx.png ".
        self._topoTuple_dyShieldingType1 = ((4, 1, 0, None, 8, 9),
                                            (6, 3, 2, 5, 10, 11),
                                            (18, 13, 12, 17, 20, 21),
                                            (None, 15, 14, 19, 22, 23))
        self._unconstraintBitsTuple_dyShieldingType1 = (7, 16)

        self._topoTuple_dyShieldingType2 = ((4, 5, 2, None, None, 1),
                                            (6, 7, None, None, None, 3),
                                            (16, 17, 12, 9, 8, None),
                                            (18, 19, 14, 11, 10, 13))
        self._unconstraintBitsTuple_dyShieldingType2 = (0, 15, 20, 21, 22, 23)

        self._topoTuple_dyShieldingType3 = ((4, 9, 12, 13, 10, 5),
                                            (6, 11, 14, 15, None, 7),
                                            (16, None, None, None, 20, 17),
                                            (18, 21, None, None, 22, 19))
        self._unconstraintBitsTuple_dyShieldingType3 = (0, 1, 2, 3, 8, 23)

    ####################################################################################################################
    def _createHexArray_regularB_11x9(self):
        '''
        See " ./Docs/BitStuffingCAC_Arrays/ "

        :param n_shieldingRow:
        :param n_shieldingCol:
        :return:
        '''
        assert self._flag_arrayLocked is False
        self._flag_arrayLocked = True

        # State of virtual bit
        self._state_virtualBit = 0

        # Init states of signal bits
        # State: 0 / 1
        self._stateList_signalBits_init = 36 * [0]

        # self._stateList_signalBits_current = 36 * [0]

        # Init states of dy-shielding bits (including the virtual dy-shielding bits)
        # The virtual bits MUST be at the TAIL of the tuple !!!
        # The state of virtual bits MUST be 'None' !!!
        # State: 0 /1 /None
        self._stateList_dyShieldingType1_init = 4 * [0] + 4 * [None]
        self._stateList_dyShieldingType2_init = 5 * [0] + 2 * [None]
        self._stateList_dyShieldingType3_init = 5 * [0] + 2 * [None]


        self._arrayTopo_nDySh1_notVirtual = 4
        self._arrayTopo_nDySh2_notVirtual = 5
        self._arrayTopo_nDySh3_notVirtual = 5

        # self._stateList_dyShieldingType1_current = 6 * [0]
        # self._stateList_dyShieldingType2_current = 6 * [0]
        # self._stateList_dyShieldingType3_current = 6 * [0]

        # The adjacent bits of each dy-shielding bit, and the bits that are unconstrained.
        # The element are the idx of signal bits.
        # The idx of virtual bits MUST be 'None' !!!
        # The adjacent bits tuple of each dy-shielding bit MUST be ranked by encoding order !!!
        # The order of each encoding circle are specified by the figures in " ./Docs/BitStuffingCAC_Arrays/xxx.png ".
        self._topoTuple_dyShieldingType1 = ((6, 2, 1, 5, 9, 10),
                                            (17, 13, 12, 16, 20, 21),
                                            (19, 15, 14, 18, 22, 23),
                                            (30, 26, 25, 29, 33, 34),
                                            (4, 0, None, None, None, 8),
                                            (None, None, 3, 7, 11, None),
                                            (28, 24, None, None, None, 32),
                                            (None, None, 27, 31, 35, None))
        self._unconstraintBitsTuple_dyShieldingType1 = ()

        self._topoTuple_dyShieldingType2 = ((4, 5, 1, None, None, 0),
                                            (6, 7, 3, None, None, 2),
                                            (17, 18, 14, 10, 9, 13),
                                            (28, 29, 25, 21, 20, 24),
                                            (30, 31, 27, 23, 22, 26),
                                            (None, 16, 12, 8, None, None),
                                            (19, None, None, None, 11, 15))
        self._unconstraintBitsTuple_dyShieldingType2 = (32, 33, 34, 35)

        self._topoTuple_dyShieldingType3 = ((4, 8, 12, 13, 9, 5),
                                            (6, 10, 14, 15, 11, 7),
                                            (17, 21, 25, 26, 22, 18),
                                            (28, 32, None, None, 33, 29),
                                            (30, 34, None, None, 35, 31),
                                            (None, None, None, 24, 20, 16),
                                            (19, 23, 27, None, None, None))
        self._unconstraintBitsTuple_dyShieldingType3 = (0, 1, 2, 3)

    ####################################################################################################################
    def _createHexArray_regularA_12x9(self):
        '''
        See " ./Docs/BitStuffingCAC_Arrays/ "

        :param n_shieldingRow:
        :param n_shieldingCol:
        :return:
        '''
        assert self._flag_arrayLocked is False
        self._flag_arrayLocked = True

        # State of virtual bit
        self._state_virtualBit = 0

        # Init states of signal bits
        # State: 0 / 1
        self._stateList_signalBits_init = 36 * [0]

        # self._stateList_signalBits_current = 36 * [0]

        # Init states of dy-shielding bits (including the virtual dy-shielding bits)
        # The virtual bits MUST be at the TAIL of the tuple !!!
        # The state of virtual bits MUST be 'None' !!!
        # State: 0 /1 /None
        self._stateList_dyShieldingType1_init = 6 * [0]
        self._stateList_dyShieldingType2_init = 6 * [0]
        self._stateList_dyShieldingType3_init = 6 * [0]

        self._arrayTopo_nDySh1_notVirtual = 6
        self._arrayTopo_nDySh2_notVirtual = 6
        self._arrayTopo_nDySh3_notVirtual = 6

        # self._stateList_dyShieldingType1_current = 6 * [0]
        # self._stateList_dyShieldingType2_current = 6 * [0]
        # self._stateList_dyShieldingType3_current = 6 * [0]

        # The adjacent bits of each dy-shielding bit, and the bits that are unconstrained.
        # The element are the idx of signal bits.
        # The idx of virtual bits MUST be 'None' !!!
        # The adjacent bits tuple of each dy-shielding bit MUST be ranked by encoding order !!!
        # The order of each encoding circle are specified by the figures in " ./Docs/BitStuffingCAC_Arrays/xxx.png ".
        self._topoTuple_dyShieldingType1 = ((4, 1, 0, None, 8, 9),
                                            (6, 3, 2, 5, 10, 11),
                                            (18, 13, 12, 17, 20, 21),
                                            (None, 15, 14, 19, 22, 23),
                                            (28, 25, 24, None, 32, 33),
                                            (30, 27, 26, 29, 34, 35))
        self._unconstraintBitsTuple_dyShieldingType1 = (7, 16, 31)

        self._topoTuple_dyShieldingType2 = ((4, 5, 2, None, None, 1),
                                            (6, 7, None, None, None, 3),
                                            (16, 17, 12, 9, 8, None),
                                            (18, 19, 14, 11, 10, 13),
                                            (28, 29, 26, 21, 20, 25),
                                            (30, 31, None, 23, 22, 27))
        self._unconstraintBitsTuple_dyShieldingType2 = (0, 15, 24, 32, 33, 34, 35)

        self._topoTuple_dyShieldingType3 = ((4, 9, 12, 13, 10, 5),
                                            (6, 11, 14, 15, None, 7),
                                            (16, None, 24, 25, 20, 17),
                                            (18, 21, 26, 27, 22, 19),
                                            (28, 33, None, None, 34, 29),
                                            (30, 35, None, None, None, 31))
        self._unconstraintBitsTuple_dyShieldingType3 = (0, 1, 2, 3, 8, 23, 32)

    ####################################################################################################################
    def _createHexArray_regularA_13x9(self):
        '''
        See " ./Docs/BitStuffingCAC_Arrays/ "

        :param n_shieldingRow:
        :param n_shieldingCol:
        :return:
        '''
        assert self._flag_arrayLocked is False
        self._flag_arrayLocked = True

        # State of virtual bit
        self._state_virtualBit = 0

        # Init states of signal bits
        # State: 0 / 1
        self._stateList_signalBits_init = 41 * [0]

        # self._stateList_signalBits_current = 36 * [0]

        # Init states of dy-shielding bits (including the virtual dy-shielding bits)
        # The virtual bits MUST be at the TAIL of the tuple !!!
        # The state of virtual bits MUST be 'None' !!!
        # State: 0 /1 /None
        self._stateList_dyShieldingType1_init = 6 * [0] + 2 * [None]
        self._stateList_dyShieldingType2_init = 6 * [0] + 1 * [None]
        self._stateList_dyShieldingType3_init = 6 * [0] + 1 * [None]

        self._arrayTopo_nDySh1_notVirtual = 6
        self._arrayTopo_nDySh2_notVirtual = 6
        self._arrayTopo_nDySh3_notVirtual = 6

        # self._stateList_dyShieldingType1_current = 6 * [0]
        # self._stateList_dyShieldingType2_current = 6 * [0]
        # self._stateList_dyShieldingType3_current = 6 * [0]

        # The adjacent bits of each dy-shielding bit, and the bits that are unconstrained.
        # The element are the idx of signal bits.
        # The idx of virtual bits MUST be 'None' !!!
        # The adjacent bits tuple of each dy-shielding bit MUST be ranked by encoding order !!!
        # The order of each encoding circle are specified by the figures in " ./Docs/BitStuffingCAC_Arrays/xxx.png ".
        self._topoTuple_dyShieldingType1 = ((5, 1, 0, None, 9, 10),
                                            (7, 3, 2, 6, 11, 12),
                                            (20, 15, 14, 19, 23, 24),
                                            (22, 17, 16, 21, 25, 26),
                                            (32, 28, 27, None, 36, 37),
                                            (34, 30, 29, 33, 38, 39),
                                            (None, None, 4, 8, 13, None),
                                            (None, None, 31, 35, 40, None))
        self._unconstraintBitsTuple_dyShieldingType1 = (18,)

        self._topoTuple_dyShieldingType2 = ((5, 6, 2, None, None, 1),
                                            (7, 8, 4, None, None, 3),
                                            (18, 19, 14, 10, 9, None),
                                            (20, 21, 16, 12, 11, 15),
                                            (32, 33, 29, 24, 23, 28),
                                            (34, 35, 31, 26, 25, 30),
                                            (22, None, None, None, 13, 17))
        self._unconstraintBitsTuple_dyShieldingType2 = (0, 27, 36, 37, 38, 39, 40)

        self._topoTuple_dyShieldingType3 = ((5, 10, 14, 15, 11, 6),
                                            (7, 12, 16, 17, 13, 8),
                                            (18, None, 27, 28, 23, 19),
                                            (20, 24, 29, 30, 25, 21),
                                            (32, 37, None, None, 38, 33),
                                            (34, 39, None, None, 40, 35),
                                            (22, 26, 31, None, None, None))
        self._unconstraintBitsTuple_dyShieldingType3 = (0, 1, 2, 3, 4, 9, 36)

    ####################################################################################################################
    def _createHexArray_regularA_18x9(self):
        '''
        See " ./Docs/BitStuffingCAC_Arrays/ "

        :param n_shieldingRow:
        :param n_shieldingCol:
        :return:
        '''
        assert self._flag_arrayLocked is False
        self._flag_arrayLocked = True

        # State of virtual bit
        self._state_virtualBit = 0

        # Init states of signal bits
        # State: 0 / 1
        self._stateList_signalBits_init = 54 * [0]

        # self._stateList_signalBits_current = 36 * [0]

        # Init states of dy-shielding bits (including the virtual dy-shielding bits)
        # The virtual bits MUST be at the TAIL of the tuple !!!
        # The state of virtual bits MUST be 'None' !!!
        # State: 0 /1 /None
        self._stateList_dyShieldingType1_init = 9 * [0]
        self._stateList_dyShieldingType2_init = 9 * [0]
        self._stateList_dyShieldingType3_init = 9 * [0]

        self._arrayTopo_nDySh1_notVirtual = 9
        self._arrayTopo_nDySh2_notVirtual = 9
        self._arrayTopo_nDySh3_notVirtual = 9

        # self._stateList_dyShieldingType1_current = 6 * [0]
        # self._stateList_dyShieldingType2_current = 6 * [0]
        # self._stateList_dyShieldingType3_current = 6 * [0]

        # The adjacent bits of each dy-shielding bit, and the bits that are unconstrained.
        # The element are the idx of signal bits.
        # The idx of virtual bits MUST be 'None' !!!
        # The adjacent bits tuple of each dy-shielding bit MUST be ranked by encoding order !!!
        # The order of each encoding circle are specified by the figures in " ./Docs/BitStuffingCAC_Arrays/xxx.png ".
        self._topoTuple_dyShieldingType1 = ((6, 1, 0, None, 12, 13),
                                            (8, 3, 2, 7, 14, 15),
                                            (10, 5, 4, 9, 16, 17),
                                            (26, 19, 18, 25, 30, 31),
                                            (28, 21, 20, 27, 32, 33),
                                            (None, 23, 22, 29, 34, 35),
                                            (42, 37, 36, None, 48, 49),
                                            (44, 39, 38, 43, 50, 51),
                                            (46, 41, 40, 45, 52, 53))
        self._unconstraintBitsTuple_dyShieldingType1 = (11, 24, 47)

        self._topoTuple_dyShieldingType2 = ((6, 7, 2, None, None, 1),
                                            (8, 9, 4, None, None, 3),
                                            (10, 11, None, None, None, 5),
                                            (24, 25, 18, 13, 12, None),
                                            (26, 27, 20, 15, 14, 19),
                                            (28, 29, 22, 17, 16, 21),
                                            (42, 43, 38, 31, 30, 37),
                                            (44, 45, 40, 33, 32, 39),
                                            (46, 47, None, 35, 34, 41))
        self._unconstraintBitsTuple_dyShieldingType2 = (0, 23, 36, 48, 49, 50, 51, 52, 53)

        self._topoTuple_dyShieldingType3 = ((6, 13, 18, 19, 14, 7),
                                            (8, 15, 20, 21, 16, 9),
                                            (10, 17, 22, 23, None, 11),
                                            (24, None, 36, 37, 30, 25),
                                            (26, 31, 38, 39, 32, 27),
                                            (28, 33, 40, 41, 34, 29),
                                            (42, 49, None, None, 50, 43),
                                            (44, 51, None, None, 52, 45),
                                            (46, 53, None, None, None, 47))
        self._unconstraintBitsTuple_dyShieldingType3 = (0, 1, 2, 3, 4, 5, 12, 35, 48)

    ####################################################################################################################
    def _createHexArray_regularA_18x12(self):
        '''
        See " ./Docs/BitStuffingCAC_Arrays/ "

        :param n_shieldingRow:
        :param n_shieldingCol:
        :return:
        '''
        assert self._flag_arrayLocked is False
        self._flag_arrayLocked = True

        # State of virtual bit
        self._state_virtualBit = 0

        # Init states of signal bits
        # State: 0 / 1
        self._stateList_signalBits_init = 72 * [0]

        # self._stateList_signalBits_current = 36 * [0]

        # Init states of dy-shielding bits (including the virtual dy-shielding bits)
        # The virtual bits MUST be at the TAIL of the tuple !!!
        # The state of virtual bits MUST be 'None' !!!
        # State: 0 /1 /None
        self._stateList_dyShieldingType1_init = 12 * [0]
        self._stateList_dyShieldingType2_init = 12 * [0]
        self._stateList_dyShieldingType3_init = 12 * [0]

        self._arrayTopo_nDySh1_notVirtual = 12
        self._arrayTopo_nDySh2_notVirtual = 12
        self._arrayTopo_nDySh3_notVirtual = 12

        # self._stateList_dyShieldingType1_current = 6 * [0]
        # self._stateList_dyShieldingType2_current = 6 * [0]
        # self._stateList_dyShieldingType3_current = 6 * [0]

        # The adjacent bits of each dy-shielding bit, and the bits that are unconstrained.
        # The element are the idx of signal bits.
        # The idx of virtual bits MUST be 'None' !!!
        # The adjacent bits tuple of each dy-shielding bit MUST be ranked by encoding order !!!
        # The order of each encoding circle are specified by the figures in " ./Docs/BitStuffingCAC_Arrays/xxx.png ".
        self._topoTuple_dyShieldingType1 = ((6, 1, 0, None, 12, 13),
                                            (8, 3, 2, 7, 14, 15),
                                            (10, 5, 4, 9, 16, 17),
                                            (26, 19, 18, 25, 30, 31),
                                            (28, 21, 20, 27, 32, 33),
                                            (None, 23, 22, 29, 34, 35),
                                            (42, 37, 36, None, 48, 49),
                                            (44, 39, 38, 43, 50, 51),
                                            (46, 41, 40, 45, 52, 53),
                                            (62, 55, 54, 61, 66, 67),
                                            (64, 57, 56, 63, 68, 69),
                                            (None, 59, 58, 65, 70, 71))
        self._unconstraintBitsTuple_dyShieldingType1 = (11, 24, 47, 60)

        self._topoTuple_dyShieldingType2 = ((6, 7, 2, None, None, 1),
                                            (8, 9, 4, None, None, 3),
                                            (10, 11, None, None, None, 5),
                                            (24, 25, 18, 13, 12, None),
                                            (26, 27, 20, 15, 14, 19),
                                            (28, 29, 22, 17, 16, 21),
                                            (42, 43, 38, 31, 30, 37),
                                            (44, 45, 40, 33, 32, 39),
                                            (46, 47, None, 35, 34, 41),
                                            (60, 61, 54, 49, 48, None),
                                            (62, 63, 56, 51, 50, 55),
                                            (64, 65, 58, 53, 52, 57))
        self._unconstraintBitsTuple_dyShieldingType2 = (0, 23, 36, 59, 66, 67, 68, 69, 70, 71)

        self._topoTuple_dyShieldingType3 = ((6, 13, 18, 19, 14, 7),
                                            (8, 15, 20, 21, 16, 9),
                                            (10, 17, 22, 23, None, 11),
                                            (24, None, 36, 37, 30, 25),
                                            (26, 31, 38, 39, 32, 27),
                                            (28, 33, 40, 41, 34, 29),
                                            (42, 49, 54, 55, 50, 43),
                                            (44, 51, 56, 57, 52, 45),
                                            (46, 53, 58, 59, None, 47),
                                            (60, None, None, None, 66, 61),
                                            (62, 67, None, None, 68, 63),
                                            (64, 69, None, None, 70, 65))
        self._unconstraintBitsTuple_dyShieldingType3 = (0, 1, 2, 3, 4, 5, 12, 35, 48, 71)

    ####################################################################################################################
    def _createHexArrayAuto_regularA_6m_x_3n(self, m, n):
        '''
        Generate the HexArray_regularA topo with 6m rows & 3n cols.
        The examples of HexArray_regularA topo are in ' ./Docs/BitStuffingCAC_Arrays/ '.

        :param m:
        :param n:
        :return:
        '''
        print("RUN: _createHexArrayAuto_regularA_6m_x_3n - m={}, n={}".format(m, n))

        assert isinstance(m, int)
        assert isinstance(n, int)
        assert m >= 2
        assert n >= 2
        n_arrayRow = 6 * m
        n_arrayCol = 3 * n

        assert self._flag_arrayLocked is False
        self._flag_arrayLocked = True

        # State of virtual bit
        self._state_virtualBit = 0

        # Create topo list
        cntDict_n_dyshTypeX = {'s1': 0,
                               's2': 0,
                               's3': 0}
        cntInt_n_signalBits = 0
        topoList_2d_idxColRow = [] # topoList_2d_idxColRow[col_i][row_i] = bitIdx (int for signal bits, 's1', 's2', 's3' for dysh, and 'nothing' for nothing).
        signalBitIdx_nextOne = 0
        dyshType_currentCol = 's2'
        for idx_col_i in range(0, n_arrayCol):
            topoList_currentCol = []
            if (idx_col_i % 2) == 0:
                bitTypeNext_int = 1 # 0 - dysh, 1 & 2 - signal bit.
                for idx_row_i in range(0, n_arrayRow):
                    if (idx_row_i % 2) == 1:
                        topoList_currentCol.append('nothing')
                    elif (idx_row_i % 2) == 0:
                        if bitTypeNext_int == 0:
                            topoList_currentCol.append(copy.deepcopy(dyshType_currentCol))
                            cntDict_n_dyshTypeX[dyshType_currentCol] = cntDict_n_dyshTypeX[dyshType_currentCol] + 1
                        else:
                            assert bitTypeNext_int in (1, 2)
                            topoList_currentCol.append(copy.deepcopy(signalBitIdx_nextOne))
                            signalBitIdx_nextOne = signalBitIdx_nextOne + 1
                            cntInt_n_signalBits = cntInt_n_signalBits + 1
                        bitTypeNext_int = bitTypeNext_int + 1
                        if bitTypeNext_int == 3:
                            bitTypeNext_int = 0
                        else:
                            assert bitTypeNext_int in (1, 2)
                    else:
                        assert False

            elif (idx_col_i % 2) == 1:
                bitTypeNext_int = 0
                for idx_row_i in range(0, n_arrayRow):
                    if (idx_row_i % 2) == 0:
                        topoList_currentCol.append('nothing')
                    elif (idx_row_i % 2) == 1:
                        if bitTypeNext_int == 0:
                            topoList_currentCol.append(copy.deepcopy(dyshType_currentCol))
                            cntDict_n_dyshTypeX[dyshType_currentCol] = cntDict_n_dyshTypeX[dyshType_currentCol] + 1
                        else:
                            assert bitTypeNext_int in (1, 2)
                            topoList_currentCol.append(copy.deepcopy(signalBitIdx_nextOne))
                            signalBitIdx_nextOne = signalBitIdx_nextOne + 1
                            cntInt_n_signalBits = cntInt_n_signalBits + 1
                        bitTypeNext_int = bitTypeNext_int + 1
                        if bitTypeNext_int == 3:
                            bitTypeNext_int = 0
                        else:
                            assert bitTypeNext_int in (1, 2)
                    else:
                        assert False
            else:
                assert False

            # Store the col list
            topoList_2d_idxColRow.append(tuple(copy.deepcopy(topoList_currentCol)))

            # Update dysh Type
            if dyshType_currentCol == 's1':
                dyshType_currentCol = 's3'
            elif dyshType_currentCol == 's2':
                dyshType_currentCol = 's1'
            elif dyshType_currentCol == 's3':
                dyshType_currentCol = 's2'

        # for col_iiii in topoList_2d_idxColRow:
        #     print(col_iiii)
        topoTuple_2d_idxColRow = tuple(copy.deepcopy(topoList_2d_idxColRow))
        assert signalBitIdx_nextOne == cntInt_n_signalBits

        # Topo analyze
        ############################################################################
        # Init states of signal bits
        # State: 0 / 1
        self._stateList_signalBits_init = cntInt_n_signalBits * [0]
        print("--> nSignalBits: {}".format(cntInt_n_signalBits))

        # self._stateList_signalBits_current = 36 * [0]

        # Init states of dy-shielding bits (including the virtual dy-shielding bits)
        # The virtual bits MUST be at the TAIL of the tuple !!!
        # The state of virtual bits MUST be 'None' !!!
        # State: 0 /1 /None
        self._stateList_dyShieldingType1_init = cntDict_n_dyshTypeX['s1'] * [0]
        self._stateList_dyShieldingType2_init = cntDict_n_dyshTypeX['s2'] * [0]
        self._stateList_dyShieldingType3_init = cntDict_n_dyshTypeX['s3'] * [0]

        self._arrayTopo_nDySh1_notVirtual = copy.deepcopy(cntDict_n_dyshTypeX['s1'])
        self._arrayTopo_nDySh2_notVirtual = copy.deepcopy(cntDict_n_dyshTypeX['s2'])
        self._arrayTopo_nDySh3_notVirtual = copy.deepcopy(cntDict_n_dyshTypeX['s3'])

        # self._stateList_dyShieldingType1_current = 6 * [0]
        # self._stateList_dyShieldingType2_current = 6 * [0]
        # self._stateList_dyShieldingType3_current = 6 * [0]

        # The adjacent bits of each dy-shielding bit, and the bits that are unconstrained.
        # The element are the idx of signal bits.
        # The idx of virtual bits MUST be 'None' !!!
        # The adjacent bits tuple of each dy-shielding bit MUST be ranked by encoding order !!!
        # The order of each encoding circle are specified by the figures in " ./Docs/BitStuffingCAC_Arrays/xxx.png ".
        self._topoList_dyShieldingType1 = []
        self._unconstraintBitsList_dyShieldingType1 = []

        self._topoList_dyShieldingType2 = []
        self._unconstraintBitsList_dyShieldingType2 = []

        self._topoList_dyShieldingType3 = []
        self._unconstraintBitsList_dyShieldingType3 = []

        for idx_topoCol_k in range(0, n_arrayCol):
            for idx_topoRow_k in range(0, n_arrayRow):
                # signal bit
                if isinstance(topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k], int):
                    # Check if this signal bit has adjacent dysh type1/2/3.
                    flagBool_hasAdjacentDyshType1 = False
                    flagBool_hasAdjacentDyshType2 = False
                    flagBool_hasAdjacentDyshType3 = False
                    idxList_signalBitInArrayEdge = []
                    for temp_idxTuple_k in ((idx_topoCol_k, idx_topoRow_k - 2),
                                            (idx_topoCol_k, idx_topoRow_k + 2),
                                            (idx_topoCol_k - 1, idx_topoRow_k - 1),
                                            (idx_topoCol_k - 1, idx_topoRow_k + 1),
                                            (idx_topoCol_k + 1, idx_topoRow_k - 1),
                                            (idx_topoCol_k + 1, idx_topoRow_k + 1)):
                        if (temp_idxTuple_k[0] >= 0) and (temp_idxTuple_k[0] < n_arrayCol) and (temp_idxTuple_k[1] >= 0) and (temp_idxTuple_k[1] < n_arrayRow):
                            if topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]] == 's1':
                                flagBool_hasAdjacentDyshType1 = True
                            elif topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]] == 's2':
                                flagBool_hasAdjacentDyshType2 = True
                            elif topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]] == 's3':
                                flagBool_hasAdjacentDyshType3 = True
                            else:
                                assert (isinstance(topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]], int) or
                                        topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]] == 'nothing')
                        else:
                            if topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k] not in idxList_signalBitInArrayEdge:
                                idxList_signalBitInArrayEdge.append(copy.deepcopy(topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k]))

                    if flagBool_hasAdjacentDyshType1 is False:
                        self._unconstraintBitsList_dyShieldingType1.append(copy.deepcopy(topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k]))
                    else:
                        assert flagBool_hasAdjacentDyshType1 is True

                    if flagBool_hasAdjacentDyshType2 is False:
                        self._unconstraintBitsList_dyShieldingType2.append(copy.deepcopy(topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k]))
                    else:
                        assert flagBool_hasAdjacentDyshType2 is True

                    if flagBool_hasAdjacentDyshType3 is False:
                        self._unconstraintBitsList_dyShieldingType3.append(copy.deepcopy(topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k]))
                    else:
                        assert flagBool_hasAdjacentDyshType3 is True

                # dysh
                elif topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k] in ('s1', 's2', 's3'):
                    idxList_currentDyshAdjacent = []
                    if topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k] == 's1':
                        # d1 ~ d6
                        for temp_idxTuple_k in ((idx_topoCol_k, idx_topoRow_k + 2),
                                                (idx_topoCol_k - 1, idx_topoRow_k + 1),
                                                (idx_topoCol_k - 1, idx_topoRow_k - 1),
                                                (idx_topoCol_k, idx_topoRow_k - 2),
                                                (idx_topoCol_k + 1, idx_topoRow_k - 1),
                                                (idx_topoCol_k + 1, idx_topoRow_k + 1)):
                            # Virtual signal bits
                            if (temp_idxTuple_k[0] < 0) or (temp_idxTuple_k[0] >= n_arrayCol) or (temp_idxTuple_k[1] < 0) or (temp_idxTuple_k[1] >= n_arrayRow):
                                idxList_currentDyshAdjacent.append(None)
                            elif topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]] == 'nothing':
                                idxList_currentDyshAdjacent.append(None)
                                assert (temp_idxTuple_k[0] % 2) == 1
                                assert temp_idxTuple_k[1] in (1, (n_arrayRow - 2))
                            # Signal bits
                            elif isinstance(topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]], int):
                                idxList_currentDyshAdjacent.append(copy.deepcopy(topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]]))
                            # Each adjacent bit of dysh must be signal bit or virtual signal bit.
                            else:
                                assert False
                        idxTuple_currentDyshAdjacent = tuple(copy.deepcopy(idxList_currentDyshAdjacent))
                        self._topoList_dyShieldingType1.append(copy.deepcopy(idxTuple_currentDyshAdjacent))

                    elif topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k] == 's2':
                        # d1 ~ d6
                        for temp_idxTuple_k in ((idx_topoCol_k + 1, idx_topoRow_k - 1),
                                                (idx_topoCol_k + 1, idx_topoRow_k + 1),
                                                (idx_topoCol_k, idx_topoRow_k + 2),
                                                (idx_topoCol_k - 1, idx_topoRow_k + 1),
                                                (idx_topoCol_k - 1, idx_topoRow_k - 1),
                                                (idx_topoCol_k, idx_topoRow_k - 2)):
                            # Virtual signal bits
                            if (temp_idxTuple_k[0] < 0) or (temp_idxTuple_k[0] >= n_arrayCol) or (temp_idxTuple_k[1] < 0) or (temp_idxTuple_k[1] >= n_arrayRow):
                                idxList_currentDyshAdjacent.append(None)
                            elif topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]] == 'nothing':
                                idxList_currentDyshAdjacent.append(None)
                                assert (temp_idxTuple_k[0] % 2) == 1
                                assert temp_idxTuple_k[1] in (1, (n_arrayRow - 2))
                            # Signal bits
                            elif isinstance(topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]], int):
                                idxList_currentDyshAdjacent.append(copy.deepcopy(topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]]))
                            # Each adjacent bit of dysh must be signal bit or virtual signal bit.
                            else:
                                assert False
                        idxTuple_currentDyshAdjacent = tuple(copy.deepcopy(idxList_currentDyshAdjacent))
                        self._topoList_dyShieldingType2.append(copy.deepcopy(idxTuple_currentDyshAdjacent))

                    elif topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k] == 's3':
                        # d1 ~ d6
                        for temp_idxTuple_k in ((idx_topoCol_k - 1, idx_topoRow_k - 1),
                                                (idx_topoCol_k, idx_topoRow_k - 2),
                                                (idx_topoCol_k + 1, idx_topoRow_k - 1),
                                                (idx_topoCol_k + 1, idx_topoRow_k + 1),
                                                (idx_topoCol_k, idx_topoRow_k + 2),
                                                (idx_topoCol_k - 1, idx_topoRow_k + 1)):
                            # Virtual signal bits
                            if (temp_idxTuple_k[0] < 0) or (temp_idxTuple_k[0] >= n_arrayCol) or (temp_idxTuple_k[1] < 0) or (temp_idxTuple_k[1] >= n_arrayRow):
                                idxList_currentDyshAdjacent.append(None)
                            elif topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]] == 'nothing':
                                idxList_currentDyshAdjacent.append(None)
                                assert (temp_idxTuple_k[0] % 2) == 1
                                assert temp_idxTuple_k[1] in (1, (n_arrayRow - 2))
                            # Signal bits
                            elif isinstance(topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]], int):
                                idxList_currentDyshAdjacent.append(copy.deepcopy(topoTuple_2d_idxColRow[temp_idxTuple_k[0]][temp_idxTuple_k[1]]))
                            # Each adjacent bit of dysh must be signal bit or virtual signal bit.
                            else:
                                assert False
                        idxTuple_currentDyshAdjacent = tuple(copy.deepcopy(idxList_currentDyshAdjacent))
                        self._topoList_dyShieldingType3.append(copy.deepcopy(idxTuple_currentDyshAdjacent))

                    else:
                        assert False

                else:
                    assert topoTuple_2d_idxColRow[idx_topoCol_k][idx_topoRow_k] == 'nothing'

        self._topoTuple_dyShieldingType1 = tuple(copy.deepcopy(self._topoList_dyShieldingType1))
        self._unconstraintBitsTuple_dyShieldingType1 = tuple(copy.deepcopy(self._unconstraintBitsList_dyShieldingType1))

        self._topoTuple_dyShieldingType2 = tuple(copy.deepcopy(self._topoList_dyShieldingType2))
        self._unconstraintBitsTuple_dyShieldingType2 = tuple(copy.deepcopy(self._unconstraintBitsList_dyShieldingType2))

        self._topoTuple_dyShieldingType3 = tuple(copy.deepcopy(self._topoList_dyShieldingType3))
        self._unconstraintBitsTuple_dyShieldingType3 = tuple(copy.deepcopy(self._unconstraintBitsList_dyShieldingType3))

        print("--> topo-dysh1: {}".format(self._topoTuple_dyShieldingType1))
        print("--> topo-unconstraint1: {}".format(self._unconstraintBitsTuple_dyShieldingType1))
        print("--> topo-dysh2: {}".format(self._topoTuple_dyShieldingType2))
        print("--> topo-unconstraint2: {}".format(self._unconstraintBitsTuple_dyShieldingType2))
        print("--> topo-dysh3: {}".format(self._topoTuple_dyShieldingType3))
        print("--> topo-unconstraint3: {}".format(self._unconstraintBitsTuple_dyShieldingType3))
        print("--> dysh: {}".format(cntDict_n_dyshTypeX))







    ################################################################################################################
    ################################################################################################################
    # Data Generation Method
    ################################################################################################################
    def _dataGen_random(self, bitWidth):
        '''
        Return a tuple containing random binary bits.
        :param bitWidth:
        :return:
        '''
        assert isinstance(bitWidth, int)
        assert bitWidth > 0

        maxDecValue = (2 ** bitWidth) - 1
        randomDecInt = random.randint(0, maxDecValue)

        randomBit_tuple = BitStuffingCAC_Analyze_HexArray.tool_convert_int2BinTuple(input_int=randomDecInt,
                                                                                    n_bit=bitWidth,
                                                                                    msbFirst=True)

        return copy.deepcopy(randomBit_tuple)

    ################################################################################################################
    ################################################################################################################
    # Simulation
    ################################################################################################################
    def runSimu_threeClk(self, dataGenMethod):
        '''

        :param dataGenMethod:
        :return: dataGenCopy_data2bTrans_signalBits_3Clk, monitor_flagsBool_ifSignalBitTrans_3Clk, monitor_nTransmitted_signalBits, monitor_signalBitsState_3Clk, monitor_dysh1State, monitor_dysh2State, monitor_dysh3State
        '''
        # Generate data
        if dataGenMethod == 'random':
            dataGen_signalBitsTuple_01 = self._dataGen_random(bitWidth=len(self.get_signalBits_currentState()))
            dataGen_signalBitsTuple_02 = self._dataGen_random(bitWidth=len(self.get_signalBits_currentState()))
            dataGen_signalBitsTuple_03 = self._dataGen_random(bitWidth=len(self.get_signalBits_currentState()))

            dataGen_dyshBitsTuple_S1_temp = self._dataGen_random(bitWidth=self.get_nDyShType1_notVirtual())
            dataGen_dyshBitsTuple_S2_temp = self._dataGen_random(bitWidth=self.get_nDyShType2_notVirtual())
            dataGen_dyshBitsTuple_S3_temp = self._dataGen_random(bitWidth=self.get_nDyShType3_notVirtual())

            dataGen_dyshBitsList_S1_temp = list(dataGen_dyshBitsTuple_S1_temp)
            dataGen_dyshBitsList_S2_temp = list(dataGen_dyshBitsTuple_S2_temp)
            dataGen_dyshBitsList_S3_temp = list(dataGen_dyshBitsTuple_S3_temp)

            for idx_dyshType1_kkk in range(0, (len(self.get_dyShieldingType1_currentState()) - self.get_nDyShType1_notVirtual())):
                dataGen_dyshBitsList_S1_temp.append(None)
            for idx_dyshType2_kkk in range(0, (len(self.get_dyShieldingType2_currentState()) - self.get_nDyShType2_notVirtual())):
                dataGen_dyshBitsList_S2_temp.append(None)
            for idx_dyshType3_kkk in range(0, (len(self.get_dyShieldingType3_currentState()) - self.get_nDyShType3_notVirtual())):
                dataGen_dyshBitsList_S3_temp.append(None)

            dataGen_dyshBitsTuple_S1 = tuple(copy.deepcopy(dataGen_dyshBitsList_S1_temp))
            dataGen_dyshBitsTuple_S2 = tuple(copy.deepcopy(dataGen_dyshBitsList_S2_temp))
            dataGen_dyshBitsTuple_S3 = tuple(copy.deepcopy(dataGen_dyshBitsList_S3_temp))




        else:
            assert False

        # Assemble the signal bits into the following form:
        # dataGen_data2bTrans_signalBits_3Clk = [[bit0_clk1, bit0_clk2, bit0_clk3], [bit1_clk1, bit1_clk2, bit1_clk3], ...]
        dataGen_data2bTrans_signalBits_3Clk = []
        for idx_i in range(0, len(self.get_signalBits_currentState())):
            threeBitsList = [copy.deepcopy(dataGen_signalBitsTuple_01[idx_i]),
                             copy.deepcopy(dataGen_signalBitsTuple_02[idx_i]),
                             copy.deepcopy(dataGen_signalBitsTuple_03[idx_i])]
            dataGen_data2bTrans_signalBits_3Clk.append(copy.deepcopy(threeBitsList))

        dataGenCopy_data2bTrans_signalBits_3Clk = copy.deepcopy(dataGen_data2bTrans_signalBits_3Clk)
        print("---Input data (signal bits) - {}: {}".format(dataGenMethod, dataGen_data2bTrans_signalBits_3Clk))

        # Monitor
        monitor_flagsBool_ifSignalBitTrans_3Clk = []
        monitor_nTransmitted_signalBits = 0
        monitor_signalBitsState_3Clk = []
        monitor_dysh1State_3Clk = []
        monitor_dysh2State_3Clk = []
        monitor_dysh3State_3Clk = []

        # Clk 1: DySh Type 1

        # Clk 1 - monitor
        #
        # flagList_signalBits_inputTransmitted:
        # Once the signal bit with idx = idx_i is traversed,
        #   flagList_signalBits_inputTransmitted[idx_i] should be changed to False.
        # Once the input bit in signal bit with idx = idx_i is transmitted,
        #   flagList_signalBits_inputTransmitted[idx_i] should be changed to True.
        flagList_signalBits_inputTransmitted = len(self.get_signalBits_currentState()) * [None]

        # Clk 1 - traverse all circle
        for idx_centerDysh_i in range(0, len(self.get_dyShieldingType1_currentState())): # For each encoding circle
            #######
            # Get the current state: circleCodewordTuple_current
            dyShieldingType1_currentState = self.get_dyShieldingType1_currentState()
            circleCodewordList_current = []
            if dyShieldingType1_currentState[idx_centerDysh_i] is None:
                circleCodewordList_current.append(copy.deepcopy(self.get_state_virtualBit()))
            elif dyShieldingType1_currentState[idx_centerDysh_i] == 0:
                circleCodewordList_current.append(0)
            elif dyShieldingType1_currentState[idx_centerDysh_i] == 1:
                circleCodewordList_current.append(1)
            else:
                assert False

            for idx_neighboringSignalBits_i in self.get_dyShieldingType1_topoTuple()[idx_centerDysh_i]:
                if idx_neighboringSignalBits_i is None:
                    circleCodewordList_current.append(self.get_state_virtualBit())
                else:
                    assert isinstance(idx_neighboringSignalBits_i, int)
                    assert idx_neighboringSignalBits_i >= 0
                    if self.get_signalBits_currentState()[idx_neighboringSignalBits_i] == 0:
                        circleCodewordList_current.append(0)
                    elif self.get_signalBits_currentState()[idx_neighboringSignalBits_i] == 1:
                        circleCodewordList_current.append(1)
                    else:
                        assert False
            assert len(circleCodewordList_current) == 7
            circleCodewordTuple_current = tuple(circleCodewordList_current)

            #######
            # Get the input data to be transmitted: circuitInputList_current
            circleInputList_current = []
            if dataGen_dyshBitsTuple_S1[idx_centerDysh_i] is None:
                circleInputList_current.append(copy.deepcopy(self.get_state_virtualBit()))
            elif dataGen_dyshBitsTuple_S1[idx_centerDysh_i] == 0:
                circleInputList_current.append(0)
            elif dataGen_dyshBitsTuple_S1[idx_centerDysh_i] == 1:
                circleInputList_current.append(1)
            else:
                assert False

            for idx_neighboringSignalBits_k in self.get_dyShieldingType1_topoTuple()[idx_centerDysh_i]:
                if idx_neighboringSignalBits_k is None:
                    circleInputList_current.append(self.get_state_virtualBit())
                else:
                    assert isinstance(idx_neighboringSignalBits_k, int)
                    assert idx_neighboringSignalBits_k >= 0
                    if dataGen_data2bTrans_signalBits_3Clk[idx_neighboringSignalBits_k][0] == 0:
                        circleInputList_current.append(0)
                    elif dataGen_data2bTrans_signalBits_3Clk[idx_neighboringSignalBits_k][0] == 1:
                        circleInputList_current.append(1)
                    else:
                        assert False
                    assert flagList_signalBits_inputTransmitted[idx_neighboringSignalBits_k] is None
                    flagList_signalBits_inputTransmitted[idx_neighboringSignalBits_k] = False
            assert len(circleInputList_current) == 7

            #######
            # Encoding & Update state
            enc_cwOutTuple, enc_nBitTrans, enc_boolTuple_ifBitTrans = self._codecInstance_BSCAC_7bit.encoder_core(bits_to_be_trans=copy.deepcopy(circleInputList_current),
                                                                                                                  last_codeword=copy.deepcopy(circleCodewordTuple_current))

            currentTopoTuple = self.get_dyShieldingType1_topoTuple()[idx_centerDysh_i]
            for idx_circleSignalBits_i in range(0, 6):
                if enc_boolTuple_ifBitTrans[(idx_circleSignalBits_i + 1)] is True:
                    idx_currentSignalBit_temp = currentTopoTuple[idx_circleSignalBits_i]
                    if isinstance(idx_currentSignalBit_temp, int):
                        assert flagList_signalBits_inputTransmitted[idx_currentSignalBit_temp] is False
                        flagList_signalBits_inputTransmitted[idx_currentSignalBit_temp] = True
                        self.updateState_signalBits_modifySingleBit(bitIdx=idx_currentSignalBit_temp, bitNewState=copy.deepcopy(enc_cwOutTuple[(idx_circleSignalBits_i + 1)]))
                        monitor_nTransmitted_signalBits = monitor_nTransmitted_signalBits + 1
                        rawBitIn_temp = dataGen_data2bTrans_signalBits_3Clk[idx_currentSignalBit_temp].pop(0)
                        assert rawBitIn_temp == enc_cwOutTuple[(idx_circleSignalBits_i + 1)]
                    else:
                        assert idx_currentSignalBit_temp is None
                else:
                    assert enc_boolTuple_ifBitTrans[(idx_circleSignalBits_i + 1)] is False

        # Clk 1 - Unconstrained signal bits
        for idx_signalBitUnconstrained_i in self.get_dyShieldingType1_unconstraintBitsTuple():
            assert isinstance(idx_signalBitUnconstrained_i, int)
            assert idx_signalBitUnconstrained_i >= 0
            assert flagList_signalBits_inputTransmitted[idx_signalBitUnconstrained_i] is None
            flagList_signalBits_inputTransmitted[idx_signalBitUnconstrained_i] = True
            rawBitIn_temp = dataGen_data2bTrans_signalBits_3Clk[idx_signalBitUnconstrained_i].pop(0)
            assert rawBitIn_temp in (0, 1)
            self.updateState_signalBits_modifySingleBit(bitIdx=idx_signalBitUnconstrained_i, bitNewState=copy.deepcopy(rawBitIn_temp))
            monitor_nTransmitted_signalBits = monitor_nTransmitted_signalBits + 1

        # Clk 1 - Update dySh bits
        self.updateState_dyShieldingType1(newState_list=copy.deepcopy(list(dataGen_dyshBitsTuple_S1)))

        # Clk 1 - Record
        print("---dysh1: In={}, State->{}; SignalBit state->{} ({}-bit transmitted, flag:{})".format(dataGen_dyshBitsTuple_S1,
                                                                                                     self.get_dyShieldingType1_currentState(),
                                                                                                     self.get_signalBits_currentState(),
                                                                                                     monitor_nTransmitted_signalBits,
                                                                                                     flagList_signalBits_inputTransmitted))
        flagTuple_signalBits_inputTransmitted = tuple(flagList_signalBits_inputTransmitted)
        monitor_flagsBool_ifSignalBitTrans_3Clk.append(copy.deepcopy(flagTuple_signalBits_inputTransmitted))
        monitor_signalBitsState_3Clk.append(copy.deepcopy(self.get_signalBits_currentState()))
        monitor_dysh1State_3Clk.append(copy.deepcopy(self.get_dyShieldingType1_currentState()))
        monitor_dysh2State_3Clk.append(copy.deepcopy(self.get_dyShieldingType2_currentState()))
        monitor_dysh3State_3Clk.append(copy.deepcopy(self.get_dyShieldingType3_currentState()))

        # Clk 2: DySh Type 2

        # Clk 2 - monitor
        #
        # flagList_signalBits_inputTransmitted:
        # Once the signal bit with idx = idx_i is traversed,
        #   flagList_signalBits_inputTransmitted[idx_i] should be changed to False.
        # Once the input bit in signal bit with idx = idx_i is transmitted,
        #   flagList_signalBits_inputTransmitted[idx_i] should be changed to True.
        flagList_signalBits_inputTransmitted = len(self.get_signalBits_currentState()) * [None]

        print("---Input data (signal bits) - {}: {}".format(dataGenMethod, dataGen_data2bTrans_signalBits_3Clk))

        # Clk 2 - traverse all circle
        for idx_centerDysh_i in range(0, len(self.get_dyShieldingType2_currentState())): # For each encoding circle
            #######
            # Get the current state: circleCodewordTuple_current
            dyShieldingType2_currentState = self.get_dyShieldingType2_currentState()
            circleCodewordList_current = []
            if dyShieldingType2_currentState[idx_centerDysh_i] is None:
                circleCodewordList_current.append(copy.deepcopy(self.get_state_virtualBit()))
            elif dyShieldingType2_currentState[idx_centerDysh_i] == 0:
                circleCodewordList_current.append(0)
            elif dyShieldingType2_currentState[idx_centerDysh_i] == 1:
                circleCodewordList_current.append(1)
            else:
                assert False

            for idx_neighboringSignalBits_i in self.get_dyShieldingType2_topoTuple()[idx_centerDysh_i]:
                if idx_neighboringSignalBits_i is None:
                    circleCodewordList_current.append(self.get_state_virtualBit())
                else:
                    assert isinstance(idx_neighboringSignalBits_i, int)
                    assert idx_neighboringSignalBits_i >= 0
                    if self.get_signalBits_currentState()[idx_neighboringSignalBits_i] == 0:
                        circleCodewordList_current.append(0)
                    elif self.get_signalBits_currentState()[idx_neighboringSignalBits_i] == 1:
                        circleCodewordList_current.append(1)
                    else:
                        assert False
            assert len(circleCodewordList_current) == 7
            circleCodewordTuple_current = tuple(circleCodewordList_current)

            #######
            # Get the input data to be transmitted: circuitInputList_current
            circleInputList_current = []
            if dataGen_dyshBitsTuple_S2[idx_centerDysh_i] is None:
                circleInputList_current.append(copy.deepcopy(self.get_state_virtualBit()))
            elif dataGen_dyshBitsTuple_S2[idx_centerDysh_i] == 0:
                circleInputList_current.append(0)
            elif dataGen_dyshBitsTuple_S2[idx_centerDysh_i] == 1:
                circleInputList_current.append(1)
            else:
                assert False

            for idx_neighboringSignalBits_k in self.get_dyShieldingType2_topoTuple()[idx_centerDysh_i]:
                if idx_neighboringSignalBits_k is None:
                    circleInputList_current.append(self.get_state_virtualBit())
                else:
                    assert isinstance(idx_neighboringSignalBits_k, int)
                    assert idx_neighboringSignalBits_k >= 0
                    if dataGen_data2bTrans_signalBits_3Clk[idx_neighboringSignalBits_k][0] == 0:
                        circleInputList_current.append(0)
                    elif dataGen_data2bTrans_signalBits_3Clk[idx_neighboringSignalBits_k][0] == 1:
                        circleInputList_current.append(1)
                    else:
                        assert False
                    assert flagList_signalBits_inputTransmitted[idx_neighboringSignalBits_k] is None
                    flagList_signalBits_inputTransmitted[idx_neighboringSignalBits_k] = False
            assert len(circleInputList_current) == 7

            #######
            # Encoding & Update state
            enc_cwOutTuple, enc_nBitTrans, enc_boolTuple_ifBitTrans = self._codecInstance_BSCAC_7bit.encoder_core(bits_to_be_trans=copy.deepcopy(circleInputList_current),
                                                                                                                  last_codeword=copy.deepcopy(circleCodewordTuple_current))

            currentTopoTuple = self.get_dyShieldingType2_topoTuple()[idx_centerDysh_i]
            for idx_circleSignalBits_i in range(0, 6):
                if enc_boolTuple_ifBitTrans[(idx_circleSignalBits_i + 1)] is True:
                    idx_currentSignalBit_temp = currentTopoTuple[idx_circleSignalBits_i]
                    if isinstance(idx_currentSignalBit_temp, int):
                        assert flagList_signalBits_inputTransmitted[idx_currentSignalBit_temp] is False
                        flagList_signalBits_inputTransmitted[idx_currentSignalBit_temp] = True
                        self.updateState_signalBits_modifySingleBit(bitIdx=idx_currentSignalBit_temp, bitNewState=copy.deepcopy(enc_cwOutTuple[(idx_circleSignalBits_i + 1)]))
                        monitor_nTransmitted_signalBits = monitor_nTransmitted_signalBits + 1
                        rawBitIn_temp = dataGen_data2bTrans_signalBits_3Clk[idx_currentSignalBit_temp].pop(0)
                        assert rawBitIn_temp == enc_cwOutTuple[(idx_circleSignalBits_i + 1)]
                    else:
                        assert idx_currentSignalBit_temp is None
                else:
                    assert enc_boolTuple_ifBitTrans[(idx_circleSignalBits_i + 1)] is False

        # Clk 2 - Unconstrained signal bits
        for idx_signalBitUnconstrained_i in self.get_dyShieldingType2_unconstraintBitsTuple():
            assert isinstance(idx_signalBitUnconstrained_i, int)
            assert idx_signalBitUnconstrained_i >= 0
            assert flagList_signalBits_inputTransmitted[idx_signalBitUnconstrained_i] is None
            flagList_signalBits_inputTransmitted[idx_signalBitUnconstrained_i] = True
            rawBitIn_temp = dataGen_data2bTrans_signalBits_3Clk[idx_signalBitUnconstrained_i].pop(0)
            assert rawBitIn_temp in (0, 1)
            self.updateState_signalBits_modifySingleBit(bitIdx=idx_signalBitUnconstrained_i, bitNewState=copy.deepcopy(rawBitIn_temp))
            monitor_nTransmitted_signalBits = monitor_nTransmitted_signalBits + 1

        # Clk 2 - Update dySh bits
        self.updateState_dyShieldingType2(newState_list=copy.deepcopy(list(dataGen_dyshBitsTuple_S2)))

        # Clk 2 - Reocrd
        print("---dysh2: In={}, State->{}; SignalBit state->{} ({}-bit transmitted, flag:{})".format(dataGen_dyshBitsTuple_S2,
                                                                                                     self.get_dyShieldingType2_currentState(),
                                                                                                     self.get_signalBits_currentState(),
                                                                                                     monitor_nTransmitted_signalBits,
                                                                                                     flagList_signalBits_inputTransmitted))
        flagTuple_signalBits_inputTransmitted = tuple(flagList_signalBits_inputTransmitted)
        monitor_flagsBool_ifSignalBitTrans_3Clk.append(copy.deepcopy(flagTuple_signalBits_inputTransmitted))
        monitor_signalBitsState_3Clk.append(copy.deepcopy(self.get_signalBits_currentState()))
        monitor_dysh1State_3Clk.append(copy.deepcopy(self.get_dyShieldingType1_currentState()))
        monitor_dysh2State_3Clk.append(copy.deepcopy(self.get_dyShieldingType2_currentState()))
        monitor_dysh3State_3Clk.append(copy.deepcopy(self.get_dyShieldingType3_currentState()))


        # Clk 3: DySh Type 3

        # Clk 3 - monitor
        #
        # flagList_signalBits_inputTransmitted:
        # Once the signal bit with idx = idx_i is traversed,
        #   flagList_signalBits_inputTransmitted[idx_i] should be changed to False.
        # Once the input bit in signal bit with idx = idx_i is transmitted,
        #   flagList_signalBits_inputTransmitted[idx_i] should be changed to True.
        flagList_signalBits_inputTransmitted = len(self.get_signalBits_currentState()) * [None]

        print("---Input data (signal bits) - {}: {}".format(dataGenMethod, dataGen_data2bTrans_signalBits_3Clk))

        # Clk 3 - traverse all circle
        for idx_centerDysh_i in range(0, len(self.get_dyShieldingType3_currentState())): # For each encoding circle
            #######
            # Get the current state: circleCodewordTuple_current
            dyShieldingType3_currentState = self.get_dyShieldingType3_currentState()
            circleCodewordList_current = []
            if dyShieldingType3_currentState[idx_centerDysh_i] is None:
                circleCodewordList_current.append(copy.deepcopy(self.get_state_virtualBit()))
            elif dyShieldingType3_currentState[idx_centerDysh_i] == 0:
                circleCodewordList_current.append(0)
            elif dyShieldingType3_currentState[idx_centerDysh_i] == 1:
                circleCodewordList_current.append(1)
            else:
                assert False

            for idx_neighboringSignalBits_i in self.get_dyShieldingType3_topoTuple()[idx_centerDysh_i]:
                if idx_neighboringSignalBits_i is None:
                    circleCodewordList_current.append(self.get_state_virtualBit())
                else:
                    assert isinstance(idx_neighboringSignalBits_i, int)
                    assert idx_neighboringSignalBits_i >= 0
                    if self.get_signalBits_currentState()[idx_neighboringSignalBits_i] == 0:
                        circleCodewordList_current.append(0)
                    elif self.get_signalBits_currentState()[idx_neighboringSignalBits_i] == 1:
                        circleCodewordList_current.append(1)
                    else:
                        assert False
            assert len(circleCodewordList_current) == 7
            circleCodewordTuple_current = tuple(circleCodewordList_current)

            #######
            # Get the input data to be transmitted: circuitInputList_current
            circleInputList_current = []
            if dataGen_dyshBitsTuple_S3[idx_centerDysh_i] is None:
                circleInputList_current.append(copy.deepcopy(self.get_state_virtualBit()))
            elif dataGen_dyshBitsTuple_S3[idx_centerDysh_i] == 0:
                circleInputList_current.append(0)
            elif dataGen_dyshBitsTuple_S3[idx_centerDysh_i] == 1:
                circleInputList_current.append(1)
            else:
                assert False

            for idx_neighboringSignalBits_k in self.get_dyShieldingType3_topoTuple()[idx_centerDysh_i]:
                if idx_neighboringSignalBits_k is None:
                    circleInputList_current.append(self.get_state_virtualBit())
                else:
                    assert isinstance(idx_neighboringSignalBits_k, int)
                    assert idx_neighboringSignalBits_k >= 0
                    if dataGen_data2bTrans_signalBits_3Clk[idx_neighboringSignalBits_k][0] == 0:
                        circleInputList_current.append(0)
                    elif dataGen_data2bTrans_signalBits_3Clk[idx_neighboringSignalBits_k][0] == 1:
                        circleInputList_current.append(1)
                    else:
                        assert False
                    assert flagList_signalBits_inputTransmitted[idx_neighboringSignalBits_k] is None
                    flagList_signalBits_inputTransmitted[idx_neighboringSignalBits_k] = False
            assert len(circleInputList_current) == 7

            #######
            # Encoding & Update state
            enc_cwOutTuple, enc_nBitTrans, enc_boolTuple_ifBitTrans = self._codecInstance_BSCAC_7bit.encoder_core(bits_to_be_trans=copy.deepcopy(circleInputList_current),
                                                                                                                  last_codeword=copy.deepcopy(circleCodewordTuple_current))

            currentTopoTuple = self.get_dyShieldingType3_topoTuple()[idx_centerDysh_i]
            for idx_circleSignalBits_i in range(0, 6):
                if enc_boolTuple_ifBitTrans[(idx_circleSignalBits_i + 1)] is True:
                    idx_currentSignalBit_temp = currentTopoTuple[idx_circleSignalBits_i]
                    if isinstance(idx_currentSignalBit_temp, int):
                        assert flagList_signalBits_inputTransmitted[idx_currentSignalBit_temp] is False
                        flagList_signalBits_inputTransmitted[idx_currentSignalBit_temp] = True
                        self.updateState_signalBits_modifySingleBit(bitIdx=idx_currentSignalBit_temp, bitNewState=copy.deepcopy(enc_cwOutTuple[(idx_circleSignalBits_i + 1)]))
                        monitor_nTransmitted_signalBits = monitor_nTransmitted_signalBits + 1
                        rawBitIn_temp = dataGen_data2bTrans_signalBits_3Clk[idx_currentSignalBit_temp].pop(0)
                        assert rawBitIn_temp == enc_cwOutTuple[(idx_circleSignalBits_i + 1)]
                    else:
                        assert idx_currentSignalBit_temp is None
                else:
                    assert enc_boolTuple_ifBitTrans[(idx_circleSignalBits_i + 1)] is False

        # Clk 3 - Unconstrained signal bits
        for idx_signalBitUnconstrained_i in self.get_dyShieldingType3_unconstraintBitsTuple():
            assert isinstance(idx_signalBitUnconstrained_i, int)
            assert idx_signalBitUnconstrained_i >= 0
            assert flagList_signalBits_inputTransmitted[idx_signalBitUnconstrained_i] is None
            flagList_signalBits_inputTransmitted[idx_signalBitUnconstrained_i] = True
            rawBitIn_temp = dataGen_data2bTrans_signalBits_3Clk[idx_signalBitUnconstrained_i].pop(0)
            assert rawBitIn_temp in (0, 1)
            self.updateState_signalBits_modifySingleBit(bitIdx=idx_signalBitUnconstrained_i, bitNewState=copy.deepcopy(rawBitIn_temp))
            monitor_nTransmitted_signalBits = monitor_nTransmitted_signalBits + 1

        # Clk 3 - Update dySh bits
        self.updateState_dyShieldingType3(newState_list=copy.deepcopy(list(dataGen_dyshBitsTuple_S3)))

        # Clk 3 - Reocrd
        print("---dysh3: In={}, State->{}; SignalBit state->{} ({}-bit transmitted, flag:{})".format(dataGen_dyshBitsTuple_S3,
                                                                                                     self.get_dyShieldingType3_currentState(),
                                                                                                     self.get_signalBits_currentState(),
                                                                                                     monitor_nTransmitted_signalBits,
                                                                                                     flagList_signalBits_inputTransmitted))
        flagTuple_signalBits_inputTransmitted = tuple(flagList_signalBits_inputTransmitted)
        monitor_flagsBool_ifSignalBitTrans_3Clk.append(copy.deepcopy(flagTuple_signalBits_inputTransmitted))
        monitor_signalBitsState_3Clk.append(copy.deepcopy(self.get_signalBits_currentState()))
        monitor_dysh1State_3Clk.append(copy.deepcopy(self.get_dyShieldingType1_currentState()))
        monitor_dysh2State_3Clk.append(copy.deepcopy(self.get_dyShieldingType2_currentState()))
        monitor_dysh3State_3Clk.append(copy.deepcopy(self.get_dyShieldingType3_currentState()))

        return dataGenCopy_data2bTrans_signalBits_3Clk, monitor_flagsBool_ifSignalBitTrans_3Clk, monitor_nTransmitted_signalBits, monitor_signalBitsState_3Clk, monitor_dysh1State_3Clk, monitor_dysh2State_3Clk, monitor_dysh3State_3Clk
















