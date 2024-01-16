# For generating some verilog codes
import datetime
import math
import time

import RingCAC_Alg.Ring2CTransCAC_Codec

def vhGen_FNSCATF_HeaderFiles(codeword_maxLength: int, if_export_file=False, export_filePath=None):
    '''
    Generate the verilog code in the header file of FNS-CATF codec design.

    :param codeword_maxLength:
    :param export_filePath:
    :param if_export_file:
    :return:
    '''
    assert if_export_file in (True, False), "export_file"
    assert isinstance(codeword_maxLength, int) and (codeword_maxLength > 3)

    vhCodeLines_list = []
    note_timestring = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if export_filePath is None:
        export_filePath = "exported_files/verilogCodeGen_ringCACCodec_{}.vh".format(note_timestring)
    vhCodeLines_list.append("// verilogCodeGen_ringCACCodec ver.202401.01: " + note_timestring + '\n')
    vhCodeLines_list.append("// codeword_maxLength={}\n".format(codeword_maxLength))
    vhCodeLines_list.append("// ------------------------------\n")
    vhCodeLines_list.append("// ------------------------------\n")
    vhCodeLines_list.append("// VAR_FNSCATF_DataInBitWidth\n")

    for cwLen_i in (4, codeword_maxLength):
        CodecRingCAC_i = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC_FNSBased(len_cw=cwLen_i)
        maxDecValue_i = CodecRingCAC_i.getParam_maxInputLimitation()
        maxInputBitWidth = math.floor(math.log2(maxDecValue_i))







    if if_export_file is True:
        with open(export_filePath, 'w') as f:
            f.writelines(vhCodeLines_list)

        f.close()
