`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/20 16:08:04
// Design Name: 
// Module Name: FNSCATF_decoder_core_07
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module FNSCATF_decoder_core_07(
    input wire [6 : 0] codein,
    output wire [`VH_FNSCATF_DataInBitWidth_7bitCW - 1 : 0] dataout
    );

    wire [5 : 0] code_q;

    assign code_q[5 : 0] = (codein[6] == 1'b0)? (codein[5 : 0]) : ({1'b0, codein[5 : 1]});

    assign dataout = (codein[6] * `VH_FNSCATF_NSValue_P6) + 
                        (code_q[5] * `VH_FNSCATF_NSValue_P5) + 
                        (code_q[4] * `VH_FNSCATF_NSValue_P4) + 
                        (code_q[3] * `VH_FNSCATF_NSValue_P3) + 
                        (code_q[2] * `VH_FNSCATF_NSValue_P2) + 
                        (code_q[1] * `VH_FNSCATF_NSValue_P1) + 
                        code_q[0];

endmodule
