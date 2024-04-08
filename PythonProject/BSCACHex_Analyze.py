import RingCAC_Alg.BitStuffingCAC_Analyze as BitStuffingCAC_Analyze

###################################################################
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

###################################################################
# Calculate the transition cnt of single encoded group (7-bit codeword).
if False:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    transCntMatrix = BSCACAnalyze_instance01.get_transCnt_singleGroup_oneClockPeriod()
    check_ifpass, check_errlist = transCntMatrix.checkMatrix()
    print(transCntMatrix)
    print(check_ifpass,check_errlist)
    transCntMatrix.showMatrix_main(config_vmin=-0.05, config_dpi=500)

####################################################################
# Calc \mu_a
if False:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    BSCACAnalyze_instance01.calcMuA_main()

####################################################################
# Calc Matrix Q & Matrix B
if True:
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


