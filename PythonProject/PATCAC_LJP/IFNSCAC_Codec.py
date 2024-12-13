# IFNS-CAC Codec
import copy
import math


class IFNSCAC_Codec:
    '''
    IFNS-CAC Codec
    '''
    def __init__(self, n_cw):
        '''
        Initialize the IFNS-CAC codec instance.
        :param n_cw: int
        '''
        assert isinstance(n_cw, int) and n_cw > 2
        self._param_codewordBitwidth = copy.deepcopy(n_cw)
        self._param_ifnsSeq, self._param_ifnsSeqSum = copy.deepcopy(self.getIFNSSeq(seq_length = (n_cw)))


    @staticmethod
    def getFNSSeq(seq_length):
        '''
        Get the FNS seq & the sum of elements.
        :param seq_length:
        :return: #1-[tuple] - FNS seq; #2-[int] - The sum of the FNS seq elements;
        '''
        assert (isinstance(seq_length, int) and (seq_length > 2))
        fns_list = [1, 1]
        sum_elements = 2
        for i in range(2, seq_length):
            element_next = fns_list[i - 2] + fns_list[i - 1]
            fns_list.append(element_next)
            sum_elements = sum_elements + element_next

        return tuple(fns_list), sum_elements

    @staticmethod
    def getIFNSSeq(seq_length):
        '''
        Get the IFNS seq & the sum of elements.
        :param seq_length:
        :return: #1-[tuple] - IFNS seq; #2-[int] - The sum of the IFNS seq elements;
        '''
        assert (isinstance(seq_length, int) and (seq_length > 2))
        fns_tuple, fns_sum = copy.deepcopy(IFNSCAC_Codec.getFNSSeq(seq_length=(seq_length + 1)))
        fns_sum = fns_sum - fns_tuple[-2]
        fns_list = list(fns_tuple)
        fns_list.pop(-2)
        ifns_tuple = tuple(fns_list)

        return ifns_tuple, fns_sum


    @staticmethod
    def getMinCodewordBitwidth(bitwidth_data):
        '''
        Get the minimum binary length of the FNS-based codewords that can present all the bitwidth_data-bit data.
        :param bitwidth_data:
        :return:
        '''
        assert isinstance(bitwidth_data, int) and bitwidth_data > 2
        data_maxv = (2 ** bitwidth_data) - 1
        n_cw = bitwidth_data - 1
        not_sat = True
        while not_sat:
            n_cw = n_cw + 1
            # Get the max value of c_cw-bit codewords
            ifns_list, cw_maxv = IFNSCAC_Codec.getIFNSSeq(seq_length=n_cw)
            if cw_maxv >= data_maxv:
                not_sat = False

        return n_cw

    @staticmethod
    def convert_boolTuple_to_intTuple(boolTuple):
        '''
        Convert tuple[bool, ...] to tuple[int, ...].
        :param boolTuple:
        :return:
        '''
        assert isinstance(boolTuple, tuple)
        intList = []
        for item_i in boolTuple:
            if item_i is True:
                intList.append(1)
            elif item_i is False:
                intList.append(0)
            else:
                assert False
        return tuple(intList)

    @staticmethod
    def convert_intTuple_to_boolTuple(intTuple):
        '''
        Convert tuple[int, ...] to tuple[bool, ...].
        :param intTuple:
        :return:
        '''
        assert isinstance(intTuple, tuple)
        boolList = []
        for item_i in intTuple:
            if item_i == 1:
                boolList.append(True)
            elif item_i == 0:
                boolList.append(False)
            else:
                assert False
        return tuple(boolList)

    def getParam_codewordBitwidth(self):
        return copy.deepcopy(self._param_codewordBitwidth)

    def getParam_ifnsSeq(self):
        return copy.deepcopy(self._param_ifnsSeq)

    def getParam_maxInputValue(self):
        '''
        Get the SUM value of the first n elements of FNS seq, in which n is the codeword bitwidth.
        :return:
        '''
        maxInValue = copy.deepcopy(self._param_ifnsSeqSum)
        return maxInValue

    def encode_IFNS(self, value, codewordType = "int"):
        '''
        IFNS-FPF Encoder.
        :param value:
        :param codewordType: String, either "bool" or "int"
        :return:
        '''
        n = self.getParam_codewordBitwidth()

        assert (isinstance(value, int) and (value >= 0))
        # Get FNS seq
        ifns_tuple = self.getParam_ifnsSeq()
        # Check
        assert (value <= self.getParam_maxInputValue())
        assert ifns_tuple[-1] == ifns_tuple[n-1]

        # Encoding - MSB
        codeword_list = []
        # print("MSB - resv={}, ns={}".format(value, ifns_tuple[-1]))
        if value >= ifns_tuple[-1]:
            codeword_list.append(True)
            resv = value - ifns_tuple[-1]
        else:
            codeword_list.append(False)
            resv = value
        # Encoding - Other bits

        if resv >= (ifns_tuple[n-2] + ifns_tuple[n-3]):
            codeword_list.append(True)
        elif resv < ifns_tuple[n-2]:
            codeword_list.append(False)
        else:
            codeword_list.append(codeword_list[-1])
        if codeword_list[-1] is True:
            resv = resv - ifns_tuple[n-2]

        for i in range(n - 3, 0, -1):
            # print("{} - resv={}, ns={}".format(i, resv, (ifns_tuple[i + 1], ifns_tuple[i])))
            if resv >= ifns_tuple[i + 1]:
                codeword_list.append(True)
            elif resv < ifns_tuple[i]:
                codeword_list.append(False)
            else:
                codeword_list.append(codeword_list[-1])
            if codeword_list[-1] is True:
                resv = resv - ifns_tuple[i]

        # Encoding - LSB
        if resv == 1:
            codeword_list.append(True)
        elif resv == 0:
            codeword_list.append(False)
        else:
            assert False

        # Reverse list
        codeword_list.reverse()
        # Post Process
        codeword_list_int = []
        for i in codeword_list:
            if i is True:
                codeword_list_int.append(1)
            elif i is False:
                codeword_list_int.append(0)
            else:
                assert False

        assert len(codeword_list_int) == n

        if codewordType == "bool":
            return tuple(codeword_list)
        elif codewordType == "int":
            return tuple(codeword_list_int)
        else:
            assert False

    def decoder_IFNS(self, codeword_tuple, codewordType = "int"):
        '''
        IFNS-FPF decoder.
        :param codeword_tuple:
        :param codewordType: String, either "int" or "bool".
        :return:
        '''

        assert isinstance(codeword_tuple, tuple)
        assert len(codeword_tuple) == self.getParam_codewordBitwidth()
        if codewordType == "int":
            codeword = copy.deepcopy(codeword_tuple)
        elif codewordType == "bool":
            codeword = IFNSCAC_Codec.convert_boolTuple_to_intTuple(boolTuple=codeword_tuple)
        else:
            assert False

        ifns_tuple = self.getParam_ifnsSeq()
        # Decoding
        value = 0
        idx_i = 0
        for i in codeword:
            if i == 1:
                value = value + ifns_tuple[idx_i]
            else:
                assert i == 0
            # print(idx_i, value, fns_tuple[idx_i], i)
            idx_i = idx_i + 1
        return value









