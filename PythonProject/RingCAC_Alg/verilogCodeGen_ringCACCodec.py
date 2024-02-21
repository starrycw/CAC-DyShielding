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

def vGen_FNSCATF_EncoderCore(codeword_bitwidth, if_export_file=False, export_filePath=None):
    '''
    Generate the verilog design of the FNSCATF-CAC encoder.

    :param codeword_bitwidth:
    :param if_export_file:
    :param export_filePath:
    :return:
    '''

    assert if_export_file in (True, False), "export_file"
    assert isinstance(codeword_bitwidth, int) and (codeword_bitwidth > 3)

    if codeword_bitwidth < 10:
        cwLenStr = '0' + str(codeword_bitwidth)
    else:
        cwLenStr = str(codeword_bitwidth)

    vhCodeLines_list = []
    note_timestring = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    if export_filePath is None:
        export_filePath = "exported_files/verilogCodeGen_FNSCATFEncoderCore{}-{}.v".format(codeword_bitwidth, note_timestring)

    vhCodeLines_list.append("`timescale 1ns / 1ps\n")
    vhCodeLines_list.append("//////////////////////////////////////////////////////////////////////////////////\n")
    vhCodeLines_list.append(
        "// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = " + note_timestring + ']\n')
    vhCodeLines_list.append("// The core logic of the FNS-CATF encoder.\n")
    vhCodeLines_list.append("// codeword_bitwidth={}\n".format(codeword_bitwidth))
    vhCodeLines_list.append("//////////////////////////////////////////////////////////////////////////////////\n")
    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("`include \"VHeader_FNSCATF.vh\"\n")
    vhCodeLines_list.append("\n")

    # Module Head
    vhCodeLines_list.append("module FNSCATF_encoder_core_{}(\n".format(codeword_bitwidth))
    vhCodeLines_list.append("    input [`VH_FNSCATF_DataInBitWidth_{}bitCW - 1 : 0] datain,\n".format(codeword_bitwidth))
    vhCodeLines_list.append("    output [{} : 0] codeout\n".format(codeword_bitwidth - 1))
    vhCodeLines_list.append("    );\n")
    vhCodeLines_list.append("\n")

    # var def
    vhCodeLines_list.append("    wire [{} : 0] q_out;\n".format(codeword_bitwidth - 1))
    vhCodeLines_list.append("\n")

    # MSB Block
    vhCodeLines_list.append("    // MSB\n")
    vhCodeLines_list.append("    wire [`VH_FNSCATF_NSValueMaxBinWidth_P{} - 1 : 0] res_block{};\n".format(codeword_bitwidth - 1,codeword_bitwidth - 1))
    vhCodeLines_list.append("    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_DataInBitWidth_{}bitCW), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P{}), .NS_VALUE(`VH_FNSCATF_NSValue_P{})) \n".format(
        codeword_bitwidth, codeword_bitwidth - 1, codeword_bitwidth - 1))
    vhCodeLines_list.append("        cmp_module{} (\n".format(codeword_bitwidth - 1))
    vhCodeLines_list.append("            .res_in(datain),\n")
    vhCodeLines_list.append("            .lock_in(1'b0),\n")
    vhCodeLines_list.append("            .q_out(q_out[{}]),\n".format(codeword_bitwidth - 1))
    vhCodeLines_list.append("            .res_out(res_block{})\n".format(codeword_bitwidth - 1))
    vhCodeLines_list.append("        );\n")
    vhCodeLines_list.append("    ///////////////////////////////////////////////////////////// \n")

    # The following 2 bits
    blockIdx_current = codeword_bitwidth - 2
    vhCodeLines_list.append("    // The following two bits\n")
    vhCodeLines_list.append("    wire [`VH_FNSCATF_NSValueMaxBinWidth_P{} - 1 : 0] res_block{};\n".format(blockIdx_current, blockIdx_current))
    vhCodeLines_list.append("    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P{}), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P{}), .NS_VALUE(`VH_FNSCATF_NSValue_P{})) \n".format(
        blockIdx_current + 1, blockIdx_current, blockIdx_current))
    vhCodeLines_list.append("        cmp_module{} (\n".format(blockIdx_current))
    vhCodeLines_list.append("            .res_in(res_block{}),\n".format(blockIdx_current + 1))
    vhCodeLines_list.append("            .lock_in(q_out[{}]),\n".format(blockIdx_current + 1))
    vhCodeLines_list.append("            .q_out(q_out[{}]),\n".format(blockIdx_current))
    vhCodeLines_list.append("            .res_out(res_block{})\n".format(blockIdx_current))
    vhCodeLines_list.append("        );\n")

    blockIdx_current = blockIdx_current - 1
    vhCodeLines_list.append("    wire [`VH_FNSCATF_NSValueMaxBinWidth_P{} - 1 : 0] res_block{};\n".format(blockIdx_current, blockIdx_current))
    vhCodeLines_list.append("    wire lock_{} = q_out[{}] | q_out[{}];\n".format(blockIdx_current + 1, blockIdx_current + 2, blockIdx_current + 1))
    vhCodeLines_list.append("    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P{}), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P{}), .NS_VALUE(`VH_FNSCATF_NSValue_P{})) \n".format(
            blockIdx_current + 1, blockIdx_current, blockIdx_current))
    vhCodeLines_list.append("        cmp_module{} (\n".format(blockIdx_current))
    vhCodeLines_list.append("            .res_in(res_block{}),\n".format(blockIdx_current + 1))
    vhCodeLines_list.append("            .lock_in(lock_{}),\n".format(blockIdx_current + 1))
    vhCodeLines_list.append("            .q_out(q_out[{}]),\n".format(blockIdx_current))
    vhCodeLines_list.append("            .res_out(res_block{})\n".format(blockIdx_current))
    vhCodeLines_list.append("        );\n")

    vhCodeLines_list.append("    ///////////////////////////////////////////////////////////// \n")

    # Other bits
    vhCodeLines_list.append("    // Other bits\n")
    for blockIdx_current in range(codeword_bitwidth - 4, 1, -1):
        vhCodeLines_list.append("    wire [`VH_FNSCATF_NSValueMaxBinWidth_P{} - 1 : 0] res_block{};\n".format(blockIdx_current, blockIdx_current))
        vhCodeLines_list.append("    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P{}), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P{}), .NS_VALUE(`VH_FNSCATF_NSValue_P{})) \n".format(
            blockIdx_current + 1, blockIdx_current, blockIdx_current))
        vhCodeLines_list.append("        cmp_module{} (\n".format(blockIdx_current))
        vhCodeLines_list.append("            .res_in(res_block{}),\n".format(blockIdx_current + 1))
        vhCodeLines_list.append("            .lock_in(q_out[{}]),\n".format(blockIdx_current + 1))
        vhCodeLines_list.append("            .q_out(q_out[{}]),\n".format(blockIdx_current))
        vhCodeLines_list.append("            .res_out(res_block{})\n".format(blockIdx_current))
        vhCodeLines_list.append("        );\n")
        vhCodeLines_list.append("\n")

    vhCodeLines_list.append("    ///////////////////////////////////////////////////////////////\n")
    vhCodeLines_list.append("\n")

    # Last cmp module
    vhCodeLines_list.append("    // Last cmp module\n")
    vhCodeLines_list.append("    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P2), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P1), .NS_VALUE(`VH_FNSCATF_NSValue_P1)) \n")
    vhCodeLines_list.append("        cmp_module1 (\n")
    vhCodeLines_list.append("            .res_in(res_block2),\n")
    vhCodeLines_list.append("            .lock_in(q_out[2]),\n")
    vhCodeLines_list.append("            .q_out(q_out[1]),\n")
    vhCodeLines_list.append("            .res_out(q_out[0])\n")
    vhCodeLines_list.append("        );\n")
    vhCodeLines_list.append("    ///////////////////////////////////////////////////////////////\n")
    vhCodeLines_list.append("\n")

    # Shift
    vhCodeLines_list.append("    // Shift\n")
    vhCodeLines_list.append("    assign codeout[{}] = q_out[{}];\n".format(codeword_bitwidth - 1, codeword_bitwidth - 1))
    vhCodeLines_list.append("    assign codeout[{} : 1] = (q_out[{}] == 1'b0)? (q_out[{} : 1]) : (q_out[{} : 0]);\n".format(
        codeword_bitwidth - 2, codeword_bitwidth - 1, codeword_bitwidth - 2, codeword_bitwidth - 3))
    vhCodeLines_list.append("    assign codeout[0] = (q_out[{}] == 1'b0)? (q_out[0]) : (1'b0);\n".format(codeword_bitwidth - 1))

    # Module End
    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("endmodule\n")


    if if_export_file is True:
        with open(export_filePath, 'w') as f:
            f.writelines(vhCodeLines_list)

        f.close()

    for codeLine_i in vhCodeLines_list:
        print(codeLine_i)

def vGen_FNSCATF_DecoderCore(codeword_bitwidth, if_export_file=False, export_filePath=None):
    '''
    Generate the verilog design of the FNSCATF-CAC decoder.

    :param codeword_bitwidth:
    :param if_export_file:
    :param export_filePath:
    :return:
    '''
    assert if_export_file in (True, False), "export_file"
    assert isinstance(codeword_bitwidth, int) and (codeword_bitwidth > 3)

    if codeword_bitwidth < 10:
        cwLenStr = '0' + str(codeword_bitwidth)
    else:
        cwLenStr = str(codeword_bitwidth)

    vhCodeLines_list = []
    note_timestring = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    if export_filePath is None:
        export_filePath = "exported_files/verilogCodeGen_FNSCATFDecoderCore{}-{}.v".format(codeword_bitwidth,
                                                                                        note_timestring)

    vhCodeLines_list.append("`timescale 1ns / 1ps\n")
    vhCodeLines_list.append("//////////////////////////////////////////////////////////////////////////////////\n")
    vhCodeLines_list.append(
        "// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = " + note_timestring + ']\n')
    vhCodeLines_list.append("// The core logic of the FNS-CATF decoder.\n")
    vhCodeLines_list.append("// codeword_bitwidth={}\n".format(codeword_bitwidth))
    vhCodeLines_list.append("//////////////////////////////////////////////////////////////////////////////////\n")
    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("`include \"VHeader_FNSCATF.vh\"\n")
    vhCodeLines_list.append("\n")

    # Module Head
    vhCodeLines_list.append("module FNSCATF_decoder_core_{}(\n".format(codeword_bitwidth))
    vhCodeLines_list.append(
        "    input [{} : 0] codein,\n".format(codeword_bitwidth - 1))
    vhCodeLines_list.append("    output [`VH_FNSCATF_DataInBitWidth_{}bitCW - 1 : 0] dataout\n".format(codeword_bitwidth))
    vhCodeLines_list.append("    );\n")
    vhCodeLines_list.append("\n")

    # Var def
    vhCodeLines_list.append("    wire [{} : 0] code_q;\n".format(codeword_bitwidth - 2))
    vhCodeLines_list.append("\n")

    # code_q
    vhCodeLines_list.append("    assign code_q[{} : 0] = (codein[{}] == 1'b0)? (codein[{} : 0]) : ({}1'b0, codein[{} : 1]{});\n".format(
        codeword_bitwidth - 2, codeword_bitwidth - 1, codeword_bitwidth - 2, "{", codeword_bitwidth - 2, "}"))

    # dataout
    vhCodeLines_list.append("    assign dataout = (codein[{}] * `VH_FNSCATF_NSValue_P{}) + \n".format(codeword_bitwidth - 1, codeword_bitwidth - 1))

    for idx_i in range(codeword_bitwidth - 2, 0, -1):
        vhCodeLines_list.append("                        (code_q[{}] * `VH_FNSCATF_NSValue_P{}) + \n".format(idx_i, idx_i))

    vhCodeLines_list.append("                        code_q[0];\n")
    vhCodeLines_list.append("\n")
    # Module End
    vhCodeLines_list.append("endmodule\n")


    if if_export_file is True:
        with open(export_filePath, 'w') as f:
            f.writelines(vhCodeLines_list)

        f.close()

    for codeLine_i in vhCodeLines_list:
        print(codeLine_i)


def svGen_tb_FNSCATF_CodecCore(codeword_bitwidth, if_export_file=False, export_filePath=None, n_simuCycle = 10000):
    '''
    Generate the tb of the FNSCATF-CAC codec core.

    :param codeword_bitwidth:
    :param if_export_file:
    :param export_filePath:
    :param n_simuCycle:
    :return:
    '''
    assert if_export_file in (True, False), "export_file"
    assert isinstance(codeword_bitwidth, int) and (codeword_bitwidth > 3)
    assert isinstance(n_simuCycle, int) and n_simuCycle >= 1

    if codeword_bitwidth < 10:
        cwLenStr = '0' + str(codeword_bitwidth)
    else:
        cwLenStr = str(codeword_bitwidth)

    vhCodeLines_list = []
    note_timestring = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    if export_filePath is None:
        export_filePath = "exported_files/verilogCodeGen_tb_FNSCATFCodecCore{}-{}.sv".format(codeword_bitwidth,
                                                                                        note_timestring)

    vhCodeLines_list.append("`timescale 1ns / 1ps\n")
    vhCodeLines_list.append("//////////////////////////////////////////////////////////////////////////////////\n")
    vhCodeLines_list.append(
        "// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = " + note_timestring + ']\n')
    vhCodeLines_list.append("// The testbench of the FNS-CATF encoder & decoder core.\n")
    vhCodeLines_list.append("// codeword_bitwidth={}\n".format(codeword_bitwidth))
    vhCodeLines_list.append("//////////////////////////////////////////////////////////////////////////////////\n")
    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("`include \"VHeader_FNSCATF.vh\"\n")
    vhCodeLines_list.append("\n")

    # Module header
    vhCodeLines_list.append("module tb_FNSCATF_codecCore{}(\n".format(codeword_bitwidth))
    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("    );\n")

    # param
    vhCodeLines_list.append("    parameter N_SIMU_CYCLE = {};\n".format(n_simuCycle))

    # instance
    vhCodeLines_list.append("    // {}-bit codec core\n".format(codeword_bitwidth))
    vhCodeLines_list.append("    wire [{} : 0] tsv_{};\n".format(codeword_bitwidth - 1, codeword_bitwidth))
    vhCodeLines_list.append("    reg [`VH_FNSCATF_DataInBitWidth_{}bitCW - 1 : 0] datain_{};\n".format(codeword_bitwidth, codeword_bitwidth))
    vhCodeLines_list.append("    wire [`VH_FNSCATF_DataInBitWidth_{}bitCW - 1 : 0] dataout_{};\n".format(codeword_bitwidth, codeword_bitwidth))

    vhCodeLines_list.append("    FNSCATF_encoder_core_{} encoder_instance{} (\n".format(codeword_bitwidth, codeword_bitwidth))
    vhCodeLines_list.append("        .datain(datain_{}),\n".format(codeword_bitwidth))
    vhCodeLines_list.append("        .codeout(tsv_{})\n".format(codeword_bitwidth))
    vhCodeLines_list.append("    );\n")
    vhCodeLines_list.append("\n")

    vhCodeLines_list.append("    FNSCATF_decoder_core_{} decoder_instance{} (\n".format(codeword_bitwidth, codeword_bitwidth))
    vhCodeLines_list.append("        .codein(tsv_{}),\n".format(codeword_bitwidth))
    vhCodeLines_list.append("        .dataout(dataout_{})\n".format(codeword_bitwidth))
    vhCodeLines_list.append("    );\n")
    vhCodeLines_list.append("\n")

    # simulation
    vhCodeLines_list.append("    static int cnt_i, cnt_err, cnt_pass, cnt_violate, idx_i;\n")
    vhCodeLines_list.append("\n")

    vhCodeLines_list.append("    initial begin\n")
    vhCodeLines_list.append("        for (cnt_i = 0; cnt_i < N_SIMU_CYCLE; cnt_i++) begin: for_cnt_i\n")
    vhCodeLines_list.append("            datain_{} = {} % (2**(`VH_FNSCATF_DataInBitWidth_{}bitCW));\n".format(codeword_bitwidth, "{$random}", codeword_bitwidth))
    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("            #1;\n")
    vhCodeLines_list.append("            if (dataout_{} != datain_{}) begin\n".format(codeword_bitwidth, codeword_bitwidth))
    vhCodeLines_list.append("                cnt_err = cnt_err + 1;\n")
    vhCodeLines_list.append("                $display(\"CODEC{}-%d-ERROR: %d -> %b -> %d\", cnt_i, datain_{}, tsv_{}, dataout_{});\n".format(
        codeword_bitwidth, codeword_bitwidth, codeword_bitwidth, codeword_bitwidth))
    vhCodeLines_list.append("            end\n")
    vhCodeLines_list.append("            else begin\n")
    vhCodeLines_list.append("                cnt_pass = cnt_pass + 1;\n")
    vhCodeLines_list.append("                $display(\"CODEC{}-%d-PASS: %d -> %b -> %d\", cnt_i, datain_{}, tsv_{}, dataout_{});\n".format(
            codeword_bitwidth, codeword_bitwidth, codeword_bitwidth, codeword_bitwidth))
    vhCodeLines_list.append("            end\n")

    vhCodeLines_list.append("            for (idx_i = 0; idx_i < {}; idx_i++) begin\n".format(codeword_bitwidth - 1))
    vhCodeLines_list.append("                if ( (tsv_{}[idx_i] != 0) && (tsv_{}[idx_i+1] != 0) ) begin\n".format(codeword_bitwidth, codeword_bitwidth))
    vhCodeLines_list.append("                    $display(\"---ERROR! CAC rule violated!---\");\n")
    vhCodeLines_list.append("                    cnt_violate = cnt_violate + 1;\n")
    vhCodeLines_list.append("                    $finish();\n")
    vhCodeLines_list.append("                end\n")
    vhCodeLines_list.append("                if ( (tsv_{}[{}] != 0) && (tsv_{}[0] != 0) ) begin\n".format(codeword_bitwidth, codeword_bitwidth - 1, codeword_bitwidth))
    vhCodeLines_list.append("                    $display(\"---ERROR! CAC rule violated!---\");\n")
    vhCodeLines_list.append("                    cnt_violate = cnt_violate + 1;\n")
    vhCodeLines_list.append("                    $finish();\n")

    vhCodeLines_list.append("                end\n")
    vhCodeLines_list.append("            end\n")
    vhCodeLines_list.append("\n")

    vhCodeLines_list.append("        end: for_cnt_i\n")
    vhCodeLines_list.append("\n")

    vhCodeLines_list.append("        $display(\"Finished! %d errors, %d ok, %d violate!\", cnt_err, cnt_pass, cnt_violate);\n")
    vhCodeLines_list.append("        $finish();\n")
    vhCodeLines_list.append("    end\n")
    vhCodeLines_list.append("\n")

    vhCodeLines_list.append("endmodule\n")

    if if_export_file is True:
        with open(export_filePath, 'w') as f:
            f.writelines(vhCodeLines_list)

        f.close()

    for codeLine_i in vhCodeLines_list:
        print(codeLine_i)






