`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/23 17:25:04
// Design Name: 
// Module Name: FNS_dec_09
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
module FNS_dec_09(
    input wire clk,
    input wire rst_n,
    input wire [8:0] codein,
    output reg [`FBLEN09 - 1 : 0] dataout
    );
    
    wire [`FBLEN09 - 1 : 0] dataout_wire;

    assign dataout_wire = (codein[8] * `FNS09) + 
                        (codein[7] * `FNS08) + (codein[6] * `FNS07) + 
                        (codein[5] * `FNS06) + (codein[4] * `FNS05) + (codein[3] * `FNS04) + (codein[2] * `FNS03) + (codein[1] * `FNS02) + 
                        (codein[0] * `FNS01);

    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            dataout[`FBLEN09 - 1 :0] <= { `FBLEN09{1'b0} };
        end
        else begin
            dataout[`FBLEN09 - 1 :0] <= dataout_wire[`FBLEN09 - 1 :0];
        end
    end
endmodule
