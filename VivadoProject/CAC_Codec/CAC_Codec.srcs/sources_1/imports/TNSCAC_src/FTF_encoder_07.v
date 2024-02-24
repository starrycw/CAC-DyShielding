`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/05/13 16:32:44
// Design Name: 
// Module Name: FTF_encoder_07
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
module FTF_encoder_07(
    input wire [`FBLEN07 - 1 : 0] datain,
    input wire clock,
    input wire rst_n,
    output reg [6:0] codeout
    );
    
    //
    wire [6:0] code_wire;
    
    // get remaining value

    wire [`FRLEN06 - 1 : 0] r06;
    wire [`FRLEN05 - 1 : 0] r05;
    wire [`FRLEN04 - 1 : 0] r04;
    
    wire [`FRLEN03 - 1 : 0] r03;
    wire [`FRLEN02 - 1 : 0] r02;
    wire [`FRLEN01 - 1 : 0] r01;
    

    assign r06 = (code_wire[06] == 0) ? (datain) : (datain - `FNS07);
    
    assign r05 = (code_wire[05] == 0) ? (r06) : (r06 - `FNS06);
    assign r04 = (code_wire[04] == 0) ? (r05) : (r05 - `FNS05);
    assign r03 = (code_wire[03] == 0) ? (r04) : (r04 - `FNS04);
    
    assign r02 = (code_wire[02] == 0) ? (r03) : (r03 - `FNS03);
    assign r01 = (code_wire[01] == 0) ? (r02) : (r02 - `FNS02);
    
    //get code

    assign code_wire[6] = (datain >= `FNS07) ? (1) : (0);
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
