`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/12/08 20:27:06
// Design Name: 
// Module Name: VCDGen_Hex8x8Trans_ForFNSCATFPaper_WorstCase
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
module VCDGen_Hex8x8Trans_ForFNSCATFPaper_WorstCase(

    );

    // VCD
    initial begin
        $dumpvars(1, VCDGen_Hex8x8Trans_ForFNSCATFPaper_WorstCase.clk, VCDGen_Hex8x8Trans_ForFNSCATFPaper_WorstCase.data_in);
        $dumpfile();
    end
    
    // CLK
    reg clk;
    initial begin
        clk <= 1'b0;
        #0.5;
        clk <= 1'b1;
        #1;
        $finish();
    end
    
    // NO CAC
    reg [63 : 0] nocac_datain;
    initial begin
        nocac_datain <= {64{1'b0}};
        #0.5;
        nocac_datain <= {64{1'b1}};
    end
    
    // FNSCATF
    reg [63 : 0] catf_datain;
    initial begin
        catf_datain <= {64{1'b0}};
        #0.5;
        catf_datain <= 64'b10101010_10101010_10101010_10101010_10101010_10101010_10101010_10101010;
    end

    //datain
    wire [63 : 0] data_in;
    assign data_in = catf_datain;

endmodule