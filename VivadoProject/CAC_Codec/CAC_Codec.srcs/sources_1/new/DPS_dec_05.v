`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/23 17:07:59
// Design Name: 
// Module Name: DPS_dec_05
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
module DPS_dec_05(
    input wire clk,
    input wire rst_n,
    input wire [4 : 0] codein,
    output reg [`DBLEN05 - 1 :0] dataout
    );

    wire [`DBLEN05 - 1 :0] dataout_wire;
   
    
    assign dataout_wire = (codein[4] * `FNS05) + (codein[3] * (`FNS04 * 2)) + (codein[2] * `FNS03) + (codein[1] * `FNS02) + 
                        (codein[0] * `FNS01);

    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            dataout[`DBLEN05 - 1 :0] <= { `DBLEN05{1'b0} };
        end
        else begin
            dataout[`DBLEN05 - 1 :0] <= dataout_wire[`DBLEN05 - 1 :0];
        end
    end
    
endmodule
