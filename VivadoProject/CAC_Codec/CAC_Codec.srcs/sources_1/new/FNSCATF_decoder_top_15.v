`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_54]
// The top logic of the FNS-CATF decoder.
// codeword_bitwidth=15
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module FNSCATF_decoder_top_15(
    input wire clk,
    input wire rst_n,
    input wire [14 : 0] codeword_in,
    output reg [`VH_FNSCATF_DataInBitWidth_15bitCW - 1 : 0] data_reg
    );

    reg [14 : 0] code_reg;
    wire [14 : 0] code_in = code_reg[14 : 0] ^ codeword_in[14 : 0];
    wire [`VH_FNSCATF_DataInBitWidth_15bitCW - 1 : 0] data_out;

    FNSCATF_decoder_core_15 docoderCore_instance_15 (
        .codein(code_in),
        .dataout(data_out)
    );

    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            data_reg[`VH_FNSCATF_DataInBitWidth_15bitCW - 1 : 0] <= { `VH_FNSCATF_DataInBitWidth_15bitCW{1'b0} };
            code_reg[14 : 0] <= { 14{1'b0} };
        end
        else begin
            data_reg <= data_out;
            code_reg <= codeword_in;
        end
    end

endmodule