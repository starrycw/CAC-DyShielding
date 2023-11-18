import copy
import math

import RingCAC_Alg.Ring2CTransCAC_Codec
import RingCAC_Alg.CAC_enum


if False: # Codec
    for len_cw in range(4, 21):
        Codec001 = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC(len_cw=len_cw)
        max_input = Codec001.getParam_maxInputLimitation()
        for dec_in in range(0, max_input + 1):
            cw_tuple = Codec001.encode(dec_value=dec_in)
            decoder_out = Codec001.decode(bin_tuple=copy.deepcopy(cw_tuple))
            print("{} -> {} -> {}".format(dec_in, cw_tuple, decoder_out))
            assert dec_in == decoder_out
            assert RingCAC_Alg.CAC_enum.ringCAC_trans_check(trans_tuple=cw_tuple, max_xtalk=2)

if True: # Bit Overhead Calc
    for len_cw in range(4, 21):
        Codec001 = RingCAC_Alg.Ring2CTransCAC_Codec.Codec_Ring2CTransCAC(len_cw=len_cw)
        max_cw_value = Codec001.getParam_maxInputLimitation()
        max_input_binLen = math.floor(math.log2(max_cw_value))
        max_input_binValue = (2 ** max_input_binLen) - 1
        overhead = (len_cw - max_input_binLen) / max_input_binLen
        print("cwLen={} - maxDec={} - maxInBitLen={} - maxInDec={} - overhead={}".format(len_cw, max_cw_value, max_input_binLen, max_input_binValue, overhead))