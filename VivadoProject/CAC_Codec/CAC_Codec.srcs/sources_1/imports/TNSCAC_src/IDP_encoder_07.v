`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/05/13 16:54:54
// Design Name: 
// Module Name: IDP_encoder_07
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
module IDP_encoder_07(  //***********
    input wire[`IBLEN07 - 1 : 0] datain,    //******************
    input wire clock,
    input wire rst_n,
    output reg[6:0] codeout    //********************
    );
    
    //
    reg [3:0] code_reg;
    wire [6 - 4 : 0] code_wire;    //*****************
    
    reg [`FRLEN03 - 1 : 0] r_msb;   //*******************
    
    //four msbs
    always @(datain) begin      //*******************
        if(datain < `FNS05) begin   
            code_reg[3:0] = 4'b0000;
            r_msb = datain; 
        end//
        
        else if( (datain >= `FNS05) && (datain < `FNS06) ) begin
            code_reg[3:0] = 4'b0001;
            r_msb = datain - `FNS04; 
        end//
        
        else if( (datain >= `FNS06) && (datain < `FNS07) ) begin
            code_reg[3:0] = 4'b1000;
            r_msb = datain - `FNS06; 
        end//
        
        else if( (datain >= `FNS07) && (datain < (`FNS06 * 2)) ) begin
            code_reg[3:0] = 4'b1001;
            r_msb = datain - `FNS04 - `FNS06; 
        end //
        
        else if( (datain >= (`FNS06 * 2)) && (datain < `FNS08) ) begin
            code_reg[3:0] = 4'b0011;
            r_msb = datain - `FNS04 - `FNS07; 
        end//
        
        else if( (datain >= `FNS08) && (datain < (`FNS07 * 2)) ) begin
            code_reg[3:0] = 4'b1100;
            r_msb = datain - `FNS07 - `FNS06; 
        end//
        
        else if( (datain >= (`FNS07 * 2)) && (datain < (`FNS07 * 2 + `FNS04)) ) begin
            code_reg[3:0] = 4'b0110;
            r_msb = datain - (`FNS07 * 2); 
        end//
        
        else if( (datain >= (`FNS07 * 2 + `FNS04)) && (datain < `FNS09) ) begin
            code_reg[3:0] = 4'b0111;
            r_msb = datain - (`FNS07 * 2) - `FNS04; 
        end//
        
        else if( (datain >= `FNS09) && (datain < (`FNS09 + `FNS04)) ) begin
            code_reg[3:0] = 4'b1110;
            r_msb = datain - (`FNS07 * 2) - `FNS06; 
        end
        
        else begin
            code_reg[3:0] = 4'b1111;
            r_msb = datain - (`FNS07 * 2) - `FNS06 - `FNS04; 
        end

    end
    

    //
    
   

 
  
    wire [`FRLEN02 - 1 : 0] r02;
    wire [`FRLEN01 - 1 : 0] r01;
    
    
    //

    
    assign r02 = (code_wire[02] == 0) ? (r_msb) : (r_msb - `FNS03);
    assign r01 = (code_wire[01] == 0) ? (r02) : (r02 - `FNS02);
    
    //
   
    
    assign code_wire[2] = (r_msb < `FNS03) ? (0) : ( (r_msb >= `FNS04) ? (1) : (code_reg[0]) );
    assign code_wire[1] = (r02 < `FNS02) ? (0) : ( (r02 >= `FNS03) ? (1) : (code_wire[2]) );
    assign code_wire[0] = r01;
    
    
    //sync
    always @(posedge clock or negedge rst_n) begin
        if (~rst_n) begin
            codeout[6 : 0] <= { 7{1'b0} };
        end
        else begin
            codeout[6 - 4 : 0] <= code_wire;
            codeout[6 : 6 - 3] <= code_reg;
        end
        
    end
    
endmodule
