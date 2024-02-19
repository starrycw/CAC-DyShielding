import copy
import math

import RingCAC_Alg.Ring2CTransCAC_Codec
import RingCAC_Alg.CAC_enum


if False: # Codec01
    for len_cw in range(4, 21):
        Codec001 = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC(len_cw=len_cw)
        max_input = Codec001.getParam_maxInputLimitation()
        for dec_in in range(0, max_input + 1):
            cw_tuple = Codec001.encode(dec_value=dec_in)
            decoder_out = Codec001.decode(bin_tuple=copy.deepcopy(cw_tuple))
            print("{} -> {} -> {}".format(dec_in, cw_tuple, decoder_out))
            assert dec_in == decoder_out
            assert RingCAC_Alg.CAC_enum.ringCAC_trans_check(trans_tuple=cw_tuple, max_xtalk=2)

if False: # Codec02
    for len_cw in range(4, 25):
        Codec002 = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC_FNSBased(len_cw=len_cw)
        max_input = Codec002.getParam_maxInputLimitation()
        for dec_in in range(0, max_input + 1):
            cw_tuple = Codec002.encode(dec_value=dec_in)
            decoder_out = Codec002.decode(bin_tuple=copy.deepcopy(cw_tuple))
            print("{} -> {} -> {}".format(dec_in, cw_tuple, decoder_out))
            assert dec_in == decoder_out
            assert RingCAC_Alg.CAC_enum.ringCAC_trans_check(trans_tuple=cw_tuple, max_xtalk=2)

if False: # Codebook Calc - 01
    for len_cw in range(4, 21):
        RingCAC_Alg.CAC_enum.calc_codeword_number_all(n_bit=len_cw)


if True: # Bit Overhead Calc - 01
    for len_cw in range(4, 21):
        Codec001 = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC(len_cw=len_cw)
        max_cw_value = Codec001.getParam_maxInputLimitation()
        max_input_binLen = math.floor(math.log2(max_cw_value))
        max_input_binValue = (2 ** max_input_binLen) - 1
        overhead = (len_cw - max_input_binLen) / max_input_binLen
        ns_tuple = Codec001.getParam_nsTuple()
        print("cwLen={} - maxDec={} - maxInBitLen={} - maxInDec={} - overhead={} - NS={}".format(len_cw, max_cw_value, max_input_binLen, max_input_binValue, overhead, ns_tuple))
        RingCAC_Alg.CAC_enum.calc_codeword_number_all(n_bit=len_cw)

    Codec002 = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC_FNSBased(len_cw=20)
    print(Codec002.getParam_codewordNumberTuple_byCodeLength())
    print(Codec002.getParam_nsTuple())

if False: # Bit Overhead Calc - 02
    for len_cw in range(4, 101):
        Codec002 = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC_FNSBased(len_cw=len_cw)
        max_cw_value = Codec002.getParam_maxInputLimitation()
        max_input_binLen = math.floor(math.log2(max_cw_value))
        max_input_binValue = (2 ** max_input_binLen) - 1
        overhead = (len_cw - max_input_binLen) / max_input_binLen
        ns_tuple = Codec002.getParam_nsTuple()
        print("cwLen={} - maxDec={} - maxInBitLen={} - maxInDec={} - overhead={} - NS={}".format(len_cw, max_cw_value, max_input_binLen, max_input_binValue, overhead, ns_tuple))