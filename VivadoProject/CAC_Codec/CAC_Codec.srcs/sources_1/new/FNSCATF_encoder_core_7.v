`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_53]
// The core logic of the FNS-CATF encoder.
// codeword_bitwidth=7
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module FNSCATF_encoder_core_7(
    input wire [`VH_FNSCATF_DataInBitWidth_7bitCW - 1 : 0] datain,
    output wire [6 : 0] codeout
    );

    wire [6 : 0] q_out;

    // MSB
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P6 - 1 : 0] res_block6;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_DataInBitWidth_7bitCW), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P6), .NS_VALUE(`VH_FNSCATF_NSValue_P6)) 
        cmp_module6 (
            .res_in(datain),
            .lock_in(1'b0),
            .q_out(q_out[6]),
            .res_out(res_block6)
        );
    ///////////////////////////////////////////////////////////// 
    // The following two bits
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P5 - 1 : 0] res_block5;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P6), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P5), .NS_VALUE(`VH_FNSCATF_NSValue_P5)) 
        cmp_module5 (
            .res_in(res_block6),
            .lock_in(q_out[6]),
            .q_out(q_out[5]),
            .res_out(res_block5)
        );
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P4 - 1 : 0] res_block4;
    wire lock_5 = q_out[6] | q_out[5];
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P5), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P4), .NS_VALUE(`VH_FNSCATF_NSValue_P4)) 
        cmp_module4 (
            .res_in(res_block5),
            .lock_in(lock_5),
            .q_out(q_out[4]),
            .res_out(res_block4)
        );
    ///////////////////////////////////////////////////////////// 
    // Other bits
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
    assign codeout[6] = q_out[6];
    assign codeout[5 : 1] = (q_out[6] == 1'b0)? (q_out[5 : 1]) : (q_out[4 : 0]);
    assign codeout[0] = (q_out[6] == 1'b0)? (q_out[0]) : (1'b0);

endmodule
