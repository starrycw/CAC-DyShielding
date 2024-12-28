########################################################################################################################
########################################################################################################################
# Description: Generating the VH files for FNS/IFNS-CAC codec designs
# Author: CWei
# Verion: 20241228
# Revision:
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
        export_filePath = "exported_files/Header_FNS-{}.vh".format(note_timestring)

    vhCodeLines_list.append("/////////////////////////////////////////////////////////////////////////////////")
    vhCodeLines_list.append("// ################################# DesignGen #################################\n")
    vhCodeLines_list.append("// ######################## https://github.com/starrycw ########################")
    vhCodeLines_list.append("// #############################################################################")
    vhCodeLines_list.append("// ### Description: VH file for FNS-CAC codec designs")
    vhCodeLines_list.append("// ### Script Version: 2024.12.28.01")
    vhCodeLines_list.append("// ### Script Revision: ")
    vhCodeLines_list.append("// ###  ")
    vhCodeLines_list.append("// ### Creation Time: "+ note_timestring)
    vhCodeLines_list.append("// ### Parameters: ")
    vhCodeLines_list.append("// ###### codeword_maxLength = {}".format(codeword_maxLength))
    vhCodeLines_list.append("// #############################################################################")
    vhCodeLines_list.append("/////////////////////////////////////////////////////////////////////////////////")

    vhCodeLines_list.append("`ifndef __HEADER_FNS__\n")
    vhCodeLines_list.append("    `define __HEADER_FNS__\n")
    vhCodeLines_list.append("\n")

    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("    `define FNS_Value_1 1\n")
    vhCodeLines_list.append("    `define FNS_DataBW_1 1\n")
    vhCodeLines_list.append("    `define FNS_ResBW_1 1\n")

    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("    `define FNS_Value_2 1\n")
    vhCodeLines_list.append("    `define FNS_DataBW_2 1\n")
    vhCodeLines_list.append("    `define FNS_ResBW_2 1\n")

    for idx_i in range()





    vhCodeLines_list.append("\n")
    vhCodeLines_list.append("`endif\n")


    if if_export_file is True:
        with open(export_filePath, 'w') as f:
            f.writelines(vhCodeLines_list)

        f.close()

    for codeLine_i in vhCodeLines_list:
        print(codeLine_i)
