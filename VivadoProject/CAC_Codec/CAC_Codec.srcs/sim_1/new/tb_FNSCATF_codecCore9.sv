`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_21-22_31_57]
// The testbench of the FNS-CATF encoder & decoder core.
// codeword_bitwidth=9
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module tb_FNSCATF_codecCore9(

    );
    parameter N_SIMU_CYCLE = 10000;
    // 9-bit codec core
    wire [8 : 0] tsv_9;
    reg [`VH_FNSCATF_DataInBitWidth_9bitCW - 1 : 0] datain_9;
    wire [`VH_FNSCATF_DataInBitWidth_9bitCW - 1 : 0] dataout_9;
    FNSCATF_encoder_core_9 encoder_instance9 (
        .datain(datain_9),
        .codeout(tsv_9)
    );

    FNSCATF_decoder_core_9 decoder_instance9 (
        .codein(tsv_9),
        .dataout(dataout_9)
    );

    static int cnt_i, cnt_err, cnt_pass, cnt_violate, idx_i;

    initial begin
        for (cnt_i = 0; cnt_i < N_SIMU_CYCLE; cnt_i++) begin: for_cnt_i
            datain_9 = {$random} % (2**(`VH_FNSCATF_DataInBitWidth_9bitCW));

            #1;
            if (dataout_9 != datain_9) begin
                cnt_err = cnt_err + 1;
                $display("CODEC9-%d-ERROR: %d -> %b -> %d", cnt_i, datain_9, tsv_9, dataout_9);
            end
            else begin
                cnt_pass = cnt_pass + 1;
                $display("CODEC9-%d-PASS: %d -> %b -> %d", cnt_i, datain_9, tsv_9, dataout_9);
            end
            for (idx_i = 0; idx_i < 8; idx_i++) begin
                if ( (tsv_9[idx_i] != 0) && (tsv_9[idx_i+1] != 0) ) begin
                    $display("---ERROR! CAC rule violated!---");
                    cnt_violate = cnt_violate + 1;
                    $finish();
                end
                if ( (tsv_9[8] != 0) && (tsv_9[0] != 0) ) begin
                    $display("---ERROR! CAC rule violated!---");
                    cnt_violate = cnt_violate + 1;
                    $finish();
                end
            end

        end: for_cnt_i

        $display("Finished! %d errors, %d ok, %d violate!", cnt_err, cnt_pass, cnt_violate);
        $finish();
    end

endmodule
