`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/12/05 16:06:53
// Design Name: 
// Module Name: VCDGen_Hex8x8Trans_ForFNSCATFPaper
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
`include "FNS.vh"
module VCDGen_Hex8x8Trans_ForFNSCATFPaper(

    );

// VCD
initial begin
    $dumpvars(1, VCDGen_Hex8x8Trans_ForFNSCATFPaper.rst_n, VCDGen_Hex8x8Trans_ForFNSCATFPaper.clk, VCDGen_Hex8x8Trans_ForFNSCATFPaper.data_in);
    $dumpfile();
end

// clk & rst
reg rst_n, clk;

initial begin
    # 100000;
    # 0.5;
    $finish();
end



initial begin
    clk <= 1'b0;
    forever #0.5 clk = ~clk;
end

initial begin
    rst_n = 1'b1;
    #0.5;
    rst_n = 1'b0;
    #0.5;
    rst_n = 1'b1;
end

// random data gen
reg [7 : 0] raw_data [7 : 0];
reg [5 : 0] raw_data_4fns [7 : 0];
reg [5 : 0] raw_data_4catf [7 : 0];
reg [6 : 0] raw_data_4mfns [7 : 0];
integer seed;
initial begin
    seed = 1;

    raw_data[0][7 : 0] <= 0;
    raw_data[1][7 : 0] <= 0;
    raw_data[2][7 : 0] <= 0;
    raw_data[3][7 : 0] <= 0;
    raw_data[4][7 : 0] <= 0;
    raw_data[5][7 : 0] <= 0;
    raw_data[6][7 : 0] <= 0;
    raw_data[7][7 : 0] <= 0;
    
    raw_data_4fns[0][5 : 0] <= 0;
    raw_data_4fns[1][5 : 0] <= 0;
    raw_data_4fns[2][5 : 0] <= 0;
    raw_data_4fns[3][5 : 0] <= 0;
    raw_data_4fns[4][5 : 0] <= 0;
    raw_data_4fns[5][5 : 0] <= 0;
    raw_data_4fns[6][5 : 0] <= 0;
    raw_data_4fns[7][5 : 0] <= 0;
    
    raw_data_4catf[0][5 : 0] <= 0;
    raw_data_4catf[1][5 : 0] <= 0;
    raw_data_4catf[2][5 : 0] <= 0;
    raw_data_4catf[3][5 : 0] <= 0;
    raw_data_4catf[4][5 : 0] <= 0;
    raw_data_4catf[5][5 : 0] <= 0;
    raw_data_4catf[6][5 : 0] <= 0;
    raw_data_4catf[7][5 : 0] <= 0;
    
    raw_data_4mfns[0][6 : 0] <= 0;
    raw_data_4mfns[1][6 : 0] <= 0;
    raw_data_4mfns[2][6 : 0] <= 0;
    raw_data_4mfns[3][6 : 0] <= 0;
    raw_data_4mfns[4][6 : 0] <= 0;
    raw_data_4mfns[5][6 : 0] <= 0;
    raw_data_4mfns[6][6 : 0] <= 0;
    raw_data_4mfns[7][6 : 0] <= 0;
    
    forever #1 begin
        raw_data[0][7 : 0] = $random(seed);
        raw_data[1][7 : 0] = $random(seed);
        raw_data[2][7 : 0] = $random(seed);
        raw_data[3][7 : 0] = $random(seed);
        raw_data[4][7 : 0] = $random(seed);
        raw_data[5][7 : 0] = $random(seed);
        raw_data[6][7 : 0] = $random(seed);
        raw_data[7][7 : 0] = $random(seed);
        
        raw_data_4fns[0][5 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS08);
        raw_data_4fns[1][5 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS08);
        raw_data_4fns[2][5 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS08);
        raw_data_4fns[3][5 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS08);
        raw_data_4fns[4][5 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS08);
        raw_data_4fns[5][5 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS08);
        raw_data_4fns[6][5 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS08);
        raw_data_4fns[7][5 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS08);
        
        raw_data_4catf[0][5 : 0] = {$random(seed)} % (`FNS09 + `FNS07 - 1);
        raw_data_4catf[1][5 : 0] = {$random(seed)} % (`FNS09 + `FNS07 - 1);
        raw_data_4catf[2][5 : 0] = {$random(seed)} % (`FNS09 + `FNS07 - 1);
        raw_data_4catf[3][5 : 0] = {$random(seed)} % (`FNS09 + `FNS07 - 1);
        raw_data_4catf[4][5 : 0] = {$random(seed)} % (`FNS09 + `FNS07 - 1);
        raw_data_4catf[5][5 : 0] = {$random(seed)} % (`FNS09 + `FNS07 - 1);
        raw_data_4catf[6][5 : 0] = {$random(seed)} % (`FNS09 + `FNS07 - 1);
        raw_data_4catf[7][5 : 0] = {$random(seed)} % (`FNS09 + `FNS07 - 1);
        
        raw_data_4mfns[0][6 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS09);
        raw_data_4mfns[1][6 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS09);
        raw_data_4mfns[2][6 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS09);
        raw_data_4mfns[3][6 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS09);
        raw_data_4mfns[4][6 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS09);
        raw_data_4mfns[5][6 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS09);
        raw_data_4mfns[6][6 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS09);
        raw_data_4mfns[7][6 : 0] = {$random(seed)} % (`FNS01 + `FNS02 + `FNS03 + `FNS04 + `FNS05 + `FNS06 + `FNS07 + `FNS09);
        
    end
end

/////////////////////////////////////////////////////////////////////////////////////////////////
// FNSCATF
wire [63 : 0] bitmap_fnscatf;

FNSCATF_encoder_top_8_extended fnscatf_00 (
    .clk(clk),
    .rst_n(rst_n),
    .datain(raw_data_4catf[0][5:0]),
    .codeword_regs({bitmap_fnscatf[0], bitmap_fnscatf[1], bitmap_fnscatf[2], bitmap_fnscatf[3], 
                    bitmap_fnscatf[11], bitmap_fnscatf[10], bitmap_fnscatf[9], bitmap_fnscatf[8]})
    );

FNSCATF_encoder_top_8_extended fnscatf_01 (
    .clk(clk),
    .rst_n(rst_n),
    .datain(raw_data_4catf[1][5:0]),
    .codeword_regs({bitmap_fnscatf[4], bitmap_fnscatf[5], bitmap_fnscatf[6], bitmap_fnscatf[7], 
                    bitmap_fnscatf[15], bitmap_fnscatf[14], bitmap_fnscatf[13], bitmap_fnscatf[12]})
    );

FNSCATF_encoder_top_8_extended fnscatf_02 (
    .clk(clk),
    .rst_n(rst_n),
    .datain(raw_data_4catf[2][5:0]),
    .codeword_regs({bitmap_fnscatf[16], bitmap_fnscatf[17], bitmap_fnscatf[18], bitmap_fnscatf[19], 
                    bitmap_fnscatf[27], bitmap_fnscatf[26], bitmap_fnscatf[25], bitmap_fnscatf[24]})
    );

FNSCATF_encoder_top_8_extended fnscatf_03 (
    .clk(clk),
    .rst_n(rst_n),
    .datain(raw_data_4catf[3][5:0]),
    .codeword_regs({bitmap_fnscatf[20], bitmap_fnscatf[21], bitmap_fnscatf[22], bitmap_fnscatf[23], 
                    bitmap_fnscatf[31], bitmap_fnscatf[30], bitmap_fnscatf[29], bitmap_fnscatf[28]})
    );

FNSCATF_encoder_top_8_extended fnscatf_04 (
    .clk(clk),
    .rst_n(rst_n),
    .datain(raw_data_4catf[4][5:0]),
    .codeword_regs({bitmap_fnscatf[32], bitmap_fnscatf[33], bitmap_fnscatf[34], bitmap_fnscatf[35], 
                    bitmap_fnscatf[43], bitmap_fnscatf[42], bitmap_fnscatf[41], bitmap_fnscatf[40]})
    );

FNSCATF_encoder_top_8_extended fnscatf_05 (
    .clk(clk),
    .rst_n(rst_n),
    .datain(raw_data_4catf[5][5:0]),
    .codeword_regs({bitmap_fnscatf[36], bitmap_fnscatf[37], bitmap_fnscatf[38], bitmap_fnscatf[39], 
                    bitmap_fnscatf[47], bitmap_fnscatf[46], bitmap_fnscatf[45], bitmap_fnscatf[44]})
    );

FNSCATF_encoder_top_8_extended fnscatf_06 (
    .clk(clk),
    .rst_n(rst_n),
    .datain(raw_data_4catf[6][5:0]),
    .codeword_regs({bitmap_fnscatf[48], bitmap_fnscatf[49], bitmap_fnscatf[50], bitmap_fnscatf[51], 
                    bitmap_fnscatf[59], bitmap_fnscatf[58], bitmap_fnscatf[57], bitmap_fnscatf[56]})
    );

FNSCATF_encoder_top_8_extended fnscatf_07 (
    .clk(clk),
    .rst_n(rst_n),
    .datain(raw_data_4catf[7][5:0]),
    .codeword_regs({bitmap_fnscatf[52], bitmap_fnscatf[53], bitmap_fnscatf[54], bitmap_fnscatf[55], 
                    bitmap_fnscatf[63], bitmap_fnscatf[62], bitmap_fnscatf[61], bitmap_fnscatf[60]})
    );

/////////////////////////////////////////////////////////////////////////////////////////////////
// FNSFTF
wire [63 : 0] bitmap_fnsftf;

FTF_encoder_08_extended fnsftf_00 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[0][5:0]),
    .codeout(bitmap_fnsftf[7:0])
    );

FTF_encoder_08_extended fnsftf_01 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[1][5:0]),
    .codeout(bitmap_fnsftf[15:8])
    );

FTF_encoder_08_extended fnsftf_02 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[2][5:0]),
    .codeout(bitmap_fnsftf[23:16])
    );

FTF_encoder_08_extended fnsftf_03 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[3][5:0]),
    .codeout(bitmap_fnsftf[31:24])
    );

FTF_encoder_08_extended fnsftf_04 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[4][5:0]),
    .codeout(bitmap_fnsftf[39:32])
    );

FTF_encoder_08_extended fnsftf_05 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[5][5:0]),
    .codeout(bitmap_fnsftf[47:40])
    );

FTF_encoder_08_extended fnsftf_06 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[6][5:0]),
    .codeout(bitmap_fnsftf[55:48])
    );

FTF_encoder_08_extended fnsftf_07 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[7][5:0]),
    .codeout(bitmap_fnsftf[63:56])
    );

/////////////////////////////////////////////////////////////////////////////////////////////////
// FNSFPF
wire [63 : 0] bitmap_fnsfpf;

FPF_encoder_08_extended fnsfpf_00 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[0][5:0]),
    .codeout(bitmap_fnsfpf[7:0])
    );

FPF_encoder_08_extended fnsfpf_01 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[1][5:0]),
    .codeout(bitmap_fnsfpf[15:8])
    );

FPF_encoder_08_extended fnsfpf_02 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[2][5:0]),
    .codeout(bitmap_fnsfpf[23:16])
    );

FPF_encoder_08_extended fnsfpf_03 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[3][5:0]),
    .codeout(bitmap_fnsfpf[31:24])
    );

FPF_encoder_08_extended fnsfpf_04 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[4][5:0]),
    .codeout(bitmap_fnsfpf[39:32])
    );

FPF_encoder_08_extended fnsfpf_05 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[5][5:0]),
    .codeout(bitmap_fnsfpf[47:40])
    );

FPF_encoder_08_extended fnsfpf_06 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[6][5:0]),
    .codeout(bitmap_fnsfpf[55:48])
    );

FPF_encoder_08_extended fnsfpf_07 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4fns[7][5:0]),
    .codeout(bitmap_fnsfpf[63:56])
    );

// DBI
wire [63 : 0] bitmap_dbi;

DBI_encoder_08 dbi_00 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data[0][6:0]),
    .codeout(bitmap_dbi[7:0])
    );

DBI_encoder_08 dbi_01 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data[1][6:0]),
    .codeout(bitmap_dbi[15:8])
    );

DBI_encoder_08 dbi_02 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data[2][6:0]),
    .codeout(bitmap_dbi[23:16])
    );

DBI_encoder_08 dbi_03 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data[3][6:0]),
    .codeout(bitmap_dbi[31:24])
    );

DBI_encoder_08 dbi_04 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data[4][6:0]),
    .codeout(bitmap_dbi[39:32])
    );

DBI_encoder_08 dbi_05 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data[5][6:0]),
    .codeout(bitmap_dbi[47:40])
    );

DBI_encoder_08 dbi_06 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data[6][6:0]),
    .codeout(bitmap_dbi[55:48])
    );

DBI_encoder_08 dbi_07 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data[7][6:0]),
    .codeout(bitmap_dbi[63:56])
    );

// No-CAC
reg [63 : 0] bitmap_nocac;

always @(posedge clk or negedge rst_n) begin
    if (~rst_n) begin
        bitmap_nocac[63 : 0] <= 0;
    end
    else begin
        bitmap_nocac[63 : 0] <= {raw_data[0][7:0], raw_data[1][7:0], raw_data[2][7:0], raw_data[3][7:0], 
                                raw_data[4][7:0], raw_data[5][7:0], raw_data[6][7:0], raw_data[7][7:0]};
    end
end



/////////////////////////////////////////////////////////////////////////////////////////////////
// MFNS
wire [63 : 0] bitmap_mfns;

MFNS_encoder_08_extended mfns_00 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4mfns[0][6:0]),
    .codeout(bitmap_mfns[7:0])
    );

MFNS_encoder_08_extended mfns_01 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4mfns[1][6:0]),
    .codeout(bitmap_mfns[15:8])
    );

MFNS_encoder_08_extended mfns_02 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4mfns[2][6:0]),
    .codeout(bitmap_mfns[23:16])
    );

MFNS_encoder_08_extended mfns_03 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4mfns[3][6:0]),
    .codeout(bitmap_mfns[31:24])
    );

MFNS_encoder_08_extended mfns_04 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4mfns[4][6:0]),
    .codeout(bitmap_mfns[39:32])
    );

MFNS_encoder_08_extended mfns_05 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4mfns[5][6:0]),
    .codeout(bitmap_mfns[47:40])
    );

MFNS_encoder_08_extended mfns_06 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4mfns[6][6:0]),
    .codeout(bitmap_mfns[55:48])
    );

MFNS_encoder_08_extended mfns_07 (
    .clock(clk),
    .rst_n(rst_n),
    .datain(raw_data_4mfns[7][6:0]),
    .codeout(bitmap_mfns[63:56])
    );

/////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////
// Eliminate X-state
reg [63 : 0] xmask;

reg [63 : 0] trans_nocac;
reg [63 : 0] trans_fnsftf;
reg [63 : 0] trans_fnsfpf;
reg [63 : 0] trans_mfns;
reg [63 : 0] trans_dbi;
reg [63 : 0] trans_fnscatf;

initial begin
    xmask <= 64'b0;
    #1;
    xmask <= {64{1'b1}};
end

always @(*) begin
    trans_nocac <= bitmap_nocac & xmask;
    trans_fnsftf <= bitmap_fnsftf & xmask;
    trans_fnsfpf <= bitmap_fnsfpf & xmask;
    trans_mfns <= bitmap_mfns & xmask;
    trans_dbi <= bitmap_dbi & xmask;
    trans_fnscatf <= bitmap_fnscatf & xmask;
end

reg [63 : 0] data_in;
always @(*) begin
    data_in = trans_fnscatf;
end

endmodule
