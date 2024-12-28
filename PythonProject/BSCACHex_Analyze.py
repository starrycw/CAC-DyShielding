import copy
import z3 as z3

import RingCAC_Alg.BitStuffingCAC_Analyze as BitStuffingCAC_Analyze
import Evaluation_Tools.array_xtalk_simu as array_xtalk_simu

########################################################################################################################
########################################################################################################################
def calcTransProbOfSingle7bitGroup():
    '''
    Calculate the transition probability of single encoded group (7-bit codeword).
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    transProbMatrix = BSCACAnalyze_instance01.get_transProb_singleGroup_oneClockPeriod()
    check_ifpass, check_errlist = transProbMatrix.checkMatrix()
    print(transProbMatrix)
    print(check_ifpass,check_errlist)
    transProbMatrix.showMatrix_main(config_vmin=-0.05, config_dpi=500)
    transProbMatrix.showMatrix_mainTimesN(n_int=(2**7), config_vmin=0, config_dpi=500)

########################################################################################################################
########################################################################################################################
def calcTransCntOfSingle7bitGroup():
    '''
    Calculate the transition cnt of single encoded group (7-bit codeword).
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    transCntMatrix = BSCACAnalyze_instance01.get_transCnt_singleGroup_oneClockPeriod()
    check_ifpass, check_errlist = transCntMatrix.checkMatrix()
    print(transCntMatrix)
    print(check_ifpass,check_errlist)
    transCntMatrix.showMatrix_main(config_vmin=-0.05, config_dpi=500)

########################################################################################################################
########################################################################################################################
def getMuAByBQ_subtask_getMatrixBAndMatrixQ():
    '''
    Calc Matrix B & Matrix Q
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    matrixB = BSCACAnalyze_instance01._calcMuA_subtask_getMatrixB()
    matrixQ_instance = BSCACAnalyze_instance01._calcMuA_subtask_getMatrixQ()
    matrixQ = matrixQ_instance.getMatrix_all()
    colIdx_list = []
    print("###############################################")
    print("#Matrix B")
    for idx_i in range(0, len(matrixB)):
        rowSum_matrixB = 0
        for idx_j in range(0, len(matrixB[idx_i])):
            rowSum_matrixB = rowSum_matrixB + matrixB[idx_i][idx_j]
            if matrixB[idx_i][idx_j] == 1:
                assert idx_j not in colIdx_list
                colIdx_list.append(idx_j)
        print("[row{}-{}] \t {}".format(idx_i, rowSum_matrixB, matrixB[idx_i]))
        assert rowSum_matrixB == 1
    print("COL IDX LIST: {}".format(colIdx_list))

    print("###############################################")
    print("#Matrix Q")

    for idx_i in range(0, len(matrixQ)):
        rowSum_matrixQ = 0
        for idx_j in range(0, len(matrixQ[idx_i])):
            rowSum_matrixQ = rowSum_matrixQ + matrixQ[idx_i][idx_j]
        print("[row{}-{}] \t {}".format(idx_i, rowSum_matrixQ, matrixQ[idx_i]))
        assert rowSum_matrixQ == 256

    return copy.deepcopy(matrixB), copy.deepcopy(matrixQ)

########################################################################################################################
########################################################################################################################
def getMuAByBQ_subtask_getMatrixBQ():
    '''
    Calc matrix BQ
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    matrixBQ = BSCACAnalyze_instance01._calcMuASimplified_subtask_getMatrixBQ()
    colIdx_list = []
    print("###############################################")

    idx_cnt = 0
    for matrixBQ_row_i in matrixBQ:
        assert len(matrixBQ_row_i) == 64
        sum_row_i = 0
        for matrixBQ_i in matrixBQ_row_i:
            sum_row_i = sum_row_i + matrixBQ_i
        assert sum_row_i == 256
        print("Row{}\t - Sum{} - {}".format(idx_cnt, sum_row_i, matrixBQ_row_i))
        idx_cnt = idx_cnt + 1

    return copy.deepcopy(matrixBQ)

########################################################################################################################
########################################################################################################################
def getMuAByBQ_main_basicConstraints():
    '''
    Calc \mu_a by BQ.
    Basic constraints only!
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    muA_z3SolverInstance = BSCACAnalyze_instance01.calcMuASimplified_useMatrixBQ_main(constraintSet='basic')

    nBitTransCnt_tuple_by7bitOldState, nBitTransMinAndMax_tuple = BSCACAnalyze_instance01.get_nBitTransmittedCnt_matrixByOldState_singleGroup_oneClockPeriod()
    assert len(nBitTransCnt_tuple_by7bitOldState) == (2 ** 7)
    nBitTransExpectation_list = []

    for idx_i in range(0, (2 ** 6)):
        cnt_nBitSum = nBitTransCnt_tuple_by7bitOldState[idx_i] + nBitTransCnt_tuple_by7bitOldState[idx_i + (2 ** 6)]
        nBitTransExpectation_list.append(copy.deepcopy(cnt_nBitSum))

    nBitTransExpectation_tuple = tuple(nBitTransExpectation_list)
    nBitAll = (2 ** 7) * 2

    sumOfMuATimesWeight = muA_z3SolverInstance.modelEvaluate_sumOfMuATimesWeight(weightTuple=copy.deepcopy(nBitTransExpectation_tuple))
    print("Expectation of the number of transmitted bits (signal bits only) in each 7-bit group: "
          "\n       {}\n       divided by\n       {}\n".format(sumOfMuATimesWeight,
                                                                         nBitAll))





########################################################################################################################
########################################################################################################################
def getMuAByBQ_main_fullConstraints():
    '''
    Calc \mu_a by BQ.
    Full constraints applied!
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    muA_z3SolverInstance = BSCACAnalyze_instance01.calcMuASimplified_useMatrixBQ_main(constraintSet='full')

    nBitTransCnt_tuple_by7bitOldState, nBitTransMinAndMax_tuple = BSCACAnalyze_instance01.get_nBitTransmittedCnt_matrixByOldState_singleGroup_oneClockPeriod()
    assert len(nBitTransCnt_tuple_by7bitOldState) == (2 ** 7)
    nBitTransExpectation_list = []

    for idx_i in range(0, (2 ** 6)):
        cnt_nBitSum = nBitTransCnt_tuple_by7bitOldState[idx_i] + nBitTransCnt_tuple_by7bitOldState[idx_i + (2 ** 6)]
        nBitTransExpectation_list.append(copy.deepcopy(cnt_nBitSum))

    nBitTransExpectation_tuple = tuple(nBitTransExpectation_list)
    nBitAll = (2 ** 7) * 2

    sumOfMuATimesWeight = muA_z3SolverInstance.modelEvaluate_sumOfMuATimesWeight(
        weightTuple=copy.deepcopy(nBitTransExpectation_tuple))
    print("Expectation of the number of transmitted bits (signal bits only) in each 7-bit group: "
          "\n       {}\n       divided by\n       {}\n".format(sumOfMuATimesWeight,
                                                               nBitAll))

########################################################################################################################
########################################################################################################################
def getMuAByCQ_subtask_getMatrixC():
    '''
    Calc matrix C
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    matrixR_a, matrixR_b, matrixR_c = BSCACAnalyze_instance01._calcMuA_subtask_getMatrixC()
    colIdx_list = []
    print("###############################################")

    assert len(matrixR_a) == 64
    assert len(matrixR_b) == 64
    assert len(matrixR_c) == 64

    for idx_row_i in range(0, 64):
        sum_row_i_a = 0
        sum_row_i_b = 0
        sum_row_i_c = 0
        for matrixR_i in matrixR_a[idx_row_i]:
            sum_row_i_a = sum_row_i_a + matrixR_i
        for matrixR_i in matrixR_b[idx_row_i]:
            sum_row_i_b = sum_row_i_b + matrixR_i
        for matrixR_i in matrixR_c[idx_row_i]:
            sum_row_i_c = sum_row_i_c + matrixR_i
        assert sum_row_i_a == 16
        assert sum_row_i_b == 16
        assert sum_row_i_c == 16
        print("Row{}\t - Sum{}-{}-{} - {}-{}-{}".format(idx_row_i, sum_row_i_a, sum_row_i_b, sum_row_i_c, matrixR_a[idx_row_i], matrixR_b[idx_row_i], matrixR_c[idx_row_i]))

    colSumList_a = []
    colSumList_b = []
    colSumList_c = []
    for idx_col_k in range(0, 64):
        sum_col_k_a = 0
        sum_col_k_b = 0
        sum_col_k_c = 0
        for idx_row_k in range(0, 64):
            sum_col_k_a = sum_col_k_a + matrixR_a[idx_row_k][idx_col_k]
            sum_col_k_b = sum_col_k_b + matrixR_b[idx_row_k][idx_col_k]
            sum_col_k_c = sum_col_k_c + matrixR_c[idx_row_k][idx_col_k]
        assert sum_col_k_a == 16
        assert sum_col_k_b == 16
        assert sum_col_k_c == 16
        colSumList_a.append(sum_col_k_a)
        colSumList_b.append(sum_col_k_b)
        colSumList_c.append(sum_col_k_c)
    print("ColSum\tA\t{}".format(colSumList_a))
    print("ColSum\tB\t{}".format(colSumList_b))
    print("ColSum\tC\t{}".format(colSumList_c))

########################################################################################################################
########################################################################################################################
def getMuAByCQ_main_basicConstraints():
    '''
    Calc \mu_a by CQ.
    Basic constraints only!
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    muA_z3SolverInstance = BSCACAnalyze_instance01.calcMuASimplified_useMatrixCQ_main(constraintSet='basic')

    nBitTransCnt_tuple_by7bitOldState, nBitTransMinAndMax_tuple = BSCACAnalyze_instance01.get_nBitTransmittedCnt_matrixByOldState_singleGroup_oneClockPeriod()
    assert len(nBitTransCnt_tuple_by7bitOldState) == (2 ** 7)
    nBitTransExpectation_list = []

    for idx_i in range(0, (2 ** 6)):
        cnt_nBitSum = nBitTransCnt_tuple_by7bitOldState[idx_i] + nBitTransCnt_tuple_by7bitOldState[idx_i + (2 ** 6)]
        nBitTransExpectation_list.append(copy.deepcopy(cnt_nBitSum))

    nBitTransExpectation_tuple = tuple(nBitTransExpectation_list)
    nBitAll = (2 ** 7) * 2

    sumOfMuATimesWeight = muA_z3SolverInstance.modelEvaluate_sumOfMuATimesWeight(weightTuple=copy.deepcopy(nBitTransExpectation_tuple))
    print("Expectation of the number of transmitted bits (signal bits only) in each 7-bit group: "
          "\n       {}\n       divided by\n       {}\n".format(sumOfMuATimesWeight,
                                                                         nBitAll))

########################################################################################################################
########################################################################################################################
def getMuAByCQ_main_fullConstraints():
    '''
    Calc \mu_a by CQ.
    Full constraints applied!
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    muA_z3SolverInstance = BSCACAnalyze_instance01.calcMuASimplified_useMatrixCQ_main(constraintSet='full')

    nBitTransCnt_tuple_by7bitOldState, nBitTransMinAndMax_tuple = BSCACAnalyze_instance01.get_nBitTransmittedCnt_matrixByOldState_singleGroup_oneClockPeriod()
    assert len(nBitTransCnt_tuple_by7bitOldState) == (2 ** 7)
    nBitTransExpectation_list = []

    for idx_i in range(0, (2 ** 6)):
        cnt_nBitSum = nBitTransCnt_tuple_by7bitOldState[idx_i] + nBitTransCnt_tuple_by7bitOldState[idx_i + (2 ** 6)]
        nBitTransExpectation_list.append(copy.deepcopy(cnt_nBitSum))

    nBitTransExpectation_tuple = tuple(nBitTransExpectation_list)
    nBitAll = (2 ** 7) * 2

    sumOfMuATimesWeight = muA_z3SolverInstance.modelEvaluate_sumOfMuATimesWeight(
        weightTuple=copy.deepcopy(nBitTransExpectation_tuple))
    print("Expectation of the number of transmitted bits (signal bits only) in each 7-bit group: "
          "\n       {}\n       divided by\n       {}\n".format(sumOfMuATimesWeight,
                                                               nBitAll))

########################################################################################################################
########################################################################################################################
def simulation_codingRateSimu_HexArrayRegularA_13x9(n_cycleRun = 100000):
    # n_cycleRun = 100000
    BSCACSimu_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Simulation_HexArray(arrayType="Hex_RegularA_13x9")
    cnt_nSignalBitsTrans = 0
    for cycle_i in range(0, n_cycleRun):
        print('Cycle-{}'.format(cycle_i))
        data2bTrans_3Clk, flagsBool_ifSignalBitTrans_3Clk, nTransmitted_signalBits, signalBitsState_3Clk, dysh1State_3Clk, dysh2State_3Clk, dysh3State_3Clk = BSCACSimu_instance01.runSimu_threeClk(dataGenMethod='random')
        cnt_nSignalBitsTrans = cnt_nSignalBitsTrans + nTransmitted_signalBits
        print('-flagsBool_ifSignalBitTrans_3Clk: {}'.format(flagsBool_ifSignalBitTrans_3Clk))
        print('-nTransmitted_signalBits: {}'.format(signalBitsState_3Clk))
        print('-signalBitsState_3Clk: {}'.format(signalBitsState_3Clk))
        print('-dysh1State_3Clk: {}'.format(dysh1State_3Clk))
        print('-dysh2State_3Clk: {}'.format(dysh2State_3Clk))
        print('-dysh3State_3Clk: {}'.format(dysh3State_3Clk))
        print('#########################################################################################################')

    print('cnt_nSignalBitsTrans = {}'.format(cnt_nSignalBitsTrans))
    nTSV_signal = len(BSCACSimu_instance01.get_signalBits_currentState())
    nTSV_dysh1 = BSCACSimu_instance01.get_nDyShType1_notVirtual()
    nTSV_dysh2 = BSCACSimu_instance01.get_nDyShType2_notVirtual()
    nTSV_dysh3 = BSCACSimu_instance01.get_nDyShType3_notVirtual()
    nTSV_dyshAll = nTSV_dysh1 + nTSV_dysh2 + nTSV_dysh3
    nTSV_all = nTSV_signal + nTSV_dyshAll
    bitOHCalc_nAll = nTSV_all * n_cycleRun * 3
    bitOHCalc_nRedundant = bitOHCalc_nAll - (nTSV_dyshAll * n_cycleRun) - cnt_nSignalBitsTrans
    bitOHCalc_OH = bitOHCalc_nRedundant / (bitOHCalc_nAll - bitOHCalc_nRedundant)
    print('signal bits coding rate: {} / {} = {}'.format(cnt_nSignalBitsTrans, (nTSV_signal * 3 * n_cycleRun), (cnt_nSignalBitsTrans / (nTSV_signal * 3 * n_cycleRun))))
    print("nTSV_all = {}, nTSV_dysh = ({}, {}, {}), nTSV_signal = {}, Cycle = {}, Bit Overhead = {} / {} = {}".format(nTSV_all, nTSV_dysh1, nTSV_dysh2, nTSV_dysh3, nTSV_signal, n_cycleRun, bitOHCalc_nRedundant, (bitOHCalc_nAll - bitOHCalc_nRedundant), bitOHCalc_OH))

########################################################################################################################
########################################################################################################################
def simulation_codingRateSimu_HexArrayRegularA_6mx3n(m, n, n_cycleRun):
    '''
    Coding rate simulation - HexArray-RegularA-6m_x_3n
    :param m:
    :param n:
    :param n_cycleRun:
    :return:
    '''
    assert isinstance(m, int)
    assert isinstance(n, int)
    assert isinstance(n_cycleRun, int)
    BSCACSimu_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Simulation_HexArray(arrayType="HexArrayAuto_regularA_6m_x_3n",
                                                                                     additionParamsTuple=(m, n))
    cnt_nSignalBitsTrans = 0
    for cycle_i in range(0, n_cycleRun):
        print('Cycle-{}'.format(cycle_i))
        data2bTrans_3Clk, flagsBool_ifSignalBitTrans_3Clk, nTransmitted_signalBits, signalBitsState_3Clk, dysh1State_3Clk, dysh2State_3Clk, dysh3State_3Clk = BSCACSimu_instance01.runSimu_threeClk(dataGenMethod='random')
        cnt_nSignalBitsTrans = cnt_nSignalBitsTrans + nTransmitted_signalBits
        print('-flagsBool_ifSignalBitTrans_3Clk: {}'.format(flagsBool_ifSignalBitTrans_3Clk))
        print('-nTransmitted_signalBits: {}'.format(signalBitsState_3Clk))
        print('-signalBitsState_3Clk: {}'.format(signalBitsState_3Clk))
        print('-dysh1State_3Clk: {}'.format(dysh1State_3Clk))
        print('-dysh2State_3Clk: {}'.format(dysh2State_3Clk))
        print('-dysh3State_3Clk: {}'.format(dysh3State_3Clk))
        print('#########################################################################################################')

    print('cnt_nSignalBitsTrans = {}'.format(cnt_nSignalBitsTrans))
    nTSV_signal = len(BSCACSimu_instance01.get_signalBits_currentState())
    nTSV_dysh1 = BSCACSimu_instance01.get_nDyShType1_notVirtual()
    nTSV_dysh2 = BSCACSimu_instance01.get_nDyShType2_notVirtual()
    nTSV_dysh3 = BSCACSimu_instance01.get_nDyShType3_notVirtual()
    nTSV_dyshAll = nTSV_dysh1 + nTSV_dysh2 + nTSV_dysh3
    nTSV_all = nTSV_signal + nTSV_dyshAll
    bitOHCalc_nAll = nTSV_all * n_cycleRun * 3
    bitOHCalc_nRedundant = bitOHCalc_nAll - (nTSV_dyshAll * n_cycleRun) - cnt_nSignalBitsTrans
    bitOHCalc_OH = bitOHCalc_nRedundant / (bitOHCalc_nAll - bitOHCalc_nRedundant)
    print('signal bits coding rate: {} / {} = {}'.format(cnt_nSignalBitsTrans, (nTSV_signal * 3 * n_cycleRun), (cnt_nSignalBitsTrans / (nTSV_signal * 3 * n_cycleRun))))
    print("nTSV_all = {}, nTSV_dysh = ({}, {}, {}), nTSV_signal = {}, Cycle = {}, Bit Overhead = {} / {} = {}".format(nTSV_all, nTSV_dysh1, nTSV_dysh2, nTSV_dysh3, nTSV_signal, n_cycleRun, bitOHCalc_nRedundant, (bitOHCalc_nAll - bitOHCalc_nRedundant), bitOHCalc_OH))

########################################################################################################################

########################################################################################################################
########################################################################################################################
def simulation_xtalkSimu_HexArrayRegularA_18x12(n_cycleRun = 1000, edgeTSVXtalkZoom = 1, edgeTSVPunishment = 0):
    '''

    :param n_cycleRun: int
    :param edgeTSVXtalkZoom: int，默认为1。边缘TSV之间的串扰级别将乘以该数值。
    :param edgeTSVPunishment: int, 默认为0.该数值将被加到每个边缘TSV的串扰级别中。
    :return:
    '''
    assert edgeTSVPunishment >= 0
    assert edgeTSVXtalkZoom >= 1
    # n_cycleRun = 100000
    BSCACSimu_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Simulation_HexArray(arrayType="Hex_RegularA_18x12")
    XtalkCalculator_instance01 = array_xtalk_simu.Array_Xtalk_Calculator(n_row=12, n_col=9)
    # cnt_nSignalBitsTrans = 0
    TSVMapping_tuple = BSCACSimu_instance01.get_topoTuple_TSVMapping_forXtalkEval_ROWbyROW()
    array_shieldState_list = []
    for row_kk in range(0, 12):
        array_shieldState_list.append((False, False, False,
                                       False, False, False,
                                       False, False, False))
    array_shieldState_tuple = tuple(array_shieldState_list)

    ###### CNT
    cnt_xtalk_stsv = {0: 0,
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

    cnt_xtalk_dtsv = {0: 0,
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


    ######Simulation Start
    arrayState_last = BSCACSimu_instance01.codewordsRemapping_getArrayState(unmappedState_stsvs=copy.deepcopy(BSCACSimu_instance01.get_signalBits_initState()),
                                                                            unmappedState_dysh1=copy.deepcopy(BSCACSimu_instance01.get_dyShieldingType1_initState()),
                                                                            unmappedState_dysh2=copy.deepcopy(BSCACSimu_instance01.get_dyShieldingType2_initState()),
                                                                            unmappedState_dysh3=copy.deepcopy(BSCACSimu_instance01.get_dyShieldingType3_initState()))

    for cycle_i in range(0, n_cycleRun):
        print('\n#########################################################################################################')
        print('Cycle-{}'.format(cycle_i))
        data2bTrans_3Clk, flagsBool_ifSignalBitTrans_3Clk, nTransmitted_signalBits, signalBitsState_3Clk, dysh1State_3Clk, dysh2State_3Clk, dysh3State_3Clk = BSCACSimu_instance01.runSimu_threeClk(dataGenMethod='random')
        # cnt_nSignalBitsTrans = cnt_nSignalBitsTrans + nTransmitted_signalBits
        # print('-flagsBool_ifSignalBitTrans_3Clk: {}'.format(flagsBool_ifSignalBitTrans_3Clk))
        # print('-nTransmitted_signalBits: {}'.format(signalBitsState_3Clk))
        print('-signalBitsState_3Clk: {}'.format(signalBitsState_3Clk))
        print('-dysh1State_3Clk: {}'.format(dysh1State_3Clk))
        print('-dysh2State_3Clk: {}'.format(dysh2State_3Clk))
        print('-dysh3State_3Clk: {}'.format(dysh3State_3Clk))

        ##########################################
        # CLK 1
        arrayState_new = BSCACSimu_instance01.codewordsRemapping_getArrayState(unmappedState_stsvs=copy.deepcopy(signalBitsState_3Clk[0]),
                                                                               unmappedState_dysh1=copy.deepcopy(dysh1State_3Clk[0]),
                                                                               unmappedState_dysh2=copy.deepcopy(dysh2State_3Clk[0]),
                                                                               unmappedState_dysh3=copy.deepcopy(dysh3State_3Clk[0]))

        xtalk_simu_result = XtalkCalculator_instance01.calc_xtalk_level_hexTopoA(array_cw01=copy.deepcopy(arrayState_last),
                                                                                 array_cw02=copy.deepcopy(arrayState_new),
                                                                                 array_shield=copy.deepcopy(array_shieldState_tuple))

        assert len(xtalk_simu_result) == 12
        assert len(xtalk_simu_result[0]) == 9
        for row_kk in range(0, 12):
            for col_kk in range(0, 9):
                assert xtalk_simu_result[row_kk][col_kk] in (0, 0.25, 0.5, 0.75,
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
                                                             12)
                if TSVMapping_tuple[row_kk][col_kk][0] == 0:
                    cnt_xtalk_stsv[xtalk_simu_result[row_kk][col_kk]] = cnt_xtalk_stsv[xtalk_simu_result[row_kk][col_kk]] + 1

                elif TSVMapping_tuple[row_kk][col_kk][0] in (1, 2, 3):
                    cnt_xtalk_dtsv[xtalk_simu_result[row_kk][col_kk]]  = cnt_xtalk_dtsv[xtalk_simu_result[row_kk][col_kk]] + 1

                else:
                    assert False

        arrayState_last = copy.deepcopy(arrayState_new)

        ##########################################
        # CLK 2
        arrayState_new = BSCACSimu_instance01.codewordsRemapping_getArrayState(
            unmappedState_stsvs=copy.deepcopy(signalBitsState_3Clk[1]),
            unmappedState_dysh1=copy.deepcopy(dysh1State_3Clk[1]),
            unmappedState_dysh2=copy.deepcopy(dysh2State_3Clk[1]),
            unmappedState_dysh3=copy.deepcopy(dysh3State_3Clk[1]))

        xtalk_simu_result = XtalkCalculator_instance01.calc_xtalk_level_hexTopoA(
            array_cw01=copy.deepcopy(arrayState_last),
            array_cw02=copy.deepcopy(arrayState_new),
            array_shield=copy.deepcopy(array_shieldState_tuple))

        assert len(xtalk_simu_result) == 12
        assert len(xtalk_simu_result[0]) == 9
        for row_kk in range(0, 12):
            for col_kk in range(0, 9):
                assert xtalk_simu_result[row_kk][col_kk] in (0, 0.25, 0.5, 0.75,
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
                                                             12)
                if TSVMapping_tuple[row_kk][col_kk][0] == 0:
                    cnt_xtalk_stsv[xtalk_simu_result[row_kk][col_kk]] = cnt_xtalk_stsv[
                                                                            xtalk_simu_result[row_kk][col_kk]] + 1

                elif TSVMapping_tuple[row_kk][col_kk][0] in (1, 2, 3):
                    cnt_xtalk_dtsv[xtalk_simu_result[row_kk][col_kk]] = cnt_xtalk_dtsv[
                                                                            xtalk_simu_result[row_kk][col_kk]] + 1

                else:
                    assert False

        arrayState_last = copy.deepcopy(arrayState_new)

        ##########################################
        # CLK 3
        arrayState_new = BSCACSimu_instance01.codewordsRemapping_getArrayState(
            unmappedState_stsvs=copy.deepcopy(signalBitsState_3Clk[2]),
            unmappedState_dysh1=copy.deepcopy(dysh1State_3Clk[2]),
            unmappedState_dysh2=copy.deepcopy(dysh2State_3Clk[2]),
            unmappedState_dysh3=copy.deepcopy(dysh3State_3Clk[2]))

        xtalk_simu_result = XtalkCalculator_instance01.calc_xtalk_level_hexTopoA(
            array_cw01=copy.deepcopy(arrayState_last),
            array_cw02=copy.deepcopy(arrayState_new),
            array_shield=copy.deepcopy(array_shieldState_tuple))

        assert len(xtalk_simu_result) == 12
        assert len(xtalk_simu_result[0]) == 9
        for row_kk in range(0, 12):
            for col_kk in range(0, 9):
                assert xtalk_simu_result[row_kk][col_kk] in (0, 0.25, 0.5, 0.75,
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
                                                             12)
                if TSVMapping_tuple[row_kk][col_kk][0] == 0:
                    cnt_xtalk_stsv[xtalk_simu_result[row_kk][col_kk]] = cnt_xtalk_stsv[
                                                                            xtalk_simu_result[row_kk][col_kk]] + 1

                elif TSVMapping_tuple[row_kk][col_kk][0] in (1, 2, 3):
                    cnt_xtalk_dtsv[xtalk_simu_result[row_kk][col_kk]] = cnt_xtalk_dtsv[
                                                                            xtalk_simu_result[row_kk][col_kk]] + 1

                else:
                    assert False

        arrayState_last = copy.deepcopy(arrayState_new)

        print("XTALK-STAVS: {}".format(cnt_xtalk_stsv))
        print("XTALK-DTSVS: {}".format(cnt_xtalk_dtsv))

    print("\n###########################################################################################################")
    print("###########################################################################################################")
    print("###########################################################################################################")
    print("XTALK-STAVS-FINAL: {}".format(cnt_xtalk_stsv))
    print("XTALK-DTSVS-FINAL: {}".format(cnt_xtalk_dtsv))






    # print('cnt_nSignalBitsTrans = {}'.format(cnt_nSignalBitsTrans))
    # nTSV_signal = len(BSCACSimu_instance01.get_signalBits_currentState())
    # nTSV_dysh1 = BSCACSimu_instance01.get_nDyShType1_notVirtual()
    # nTSV_dysh2 = BSCACSimu_instance01.get_nDyShType2_notVirtual()
    # nTSV_dysh3 = BSCACSimu_instance01.get_nDyShType3_notVirtual()
    # nTSV_dyshAll = nTSV_dysh1 + nTSV_dysh2 + nTSV_dysh3
    # nTSV_all = nTSV_signal + nTSV_dyshAll
    # bitOHCalc_nAll = nTSV_all * n_cycleRun * 3
    # bitOHCalc_nRedundant = bitOHCalc_nAll - (nTSV_dyshAll * n_cycleRun) - cnt_nSignalBitsTrans
    # bitOHCalc_OH = bitOHCalc_nRedundant / (bitOHCalc_nAll - bitOHCalc_nRedundant)
    # print('signal bits coding rate: {} / {} = {}'.format(cnt_nSignalBitsTrans, (nTSV_signal * 3 * n_cycleRun), (cnt_nSignalBitsTrans / (nTSV_signal * 3 * n_cycleRun))))
    # print("nTSV_all = {}, nTSV_dysh = ({}, {}, {}), nTSV_signal = {}, Cycle = {}, Bit Overhead = {} / {} = {}".format(nTSV_all, nTSV_dysh1, nTSV_dysh2, nTSV_dysh3, nTSV_signal, n_cycleRun, bitOHCalc_nRedundant, (bitOHCalc_nAll - bitOHCalc_nRedundant), bitOHCalc_OH))

########################################################################################################################
########################################################################################################################

########################################################################################################################
########################################################################################################################
# Get the sum of the number of transmitted bits in each case: old_state = listIdx, dataIn = All 0 ~ All 1;
# And then calculate the min / average / max bit overhead.
def calcNumberOfTransBitsOfSingle7bitGroup():
    '''
    Get the sum of the number of transmitted bits in each case: old_state = listIdx, dataIn = All 0 ~ All 1;
    And then calculate the min / average / max bit overhead.
    :return:
    '''
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    resultTuple_sumValue, resultTuple_minAndMax = BSCACAnalyze_instance01.get_nBitTransmittedCnt_matrixByOldState_singleGroup_oneClockPeriod()
    print("The sum of transmitted bits for each old_state: {}".format(resultTuple_sumValue))
    print("The min / max value of the sum of transmitted bits for each /'old_state + data_in/' case: {} / {}".format(resultTuple_minAndMax[0], resultTuple_minAndMax[1]))
    print("The min / max value of the sum of transmitted bits for each old_state: {} / {}".format(resultTuple_minAndMax[2], resultTuple_minAndMax[3]))
    result_average = resultTuple_minAndMax[4] / (2 ** 7)
    print("The value of the sum of transmitted bits for each old_state: {} / {} = {}".format(resultTuple_minAndMax[4], (2 ** 7), result_average))
    calcSignalBitCodingRate_lowest = (resultTuple_minAndMax[2] - (2 ** 7)) / ((2 ** 7) * 6)
    calcSignalBitCodingRate_highest = (resultTuple_minAndMax[3] - (2 ** 7)) / ((2 ** 7) * 6)
    calcSignalBitCodingRate_average = (result_average - (2 ** 7)) / ((2 ** 7) * 6)

    calcOH_lowest = (((2 ** 7) * 9) - resultTuple_minAndMax[3]) / (resultTuple_minAndMax[3])
    calcOH_highest = (((2 ** 7) * 9) - resultTuple_minAndMax[2]) / (resultTuple_minAndMax[2])
    calcOH_average = (((2 ** 7) * 9) - result_average) / (result_average)

    print("The coding rate of signal bits only: BEST={}, AVG={}, WORST={}".format(calcSignalBitCodingRate_highest,
                                                                                  calcSignalBitCodingRate_average,
                                                                                  calcSignalBitCodingRate_lowest))
    print("The bit overhead of inf array: BEST={}, AVG={}, WORST={}".format(calcOH_lowest,
                                                                            calcOH_average,
                                                                            calcOH_highest))

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

