`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/23 17:25:04
// Design Name: 
// Module Name: FTF_encoder_09
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


`include "FNS.vh"
module FTF_encoder_09(
    input wire [`FBLEN09 - 1 : 0] datain,
    input wire clock,
    input wire rst_n,
    output reg [8:0] codeout
    );
    
    //
    wire [8:0] code_wire;
    
    // get remaining value

    wire [`FRLEN08 - 1 : 0] r08;
    wire [`FRLEN07 - 1 : 0] r07;
    
    wire [`FRLEN06 - 1 : 0] r06;
    wire [`FRLEN05 - 1 : 0] r05;
    wire [`FRLEN04 - 1 : 0] r04;
    
    wire [`FRLEN03 - 1 : 0] r03;
    wire [`FRLEN02 - 1 : 0] r02;
    wire [`FRLEN01 - 1 : 0] r01;
    

    assign r08 = (code_wire[8] == 0) ? (datain) : (datain - `FNS09);
    assign r07 = (code_wire[7] == 0) ? (r08) : (r08 - `FNS08);
    assign r06 = (code_wire[06] == 0) ? (r07) : (r07 - `FNS07);
    
    assign r05 = (code_wire[05] == 0) ? (r06) : (r06 - `FNS06);
    assign r04 = (code_wire[04] == 0) ? (r05) : (r05 - `FNS05);
    assign r03 = (code_wire[03] == 0) ? (r04) : (r04 - `FNS04);
    
    assign r02 = (code_wire[02] == 0) ? (r03) : (r03 - `FNS03);
    assign r01 = (code_wire[01] == 0) ? (r02) : (r02 - `FNS02);
    
    //get code

    assign code_wire[8] = (datain >= `FNS09) ? (1) : (0);
    assign code_wire[7] = (r08 >= `FNS09) ? (1) : (0);
    assign code_wire[6] = (r07 >= `FNS07) ? (1) : (0);
    assign code_wire[5] = (r06 >= `FNS07) ? (1) : (0);
    assign code_wire[4] = (r05 >= `FNS05) ? (1) : (0);
    assign code_wire[3] = (r04 >= `FNS05) ? (1) : (0);
    assign code_wire[2] = (r03 >= `FNS03) ? (1) : (0);
    assign code_wire[1] = (r02 >= `FNS03) ? (1) : (0);
    assign code_wire[0] = r01;

    //sync
    always @(posedge clock or negedge rst_n) begin
        if (~rst_n) begin
            codeout <= 0;
        end
        else begin
            codeout <= code_wire;
        end
    end
    

endmodule
