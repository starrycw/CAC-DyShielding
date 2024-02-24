`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/23 17:25:04
// Design Name: 
// Module Name: FTF_encoder_05
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
module FTF_encoder_05(
    input wire [`FBLEN05 - 1 : 0] datain,
    input wire clock,
    input wire rst_n,
    output reg [4:0] codeout
    );
    
    //
    wire [4:0] code_wire;
    
    // get remaining value

    wire [`FRLEN04 - 1 : 0] r04;
    wire [`FRLEN03 - 1 : 0] r03;
    wire [`FRLEN02 - 1 : 0] r02;
    wire [`FRLEN01 - 1 : 0] r01;
    

    assign r04 = (code_wire[04] == 0) ? (datain) : (datain - `FNS05);
    
    assign r03 = (code_wire[03] == 0) ? (r04) : (r04 - `FNS04);
    
    assign r02 = (code_wire[02] == 0) ? (r03) : (r03 - `FNS03);
    assign r01 = (code_wire[01] == 0) ? (r02) : (r02 - `FNS02);
    
    //get code

    assign code_wire[4] = (datain >= `FNS05) ? (1) : (0);
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
