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
if True:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    BSCACAnalyze_instance01.calcMuA_main()

