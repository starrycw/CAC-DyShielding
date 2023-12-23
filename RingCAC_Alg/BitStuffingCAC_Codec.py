import copy


class BSCAC_ForHexDyS2C_2CSupFor7bitGroup:
    '''
    Implementation of the Bit-Stuffing Codec for a 7-bit group (1 center TSV + 6 surrounding TSVs), designed for the hex TSV array with 2C dy-shielding.
    '''
    def __init__(self, instance_id=None):
        self.Param_id = instance_id

    def encoder_core(self, bits_to_be_trans: list, last_codeword: tuple):
        '''
        Core algorithm.
        ######################
        #         d1         #
        #   d6          d2   #
        #         d0         #
        #   d5          d3   #
        #         d4         #
        ######################

        The -2C algorithm are as follows:

        1. If d0 has no transition in [t-1]->[t]:
            d1 ~ d6 are encoded in order.
            If d{i}[t-1] == d{i-1}[t] != d{i-1}[t-1], in which 2 <= i <= 6, then d{i}[t] should be a stuffing bit.
            Otherwise, d{i}[t] transmits a data bit.

        2. If d0 has a transition in [t-1]->[t]:
            Firstly, mark all the d{i} satisfying d{i}[t-1] == d0[t-1] as the free bit, in which 1 <= i <= 6. The free bits transmit data bits.
            Secondly, for the remaining d{i} except free bits: If none of its two adjancent bits are free bits, it transmits data bit; otherwise, it should be a stuffing bit.

        :param bits_to_be_trans:
        :param last_codeword:
        :return: tuple, int, list - The codeword tuple, the number of data bits encoded, and the unprocessed data bit list.
        '''
        assert isinstance(bits_to_be_trans, list)
        assert isinstance(last_codeword, tuple)
        assert len(last_codeword) == 7

        n_transmitted_bits = 0 # The data bit number can be processed in this encoding
        current_data_bits_list = copy.deepcopy(bits_to_be_trans) # A copy of data bit list
        codeword_list = []

        # main
        assert last_codeword[0] in (0, 1)
        assert current_data_bits_list[0] in (0, 1)
        codeword_list.append(current_data_bits_list.pop(0))
        n_transmitted_bits = 1

        if last_codeword[0] == bits_to_be_trans[0]: # Case 1
            # d1 is a data bit
            assert current_data_bits_list[0] in (0, 1)
            assert last_codeword[1] in (0, 1)
            codeword_list.append(current_data_bits_list.pop(0))
            n_transmitted_bits = n_transmitted_bits + 1

            # d2 ~ d6
            for idx_i in range(2, 7):
                assert current_data_bits_list[0] in (0, 1)
                assert last_codeword[idx_i] in (0, 1)
                if (last_codeword[idx_i] == codeword_list[-1]) and (last_codeword[idx_i] != last_codeword[idx_i - 1]):
                    codeword_list.append(last_codeword[idx_i])
                else:
                    codeword_list.append(current_data_bits_list.pop(0))
                    n_transmitted_bits = n_transmitted_bits + 1

        else: # Case 2
            # free bits
            flags_freebit = []
            flags_freebit.append('hi!')
            for idx_i in range(1, 7):
                assert last_codeword[idx_i] in (0, 1)
                if last_codeword[idx_i] == last_codeword[0]:
                    flags_freebit.append(True)
                else:
                    flags_freebit.append(False)
            # print(flags_freebit)

            # d1
            assert current_data_bits_list[0] in (0, 1)
            if (flags_freebit[1] is True) or ( (flags_freebit[6] is False) and (flags_freebit[2] is False) ):
                codeword_list.append(current_data_bits_list.pop(0))
                n_transmitted_bits = n_transmitted_bits + 1
            else:
                codeword_list.append(last_codeword[1])

            # d2 ~ d5
            for idx_k in range(2, 6):
                assert current_data_bits_list[0] in (0, 1)
                if (flags_freebit[idx_k] is True) or ( (flags_freebit[idx_k - 1] is False) and (flags_freebit[idx_k + 1] is False) ):
                    codeword_list.append(current_data_bits_list.pop(0))
                    n_transmitted_bits = n_transmitted_bits + 1
                else:
                    codeword_list.append(last_codeword[idx_k])

            # d6
            assert current_data_bits_list[0] in (0, 1)
            if (flags_freebit[6] is True) or ( (flags_freebit[5] is False) and (flags_freebit[1] is False) ):
                codeword_list.append(current_data_bits_list.pop(0))
                n_transmitted_bits = n_transmitted_bits + 1
            else:
                codeword_list.append(last_codeword[6])

        assert len(codeword_list) == 7
        codeword_tuple = tuple(codeword_list)
        return codeword_tuple, n_transmitted_bits, copy.deepcopy(current_data_bits_list)


    def decoder_core(self, codeword_to_be_decode: tuple, last_codeword: tuple):
        '''
        Core algorithm.
        ######################
        #         d1         #
        #   d6          d2   #
        #         d0         #
        #   d5          d3   #
        #         d4         #
        ######################

        The -2C algorithm are as follows:

        1. If d0 has no transition in [t-1]->[t]:
            d1 ~ d6 are encoded in order.
            If d{i}[t-1] == d{i-1}[t] != d{i-1}[t-1], in which 2 <= i <= 6, then d{i}[t] should be a stuffing bit.
            Otherwise, d{i}[t] transmits a data bit.

        2. If d0 has a transition in [t-1]->[t]:
            Firstly, mark all the d{i} satisfying d{i}[t-1] == d0[t-1] as the free bit, in which 1 <= i <= 6. The free bits transmit data bits.
            Secondly, for the remaining d{i} except free bits: If none of its two adjancent bits are free bits, it transmits data bit; otherwise, it should be a stuffing bit.

        :param codeword_to_be_decode:
        :param last_codeword:
        :return:
        '''
        assert isinstance(codeword_to_be_decode, tuple)
        assert isinstance(last_codeword, tuple)
        assert len(codeword_to_be_decode) == 7
        assert len(last_codeword) == 7
        for idx_i in range(0, 7):
            assert codeword_to_be_decode[idx_i] in (0, 1)
            assert last_codeword[idx_i] in (0, 1)

        data_recovered_list = []
        idx_list_stuffingbit = []
        data_recovered_list.append(codeword_to_be_decode[0])

        if codeword_to_be_decode[0] == last_codeword[0]: # Case 1
            # c1
            data_recovered_list.append(codeword_to_be_decode[1])
            # c2 ~ c6
            for idx_i in range(2, 7):
                if (last_codeword[idx_i] != last_codeword[idx_i-1]) and (last_codeword[idx_i] == codeword_to_be_decode[idx_i-1]):
                    idx_list_stuffingbit.append(idx_i)
                else:
                    data_recovered_list.append(codeword_to_be_decode[idx_i])

        else: # Case2
            # free bits
            flags_freebit = []
            flags_freebit.append('hi!')
            for idx_i in range(1, 7):
                if last_codeword[idx_i] == last_codeword[0]:
                    flags_freebit.append(True)
                else:
                    flags_freebit.append(False)
            # c1
            if (flags_freebit[1] is True) or ( (flags_freebit[6] is False) and (flags_freebit[2] is False) ):
                data_recovered_list.append(codeword_to_be_decode[1])
            else:
                idx_list_stuffingbit.append(1)

            # c2 ~ c5
            for idx_i in range(2, 6):
                if (flags_freebit[idx_i] is True) or ( (flags_freebit[idx_i - 1] is False) and (flags_freebit[idx_i + 1] is False) ):
                    data_recovered_list.append(codeword_to_be_decode[idx_i])
                else:
                    idx_list_stuffingbit.append(idx_i)

            # c6
            if (flags_freebit[6] is True) or ( (flags_freebit[5] is False) and (flags_freebit[1] is False) ):
                data_recovered_list.append(codeword_to_be_decode[6])
            else:
                idx_list_stuffingbit.append(6)

        # print(len(idx_list_stuffingbit), len(data_recovered_list))
        assert len(idx_list_stuffingbit) + len(data_recovered_list) == 7
        data_recovered_tuple = tuple(data_recovered_list)
        idx_tuple_stuffingbit = tuple(idx_list_stuffingbit)

        return data_recovered_tuple, idx_tuple_stuffingbit
