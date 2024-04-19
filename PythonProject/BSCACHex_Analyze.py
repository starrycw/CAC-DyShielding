import RingCAC_Alg.BitStuffingCAC_Analyze as BitStuffingCAC_Analyze

########################################################################################################################
# Calculate the transition probability of single encoded group (7-bit codeword).
if False:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    transProbMatrix = BSCACAnalyze_instance01.get_transProb_singleGroup_oneClockPeriod()
    check_ifpass, check_errlist = transProbMatrix.checkMatrix()
    print(transProbMatrix)
    print(check_ifpass,check_errlist)
    transProbMatrix.showMatrix_main(config_vmin=-0.05, config_dpi=500)
    transProbMatrix.showMatrix_mainTimesN(n_int=(2**7), config_vmin=0, config_dpi=500)

########################################################################################################################
# Calculate the transition cnt of single encoded group (7-bit codeword).
if False:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    transCntMatrix = BSCACAnalyze_instance01.get_transCnt_singleGroup_oneClockPeriod()
    check_ifpass, check_errlist = transCntMatrix.checkMatrix()
    print(transCntMatrix)
    print(check_ifpass,check_errlist)
    transCntMatrix.showMatrix_main(config_vmin=-0.05, config_dpi=500)

########################################################################################################################
# Calc \mu_a
# if False:
#     msbFirst = True
#     BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
#     BSCACAnalyze_instance01.calcMuA_main()

########################################################################################################################
# Calc Matrix Q & Matrix B
if False:
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

########################################################################################################################
# Calc matrix BQ
if False:
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

########################################################################################################################
# Calc \mu_a by BQ - Simplified! Basic constraint!
if False:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    BSCACAnalyze_instance01.calcMuASimplified_useMatrixBQ_main(constraintSet='basic')

########################################################################################################################
# Calc \mu_a by BQ - Simplified! Full constraint!
if False:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    BSCACAnalyze_instance01.calcMuASimplified_useMatrixBQ_main(constraintSet='full')

########################################################################################################################
# Calc matrix C
if False:
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
# Calc \mu_a by CQ - Simplified! Basic constraint!
if False:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    BSCACAnalyze_instance01.calcMuASimplified_useMatrixCQ_main(constraintSet='basic')

########################################################################################################################
# Calc \mu_a by CQ - Simplified! Full constraint!
if False:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    BSCACAnalyze_instance01.calcMuASimplified_useMatrixCQ_main(constraintSet='full')

########################################################################################################################
# Coding rate simulation - HexArray-RegularA-11x8
if True:
    n_cycleRun = 1000
    BSCACSimu_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Simulation_HexArray(arrayType="Hex_RegularA_11x8")
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
    nTSV_dysh1 = 6
    nTSV_dysh2 = 6
    nTSV_dysh3 = 6
    nTSV_dyshAll = nTSV_dysh1 + nTSV_dysh2 + nTSV_dysh3
    nTSV_all = nTSV_signal + nTSV_dyshAll
    bitOHCalc_nAll = nTSV_all * n_cycleRun * 3
    bitOHCalc_nRedundant = bitOHCalc_nAll - (nTSV_dyshAll * n_cycleRun) - cnt_nSignalBitsTrans
    bitOHCalc_OH = bitOHCalc_nRedundant / (bitOHCalc_nAll - bitOHCalc_nRedundant)
    print('signal bits coding rate: {} / {} = {}'.format(cnt_nSignalBitsTrans, (nTSV_signal * 3 * n_cycleRun), (cnt_nSignalBitsTrans / (nTSV_signal * 3 * n_cycleRun))))
    print("nTSV_all = {}, Cycle = {}, Bit Overhead = {} / {} = {}".format(nTSV_all, n_cycleRun, bitOHCalc_nRedundant, (bitOHCalc_nAll - bitOHCalc_nRedundant), bitOHCalc_OH))

