`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_54]
// The testbench of the FNS-CATF encoder & decoder.
// codeword_bitwidth=16
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module tb_FNSCATF_codecTop16(

    );
    parameter N_SIMU_CYCLE = 10000;
    reg clk_encoder, clk_decoder, rst_n;
    reg [15 : 0] tsvLast;
    wire [15 : 0] tsvTrans;
    // 16-bit codec core
    reg [15 : 0] tsv_16;
    reg [`VH_FNSCATF_DataInBitWidth_16bitCW - 1 : 0] datain_16;
    reg [`VH_FNSCATF_DataInBitWidth_16bitCW - 1 : 0] dataout_16;
    assign tsvTrans = tsvLast ^ tsv_16;
    FNSCATF_encoder_top_16 encoder_instance16 (
        .clk(clk_encoder),
        .rst_n(rst_n),
        .datain(datain_16),
        .codeword_regs(tsv_16)
    );

    FNSCATF_decoder_top_16 decoder_instance16 (
        .clk(clk_decoder),
        .rst_n(rst_n),
        .codeword_in(tsv_16),
        .data_reg(dataout_16)
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
        tsv_16 <= 0;
        tsvLast <= 0;
        datain_16 <= 0;
        #1;
        clk_encoder <= 1;
        #1;
        clk_decoder <= 1;
        #1;
        for (cnt_i = 0; cnt_i < N_SIMU_CYCLE; cnt_i++) begin: for_cnt_i
            #1;
            clk_encoder <= 0;
            clk_decoder <= 0;
            tsvLast <= tsv_16;
            datain_16 = {$random} % (2**(`VH_FNSCATF_DataInBitWidth_16bitCW));

            #1;
            clk_encoder <= 1;
            #1;
            clk_decoder <= 1;
            #1;
            if (dataout_16 != datain_16) begin
                cnt_err = cnt_err + 1;
                $display("CODEC16-%d-ERROR: %d -> %b -> %d", cnt_i, datain_16, tsv_16, dataout_16);
            end
            else begin
                cnt_pass = cnt_pass + 1;
                $display("CODEC16-%d-PASS: %d -> %b -> %d", cnt_i, datain_16, tsv_16, dataout_16);
            end
            for (idx_i = 0; idx_i < 15; idx_i++) begin
                if ( (tsvTrans[idx_i] != 0) && (tsvTrans[idx_i+1] != 0) ) begin
                    $display("---ERROR! CAC rule violated!---");
                    cnt_violate = cnt_violate + 1;
                    $finish();
                end
                if ( (tsvTrans[15] != 0) && (tsvTrans[0] != 0) ) begin
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
