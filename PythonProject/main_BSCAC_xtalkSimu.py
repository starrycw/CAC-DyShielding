import FNSCATFCAC_xtalkSimuInArray as FNSCATFCAC_xtalkSimuInArray
import BSCACHex_Analyze as BSCACHex_Analyze

n_simuCycle = 1000
edgeTSVXtalkZoom = 1
edgeTSVPunishment = 0

########################################################################################################################
# BSCAC - 12x9 Hex Array
if False:
    BSCACHex_Analyze.simulation_xtalkSimu_HexArrayRegularA_18x12(n_cycleRun=n_simuCycle,
                                                                 edgeTSVXtalkZoom=edgeTSVXtalkZoom,
                                                                 edgeTSVPunishment=edgeTSVPunishment)

########################################################################################################################
# NoCAC - 12x9 Hex Array
if False:
    simu_instance01 = FNSCATFCAC_xtalkSimuInArray.FNSCATF_xtalkSimu()
    simu_instance01.runSimu_12x9HexArray_NoCAC(n_cycle=n_simuCycle,
                                               edgeEffect_hexWeight=edgeTSVXtalkZoom,
                                               edgeEffect_hexPunishment=edgeTSVPunishment)

########################################################################################################################
# FNS-FPF - 12x9 Hex Array
if False:
    simu_instance01 = FNSCATFCAC_xtalkSimuInArray.FNSCATF_xtalkSimu()
    simu_instance01.runSimu_12x9HexArray_RowByRow(n_cycle=n_simuCycle,
                                                  CAC_name='FNS-FPF',
                                                  edgeEffect_hexWeight=edgeTSVXtalkZoom,
                                                  edgeEffect_hexPunishment=edgeTSVPunishment)

########################################################################################################################
# FNS-FTF - 12x9 Hex Array
if True:
    simu_instance01 = FNSCATFCAC_xtalkSimuInArray.FNSCATF_xtalkSimu()
    simu_instance01.runSimu_12x9HexArray_RowByRow(n_cycle=n_simuCycle,
                                                  CAC_name='FNS-FTF',
                                                  edgeEffect_hexWeight=edgeTSVXtalkZoom,
                                                  edgeEffect_hexPunishment=edgeTSVPunishment)