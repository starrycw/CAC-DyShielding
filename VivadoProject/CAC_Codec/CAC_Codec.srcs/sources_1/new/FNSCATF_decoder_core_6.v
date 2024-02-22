`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_53]
// The core logic of the FNS-CATF decoder.
// codeword_bitwidth=6
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module FNSCATF_decoder_core_6(
    input wire [5 : 0] codein,
    output wire [`VH_FNSCATF_DataInBitWidth_6bitCW - 1 : 0] dataout
    );

    wire [4 : 0] code_q;

    assign code_q[4 : 0] = (codein[5] == 1'b0)? (codein[4 : 0]) : ({1'b0, codein[4 : 1]});
    assign dataout = (codein[5] * `VH_FNSCATF_NSValue_P5) + 
                        (code_q[4] * `VH_FNSCATF_NSValue_P4) + 
                        (code_q[3] * `VH_FNSCATF_NSValue_P3) + 
                        (code_q[2] * `VH_FNSCATF_NSValue_P2) + 
                        (code_q[1] * `VH_FNSCATF_NSValue_P1) + 
                        code_q[0];

endmodule
