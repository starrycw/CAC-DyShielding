`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_54]
// The top logic of the FNS-CATF encoder.
// codeword_bitwidth=14
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module FNSCATF_encoder_top_14(
    input wire clk,
    input wire rst_n,
    input wire [`VH_FNSCATF_DataInBitWidth_14bitCW - 1 : 0] datain,
    output reg [13 : 0] codeword_regs
    );

    wire [13 : 0] codeout;
    wire [13 : 0] codeword_new = codeword_regs[13 : 0] ^ codeout[13 : 0];

    FNSCATF_encoder_core_14 encoderCore_instance_14 (
        .datain(datain),
        .codeout(codeout)
    );
    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            codeword_regs[13 : 0] <= { 14{1'b0} };
        end
        else begin
            codeword_regs[13 : 0] <= codeword_new;
        end
    end
endmodule