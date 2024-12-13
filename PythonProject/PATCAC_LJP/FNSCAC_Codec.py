# FNS-CAC Codec
import copy
import math


class FNSCAC_Codec:
    '''
    FNS-CAC Codec
    '''
    def __init__(self, n_cw):
        '''
        Initialize the FNS-CAC codec instance.
        :param n_cw: int
        '''
        assert isinstance(n_cw, int) and n_cw > 2
        self._param_codewordBitwidth = copy.deepcopy(n_cw)
        self._param_fnsSeq, self._param_fnsSeqSum = copy.deepcopy(self.getFNSSeq(seq_length = (n_cw + 1)))


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
            fns_list, cw_maxv = FNSCAC_Codec.getFNSSeq(seq_length=n_cw)
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

    def getParam_fnsSeq(self):
        return copy.deepcopy(self._param_fnsSeq)

    def getParam_maxInputValue(self):
        '''
        Get the SUM value of the first n elements of FNS seq, in which n is the codeword bitwidth.
        :return:
        '''
        maxInValue = self._param_fnsSeqSum - self.getParam_fnsSeq()[-1]
        return maxInValue

    def encode_FNSFPF(self, value, codewordType = "int"):
        '''
        FNS-FPF Encoder.
        :param value:
        :param codewordType: String, either "bool" or "int"
        :return:
        '''
        n = self.getParam_codewordBitwidth()

        assert (isinstance(value, int) and (value >= 0))
        # Get FNS seq
        fns_tuple = self.getParam_fnsSeq()
        # Check
        assert (value <= self.getParam_maxInputValue())
        assert fns_tuple[-1] == fns_tuple[n]

        # Encoding - MSB
        codeword_list = []
        if value >= fns_tuple[-1]:
            codeword_list.append(True)
            resv = value - fns_tuple[-2]
        else:
            codeword_list.append(False)
            resv = value
        # Encoding - Other bits
        for i in range(n - 2, 0, -1):
            if resv >= fns_tuple[i + 1]:
                codeword_list.append(True)
            elif resv < fns_tuple[i]:
                codeword_list.append(False)
            else:
                codeword_list.append(codeword_list[-1])
            if codeword_list[-1] is True:
                resv = resv - fns_tuple[i]
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

    def encode_FNSFTF(self, value, codewordType = "int"):
        '''
        FNS-FTF Encoder.
        :param value:
        :param codewordType: String, either "bool" or "int"
        :return:
        '''
        n = self.getParam_codewordBitwidth()

        assert (isinstance(value, int) and (value >= 0))
        # Get FNS seq
        fns_tuple = self.getParam_fnsSeq()
        # Check
        assert (value <= self.getParam_maxInputValue())
        assert fns_tuple[-1] == fns_tuple[n]

        # Encoding
        resv = copy.deepcopy(value)
        codeword_list = []
        for i in range(n - 1, 0, -1):
            idx_fnsElement = (2 * math.floor((i + 1) / 2))
            # print("ns = {}, resv = {}".format(fns_tuple[idx_fnsElement], resv))
            if resv < fns_tuple[idx_fnsElement]:
                codeword_list.append(False)
            else:
                codeword_list.append(True)
                resv = resv - fns_tuple[i]

        # Encoding - LSB
        if resv == 1:
            codeword_list.append(True)
        elif resv == 0:
            codeword_list.append(False)
        else:
            print("ERROR: resv = {}".format(resv))
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

    def decoder_FNS(self, codeword_tuple, codewordType = "int"):
        '''
        FNS-FPF/FTF decoder.
        :param codeword_tuple:
        :param codewordType: String, either "int" or "bool".
        :return:
        '''

        assert isinstance(codeword_tuple, tuple)
        assert len(codeword_tuple) == self.getParam_codewordBitwidth()
        if codewordType == "int":
            codeword = copy.deepcopy(codeword_tuple)
        elif codewordType == "bool":
            codeword = FNSCAC_Codec.convert_boolTuple_to_intTuple(boolTuple=codeword_tuple)
        else:
            assert False

        fns_tuple = self.getParam_fnsSeq()
        # Decoding
        value = 0
        idx_i = 0
        for i in codeword:
            if i == 1:
                value = value + fns_tuple[idx_i]
            else:
                assert i == 0
            # print(idx_i, value, fns_tuple[idx_i], i)
            idx_i = idx_i + 1
        return value









