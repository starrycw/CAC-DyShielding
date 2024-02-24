`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/24 17:58:23
// Design Name: 
// Module Name: IDP_dec_09
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
module IDP_dec_09(
    input wire clk,
    input wire rst_n,
    input wire [8:0] codein,
    output reg [`IBLEN09 - 1 : 0] dataout
    );

    wire [`IBLEN09 - 1 : 0] dataout_wire;
    
    assign dataout_wire = (codein[8] * `FNS08) + (codein[7] * `FNS09) + (codein[6] * `FNS09) + (codein[5] * `FNS06) +  
                        (codein[4] * `FNS05) + (codein[3] * `FNS04) + (codein[2] * `FNS03) + (codein[1] * `FNS02) + 
                        (codein[0] * `FNS01);
    
    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            dataout[`IBLEN09 - 1 :0] <= { `IBLEN09{1'b0} };
        end
        else begin
            dataout[`IBLEN09 - 1 :0] <= dataout_wire[`IBLEN09 - 1 :0];
        end
    end
endmodule
