`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/05/13 16:54:54
// Design Name: 
// Module Name: IDP_encoder_11
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
module IDP_encoder_11(  //***********
    input wire[`IBLEN11 - 1 : 0] datain,    //******************
    input wire clock,
    input wire rst_n,
    output reg[10:0] codeout    //********************
    );
    
    //
    reg [3:0] code_reg;
    wire [10 - 4 : 0] code_wire;    //*****************
    
    reg [`FRLEN07 - 1 : 0] r_msb;   //*******************
    
    //four msbs
    always @(datain) begin      //*******************
        if(datain < `FNS09) begin   
            code_reg[3:0] = 4'b0000;
            r_msb = datain; 
        end//
        
        else if( (datain >= `FNS09) && (datain < `FNS10) ) begin
            code_reg[3:0] = 4'b0001;
            r_msb = datain - `FNS08; 
        end//
        
        else if( (datain >= `FNS10) && (datain < `FNS11) ) begin
            code_reg[3:0] = 4'b1000;
            r_msb = datain - `FNS10; 
        end//
        
        else if( (datain >= `FNS11) && (datain < (`FNS10 * 2)) ) begin
            code_reg[3:0] = 4'b1001;
            r_msb = datain - `FNS08 - `FNS10; 
        end //
        
        else if( (datain >= (`FNS10 * 2)) && (datain < `FNS12) ) begin
            code_reg[3:0] = 4'b0011;
            r_msb = datain - `FNS08 - `FNS11; 
        end//
        
        else if( (datain >= `FNS12) && (datain < (`FNS11 * 2)) ) begin
            code_reg[3:0] = 4'b1100;
            r_msb = datain - `FNS11 - `FNS10; 
        end//
        
        else if( (datain >= (`FNS11 * 2)) && (datain < (`FNS11 * 2 + `FNS08)) ) begin
            code_reg[3:0] = 4'b0110;
            r_msb = datain - (`FNS11 * 2); 
        end//
        
        else if( (datain >= (`FNS11 * 2 + `FNS08)) && (datain < `FNS13) ) begin
            code_reg[3:0] = 4'b0111;
            r_msb = datain - (`FNS11 * 2) - `FNS08; 
        end//
        
        else if( (datain >= `FNS13) && (datain < (`FNS13 + `FNS08)) ) begin
            code_reg[3:0] = 4'b1110;
            r_msb = datain - (`FNS11 * 2) - `FNS10; 
        end
        
        else begin
            code_reg[3:0] = 4'b1111;
            r_msb = datain - (`FNS11 * 2) - `FNS10 - `FNS08; 
        end

    end
    

    //
    
   

 
    wire [`FRLEN06 - 1 : 0] r06;
    wire [`FRLEN05 - 1 : 0] r05;
    wire [`FRLEN04 - 1 : 0] r04;
    
    wire [`FRLEN03 - 1 : 0] r03;
    wire [`FRLEN02 - 1 : 0] r02;
    wire [`FRLEN01 - 1 : 0] r01;
    
    
    //



    
 
    assign r06 = (code_wire[06] == 0) ? (r_msb) : (r_msb - `FNS07);
    
    assign r05 = (code_wire[05] == 0) ? (r06) : (r06 - `FNS06);
    assign r04 = (code_wire[04] == 0) ? (r05) : (r05 - `FNS05);
    assign r03 = (code_wire[03] == 0) ? (r04) : (r04 - `FNS04);
    
    assign r02 = (code_wire[02] == 0) ? (r03) : (r03 - `FNS03);
    assign r01 = (code_wire[01] == 0) ? (r02) : (r02 - `FNS02);
    
    //
   
    
  
    assign code_wire[6] = (r_msb < `FNS07) ? (0) : ( (r_msb >= `FNS08) ? (1) : (code_reg[0]) );
    
    assign code_wire[5] = (r06 < `FNS06) ? (0) : ( (r06 >= `FNS07) ? (1) : (code_wire[6]) );
    assign code_wire[4] = (r05 < `FNS05) ? (0) : ( (r05 >= `FNS06) ? (1) : (code_wire[5]) );
    assign code_wire[3] = (r04 < `FNS04) ? (0) : ( (r04 >= `FNS05) ? (1) : (code_wire[4]) );
    
    assign code_wire[2] = (r03 < `FNS03) ? (0) : ( (r03 >= `FNS04) ? (1) : (code_wire[3]) );
    assign code_wire[1] = (r02 < `FNS02) ? (0) : ( (r02 >= `FNS03) ? (1) : (code_wire[2]) );
    assign code_wire[0] = r01;
    
    
    //sync
    always @(posedge clock or negedge rst_n) begin
        if (~rst_n) begin
            codeout[10 : 0] <= { 11{1'b0} };
        end
        else begin
            codeout[10 - 4 : 0] <= code_wire;
            codeout[10 : 10 - 3] <= code_reg;
        end
        
    end
    
endmodule
