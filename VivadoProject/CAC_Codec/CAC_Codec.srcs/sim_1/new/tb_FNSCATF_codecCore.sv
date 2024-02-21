`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/02/20 21:14:18
// Design Name: 
// Module Name: tb_FNSCATF_codecCore
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

module tb_FNSCATF_codecCore(

    );
    parameter N_SIMU_CYCLE = 10000;

    // 7-bit codec core
    wire [6 : 0] tsv_07;
    reg [`VH_FNSCATF_DataInBitWidth_7bitCW - 1 : 0] datain_07;
    wire [`VH_FNSCATF_DataInBitWidth_7bitCW - 1 : 0] dataout_07;
    FNSCATF_encoder_core_07 encoder07 (
        .datain(datain_07),
        .codeout(tsv_07)
    );

    FNSCATF_decoder_core_07 decoder07 (
        .codein(tsv_07),
        .dataout(dataout_07)
    );


    static int cnt_i, cnt_err, cnt_pass, idx_i;

    initial begin
        for (cnt_i = 0; cnt_i < N_SIMU_CYCLE; cnt_i++) begin: for_cnt_i
            datain_07 = {$random} % (2**(`VH_FNSCATF_DataInBitWidth_7bitCW));
           
            #1;
            if (dataout_07 != datain_07) begin
                cnt_err = cnt_err + 1;
                $display("CODEC07-%d-ERROR: %d -> %b -> %d", cnt_i, datain_07, tsv_07, dataout_07);
            end
            else begin
                cnt_pass = cnt_pass + 1;
                $display("CODEC07-%d-PASS: %d -> %b -> %d", cnt_i, datain_07, tsv_07, dataout_07);
            end
            for (idx_i = 0; idx_i < 6; idx_i++) begin
                if ( (tsv_07[idx_i] != 0) && (tsv_07[idx_i+1] != 0) ) begin
                    $display("---ERROR! CAC rule violated!---");
                    $finish();
                end
                if ( (tsv_07[6] != 0) && (tsv_07[0] != 0) ) begin
                    $display("---ERROR! CAC rule violated!---");
                    $finish();
                end
            end

        end: for_cnt_i
        
        $display("Finished! %d errors, %d ok!", cnt_err, cnt_pass);
        $finish();
    end

endmodule
