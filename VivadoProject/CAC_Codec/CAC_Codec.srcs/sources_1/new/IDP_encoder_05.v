`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/24 17:58:23
// Design Name: 
// Module Name: IDP_encoder_05
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
module IDP_encoder_05(  //***********
    input wire[`IBLEN05 - 1 : 0] datain,    //******************
    input wire clock,
    input wire rst_n,
    output reg[4:0] codeout    //********************
    );
    
    //
    reg [3:0] code_reg;
    wire code_wire;    //*****************
    
    reg r_msb;   //*******************
    
    //four msbs
    always @(datain) begin      //*******************
        if(datain < `FNS03) begin   
            code_reg[3:0] = 4'b0000;
            r_msb = datain; 
        end//
        
        else if( (datain >= `FNS03) && (datain < `FNS04) ) begin
            code_reg[3:0] = 4'b0001;
            r_msb = datain - `FNS02; 
        end//
        
        else if( (datain >= `FNS04) && (datain < `FNS05) ) begin
            code_reg[3:0] = 4'b1000;
            r_msb = datain - `FNS04; 
        end//
        
        else if( (datain >= `FNS05) && (datain < (`FNS04 * 2)) ) begin
            code_reg[3:0] = 4'b1001;
            r_msb = datain - `FNS02 - `FNS04; 
        end //
        
        else if( (datain >= (`FNS04 * 2)) && (datain < `FNS06) ) begin
            code_reg[3:0] = 4'b0011;
            r_msb = datain - `FNS02 - `FNS05; 
        end//
        
        else if( (datain >= `FNS06) && (datain < (`FNS05 * 2)) ) begin
            code_reg[3:0] = 4'b1100;
            r_msb = datain - `FNS05 - `FNS04; 
        end//
        
        else if( (datain >= (`FNS05 * 2)) && (datain < (`FNS05 * 2 + `FNS02)) ) begin
            code_reg[3:0] = 4'b0110;
            r_msb = datain - (`FNS05 * 2); 
        end//
        
        else if( (datain >= (`FNS05 * 2 + `FNS02)) && (datain < `FNS07) ) begin
            code_reg[3:0] = 4'b0111;
            r_msb = datain - (`FNS05 * 2) - `FNS02; 
        end//
        
        else if( (datain >= `FNS07) && (datain < (`FNS07 + `FNS02)) ) begin
            code_reg[3:0] = 4'b1110;
            r_msb = datain - (`FNS05 * 2) - `FNS04; 
        end
        
        else begin
            code_reg[3:0] = 4'b1111;
            r_msb = datain - (`FNS05 * 2) - `FNS04 - `FNS02; 
        end

    end
    

    //
    
   

 
  
    // wire [`FRLEN02 - 1 : 0] r02;
    // wire [`FRLEN01 - 1 : 0] r01;
    
    
    //

    
    // assign r02 = (code_wire[02] == 0) ? (r_msb) : (r_msb - `FNS03);
    // assign r01 = (code_wire[01] == 0) ? (r02) : (r02 - `FNS02);
    
    // //
   
    
    // assign code_wire[2] = (r_msb < `FNS03) ? (0) : ( (r_msb >= `FNS04) ? (1) : (code_reg[0]) );
    // assign code_wire[1] = (r02 < `FNS02) ? (0) : ( (r02 >= `FNS03) ? (1) : (code_wire[2]) );
    assign code_wire = r_msb;
    
    
    //sync
    always @(posedge clock or negedge rst_n) begin
        if (~rst_n) begin
            codeout[4 : 0] <= { 5{1'b0} };
        end
        else begin
            codeout[0] <= code_wire;
            codeout[4 : 1] <= code_reg;
        end
        
    end
    
endmodule
