`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_53]
// The top logic of the FNS-CATF encoder.
// codeword_bitwidth=11
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module FNSCATF_encoder_top_11(
    input wire clk,
    input wire rst_n,
    input wire [`VH_FNSCATF_DataInBitWidth_11bitCW - 1 : 0] datain,
    output reg [10 : 0] codeword_regs
    );

    wire [10 : 0] codeout;
    wire [10 : 0] codeword_new = codeword_regs[10 : 0] ^ codeout[10 : 0];

    FNSCATF_encoder_core_11 encoderCore_instance_11 (
        .datain(datain),
        .codeout(codeout)
    );
    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            codeword_regs[10 : 0] <= { 11{1'b0} };
        end
        else begin
            codeword_regs[10 : 0] <= codeword_new;
        end
    end
endmodule