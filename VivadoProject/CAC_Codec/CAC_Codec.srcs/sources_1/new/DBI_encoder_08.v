`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/12/05 17:45:26
// Design Name: 
// Module Name: DBI_encoder_08
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


module DBI_encoder_08(
    input wire [6 : 0] datain,
    input wire clock,
    input wire rst_n,
    output reg [7 : 0] codeout
    );
    
    wire [7 : 0] data_pos, data_rev;
    wire [7 : 0] data_pos_n_inv;
    assign data_pos[7 : 0] = {datain[6 : 0], 1'b0};
    assign data_rev[7 : 0] = ~data_pos;
    assign data_pos_n_inv = data_pos[7 : 0] ^ codeout;
    
    always @(posedge clock or negedge rst_n) begin
        if (~rst_n) begin
            codeout <= 0;
        end
        else if (data_pos_n_inv[0] + data_pos_n_inv[1] + data_pos_n_inv[2] + data_pos_n_inv[3] + 
                data_pos_n_inv[4] + data_pos_n_inv[5] + data_pos_n_inv[6] + data_pos_n_inv[7] < 5 ) begin
            codeout <= data_pos;
        end
        else begin
            codeout <= data_rev;
        end
    end
    
endmodule
