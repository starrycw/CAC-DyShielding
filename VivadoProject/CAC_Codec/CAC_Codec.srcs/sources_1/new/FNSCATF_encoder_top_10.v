`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_53]
// The top logic of the FNS-CATF encoder.
// codeword_bitwidth=10
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module FNSCATF_encoder_top_10(
    input wire clk,
    input wire rst_n,
    input wire [`VH_FNSCATF_DataInBitWidth_10bitCW - 1 : 0] datain,
    output reg [9 : 0] codeword_regs
    );

    wire [9 : 0] codeout;
    wire [9 : 0] codeword_new = codeword_regs[9 : 0] ^ codeout[9 : 0];

    FNSCATF_encoder_core_10 encoderCore_instance_10 (
        .datain(datain),
        .codeout(codeout)
    );
    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            codeword_regs[9 : 0] <= { 10{1'b0} };
        end
        else begin
            codeword_regs[9 : 0] <= codeword_new;
        end
    end
endmodule