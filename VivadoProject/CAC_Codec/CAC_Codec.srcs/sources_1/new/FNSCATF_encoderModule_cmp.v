`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/19 20:48:04
// Design Name: 
// Module Name: FNSCATF_encoderModule_cmp
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


module FNSCATF_encoderModule_cmp #(parameter RES_IN_WIDTH = 2, RES_OUT_WIDTH = 2, NS_VALUE = 2)(
    input wire [RES_IN_WIDTH - 1 : 0] res_in,
    input wire lock_in,
    output wire q_out,
    output wire [RES_OUT_WIDTH - 1 : 0] res_out
    );
    
    assign q_out = (lock_in == 1'b1)? (1'b0) : ( (res_in < NS_VALUE)? (1'b0) : (1'b1) );
    assign res_out = (q_out == 1'b0)? (res_in) : (res_in - NS_VALUE);
        
endmodule
