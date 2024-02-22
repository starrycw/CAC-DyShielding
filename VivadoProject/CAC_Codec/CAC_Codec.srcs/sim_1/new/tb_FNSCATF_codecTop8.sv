`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_53]
// The testbench of the FNS-CATF encoder & decoder.
// codeword_bitwidth=8
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module tb_FNSCATF_codecTop8(

    );
    parameter N_SIMU_CYCLE = 10000;
    reg clk_encoder, clk_decoder, rst_n;
    reg [7 : 0] tsvLast;
    wire [7 : 0] tsvTrans;
    // 8-bit codec core
    reg [7 : 0] tsv_8;
    reg [`VH_FNSCATF_DataInBitWidth_8bitCW - 1 : 0] datain_8;
    reg [`VH_FNSCATF_DataInBitWidth_8bitCW - 1 : 0] dataout_8;
    assign tsvTrans = tsvLast ^ tsv_8;
    FNSCATF_encoder_top_8 encoder_instance8 (
        .clk(clk_encoder),
        .rst_n(rst_n),
        .datain(datain_8),
        .codeword_regs(tsv_8)
    );

    FNSCATF_decoder_top_8 decoder_instance8 (
        .clk(clk_decoder),
        .rst_n(rst_n),
        .codeword_in(tsv_8),
        .data_reg(dataout_8)
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
        tsv_8 <= 0;
        tsvLast <= 0;
        datain_8 <= 0;
        #1;
        clk_encoder <= 1;
        #1;
        clk_decoder <= 1;
        #1;
        for (cnt_i = 0; cnt_i < N_SIMU_CYCLE; cnt_i++) begin: for_cnt_i
            #1;
            clk_encoder <= 0;
            clk_decoder <= 0;
            tsvLast <= tsv_8;
            datain_8 = {$random} % (2**(`VH_FNSCATF_DataInBitWidth_8bitCW));

            #1;
            clk_encoder <= 1;
            #1;
            clk_decoder <= 1;
            #1;
            if (dataout_8 != datain_8) begin
                cnt_err = cnt_err + 1;
                $display("CODEC8-%d-ERROR: %d -> %b -> %d", cnt_i, datain_8, tsv_8, dataout_8);
            end
            else begin
                cnt_pass = cnt_pass + 1;
                $display("CODEC8-%d-PASS: %d -> %b -> %d", cnt_i, datain_8, tsv_8, dataout_8);
            end
            for (idx_i = 0; idx_i < 7; idx_i++) begin
                if ( (tsvTrans[idx_i] != 0) && (tsvTrans[idx_i+1] != 0) ) begin
                    $display("---ERROR! CAC rule violated!---");
                    cnt_violate = cnt_violate + 1;
                    $finish();
                end
                if ( (tsvTrans[7] != 0) && (tsvTrans[0] != 0) ) begin
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
