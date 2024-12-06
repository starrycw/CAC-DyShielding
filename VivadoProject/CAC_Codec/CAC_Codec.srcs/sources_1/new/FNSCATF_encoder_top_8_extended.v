`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/12/06 16:24:35
// Design Name: 
// Module Name: FNSCATF_encoder_top_8_extended
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

module FNSCATF_encoder_top_8_extended(
    input wire clk,
    input wire rst_n,
    input wire [`VH_FNSCATF_DataInBitWidth_8bitCW : 0] datain,
    output reg [7 : 0] codeword_regs
    );

    wire [7 : 0] codeout;
    wire [7 : 0] codeword_new = codeword_regs[7 : 0] ^ codeout[7 : 0];

    FNSCATF_encoder_core_8_extended encoderCore_instance_8 (
        .datain(datain),
        .codeout(codeout)
    );
    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            codeword_regs[7 : 0] <= { 8{1'b0} };
        end
        else begin
            codeword_regs[7 : 0] <= codeword_new;
        end
    end
endmodule
