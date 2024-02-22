`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_54]
// The top logic of the FNS-CATF encoder.
// codeword_bitwidth=16
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module FNSCATF_encoder_top_16(
    input wire clk,
    input wire rst_n,
    input wire [`VH_FNSCATF_DataInBitWidth_16bitCW - 1 : 0] datain,
    output reg [15 : 0] codeword_regs
    );

    wire [15 : 0] codeout;
    wire [15 : 0] codeword_new = codeword_regs[15 : 0] ^ codeout[15 : 0];

    FNSCATF_encoder_core_16 encoderCore_instance_16 (
        .datain(datain),
        .codeout(codeout)
    );
    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            codeword_regs[15 : 0] <= { 16{1'b0} };
        end
        else begin
            codeword_regs[15 : 0] <= codeword_new;
        end
    end
endmodule