# Examples

########################################################################################################################
########################################################################################################################
# FNS-CATF Codec Designs
########################################################################################################################
if True:
    import RingCAC_Alg.verilogCodeGen_ringCACCodec

    for codeword_len in range(5, 17): # Codeword length
        # FNSCATF Encoder Core
        RingCAC_Alg.verilogCodeGen_ringCACCodec.vGen_FNSCATF_EncoderCore(codeword_bitwidth=codeword_len, if_export_file=False)
        # FNSCATF Decoder Core
        RingCAC_Alg.verilogCodeGen_ringCACCodec.vGen_FNSCATF_DecoderCore(codeword_bitwidth=codeword_len, if_export_file=True)
        # Testbench of FNSCATF Codec Core
        RingCAC_Alg.verilogCodeGen_ringCACCodec.svGen_tb_FNSCATF_CodecCore(codeword_bitwidth=codeword_len, if_export_file=True, n_simuCycle=10000)

        # FNSCATF Encoder Top
        RingCAC_Alg.verilogCodeGen_ringCACCodec.vGen_FNSCATF_EncoderTop(codeword_bitwidth=codeword_len, if_export_file=True)
        # FNSCATF Decoder Top
        RingCAC_Alg.verilogCodeGen_ringCACCodec.vGen_FNSCATF_DecoderTop(codeword_bitwidth=codeword_len, if_export_file=True)
        # Testbench of FNSCATF Codec Top
        RingCAC_Alg.verilogCodeGen_ringCACCodec.svGen_tb_FNSCATF_CodecTop(codeword_bitwidth=codeword_len, if_export_file=True)
########################################################################################################################
########################################################################################################################