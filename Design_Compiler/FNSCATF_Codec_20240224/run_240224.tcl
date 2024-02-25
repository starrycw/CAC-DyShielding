set param_period 1

set param_inputdelay 0.01


set FNSCATF_encoder_designs {FNSCATF_encoder_top_5 FNSCATF_encoder_top_6 FNSCATF_encoder_top_7 FNSCATF_encoder_top_8 FNSCATF_encoder_top_9 FNSCATF_encoder_top_10 FNSCATF_encoder_top_11 FNSCATF_encoder_top_12 FNSCATF_encoder_top_13 FNSCATF_encoder_top_14 FNSCATF_encoder_top_15 FNSCATF_encoder_top_16}

set FNSCATF_decoder_designs {FNSCATF_decoder_top_5 FNSCATF_decoder_top_6 FNSCATF_decoder_top_7 FNSCATF_decoder_top_8 FNSCATF_decoder_top_9 FNSCATF_decoder_top_10 FNSCATF_decoder_top_11 FNSCATF_decoder_top_12 FNSCATF_decoder_top_13 FNSCATF_decoder_top_14 FNSCATF_decoder_top_15 FNSCATF_decoder_top_16}

set FPF_encoder_designs {FPF_encoder_05 FPF_encoder_07 FPF_encoder_09 FPF_encoder_12 FPF_encoder_14 FPF_encoder_16}

set FTF_encoder_designs {FTF_encoder_05 FTF_encoder_07 FTF_encoder_09 FTF_encoder_12 FTF_encoder_14 FTF_encoder_16}

set FNS_decoder_designs {FNS_dec_05 FNS_dec_07 FNS_dec_09 FNS_dec_12 FNS_dec_14 FNS_dec_16}

set DPS_encoder_designs {DPS_encoder_05 DPS_encoder_07 DPS_encoder_09 DPS_encoder_11 DPS_encoder_13 DPS_encoder_16}

set DPS_decoder_designs {DPS_dec_05 DPS_dec_07 DPS_dec_09 DPS_dec_11 DPS_dec_13 DPS_dec_16}

set IDP_encoder_designs {IDP_encoder_05 IDP_encoder_07 IDP_encoder_09 IDP_encoder_11 IDP_encoder_14 IDP_encoder_16}

set IDP_decoder_designs {IDP_dec_05 IDP_dec_07 IDP_dec_09 IDP_dec_11 IDP_dec_14 IDP_dec_16}



foreach FNSCATF_enc_i $FNSCATF_encoder_designs {

    elaborate $FNSCATF_enc_i -architecture verilog -library DEFAULT -update

    reset_design

    create_clock -period $param_period [get_ports clk]

    set_input_delay -max $param_inputdelay -clock clk [get_ports datain]

    compile_ultra

    set report_name Report_

    append report_name $FNSCATF_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .area_rpt

    report_area > $report_name

    set report_name Report_

    append report_name $FNSCATF_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .pwr_rpt

    report_power > $report_name

    set report_name Report_

    append report_name $FNSCATF_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .delay_rpt

    report_timing -from [get_ports datain] -to [get_ports codeout[0]] > $report_name
}


foreach FNSCATF_dec_i $FNSCATF_decoder_designs {

    elaborate $FNSCATF_dec_i -architecture verilog -library DEFAULT -update

    reset_design

    create_clock -period $param_period [get_ports clk]

    set_input_delay -max $param_inputdelay -clock clk [get_ports codeword_in]

    compile_ultra

    set report_name Report_

    append report_name $FNSCATF_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .area_rpt

    report_area > $report_name

    set report_name Report_

    append report_name $FNSCATF_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .pwr_rpt

    report_power > $report_name

    set report_name Report_

    append report_name $FNSCATF_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .delay_rpt

    report_timing -from [get_ports codeword_in] > $report_name
}


foreach FPF_enc_i $FPF_encoder_designs {

    elaborate $FPF_enc_i -architecture verilog -library DEFAULT -update

    reset_design

    create_clock -period $param_period [get_ports clock]

    set_input_delay -max $param_inputdelay -clock clock [get_ports datain]

    compile_ultra

    set report_name Report_

    append report_name $FPF_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .area_rpt

    report_area > $report_name

    set report_name Report_

    append report_name $FPF_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .pwr_rpt

    report_power > $report_name

    set report_name Report_

    append report_name $FPF_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .delay_rpt

    report_timing -from [get_ports datain] > $report_name
}

foreach FTF_enc_i $FTF_encoder_designs {

    elaborate $FTF_enc_i -architecture verilog -library DEFAULT -update

    reset_design

    create_clock -period $param_period [get_ports clock]

    set_input_delay -max $param_inputdelay -clock clock [get_ports datain]

    compile_ultra

    set report_name Report_

    append report_name $FTF_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .area_rpt

    report_area > $report_name

    set report_name Report_

    append report_name $FTF_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .pwr_rpt

    report_power > $report_name

    set report_name Report_

    append report_name $FTF_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .delay_rpt

    report_timing -from [get_ports datain] > $report_name
}

foreach FNS_dec_i $FNS_decoder_designs {

    elaborate $FNS_dec_i -architecture verilog -library DEFAULT -update

    reset_design

    create_clock -period $param_period [get_ports clk]

    set_input_delay -max $param_inputdelay -clock clk [get_ports codein]

    compile_ultra

    set report_name Report_

    append report_name $FNS_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .area_rpt

    report_area > $report_name

    set report_name Report_

    append report_name $FNS_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .pwr_rpt

    report_power > $report_name

    set report_name Report_

    append report_name $FNS_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .delay_rpt

    report_timing -from [get_ports codein] > $report_name
}




foreach DPS_enc_i $DPS_encoder_designs {

    elaborate $DPS_enc_i -architecture verilog -library DEFAULT -update

    reset_design

    create_clock -period $param_period [get_ports clock]

    set_input_delay -max $param_inputdelay -clock clock [get_ports datain]

    compile_ultra

    set report_name Report_

    append report_name $DPS_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .area_rpt

    report_area > $report_name

    set report_name Report_

    append report_name $DPS_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .pwr_rpt

    report_power > $report_name

    set report_name Report_

    append report_name $DPS_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .delay_rpt

    report_timing -from [get_ports datain] > $report_name
}

foreach DPS_dec_i $DPS_decoder_designs {

    elaborate $DPS_dec_i -architecture verilog -library DEFAULT -update

    reset_design

    create_clock -period $param_period [get_ports clk]

    set_input_delay -max $param_inputdelay -clock clk [get_ports codein]

    compile_ultra

    set report_name Report_

    append report_name $DPS_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .area_rpt

    report_area > $report_name

    set report_name Report_

    append report_name $DPS_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .pwr_rpt

    report_power > $report_name

    set report_name Report_

    append report_name $DPS_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .delay_rpt

    report_timing -from [get_ports codein] > $report_name
}




foreach IDP_enc_i $IDP_encoder_designs {

    elaborate $IDP_enc_i -architecture verilog -library DEFAULT -update

    reset_design

    create_clock -period $param_period [get_ports clock]

    set_input_delay -max $param_inputdelay -clock clock [get_ports datain]

    compile_ultra

    set report_name Report_

    append report_name $IDP_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .area_rpt

    report_area > $report_name

    set report_name Report_

    append report_name $IDP_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .pwr_rpt

    report_power > $report_name

    set report_name Report_

    append report_name $IDP_enc_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .delay_rpt

    report_timing -from [get_ports datain] > $report_name
}

foreach IDP_dec_i $IDP_decoder_designs {

    elaborate $IDP_dec_i -architecture verilog -library DEFAULT -update

    reset_design

    create_clock -period $param_period [get_ports clk]

    set_input_delay -max $param_inputdelay -clock clk [get_ports codein]

    compile_ultra

    set report_name Report_

    append report_name $IDP_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .area_rpt

    report_area > $report_name

    set report_name Report_

    append report_name $IDP_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .pwr_rpt

    report_power > $report_name

    set report_name Report_

    append report_name $IDP_dec_i

    append report_name -

    append report_name $param_period

    append report_name -

    append report_name $param_inputdelay

    append report_name .delay_rpt

    report_timing -from [get_ports codein] > $report_name
}