`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// verilogCodeGen_ringCACCodec [ver = 20240221-01] [Creation Time = 2024_02_22-21_06_54]
// The testbench of the FNS-CATF encoder & decoder.
// codeword_bitwidth=13
//////////////////////////////////////////////////////////////////////////////////

`include "VHeader_FNSCATF.vh"

module tb_FNSCATF_codecTop13(

    );
    parameter N_SIMU_CYCLE = 10000;
    reg clk_encoder, clk_decoder, rst_n;
    reg [12 : 0] tsvLast;
    wire [12 : 0] tsvTrans;
    // 13-bit codec core
    reg [12 : 0] tsv_13;
    reg [`VH_FNSCATF_DataInBitWidth_13bitCW - 1 : 0] datain_13;
    reg [`VH_FNSCATF_DataInBitWidth_13bitCW - 1 : 0] dataout_13;
    assign tsvTrans = tsvLast ^ tsv_13;
    FNSCATF_encoder_top_13 encoder_instance13 (
        .clk(clk_encoder),
        .rst_n(rst_n),
        .datain(datain_13),
        .codeword_regs(tsv_13)
    );

    FNSCATF_decoder_top_13 decoder_instance13 (
        .clk(clk_decoder),
        .rst_n(rst_n),
        .codeword_in(tsv_13),
        .data_reg(dataout_13)
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
        tsv_13 <= 0;
        tsvLast <= 0;
        datain_13 <= 0;
        #1;
        clk_encoder <= 1;
        #1;
        clk_decoder <= 1;
        #1;
        for (cnt_i = 0; cnt_i < N_SIMU_CYCLE; cnt_i++) begin: for_cnt_i
            #1;
            clk_encoder <= 0;
            clk_decoder <= 0;
            tsvLast <= tsv_13;
            datain_13 = {$random} % (2**(`VH_FNSCATF_DataInBitWidth_13bitCW));

            #1;
            clk_encoder <= 1;
            #1;
            clk_decoder <= 1;
            #1;
            if (dataout_13 != datain_13) begin
                cnt_err = cnt_err + 1;
                $display("CODEC13-%d-ERROR: %d -> %b -> %d", cnt_i, datain_13, tsv_13, dataout_13);
            end
            else begin
                cnt_pass = cnt_pass + 1;
                $display("CODEC13-%d-PASS: %d -> %b -> %d", cnt_i, datain_13, tsv_13, dataout_13);
            end
            for (idx_i = 0; idx_i < 12; idx_i++) begin
                if ( (tsvTrans[idx_i] != 0) && (tsvTrans[idx_i+1] != 0) ) begin
                    $display("---ERROR! CAC rule violated!---");
                    cnt_violate = cnt_violate + 1;
                    $finish();
                end
                if ( (tsvTrans[12] != 0) && (tsvTrans[0] != 0) ) begin
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
