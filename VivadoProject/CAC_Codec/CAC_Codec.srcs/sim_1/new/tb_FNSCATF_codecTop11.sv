`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_53]
// The testbench of the FNS-CATF encoder & decoder.
// codeword_bitwidth=11
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module tb_FNSCATF_codecTop11(

    );
    parameter N_SIMU_CYCLE = 10000;
    reg clk_encoder, clk_decoder, rst_n;
    reg [10 : 0] tsvLast;
    wire [10 : 0] tsvTrans;
    // 11-bit codec core
    reg [10 : 0] tsv_11;
    reg [`VH_FNSCATF_DataInBitWidth_11bitCW - 1 : 0] datain_11;
    reg [`VH_FNSCATF_DataInBitWidth_11bitCW - 1 : 0] dataout_11;
    assign tsvTrans = tsvLast ^ tsv_11;
    FNSCATF_encoder_top_11 encoder_instance11 (
        .clk(clk_encoder),
        .rst_n(rst_n),
        .datain(datain_11),
        .codeword_regs(tsv_11)
    );

    FNSCATF_decoder_top_11 decoder_instance11 (
        .clk(clk_decoder),
        .rst_n(rst_n),
        .codeword_in(tsv_11),
        .data_reg(dataout_11)
    );

    static int cnt_i, cnt_err, cnt_pass, cnt_violate, idx_i;

    initial begin
        #1;
        rst_n <= 1;
        clk_encoder <= 0;
        clk_decoder <= 0;
        #1;
        rst_n <= 0;
        #1;
        rst_n <= 1;
        tsv_11 <= 0;
        tsvLast <= 0;
        datain_11 <= 0;
        #1;
        clk_encoder <= 1;
        #1;
        clk_decoder <= 1;
        #1;
        for (cnt_i = 0; cnt_i < N_SIMU_CYCLE; cnt_i++) begin: for_cnt_i
            #1;
            clk_encoder <= 0;
            clk_decoder <= 0;
            tsvLast <= tsv_11;
            datain_11 = {$random} % (2**(`VH_FNSCATF_DataInBitWidth_11bitCW));

            #1;
            clk_encoder <= 1;
            #1;
            clk_decoder <= 1;
            #1;
            if (dataout_11 != datain_11) begin
                cnt_err = cnt_err + 1;
                $display("CODEC11-%d-ERROR: %d -> %b -> %d", cnt_i, datain_11, tsv_11, dataout_11);
            end
            else begin
                cnt_pass = cnt_pass + 1;
                $display("CODEC11-%d-PASS: %d -> %b -> %d", cnt_i, datain_11, tsv_11, dataout_11);
            end
            for (idx_i = 0; idx_i < 10; idx_i++) begin
                if ( (tsvTrans[idx_i] != 0) && (tsvTrans[idx_i+1] != 0) ) begin
                    $display("---ERROR! CAC rule violated!---");
                    cnt_violate = cnt_violate + 1;
                    $finish();
                end
                if ( (tsvTrans[10] != 0) && (tsvTrans[0] != 0) ) begin
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
