import RingCAC_Alg.verilogCodeGen_ringCACCodec

for codeword_len in range(5, 17):
    #
    RingCAC_Alg.verilogCodeGen_ringCACCodec.vGen_FNSCATF_EncoderCore(codeword_bitwidth=codeword_len, if_export_file=True)
    RingCAC_Alg.verilogCodeGen_ringCACCodec.vGen_FNSCATF_DecoderCore(codeword_bitwidth=codeword_len, if_export_file=True)
    # RingCAC_Alg.verilogCodeGen_ringCACCodec.svGen_tb_FNSCATF_CodecCore(codeword_bitwidth=codeword_len, if_export_file=True, n_simuCycle=10000)

    RingCAC_Alg.verilogCodeGen_ringCACCodec.vGen_FNSCATF_EncoderTop(codeword_bitwidth=codeword_len, if_export_file=True)
    RingCAC_Alg.verilogCodeGen_ringCACCodec.vGen_FNSCATF_DecoderTop(codeword_bitwidth=codeword_len, if_export_file=True)
    RingCAC_Alg.verilogCodeGen_ringCACCodec.svGen_tb_FNSCATF_CodecTop(codeword_bitwidth=codeword_len, if_export_file=True)
    #