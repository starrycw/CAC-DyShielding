# Calculate and compare the bit overhead of CAC algorithms.
import math

import matplotlib.pyplot as plt

import OtherCAC_Alg.FNSCAC_Codec as FNSCAC_Codec
import RingCAC_Alg.Ring2CTransCAC_Codec as FNSCATFCAC_Codec


###########################################################
###########################################################
# FNS-CAC Overhead
###########################################################
def getCACBitOverhead_FNS(n_cw):
    '''
    Get the bit overhead of the FNS-CAC algorithm.

    :param n_cw: The bit-width of the codeword.
    :return: int
    '''
    assert isinstance(n_cw, int) and n_cw > 3
    fns_seq_tuple, fns_seq_sum = FNSCAC_Codec.FNSCAC_Codec.getFNSSeq(seq_length=n_cw)
    cw_maxValue_bitWidth = math.floor(math.log2(fns_seq_sum + 1))

    return cw_maxValue_bitWidth

###########################################################
###########################################################
# IFNS-CAC Overhead
###########################################################
def getCACBitOverhead_IFNS(n_cw):
    '''
    Get the bit overhead of the IFNS CAC.
    
    :param n_cw: The bit-width of the codeword.
    :return: int
    '''
    assert isinstance(n_cw, int) and n_cw > 3
    fns_seq_tuple, fns_seq_sum = FNSCAC_Codec.FNSCAC_Codec.getFNSSeq(seq_length = (n_cw + 1))
    ifns_sum = fns_seq_sum - fns_seq_tuple[-2]
    cw_maxValue_bitWidth = math.floor(math.log2(ifns_sum + 1))

    return cw_maxValue_bitWidth

###########################################################
###########################################################
# FNS-CATF-CAC Overhead
###########################################################
def getCACBitOverhead_FNSCATF(n_cw):
    '''
    Get the bit overhead of the FNS-CATF algorithm.
    :param n_cw: The bit-width of the codeword.
    :return: int
    '''
    assert isinstance(n_cw, int) and n_cw > 3
    FNSCATF_CodecInstance = FNSCATFCAC_Codec.Codec_Ring2CTransCAC_FNSBased(len_cw=n_cw)
    cw_maxValue_dec = FNSCATF_CodecInstance.getParam_maxInputLimitation()
    cw_maxValue_bitWidth = math.floor(math.log2(cw_maxValue_dec + 1))

    return cw_maxValue_bitWidth

########################################################################################################################
###########################################################
########################## MAIN ###########################
###########################################################
# CACName_List - FNS, IFNS, FNSCATF
CACName_list = ['FNS', 'IFNS', 'FNSCATF']
CACCodewordLen_min = 4
CACCodewordLen_max = 50

FNSCATF_betterCodewordLength = []
FNSCATF_bestCodewordLength = []

CAC_CodewordLen_list = []
CAC_InputDataBit_list = []
CAC_BitOverhead_list = []
for CACName_i in CACName_list:
    CAC_InputDataBit_list.append([])
    CAC_BitOverhead_list.append([])

for cw_len_i in range(CACCodewordLen_min, CACCodewordLen_max + 1):
    CAC_CodewordLen_list.append(cw_len_i)
    for CACIdx_i in range(0, len(CACName_list)):
        if CACName_list[CACIdx_i] == "FNS":
            maxDatainLen = getCACBitOverhead_FNS(n_cw=cw_len_i)
        elif CACName_list[CACIdx_i] == "IFNS":
            maxDatainLen = getCACBitOverhead_IFNS(n_cw=cw_len_i)
        elif CACName_list[CACIdx_i] == "FNSCATF":
            maxDatainLen = getCACBitOverhead_FNSCATF(n_cw=cw_len_i)
        else:
            assert False
        CAC_InputDataBit_list[CACIdx_i].append(maxDatainLen)
        CAC_BitOverhead_list[CACIdx_i].append( (cw_len_i - maxDatainLen) / maxDatainLen )

    if CAC_InputDataBit_list[2][-1] >= CAC_InputDataBit_list[0][-1]:
        FNSCATF_betterCodewordLength.append(cw_len_i)
    if CAC_InputDataBit_list[2][-1] >= CAC_InputDataBit_list[1][-1]:
        FNSCATF_bestCodewordLength.append(cw_len_i)


plt.figure()
for CACIdx_i in range(0, len(CACName_list)):
    plt.plot(CAC_CodewordLen_list, CAC_InputDataBit_list[CACIdx_i], label=CACName_list[CACIdx_i])

plt.rcParams.update({"font.size": 16})

plt.legend()
plt.xlabel("Codeword bit-width (bit)", fontsize=16)
plt.ylabel("Bit-width of input data (bit)", fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.savefig("exported_files/CAC_dataInBitWidth.png", bbox_inches='tight', dpi=300)

plt.figure()
for CACIdx_i in range(0, len(CACName_list)):
    plt.plot(CAC_CodewordLen_list, CAC_BitOverhead_list[CACIdx_i], label=CACName_list[CACIdx_i])

plt.rcParams.update({"font.size": 16})

plt.legend()
plt.xlabel("Codeword bit-width (bit)", fontsize=16)
plt.ylabel("Bit overhead", fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# plt.tight_layout(pad=1.08)
plt.savefig("exported_files/CAC_bitOverhead.png", bbox_inches="tight", dpi=300)
plt.show()

print("OH(FNSCATF)==OH(FNS): {}".format(FNSCATF_betterCodewordLength))
print("OH(FNSCATF)==OH(IFNS): {}".format(FNSCATF_bestCodewordLength))




