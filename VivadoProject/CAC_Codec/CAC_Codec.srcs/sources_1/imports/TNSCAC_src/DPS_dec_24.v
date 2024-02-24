`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/06/06 17:57:11
// Design Name: 
// Module Name: DPS_dec_24
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
module DPS_dec_24(
    input wire clk,
    input wire rst_n,
    input wire [23 : 0] codein,
    output reg [`DBLEN24 - 1 :0] dataout
    );

    wire [`DBLEN24 - 1 :0] dataout_wire;
   
    
    assign dataout_wire = (codein[23] * `FNS24) + (codein[22] * (`FNS23 * 2)) + (codein[21] * `FNS22) + (codein[20] * `FNS21) + (codein[19] * `FNS20) + (codein[18] * `FNS19) + 
                        (codein[17] * `FNS18) + (codein[16] * `FNS17) + 
                        (codein[15] * `FNS16) + (codein[14] * `FNS15) + (codein[13] * `FNS14) + (codein[12] * `FNS13) + (codein[11] * `FNS12) + 
                        (codein[10] * `FNS11) + (codein[9] * `FNS10) + (codein[8] * `FNS09) + (codein[7] * `FNS08) + (codein[6] * `FNS07) + 
                        (codein[5] * `FNS06) + (codein[4] * `FNS05) + (codein[3] * `FNS04) + (codein[2] * `FNS03) + (codein[1] * `FNS02) + 
                        (codein[0] * `FNS01);

    always @(posedge clk or negedge rst_n) begin
        if (~rst_n) begin
            dataout[`DBLEN24 - 1 :0] <= { `DBLEN24{1'b0} };
        end
        else begin
            dataout[`DBLEN24 - 1 :0] <= dataout_wire[`DBLEN24 - 1 :0];
        end
    end
    
endmodule

