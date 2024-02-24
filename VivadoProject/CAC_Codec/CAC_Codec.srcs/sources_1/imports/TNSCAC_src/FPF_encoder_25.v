`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/06/06 15:47:52
// Design Name: 
// Module Name: FPF_encoder_25
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
module FPF_encoder_25(
    input wire [`FBLEN25 - 1 : 0] datain,
    input wire clock,
    input wire rst_n,
    output reg [24:0] codeout
    );
    
    //
    wire [24:0] code_wire;
    
    // get remaining value
    wire [`FRLEN24 - 1 : 0] r24;
    wire [`FRLEN23 - 1 : 0] r23;
    wire [`FRLEN22 - 1 : 0] r22;
    
    wire [`FRLEN21 - 1 : 0] r21;
    wire [`FRLEN20 - 1 : 0] r20;
    wire [`FRLEN19 - 1 : 0] r19;
    
    wire [`FRLEN18 - 1 : 0] r18;
    wire [`FRLEN17 - 1 : 0] r17;
    wire [`FRLEN16 - 1 : 0] r16;
    
    wire [`FRLEN15 - 1 : 0] r15;
    wire [`FRLEN14 - 1 : 0] r14;
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
    

    assign r24 = (code_wire[24] == 0) ? (datain) : (datain - `FNS25);
    
    assign r23 = (code_wire[23] == 0) ? (r24) : (r24 - `FNS24);
    assign r22 = (code_wire[22] == 0) ? (r23) : (r23 - `FNS23);
    assign r21 = (code_wire[21] == 0) ? (r22) : (r22 - `FNS22);
    
    assign r20 = (code_wire[20] == 0) ? (r21) : (r21 - `FNS21);
    assign r19 = (code_wire[19] == 0) ? (r20) : (r20 - `FNS20);
    assign r18 = (code_wire[18] == 0) ? (r19) : (r19 - `FNS19);
    
    assign r17 = (code_wire[17] == 0) ? (r18) : (r18 - `FNS18);
    assign r16 = (code_wire[16] == 0) ? (r17) : (r17 - `FNS17);
    assign r15 = (code_wire[15] == 0) ? (r16) : (r16 - `FNS16);
    
    assign r14 = (code_wire[14] == 0) ? (r15) : (r15 - `FNS15);
    assign r13 = (code_wire[13] == 0) ? (r14) : (r14 - `FNS14);
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
    assign code_wire[24] = (datain >= `FNS26) ? (1) : (0);
    
    assign code_wire[23] = (r24 < `FNS24) ? (0) : ( (r24 >= `FNS25) ? (1) : (code_wire[24]) );
    assign code_wire[22] = (r23 < `FNS23) ? (0) : ( (r23 >= `FNS24) ? (1) : (code_wire[23]) );
    assign code_wire[21] = (r22 < `FNS22) ? (0) : ( (r22 >= `FNS23) ? (1) : (code_wire[22]) );
    
    assign code_wire[20] = (r21 < `FNS21) ? (0) : ( (r21 >= `FNS22) ? (1) : (code_wire[21]) );
    assign code_wire[19] = (r20 < `FNS20) ? (0) : ( (r20 >= `FNS21) ? (1) : (code_wire[20]) );
    assign code_wire[18] = (r19 < `FNS19) ? (0) : ( (r19 >= `FNS20) ? (1) : (code_wire[19]) );
    
    assign code_wire[17] = (r18 < `FNS18) ? (0) : ( (r18 >= `FNS19) ? (1) : (code_wire[18]) );
    assign code_wire[16] = (r17 < `FNS17) ? (0) : ( (r17 >= `FNS18) ? (1) : (code_wire[17]) );
    assign code_wire[15] = (r16 < `FNS16) ? (0) : ( (r16 >= `FNS17) ? (1) : (code_wire[16]) );
    
    assign code_wire[14] = (r15 < `FNS15) ? (0) : ( (r15 >= `FNS16) ? (1) : (code_wire[15]) );
    assign code_wire[13] = (r14 < `FNS14) ? (0) : ( (r14 >= `FNS15) ? (1) : (code_wire[14]) );
    assign code_wire[12] = (r13 < `FNS13) ? (0) : ( (r13 >= `FNS14) ? (1) : (code_wire[13]) );
    
    assign code_wire[11] = (r12 < `FNS12) ? (0) : ( (r12 >= `FNS13) ? (1) : (code_wire[12]) );
    assign code_wire[10] = (r11 < `FNS11) ? (0) : ( (r11 >= `FNS12) ? (1) : (code_wire[11]) );
    assign code_wire[9] = (r10 < `FNS10) ? (0) : ( (r10 >= `FNS11) ? (1) : (code_wire[10]) );
    
    assign code_wire[8] = (r09 < `FNS09) ? (0) : ( (r09 >= `FNS10) ? (1) : (code_wire[9]) );
    assign code_wire[7] = (r08 < `FNS08) ? (0) : ( (r08 >= `FNS09) ? (1) : (code_wire[8]) );
    assign code_wire[6] = (r07 < `FNS07) ? (0) : ( (r07 >= `FNS08) ? (1) : (code_wire[7]) );
    
    assign code_wire[5] = (r06 < `FNS06) ? (0) : ( (r06 >= `FNS07) ? (1) : (code_wire[6]) );
    assign code_wire[4] = (r05 < `FNS05) ? (0) : ( (r05 >= `FNS06) ? (1) : (code_wire[5]) );
    assign code_wire[3] = (r04 < `FNS04) ? (0) : ( (r04 >= `FNS05) ? (1) : (code_wire[4]) );
    
    assign code_wire[2] = (r03 < `FNS03) ? (0) : ( (r03 >= `FNS04) ? (1) : (code_wire[3]) );
    assign code_wire[1] = (r02 < `FNS02) ? (0) : ( (r02 >= `FNS03) ? (1) : (code_wire[2]) );
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

