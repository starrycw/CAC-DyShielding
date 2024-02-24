`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/05/13 16:32:44
// Design Name: 
// Module Name: FNS_dec_12
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
module FNS_dec_12(
    input wire clk,
    input wire rst_n,
    input wire [11:0] codein,
    output reg [`FBLEN12 - 1 : 0] dataout
    );
    
    wire [`FBLEN12 - 1 : 0] dataout_wire;

    assign dataout_wire = (codein[11] * `FNS12) + 
                        (codein[10] * `FNS11) + (codein[9] * `FNS10) + (codein[8] * `FNS09) + (codein[7] * `FNS08) + (codein[6] * `FNS07) + 
                        (codein[5] * `FNS06) + (codein[4] * `FNS05) + (codein[3] * `FNS04) + (codein[2] * `FNS03) + (codein[1] * `FNS02) + 
                        (codein[0] * `FNS01);

    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            dataout[`FBLEN12 - 1 :0] <= { `FBLEN12{1'b0} };
        end
        else begin
            dataout[`FBLEN12 - 1 :0] <= dataout_wire[`FBLEN12 - 1 :0];
        end
    end
endmodule

