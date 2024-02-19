`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/19 20:21:24
// Design Name: 
// Module Name: FNSCATF_encoder_core_07
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

module FNSCATF_encoder_core_07(
    input [`VH_FNSCATF_DataInBitWidth_7bitCW - 1 : 0] datain,
    output [6 : 0] codeout
    );
    
    wire [6 : 0] q_out;
    
    // MSB
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P6 - 1 : 0] res_block06;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_DataInBitWidth_7bitCW), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P6), .NS_VALUE(`VH_FNSCATF_NSValue_P6)) 
        cmp_module06 (
            .res_in(datain),
            .lock_in(1'b0),
            .q_out(q_out[6]),
            .res_out(res_block06)
        );
    /////////////////////////////////////////////////////////////        
    // The following two bits
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P5 - 1 : 0] res_block05;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P6), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P5), .NS_VALUE(`VH_FNSCATF_NSValue_P5)) 
        cmp_module05 (
            .res_in(res_block06),
            .lock_in(q_out[6]),
            .q_out(q_out[5]),
            .res_out(res_block05)
        );
        
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P4 - 1 : 0] res_block04;
    wire lock_05 = q_out[6] | q_out[5];
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P5), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P4), .NS_VALUE(`VH_FNSCATF_NSValue_P4)) 
        cmp_module04 (
            .res_in(res_block05),
            .lock_in(lock_05),
            .q_out(q_out[4]),
            .res_out(res_block04)
        );
    //////////////////////////////////////////////////////////////
    // Other bits
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P3 - 1 : 0] res_block03;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P4), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P3), .NS_VALUE(`VH_FNSCATF_NSValue_P3)) 
        cmp_module03 (
            .res_in(res_block04),
            .lock_in(q_out[4]),
            .q_out(q_out[3]),
            .res_out(res_block03)
        );
        
    wire [`VH_FNSCATF_NSValueMaxBinWidth_P2 - 1 : 0] res_block02;
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P3), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P2), .NS_VALUE(`VH_FNSCATF_NSValue_P2)) 
        cmp_module02 (
            .res_in(res_block03),
            .lock_in(q_out[3]),
            .q_out(q_out[2]),
            .res_out(res_block02)
        );
    
    ///////////////////////////////////////////////////////////////
    // Last cmp module
    FNSCATF_encoderModule_cmp #(.RES_IN_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P2), .RES_OUT_WIDTH(`VH_FNSCATF_NSValueMaxBinWidth_P1), .NS_VALUE(`VH_FNSCATF_NSValue_P1)) 
        cmp_module01 (
            .res_in(res_block02),
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
