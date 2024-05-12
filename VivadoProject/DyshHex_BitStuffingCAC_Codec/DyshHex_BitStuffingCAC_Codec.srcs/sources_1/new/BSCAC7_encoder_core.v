`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/05/10 15:46:12
// Design Name: 
// Module Name: BSCAC7_encoder_core
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: THe 7-bit bit-stuffing CAC encoder, designed for DyshHex TSV arrays.
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module BSCAC7_encoder_core(
    input wire [0 : 6] state_old, 
    input wire [0 : 6] data_in, 
    output wire [0 : 6] state_new, 
    output wire [1 : 6] flag_stuffing // 0- not stuffing bit; 1 - stuffing bit
    );

    // XORs
    wire [0 : 6] xor_ci;
    assign xor_ci[0 : 6] = state_old[0 : 6] ^ state_new[0 : 6];


    // Flags: 1 - not free bit; 0 - free bit.
    wire notfree_c1 = state_old[0] ^ state_old[1];
    wire notfree_c2 = state_old[0] ^ state_old[2];
    wire notfree_c3 = state_old[0] ^ state_old[3];
    wire notfree_c4 = state_old[0] ^ state_old[4];
    wire notfree_c5 = state_old[0] ^ state_old[5];
    wire notfree_c6 = state_old[0] ^ state_old[6];

    // Get state_new 
    assign state_new[0] = data_in[0];
    assign state_new[1] = ((~flag_stuffing[1]) & data_in[1]) | (flag_stuffing[1] & state_old[1]);
    assign state_new[2] = ((~flag_stuffing[2]) & data_in[2]) | (flag_stuffing[2] & state_old[2]);
    assign state_new[3] = ((~flag_stuffing[3]) & data_in[3]) | (flag_stuffing[3] & state_old[3]);
    assign state_new[4] = ((~flag_stuffing[4]) & data_in[4]) | (flag_stuffing[4] & state_old[4]);
    assign state_new[5] = ((~flag_stuffing[5]) & data_in[5]) | (flag_stuffing[5] & state_old[5]);
    assign state_new[6] = ((~flag_stuffing[6]) & data_in[6]) | (flag_stuffing[6] & state_old[6]);

    // If xor_c0 == 0:
    wire [1 : 6] flag_stuffing_case0;
    assign flag_stuffing_case0[1] = 1'b0;
    assign flag_stuffing_case0[2] = (state_old[2] ^ state_old[1]) & (~xor_ci[2]);
    assign flag_stuffing_case0[3] = (state_old[3] ^ state_old[2]) & (~xor_ci[3]);
    assign flag_stuffing_case0[4] = (state_old[4] ^ state_old[3]) & (~xor_ci[4]);
    assign flag_stuffing_case0[5] = (state_old[5] ^ state_old[4]) & (~xor_ci[5]);
    assign flag_stuffing_case0[6] = (state_old[6] ^ state_old[5]) & (~xor_ci[6]);

    // If xor_c0 == 1:
    wire [1 : 6] flag_notstuffing_case1;
    assign flag_notstuffing_case1[1] = (~notfree_c1) | 
                                       (notfree_c6 & notfree_c2) | 
                                       ((~notfree_c6) & (~notfree_c2) & (~xor_ci[6]) & (~xor_ci[2]));
    assign flag_notstuffing_case1[2] = (~notfree_c2) | 
                                       (notfree_c1 & notfree_c3) | 
                                       (notfree_c1 & xor_ci[1]) | 
                                       ((~notfree_c1) & (~notfree_c3) & (~xor_ci[1]) & (~xor_ci[3]));
    assign flag_notstuffing_case1[3] = (~notfree_c3) | 
                                       (notfree_c2 & notfree_c4) | 
                                       (notfree_c2 & xor_ci[2]) | 
                                       ((~notfree_c2) & (~notfree_c4) & (~xor_ci[2]) & (~xor_ci[4]));
    assign flag_notstuffing_case1[4] = (~notfree_c4) | 
                                       (notfree_c3 & notfree_c5) | 
                                       (notfree_c3 & xor_ci[3]) | 
                                       ((~notfree_c3) & (~notfree_c5) & (~xor_ci[3]) & (~xor_ci[5]));
    assign flag_notstuffing_case1[5] = (~notfree_c5) | 
                                       (notfree_c4 & notfree_c6) | 
                                       (notfree_c4 & xor_ci[4]) | 
                                       ((~notfree_c4) & (~notfree_c6) & (~xor_ci[4]) & (~xor_ci[6]));
    assign flag_notstuffing_case1[6] = (~notfree_c6) | 
                                       (notfree_c5 & notfree_c1) | 
                                       (notfree_c5 & xor_ci[5]) | 
                                       (notfree_c1 & xor_ci[1]) | 
                                       ((~notfree_c5) & (~notfree_c1) & (~xor_ci[5]) & (~xor_ci[1]));
    
    // flag_stuffing
    assign flag_stuffing[1 : 6] = (xor_ci[0] == 1'b1)? (~flag_notstuffing_case1) : (flag_stuffing_case0);


endmodule

