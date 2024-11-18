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

    def xtalkCalc(self, codeword_tuple_last: tuple[int, ...], codeword_tuple_current: tuple[int, ...]):
        '''
        Calc the xtalk of each bit in transition (d'0, d'1, ..., d'6)->(d0, d1, ..., d6).
        ######################
        #         d1         #
        #   d6          d2   #
        #         d0         #
        #   d5          d3   #
        #         d4         #
        ######################
        :param codeword_tuple_last: tuple
        :param codeword_tuple_current: tuple
        :return:
        '''

        #######################################################
        def subfunc_xtalk_calc(cw01, cw02):
            assert isinstance(cw01, tuple) and isinstance(cw02, tuple)
            assert cw01 in ((0, 0), (0, 1), (1, 0), (1, 1))
            assert cw02 in ((0, 0), (0, 1), (1, 0), (1, 1))
            if (cw02[0] - cw01[0]) == (cw02[1] - cw01[1]):
                return 0
            elif (cw02[0] - cw01[0]) == 0 or (cw02[1] - cw01[1]) == 0:
                return 1
            elif (cw02[0] - cw01[0]) + (cw02[1] - cw01[1]) == 0:
                return 2
            else:
                assert False
        #######################################################

        assert isinstance(codeword_tuple_last, tuple) and len(codeword_tuple_last) == 7
        assert isinstance(codeword_tuple_current, tuple) and len(codeword_tuple_current) == 7

        xtalk_list = []

        ####################0, 1, 2, 3, 4, 5, 6##########
        adjancentMatrix = ((0, 1, 1, 1, 1, 1, 1),##0
                           (1, 0, 1, 0, 0, 0, 1),##1
                           (1, 1, 0, 1, 0, 0, 0),##2
                           (1, 0, 1, 0, 1, 0, 0),##3
                           (1, 0, 0, 1, 0, 1, 0),##4
                           (1, 0, 0, 0, 1, 0, 1),##5
                           (1, 1, 0, 0, 0, 1, 0),##6
                           )
        for idx_a in range(0, 7):
            xtalk_sum = 0
            for idx_b in range(0, 7):
                cwww01 = (codeword_tuple_last[idx_a], codeword_tuple_last[idx_b])
                cwww02 = (codeword_tuple_current[idx_a], codeword_tuple_current[idx_b])
                xtalk_sum = xtalk_sum + ( (adjancentMatrix[idx_a][idx_b]) * subfunc_xtalk_calc(cw01=cwww01, cw02=cwww02) )
            xtalk_list.append(xtalk_sum)
            if xtalk_sum > 4:
                assert idx_a == 0

        xtalk_tuple = tuple(xtalk_list)
        return xtalk_tuple

    def xtalkCalc_noAssert(self, codeword_tuple_last: tuple[int, ...], codeword_tuple_current: tuple[int, ...]):
        '''
        Calc the xtalk of each bit in transition (d'0, d'1, ..., d'6)->(d0, d1, ..., d6).
        ######################
        #         d1         #
        #   d6          d2   #
        #         d0         #
        #   d5          d3   #
        #         d4         #
        ######################
        :param codeword_tuple_last: tuple
        :param codeword_tuple_current: tuple
        :return:
        '''

        #######################################################
        def subfunc_xtalk_calc(cw01, cw02):
            assert isinstance(cw01, tuple) and isinstance(cw02, tuple)
            assert cw01 in ((0, 0), (0, 1), (1, 0), (1, 1))
            assert cw02 in ((0, 0), (0, 1), (1, 0), (1, 1))
            if (cw02[0] - cw01[0]) == (cw02[1] - cw01[1]):
                return 0
            elif (cw02[0] - cw01[0]) == 0 or (cw02[1] - cw01[1]) == 0:
                return 1
            elif (cw02[0] - cw01[0]) + (cw02[1] - cw01[1]) == 0:
                return 2
            else:
                assert False
        #######################################################

        assert isinstance(codeword_tuple_last, tuple) and len(codeword_tuple_last) == 7
        assert isinstance(codeword_tuple_current, tuple) and len(codeword_tuple_current) == 7

        xtalk_list = []

        ####################0, 1, 2, 3, 4, 5, 6##########
        adjancentMatrix = ((0, 1, 1, 1, 1, 1, 1),##0
                           (1, 0, 1, 0, 0, 0, 1),##1
                           (1, 1, 0, 1, 0, 0, 0),##2
                           (1, 0, 1, 0, 1, 0, 0),##3
                           (1, 0, 0, 1, 0, 1, 0),##4
                           (1, 0, 0, 0, 1, 0, 1),##5
                           (1, 1, 0, 0, 0, 1, 0),##6
                           )
        for idx_a in range(0, 7):
            xtalk_sum = 0
            for idx_b in range(0, 7):
                cwww01 = (codeword_tuple_last[idx_a], codeword_tuple_last[idx_b])
                cwww02 = (codeword_tuple_current[idx_a], codeword_tuple_current[idx_b])
                xtalk_sum = xtalk_sum + ( (adjancentMatrix[idx_a][idx_b]) * subfunc_xtalk_calc(cw01=cwww01, cw02=cwww02) )
            xtalk_list.append(xtalk_sum)
            # if xtalk_sum > 4:
            #     assert idx_a == 0

        xtalk_tuple = tuple(xtalk_list)
        return xtalk_tuple


class BSCAC_ForHexDyS2C_2CSupFor7bitGroup_ver20231224(BSCAC_ForHexDyS2C_2CSupFor7bitGroup):
    '''
    Implementation of the Bit-Stuffing Codec for a 7-bit group (1 center TSV + 6 surrounding TSVs), designed for the hex TSV array with 2C dy-shielding.
    Revised version - 20231224
    Based on the class BSCAC_ForHexDyS2C_2CSupFor7bitGroup.
    Changes:
        Improved codec algorithms:  In the case that d0 has a transition in [t-1]->[t], the bit that are not free bit but has at least one adjacent free bit now has a chance to transmit data bit.

    '''
    def __init__(self, instance_id=None):
        super().__init__(instance_id)

    def encoder_core(self, bits_to_be_trans: list, last_codeword: tuple):
        '''
        Core algorithm - Version 20231224.
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
            Secondly, for the remaining d{i} except free bits: If none of its two adjancent bits are free bits, it transmits data bit;
            Finally, for the bits that are not free bits but has at least one adjacent free bit:
                if all the adjacent free bits has no transition, or it has a non-free bit that has a transition, it transmits data bit;
                Otherwise, it transmits redundant bit.

        :param bits_to_be_trans:
        :param last_codeword:
        :return: tuple, int, list - The codeword tuple, the number of data bits encoded, and the unprocessed data bit list.
        '''
        assert isinstance(bits_to_be_trans, list)
        assert isinstance(last_codeword, tuple)
        assert len(last_codeword) == 7

        n_transmitted_bits = 0  # The data bit number can be processed in this encoding
        current_data_bits_list = copy.deepcopy(bits_to_be_trans)  # A copy of data bit list
        codeword_list = []

        # main
        assert last_codeword[0] in (0, 1)
        assert current_data_bits_list[0] in (0, 1)
        codeword_list.append(current_data_bits_list.pop(0))
        n_transmitted_bits = 1

        if last_codeword[0] == bits_to_be_trans[0]:  # Case 1
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

        else:  # Case 2
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

            flags_bit_noAdjacentFreeBit = []
            flags_bit_noAdjacentFreeBit.append('hi!')
            if (flags_freebit[2] is False) and (flags_freebit[6] is False):
                flags_bit_noAdjacentFreeBit.append(True)
            else:
                flags_bit_noAdjacentFreeBit.append(False)
            for idx_i in range(2, 6):
                if (flags_freebit[idx_i - 1] is False) and (flags_freebit[idx_i + 1] is False):
                    flags_bit_noAdjacentFreeBit.append(True)
                else:
                    flags_bit_noAdjacentFreeBit.append(False)
            if (flags_freebit[1] is False) and (flags_freebit[5] is False):
                flags_bit_noAdjacentFreeBit.append(True)
            else:
                flags_bit_noAdjacentFreeBit.append(False)

            idx_list_unprocessed = []

            # d1
            assert current_data_bits_list[0] in (0, 1)
            if (flags_freebit[1] is True) or ((flags_freebit[6] is False) and (flags_freebit[2] is False)):
                codeword_list.append(current_data_bits_list.pop(0))
                n_transmitted_bits = n_transmitted_bits + 1
            else:
                codeword_list.append(None)
                idx_list_unprocessed.append(1)

            # d2 ~ d5
            for idx_k in range(2, 6):
                assert current_data_bits_list[0] in (0, 1)
                if (flags_freebit[idx_k] is True) or ((flags_freebit[idx_k - 1] is False) and (flags_freebit[idx_k + 1] is False)):
                    codeword_list.append(current_data_bits_list.pop(0))
                    n_transmitted_bits = n_transmitted_bits + 1
                else:
                    codeword_list.append(None)
                    idx_list_unprocessed.append(idx_k)

            # d6
            assert current_data_bits_list[0] in (0, 1)
            if (flags_freebit[6] is True) or ((flags_freebit[5] is False) and (flags_freebit[1] is False)):
                codeword_list.append(current_data_bits_list.pop(0))
                n_transmitted_bits = n_transmitted_bits + 1
            else:
                codeword_list.append(None)
                idx_list_unprocessed.append(6)

            # Unprocessed bits
            for idx_r in idx_list_unprocessed:
                if idx_r == 1:
                    if (flags_freebit[6] is True) and (flags_freebit[2] is True) and (codeword_list[6] == last_codeword[6]) and (codeword_list[2] == last_codeword[2]):
                        codeword_list[1] = current_data_bits_list.pop(0)
                        n_transmitted_bits = n_transmitted_bits + 1
                    elif (flags_freebit[6] is False) and (codeword_list[6] != last_codeword[6]) and (flags_bit_noAdjacentFreeBit[6] is True):
                        codeword_list[1] = current_data_bits_list.pop(0)
                        n_transmitted_bits = n_transmitted_bits + 1
                    elif (flags_freebit[2] is False) and (codeword_list[2] != last_codeword[2]) and (flags_bit_noAdjacentFreeBit[2] is True):
                        codeword_list[1] = current_data_bits_list.pop(0)
                        n_transmitted_bits = n_transmitted_bits + 1
                    else:
                        codeword_list[1] = last_codeword[1]

                elif idx_r == 6:
                    if (flags_freebit[5] is True) and (flags_freebit[1] is True) and (codeword_list[5] == last_codeword[5]) and (codeword_list[1] == last_codeword[1]):
                        codeword_list[6] = current_data_bits_list.pop(0)
                        n_transmitted_bits = n_transmitted_bits + 1
                    elif (flags_freebit[5] is False) and (codeword_list[5] != last_codeword[5]):
                        codeword_list[6] = current_data_bits_list.pop(0)
                        n_transmitted_bits = n_transmitted_bits + 1
                    elif (flags_freebit[1] is False) and (codeword_list[1] != last_codeword[1]):
                        codeword_list[6] = current_data_bits_list.pop(0)
                        n_transmitted_bits = n_transmitted_bits + 1
                    else:
                        codeword_list[6] = last_codeword[6]

                else:
                    if (flags_freebit[idx_r - 1] is True) and (flags_freebit[idx_r + 1] is True) and (codeword_list[idx_r - 1] == last_codeword[idx_r - 1]) and (codeword_list[idx_r + 1] == last_codeword[idx_r + 1]):
                        codeword_list[idx_r] = current_data_bits_list.pop(0)
                        n_transmitted_bits = n_transmitted_bits + 1
                    elif (flags_freebit[idx_r - 1] is False) and (codeword_list[idx_r - 1] != last_codeword[idx_r - 1]):
                        codeword_list[idx_r] = current_data_bits_list.pop(0)
                        n_transmitted_bits = n_transmitted_bits + 1
                    elif (flags_freebit[idx_r + 1] is False) and (codeword_list[idx_r + 1] != last_codeword[idx_r + 1]) and (flags_bit_noAdjacentFreeBit[idx_r + 1] is True):
                        codeword_list[idx_r] = current_data_bits_list.pop(0)
                        n_transmitted_bits = n_transmitted_bits + 1
                    else:
                        codeword_list[idx_r] = last_codeword[idx_r]

        assert len(codeword_list) == 7
        codeword_tuple = tuple(codeword_list)
        return codeword_tuple, n_transmitted_bits, copy.deepcopy(current_data_bits_list)

    def decoder_core(self, codeword_to_be_decode: tuple, last_codeword: tuple):
        '''
        Core algorithm - Version 20231224.
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
            Secondly, for the remaining d{i} except free bits: If none of its two adjancent bits are free bits, it transmits data bit;
            Finally, for the bits that are not free bits but has at least one adjacent free bit:
                if all the adjacent free bits has no transition, or it has a non-free bit that has a transition, it transmits data bit;
                Otherwise, it transmits redundant bit.

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

            flags_bit_noAdjacentFreeBit = []
            flags_bit_noAdjacentFreeBit.append('hi!')
            if (flags_freebit[2] is False) and (flags_freebit[6] is False):
                flags_bit_noAdjacentFreeBit.append(True)
            else:
                flags_bit_noAdjacentFreeBit.append(False)
            for idx_i in range(2, 6):
                if (flags_freebit[idx_i - 1] is False) and (flags_freebit[idx_i + 1] is False):
                    flags_bit_noAdjacentFreeBit.append(True)
                else:
                    flags_bit_noAdjacentFreeBit.append(False)
            if (flags_freebit[1] is False) and (flags_freebit[5] is False):
                flags_bit_noAdjacentFreeBit.append(True)
            else:
                flags_bit_noAdjacentFreeBit.append(False)

            idx_list_unprocessed = []


            # c1
            if (flags_freebit[1] is True) or ( (flags_freebit[6] is False) and (flags_freebit[2] is False) ):
                data_recovered_list.append(codeword_to_be_decode[1])
            else:
                idx_list_unprocessed.append(1)


            # c2 ~ c5
            for idx_i in range(2, 6):
                if (flags_freebit[idx_i] is True) or ( (flags_freebit[idx_i - 1] is False) and (flags_freebit[idx_i + 1] is False) ):
                    data_recovered_list.append(codeword_to_be_decode[idx_i])
                else:
                    idx_list_unprocessed.append(idx_i)


            # c6
            if (flags_freebit[6] is True) or ( (flags_freebit[5] is False) and (flags_freebit[1] is False) ):
                data_recovered_list.append(codeword_to_be_decode[6])
            else:
                idx_list_unprocessed.append(6)


            for idx_r in idx_list_unprocessed:
                if idx_r == 1:
                    if (flags_freebit[6] is True) and (flags_freebit[2] is True) and (
                            codeword_to_be_decode[6] == last_codeword[6]) and (
                            codeword_to_be_decode[2] == last_codeword[2]):
                        data_recovered_list.append(codeword_to_be_decode[1])
                    elif (flags_freebit[6] is False) and (codeword_to_be_decode[6] != last_codeword[6]) and (
                            flags_bit_noAdjacentFreeBit[6] is True):
                        data_recovered_list.append(codeword_to_be_decode[1])
                    elif (flags_freebit[2] is False) and (codeword_to_be_decode[2] != last_codeword[2]) and (
                            flags_bit_noAdjacentFreeBit[2] is True):
                        data_recovered_list.append(codeword_to_be_decode[1])
                    else:
                        idx_list_stuffingbit.append(1)
                elif idx_r == 6:
                    if (flags_freebit[5] is True) and (flags_freebit[1] is True) and (
                            codeword_to_be_decode[5] == last_codeword[5]) and (
                            codeword_to_be_decode[1] == last_codeword[1]):
                        data_recovered_list.append(codeword_to_be_decode[6])
                    elif (flags_freebit[5] is False) and (codeword_to_be_decode[5] != last_codeword[5]):
                        data_recovered_list.append(codeword_to_be_decode[6])
                    elif (flags_freebit[1] is False) and (codeword_to_be_decode[1] != last_codeword[1]):
                        data_recovered_list.append(codeword_to_be_decode[6])
                    else:
                        idx_list_stuffingbit.append(6)
                else:
                    if (flags_freebit[idx_r - 1] is True) and (flags_freebit[idx_r + 1] is True) and (codeword_to_be_decode[idx_r - 1] == last_codeword[idx_r - 1]) and (codeword_to_be_decode[idx_r + 1] == last_codeword[idx_r + 1]):
                        data_recovered_list.append(codeword_to_be_decode[idx_r])
                    elif (flags_freebit[idx_r - 1] is False) and (codeword_to_be_decode[idx_r - 1] != last_codeword[idx_r - 1]):
                        data_recovered_list.append(codeword_to_be_decode[idx_r])
                    elif (flags_freebit[idx_r + 1] is False) and (codeword_to_be_decode[idx_r + 1] != last_codeword[idx_r + 1]) and (flags_bit_noAdjacentFreeBit[idx_r + 1] is True):
                        data_recovered_list.append(codeword_to_be_decode[idx_r])
                    else:
                        idx_list_stuffingbit.append(idx_r)



        # print(len(idx_list_stuffingbit), len(data_recovered_list))
        assert len(idx_list_stuffingbit) + len(data_recovered_list) == 7
        data_recovered_tuple = tuple(data_recovered_list)
        idx_tuple_stuffingbit = tuple(idx_list_stuffingbit)

        return data_recovered_tuple, idx_tuple_stuffingbit




class BSCAC_ForHexDyS2C_2CSupFor7bitGroup_parallelDataIn(BSCAC_ForHexDyS2C_2CSupFor7bitGroup):
    '''
    Implementation of the Bit-Stuffing Codec for a 7-bit group (1 center TSV + 6 surrounding TSVs), designed for the hex TSV array with 2C dy-shielding.
    Revised version - 20231224
    Based on the class BSCAC_ForHexDyS2C_2CSupFor7bitGroup.
    Changes:
        Improved codec algorithms:  In the case that d0 has a transition in [t-1]->[t], the bit that are not free bit but has at least one adjacent free bit now has a chance to transmit data bit.

    来自2024.10.30的注释-留给未来的提醒：
      该算法其实是对应了verilog设计的。过了好久时间，已经对该代码没什么印象了，所以再次看该算法，会觉得case2部分的逻辑似乎与verilog算法不对应。
      但是，再仔细想想，其实是对应的！不要用设计电路的思维看待该代码！
      下次想要做出改动的时候要慎重！

    '''
    def __init__(self, instance_id=None):
        super().__init__(instance_id)


    def encoder_core(self, bits_to_be_trans: list, last_codeword: tuple):
        '''
        Core algorithm - parallel input.
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
            Secondly, for the remaining d{i} except free bits: If none of its two adjancent bits are free bits, it transmits data bit;
            Finally, for the bits that are not free bits but has at least one adjacent free bit:
                if all the adjacent free bits has no transition, or it has a non-free bit that has a transition, it transmits data bit;
                Otherwise, it transmits redundant bit.

        :param bits_to_be_trans:
        :param last_codeword:
        :return: tuple, int, list - The codeword tuple, the number of data bits encoded, and the bool list indicating if the input bit has been transmitted.
        '''
        assert isinstance(bits_to_be_trans, list)
        assert len(bits_to_be_trans) == 7
        assert isinstance(last_codeword, tuple)
        assert len(last_codeword) == 7

        flagList_inputTransmitted = 7 * [False]
        current_data_bits_list = copy.deepcopy(bits_to_be_trans)  # A copy of data bit list
        codeword_list = []

        # main
        assert last_codeword[0] in (0, 1)
        assert current_data_bits_list[0] in (0, 1)
        codeword_list.append(current_data_bits_list[0])
        assert flagList_inputTransmitted[0] is False
        flagList_inputTransmitted[0] = True
        n_transmitted_bits = 1

        if last_codeword[0] == bits_to_be_trans[0]:  # Case 1
            # d1 is a data bit
            assert current_data_bits_list[1] in (0, 1)
            assert last_codeword[1] in (0, 1)
            codeword_list.append(current_data_bits_list[1])
            assert flagList_inputTransmitted[1] is False
            flagList_inputTransmitted[1] = True
            n_transmitted_bits = n_transmitted_bits + 1

            # d2 ~ d6
            for idx_i in range(2, 7):
                assert current_data_bits_list[idx_i] in (0, 1)
                assert last_codeword[idx_i] in (0, 1)
                if (last_codeword[idx_i] == codeword_list[-1]) and (last_codeword[idx_i] != last_codeword[idx_i - 1]):
                    codeword_list.append(last_codeword[idx_i])
                else:
                    codeword_list.append(current_data_bits_list[idx_i])
                    assert flagList_inputTransmitted[idx_i] is False
                    flagList_inputTransmitted[idx_i] = True
                    n_transmitted_bits = n_transmitted_bits + 1

        else:  # Case 2
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

            # flags_bit_noAdjacentFreeBit = []
            # flags_bit_noAdjacentFreeBit.append('hi!')
            # if (flags_freebit[2] is False) and (flags_freebit[6] is False):
            #     flags_bit_noAdjacentFreeBit.append(True)
            # else:
            #     flags_bit_noAdjacentFreeBit.append(False)
            # for idx_i in range(2, 6):
            #     if (flags_freebit[idx_i - 1] is False) and (flags_freebit[idx_i + 1] is False):
            #         flags_bit_noAdjacentFreeBit.append(True)
            #     else:
            #         flags_bit_noAdjacentFreeBit.append(False)
            # if (flags_freebit[1] is False) and (flags_freebit[5] is False):
            #     flags_bit_noAdjacentFreeBit.append(True)
            # else:
            #     flags_bit_noAdjacentFreeBit.append(False)

            idx_list_unprocessed = []

            # d1
            assert current_data_bits_list[1] in (0, 1)
            if (flags_freebit[1] is True) or ((flags_freebit[6] is False) and (flags_freebit[2] is False)):
                codeword_list.append(current_data_bits_list[1])
                assert flagList_inputTransmitted[1] is False
                flagList_inputTransmitted[1] = True
                n_transmitted_bits = n_transmitted_bits + 1
            else:
                codeword_list.append(None)
                idx_list_unprocessed.append(1)

            # d2 ~ d5
            for idx_k in range(2, 6):
                assert current_data_bits_list[idx_k] in (0, 1)
                if (flags_freebit[idx_k] is True) or ((flags_freebit[idx_k - 1] is False) and (flags_freebit[idx_k + 1] is False)):
                    codeword_list.append(current_data_bits_list[idx_k])
                    assert flagList_inputTransmitted[idx_k] is False
                    flagList_inputTransmitted[idx_k] = True
                    n_transmitted_bits = n_transmitted_bits + 1
                else:
                    codeword_list.append(None)
                    idx_list_unprocessed.append(idx_k)

            # d6
            assert current_data_bits_list[6] in (0, 1)
            if (flags_freebit[6] is True) or ((flags_freebit[5] is False) and (flags_freebit[1] is False)):
                codeword_list.append(current_data_bits_list[6])
                assert flagList_inputTransmitted[6] is False
                flagList_inputTransmitted[6] = True
                n_transmitted_bits = n_transmitted_bits + 1
            else:
                codeword_list.append(None)
                idx_list_unprocessed.append(6)

            # Unprocessed bits
            for idx_r in idx_list_unprocessed:

                if idx_r == 1:
                    if ( (flags_freebit[6] is True)
                            and (flags_freebit[2] is True)
                            and (codeword_list[6] == last_codeword[6])
                            and (codeword_list[2] == last_codeword[2]) ):
                        codeword_list[1] = current_data_bits_list[1]
                        assert flagList_inputTransmitted[1] is False
                        flagList_inputTransmitted[1] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[6] is False)
                           and (codeword_list[2] in (0, 1))
                           and (codeword_list[2] == last_codeword[2]) ):
                        codeword_list[1] = current_data_bits_list[1]
                        assert flagList_inputTransmitted[1] is False
                        flagList_inputTransmitted[1] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[2] is False)
                           and (codeword_list[6] in (0, 1))
                           and (codeword_list[6] == last_codeword[6]) ):
                        codeword_list[1] = current_data_bits_list[1]
                        assert flagList_inputTransmitted[1] is False
                        flagList_inputTransmitted[1] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[6] is False)
                           and (codeword_list[6] in (0, 1))
                           and (codeword_list[6] != last_codeword[6]) ):
                        codeword_list[1] = current_data_bits_list[1]
                        assert flagList_inputTransmitted[1] is False
                        flagList_inputTransmitted[1] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[2] is False)
                           and (codeword_list[2] in (0, 1))
                           and (codeword_list[2] != last_codeword[2]) ):
                        codeword_list[1] = current_data_bits_list[1]
                        assert flagList_inputTransmitted[1] is False
                        flagList_inputTransmitted[1] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    else:
                        codeword_list[1] = last_codeword[1]

                elif idx_r in (2, 3, 4, 5):
                    if ( (flags_freebit[idx_r - 1] is True)
                            and (flags_freebit[idx_r + 1] is True)
                            and (codeword_list[idx_r - 1] == last_codeword[idx_r - 1])
                            and (codeword_list[idx_r + 1] == last_codeword[idx_r + 1]) ):
                        codeword_list[idx_r] = current_data_bits_list[idx_r]
                        assert flagList_inputTransmitted[idx_r] is False
                        flagList_inputTransmitted[idx_r] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[idx_r - 1] is False)
                           and (codeword_list[idx_r + 1] in (0, 1))
                           and (codeword_list[idx_r + 1] == last_codeword[idx_r + 1]) ):
                        codeword_list[idx_r] = current_data_bits_list[idx_r]
                        assert flagList_inputTransmitted[idx_r] is False
                        flagList_inputTransmitted[idx_r] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[idx_r + 1] is False)
                           and (codeword_list[idx_r - 1] in (0, 1))
                           and (codeword_list[idx_r - 1] == last_codeword[idx_r - 1]) ):
                        codeword_list[idx_r] = current_data_bits_list[idx_r]
                        assert flagList_inputTransmitted[idx_r] is False
                        flagList_inputTransmitted[idx_r] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[idx_r - 1] is False)
                           and (codeword_list[idx_r - 1] in (0, 1))
                           and (codeword_list[idx_r - 1] != last_codeword[idx_r - 1]) ):
                        codeword_list[idx_r] = current_data_bits_list[idx_r]
                        assert flagList_inputTransmitted[idx_r] is False
                        flagList_inputTransmitted[idx_r] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[idx_r + 1] is False)
                           and (codeword_list[idx_r + 1] in (0, 1))
                           and (codeword_list[idx_r + 1] != last_codeword[idx_r + 1]) ):
                        codeword_list[idx_r] = current_data_bits_list[idx_r]
                        assert flagList_inputTransmitted[idx_r] is False
                        flagList_inputTransmitted[idx_r] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    else:
                        codeword_list[idx_r] = last_codeword[idx_r]


                elif idx_r == 6:
                    if ( (flags_freebit[5] is True)
                            and (flags_freebit[1] is True)
                            and (codeword_list[5] == last_codeword[5])
                            and (codeword_list[1] == last_codeword[1]) ):
                        codeword_list[6] = current_data_bits_list[6]
                        assert flagList_inputTransmitted[6] is False
                        flagList_inputTransmitted[6] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[5] is False)
                           and (codeword_list[1] in (0, 1))
                           and (codeword_list[1] == last_codeword[1]) ):
                        codeword_list[6] = current_data_bits_list[6]
                        assert flagList_inputTransmitted[6] is False
                        flagList_inputTransmitted[6] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[1] is False)
                           and (codeword_list[5] in (0, 1))
                           and (codeword_list[5] == last_codeword[5]) ):
                        codeword_list[6] = current_data_bits_list[6]
                        assert flagList_inputTransmitted[6] is False
                        flagList_inputTransmitted[6] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[5] is False)
                           and (codeword_list[5] in (0, 1))
                           and (codeword_list[5] != last_codeword[5]) ):
                        codeword_list[6] = current_data_bits_list[6]
                        assert flagList_inputTransmitted[6] is False
                        flagList_inputTransmitted[6] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    elif ( (flags_freebit[1] is False)
                           and (codeword_list[1] in (0, 1))
                           and (codeword_list[1] != last_codeword[1]) ):
                        codeword_list[6] = current_data_bits_list[6]
                        assert flagList_inputTransmitted[6] is False
                        flagList_inputTransmitted[6] = True
                        n_transmitted_bits = n_transmitted_bits + 1

                    else:
                        codeword_list[6] = last_codeword[6]

                else:
                    assert False

        assert len(codeword_list) == 7
        codeword_tuple = tuple(codeword_list)
        flagTuple_inputTransmitted = tuple(flagList_inputTransmitted)
        return codeword_tuple, n_transmitted_bits, copy.deepcopy(flagTuple_inputTransmitted)

    def decoder_core(self, codeword_to_be_decode: tuple, last_codeword: tuple):
        '''
        Core algorithm - Version 20231224.
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
            Secondly, for the remaining d{i} except free bits: If none of its two adjancent bits are free bits, it transmits data bit;
            Finally, for the bits that are not free bits but has at least one adjacent free bit:
                if all the adjacent free bits has no transition, or it has a non-free bit that has a transition, it transmits data bit;
                Otherwise, it transmits redundant bit.

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
                    data_recovered_list.append(None)
                else:
                    data_recovered_list.append(codeword_to_be_decode[idx_i])

        else:  # Case 2
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

            # flags_bit_noAdjacentFreeBit = []
            # flags_bit_noAdjacentFreeBit.append('hi!')
            # if (flags_freebit[2] is False) and (flags_freebit[6] is False):
            #     flags_bit_noAdjacentFreeBit.append(True)
            # else:
            #     flags_bit_noAdjacentFreeBit.append(False)
            # for idx_i in range(2, 6):
            #     if (flags_freebit[idx_i - 1] is False) and (flags_freebit[idx_i + 1] is False):
            #         flags_bit_noAdjacentFreeBit.append(True)
            #     else:
            #         flags_bit_noAdjacentFreeBit.append(False)
            # if (flags_freebit[1] is False) and (flags_freebit[5] is False):
            #     flags_bit_noAdjacentFreeBit.append(True)
            # else:
            #     flags_bit_noAdjacentFreeBit.append(False)

            idx_list_unprocessed = []

            # d1
            # assert current_data_bits_list[1] in (0, 1)
            if (flags_freebit[1] is True) or ((flags_freebit[6] is False) and (flags_freebit[2] is False)):
                data_recovered_list.append(codeword_to_be_decode[1])
            else:
                data_recovered_list.append(None)
                idx_list_unprocessed.append(1)

            # d2 ~ d5
            for idx_k in range(2, 6):
                # assert current_data_bits_list[idx_k] in (0, 1)
                if (flags_freebit[idx_k] is True) or ((flags_freebit[idx_k - 1] is False) and (flags_freebit[idx_k + 1] is False)):
                    data_recovered_list.append(codeword_to_be_decode[idx_k])
                else:
                    data_recovered_list.append(None)
                    idx_list_unprocessed.append(idx_k)

            # d6
            # assert current_data_bits_list[6] in (0, 1)
            if (flags_freebit[6] is True) or ((flags_freebit[5] is False) and (flags_freebit[1] is False)):
                data_recovered_list.append(codeword_to_be_decode[6])
            else:
                data_recovered_list.append(None)
                idx_list_unprocessed.append(6)

            # Unprocessed bits
            for idx_r in idx_list_unprocessed:

                if idx_r == 1:
                    if ( (flags_freebit[6] is True)
                            and (flags_freebit[2] is True)
                            and (data_recovered_list[6] == last_codeword[6])
                            and (data_recovered_list[2] == last_codeword[2]) ):
                        data_recovered_list[1] = codeword_to_be_decode[1]

                    elif ( (flags_freebit[6] is False)
                           and (data_recovered_list[2] in (0, 1))
                           and (data_recovered_list[2] == last_codeword[2]) ):
                        data_recovered_list[1] = codeword_to_be_decode[1]

                    elif ( (flags_freebit[2] is False)
                           and (data_recovered_list[6] in (0, 1))
                           and (data_recovered_list[6] == last_codeword[6]) ):
                        data_recovered_list[1] = codeword_to_be_decode[1]

                    elif ( (flags_freebit[6] is False)
                           and (data_recovered_list[6] in (0, 1))
                           and (data_recovered_list[6] != last_codeword[6]) ):
                        data_recovered_list[1] = codeword_to_be_decode[1]

                    elif ( (flags_freebit[2] is False)
                           and (data_recovered_list[2] in (0, 1))
                           and (data_recovered_list[2] != last_codeword[2]) ):
                        data_recovered_list[1] = codeword_to_be_decode[1]

                    else:
                        idx_list_stuffingbit.append(1)

                elif idx_r in (2, 3, 4, 5):
                    if ( (flags_freebit[idx_r - 1] is True)
                            and (flags_freebit[idx_r + 1] is True)
                            and (data_recovered_list[idx_r - 1] == last_codeword[idx_r - 1])
                            and (data_recovered_list[idx_r + 1] == last_codeword[idx_r + 1]) ):
                        data_recovered_list[idx_r] = codeword_to_be_decode[idx_r]

                    elif ( (flags_freebit[idx_r - 1] is False)
                           and (data_recovered_list[idx_r + 1] in (0, 1))
                           and (data_recovered_list[idx_r + 1] == last_codeword[idx_r + 1]) ):
                        data_recovered_list[idx_r] = codeword_to_be_decode[idx_r]

                    elif ( (flags_freebit[idx_r + 1] is False)
                           and (data_recovered_list[idx_r - 1] in (0, 1))
                           and (data_recovered_list[idx_r - 1] == last_codeword[idx_r - 1]) ):
                        data_recovered_list[idx_r] = codeword_to_be_decode[idx_r]

                    elif ( (flags_freebit[idx_r - 1] is False)
                           and (data_recovered_list[idx_r - 1] in (0, 1))
                           and (data_recovered_list[idx_r - 1] != last_codeword[idx_r - 1]) ):
                        data_recovered_list[idx_r] = codeword_to_be_decode[idx_r]

                    elif ( (flags_freebit[idx_r + 1] is False)
                           and (data_recovered_list[idx_r + 1] in (0, 1))
                           and (data_recovered_list[idx_r + 1] != last_codeword[idx_r + 1]) ):
                        data_recovered_list[idx_r] = codeword_to_be_decode[idx_r]

                    else:
                        idx_list_stuffingbit.append(idx_r)


                elif idx_r == 6:
                    if ( (flags_freebit[5] is True)
                            and (flags_freebit[1] is True)
                            and (data_recovered_list[5] == last_codeword[5])
                            and (data_recovered_list[1] == last_codeword[1]) ):
                        data_recovered_list[6] = codeword_to_be_decode[6]

                    elif ( (flags_freebit[5] is False)
                           and (data_recovered_list[1] in (0, 1))
                           and (data_recovered_list[1] == last_codeword[1]) ):
                        data_recovered_list[6] = codeword_to_be_decode[6]

                    elif ( (flags_freebit[1] is False)
                           and (data_recovered_list[5] in (0, 1))
                           and (data_recovered_list[5] == last_codeword[5]) ):
                        data_recovered_list[6] = codeword_to_be_decode[6]

                    elif ( (flags_freebit[5] is False)
                           and (data_recovered_list[5] in (0, 1))
                           and (data_recovered_list[5] != last_codeword[5]) ):
                        data_recovered_list[6] = codeword_to_be_decode[6]

                    elif ( (flags_freebit[1] is False)
                           and (data_recovered_list[1] in (0, 1))
                           and (data_recovered_list[1] != last_codeword[1]) ):
                        data_recovered_list[6] = codeword_to_be_decode[6]

                    else:
                        idx_list_stuffingbit.append(6)

                else:
                    assert False


        # print(len(idx_list_stuffingbit), len(data_recovered_list))
        data_recovered_tuple = tuple(copy.deepcopy(data_recovered_list))
        idx_tuple_stuffingbit = tuple(copy.deepcopy(idx_list_stuffingbit))
        assert len(data_recovered_list) == 7
        cnt_check_iii = 0
        for bit_check_iii in data_recovered_list:
            if bit_check_iii in (0, 1):
                cnt_check_iii = cnt_check_iii + 1
            else:
                assert bit_check_iii is None
        assert (cnt_check_iii + len(idx_list_stuffingbit)) == 7


        return data_recovered_tuple, idx_tuple_stuffingbit



class BSCAC_ForHexDyS2C_2CSupFor7bitGroup_Main(BSCAC_ForHexDyS2C_2CSupFor7bitGroup_parallelDataIn):
    '''
    The MAIN class of BSCAC_ForHexDyS2C_2CSupFor7bitGroup.

    You can use this class in other python files, and link it to the class you want to use.

    '''
    def __init__(self, instance_id=None):
        super().__init__(instance_id)