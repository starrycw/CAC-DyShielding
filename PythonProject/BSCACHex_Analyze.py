import RingCAC_Alg.BitStuffingCAC_Analyze as BitStuffingCAC_Analyze

###################################################################
# Calculate the transition probability of single encoded group (7-bit codeword).
if True:
    msbFirst = True
    BSCACAnalyze_instance01 = BitStuffingCAC_Analyze.BitStuffingCAC_Analyze_HexArray(config_msbFirst=msbFirst)
    transProbMatrix = BSCACAnalyze_instance01.get_transProb_singleGroup_oneClockPeriod()
    check_ifpass, check_errlist = transProbMatrix.checkMatrix_transProb()
    print(transProbMatrix)
    print(check_ifpass,check_errlist)
    transProbMatrix.showMatrix_transProb(config_vmin=-0.05, config_dpi=500)
    transProbMatrix.showMatrix_transProb_timesN(n_int=(2**7), config_vmin=0, config_dpi=500)
