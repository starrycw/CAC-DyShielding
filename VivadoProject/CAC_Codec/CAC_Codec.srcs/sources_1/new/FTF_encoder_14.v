`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/23 17:25:04
// Design Name: 
// Module Name: FTF_encoder_14
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
module FTF_encoder_14(
    input wire [`FBLEN14 - 1 : 0] datain,
    input wire clock,
    input wire rst_n,
    output reg [13:0] codeout
    );
    
    //
    wire [13:0] code_wire;
    
    // get remaining value

    wire [`FRLEN13 - 1 : 0] r13;
    wire [`FRLEN12 - 1 : 0] r12;
    wire [`FRLEN11 - 1 : 0] r11;
    wire [`FRLEN10 - 1 : 0] r10;
    
    wire [`FRLEN09 - 1 : 0] r09;
    wire [`FRLEN08 - 1 : 0] r08;
    wire [`FRLEN07 - 1 : 0] r07;
    
    wire [`FRLEN06 - 1 : 0] r06;
    wire [`FRLEN05 - 1 : 0] r05;
    wire [`FRLEN04 - 1 : 0] r04;
    
    wire [`FRLEN03 - 1 : 0] r03;
    wire [`FRLEN02 - 1 : 0] r02;
    wire [`FRLEN01 - 1 : 0] r01;
    


    assign r13 = (code_wire[13] == 0) ? (datain) : (datain - `FNS14);
    
    assign r12 = (code_wire[12] == 0) ? (r13) : (r13 - `FNS13);
    
    assign r11 = (code_wire[11] == 0) ? (r12) : (r12 - `FNS12);
    assign r10 = (code_wire[10] == 0) ? (r11) : (r11 - `FNS11);
    assign r09 = (code_wire[09] == 0) ? (r10) : (r10 - `FNS10);
    
    assign r08 = (code_wire[08] == 0) ? (r09) : (r09 - `FNS09);
    assign r07 = (code_wire[07] == 0) ? (r08) : (r08 - `FNS08);
    assign r06 = (code_wire[06] == 0) ? (r07) : (r07 - `FNS07);
    
    assign r05 = (code_wire[05] == 0) ? (r06) : (r06 - `FNS06);
    assign r04 = (code_wire[04] == 0) ? (r05) : (r05 - `FNS05);
    assign r03 = (code_wire[03] == 0) ? (r04) : (r04 - `FNS04);
    
    assign r02 = (code_wire[02] == 0) ? (r03) : (r03 - `FNS03);
    assign r01 = (code_wire[01] == 0) ? (r02) : (r02 - `FNS02);
    
    //get code

    assign code_wire[13] = (datain >= `FNS15) ? (1) : (0);
    assign code_wire[12] = (r13 >= `FNS13) ? (1) : (0);
    assign code_wire[11] = (r12 >= `FNS13) ? (1) : (0);
    assign code_wire[10] = (r11 >= `FNS11) ? (1) : (0);
    assign code_wire[9] = (r10 >= `FNS11) ? (1) : (0);
    assign code_wire[8] = (r09 >= `FNS09) ? (1) : (0);
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
