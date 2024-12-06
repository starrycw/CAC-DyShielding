`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/12/06 16:25:10
// Design Name: 
// Module Name: FNSCATF_encoder_core_8_extended
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


`include "VHeader_FNSCATF.vh"

module FNSCATF_encoder_core_8_extended(
    input wire [`VH_FNSCATF_DataInBitWidth_8bitCW : 0] datain,
    output wire [7 : 0] codeout
    );

    wire [7 : 0] q_out;

    // MSB
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P7 - 1 : 0] res_block7;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_DataInBitWidth_8bitCW + 1), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P7), .NS_VALUE(`VH_FNSCATF_NSValue_P7)) 
        cmp_module7 (
            .res_in(datain),
            .lock_in(1'b0),
            .q_out(q_out[7]),
            .res_out(res_block7)
        );
    ///////////////////////////////////////////////////////////// 
    // The following two bits
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P6 - 1 : 0] res_block6;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P7), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P6), .NS_VALUE(`VH_FNSCATF_NSValue_P6)) 
        cmp_module6 (
            .res_in(res_block7),
            .lock_in(q_out[7]),
            .q_out(q_out[6]),
            .res_out(res_block6)
        );
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P5 - 1 : 0] res_block5;
    wire lock_6 = q_out[7] | q_out[6];
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P6), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P5), .NS_VALUE(`VH_FNSCATF_NSValue_P5)) 
        cmp_module5 (
            .res_in(res_block6),
            .lock_in(lock_6),
            .q_out(q_out[5]),
            .res_out(res_block5)
        );
    ///////////////////////////////////////////////////////////// 
    // Other bits
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P4 - 1 : 0] res_block4;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P5), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P4), .NS_VALUE(`VH_FNSCATF_NSValue_P4)) 
        cmp_module4 (
            .res_in(res_block5),
            .lock_in(q_out[5]),
            .q_out(q_out[4]),
            .res_out(res_block4)
        );

    wire [`VH_FNSCATF_NSValueMaxBinWidth_P3 - 1 : 0] res_block3;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P4), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P3), .NS_VALUE(`VH_FNSCATF_NSValue_P3)) 
        cmp_module3 (
            .res_in(res_block4),
            .lock_in(q_out[4]),
            .q_out(q_out[3]),
            .res_out(res_block3)
        );

    wire [`VH_FNSCATF_NSValueMaxBinWidth_P2 - 1 : 0] res_block2;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P3), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P2), .NS_VALUE(`VH_FNSCATF_NSValue_P2)) 
        cmp_module2 (
            .res_in(res_block3),
            .lock_in(q_out[3]),
            .q_out(q_out[2]),
            .res_out(res_block2)
        );

    ///////////////////////////////////////////////////////////////

    // Last cmp module
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P2), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P1), .NS_VALUE(`VH_FNSCATF_NSValue_P1)) 
        cmp_module1 (
            .res_in(res_block2),
            .lock_in(q_out[2]),
            .q_out(q_out[1]),
            .res_out(q_out[0])
        );
    ///////////////////////////////////////////////////////////////

    // Shift
    assign codeout[7] = q_out[7];
    assign codeout[6 : 1] = (q_out[7] == 1'b0)? (q_out[6 : 1]) : (q_out[5 : 0]);
    assign codeout[0] = (q_out[7] == 1'b0)? (q_out[0]) : (1'b0);

endmodule

