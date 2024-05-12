`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/05/10 15:57:05
// Design Name: 
// Module Name: BSCAC7_encoder_top_basic
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: The top design of the BSCAC7 encoder. 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module BSCAC7_encoder_top_basic(
    input wire clk, 
    input wire [0 : 6] state_old, 
    input wire [0 : 6] data_in, 
    output reg [0 : 6] current_state, 
    output wire [1 : 6] flag_stuffing // 0- not stuffing bit; 1 - stuffing bit
    );

    wire [0 : 6] state_new;

    BSCAC7_encoder_core encoderCore_01(.state_old(state_old), 
                                       .data_in(data_in), 
                                       .state_new(state_new), 
                                       .flag_stuffing(flag_stuffing));

    always @(posedge clk) begin
        current_state <= state_new;
    end

endmodule
