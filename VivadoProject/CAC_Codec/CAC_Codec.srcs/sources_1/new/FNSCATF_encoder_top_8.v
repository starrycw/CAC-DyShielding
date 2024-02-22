`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_53]
// The top logic of the FNS-CATF encoder.
// codeword_bitwidth=8
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module FNSCATF_encoder_top_8(
    input wire clk,
    input wire rst_n,
    input wire [`VH_FNSCATF_DataInBitWidth_8bitCW - 1 : 0] datain,
    output reg [7 : 0] codeword_regs
    );

    wire [7 : 0] codeout;
    wire [7 : 0] codeword_new = codeword_regs[7 : 0] ^ codeout[7 : 0];

    FNSCATF_encoder_core_8 encoderCore_instance_8 (
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