########################################################################################################################
########################################################################################################################
# Description: Generating the VH files for FNS/IFNS-CAC codec designs
# Author: CWei
# Verion: 20241228
# Rexision:
########################################################################################################################
########################################################################################################################

import datetime
import math
import time

def genVH_FNS_HeaderFiles(codeword_maxLength: int, if_export_file=False, export_filePath=None):
    '''
    Generate the verilog code in the header file of FNS-CAC codec design.

    :param codeword_maxLength:
    :param export_filePath:
    :param if_export_file:
    :return:
    '''
    assert if_export_file in (True, False), "export_file"
    assert isinstance(codeword_maxLength, int) and (codeword_maxLength > 3)

    vhCodeLines_list = []
    note_timestring = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    if export_filePath is None:
        export_filePath = "exported_files/verilogCodeGen_ringCACCodec-{}.vh".format(note_timestring)

    vhCodeLines_list.append("// verilogCodeGen_ringCACCodec [ver = 20240219-01] [Creation Time = " + note_timestring + ']\n')
    vhCodeLines_list.append("// codeword_maxLength={}\n".format(codeword_maxLength))
    vhCodeLines_list.append("// ------------------------------\n")
    vhCodeLines_list.append("// ------------------------------\n")
    vhCodeLines_list.append("`ifndef __FNSCATF_HEADER__\n")
    vhCodeLines_list.append("    `define __FNSCATF_HEADER__\n")
    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("    // ------------------------------\n")
    vhCodeLines_list.append("    // VH_FNSCATF_DataInBitWidth\n")
    vhCodeLines_list.append("    // The value of VH_FNSCATF_DataInBitWidth_[i]bitCW is the max input data bitwidth of the encoder generating i-bit codeword. \n")
    vhCodeLines_list.append("    // For example: input wire [`VH_FNSCATF_DataInBitWidth_7bitCW - 1 : 0] datain\n")

    for cwLen_i in range(4, codeword_maxLength + 1):
        CodecRingCAC_i = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC_FNSBased(len_cw=cwLen_i)
        maxDecValue_i = CodecRingCAC_i.getParam_maxInputLimitation()
        maxInputBitWidth = math.floor(math.log2(maxDecValue_i))
        vhCodeLines_list.append("    `define VH_FNSCATF_DataInBitWidth_{}bitCW {}\n".format(cwLen_i, maxInputBitWidth))

    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("    // ---------------------------------\n")
    vhCodeLines_list.append("    // VH_FNSCATF_NSValue & VH_FNSCATF_NSValueMaxBinWidth\n")
    vhCodeLines_list.append("    // The value of VH_FNSCATF_NSValue_Pn is the number of the n-bit ATF (not CATF) codewords.\n")
    vhCodeLines_list.append("    // The value of VH_FNSCATF_NSValueMaxBinWidth_Pn is the bit-width of VH_FNSCATF_NSValue_P.\n")
    nsValue_a = 1
    nsValue_b = 1
    for cwLen_k in range(1, codeword_maxLength + 1):
        nsValue_c = nsValue_a + nsValue_b
        vhCodeLines_list.append("    `define VH_FNSCATF_NSValue_P{} {}\n".format(cwLen_k, nsValue_c))
        ns_valuec_binWidthCeil = math.ceil(math.log2(nsValue_c))
        vhCodeLines_list.append("    `define VH_FNSCATF_NSValueMaxBinWidth_P{} {}\n".format(cwLen_k, ns_valuec_binWidthCeil))
        nsValue_a = nsValue_b
        nsValue_b = nsValue_c

    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("`endif\n")


    if if_export_file is True:
        with open(export_filePath, 'w') as f:
            f.writelines(vhCodeLines_list)

        f.close()

    for codeLine_i in vhCodeLines_list:
        print(codeLine_i)
