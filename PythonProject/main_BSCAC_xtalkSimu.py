import FNSCATFCAC_xtalkSimuInArray as FNSCATFCAC_xtalkSimuInArray
import BSCACHex_Analyze as BSCACHex_Analyze

n_simuCycle = 1000
edgeTSVXtalkZoom = 1
edgeTSVPunishment = 0

########################################################################################################################
# BSCAC - 12x9 Hex Array
if True:
    BSCACHex_Analyze.simulation_xtalkSimu_HexArrayRegularA_18x12(n_cycleRun=n_simuCycle,
                                                                 edgeTSVXtalkZoom=edgeTSVXtalkZoom,
                                                                 edgeTSVPunishment=edgeTSVPunishment)

