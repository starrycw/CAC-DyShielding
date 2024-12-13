import copy


class PATCAC_Codec_LJP20241213:
    def __init__(self, n_cw):
        '''

        :param n_cw: Codeword bit-width
        '''
        assert isinstance(n_cw, int) and n_cw > 2
        self._param_codewordBitwidth = copy.deepcopy(n_cw)
        self._param_patSeq, self._param_patSeqSum = copy.deepcopy(self.getPATSeq(seq_length = n_cw))

    @staticmethod
    def getPATSeq(seq_length):
        assert (isinstance(seq_length, int) and (seq_length > 2))
        pat_list = [1, 2]
        maxdata = 2
        for i in range(2, seq_length):
            element_next = pat_list[i - 2] * 3
            pat_list.append(element_next)
        if seq_length % 2 == 0:
            maxdata = pat_list[-1] + pat_list[-2] - 1
        elif seq_length % 2 == 1:
            maxdata = pat_list[-1] + pat_list[-2] + pat_list[-3] - 1
        return tuple(pat_list), maxdata

    def getParam_maxInputLimitation(self):
        return copy.deepcopy(self._param_patSeqSum)

    def getParam_codewordBitWidth(self):
        return copy.deepcopy(self._param_codewordBitwidth)

    def encode(self, value, codewordType = "int"):
        '''

        :param value: Value to be encoded
        :param codewordType: 'int' (Default) or 'bool'
        :return:
        '''
        # pat_tuple, maxvalue = getPatseq(seq_length)
        pat_tuple = copy.deepcopy(self._param_patSeq)
        maxvalue = copy.deepcopy(self._param_patSeqSum)
        seq_length = copy.deepcopy(self._param_codewordBitwidth)

        assert (isinstance(value, int) and (value >= 0))
        assert (value <= maxvalue)
        # assert (codewordType == "int")

        codeword_list = []
        if value >= pat_tuple[-1]:
            codeword_list.append(True)
            resv = value - pat_tuple[-1]
        else:
            codeword_list.append(False)
            resv = value
        for i in range(seq_length - 2, 0, -1):
            if resv >= pat_tuple[i]:
                codeword_list.append(True)
                resv = resv - pat_tuple[i]
            else:
                codeword_list.append(False)
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

        assert len(codeword_list_int) == self.getParam_codewordBitWidth()

        if codewordType == "bool":
            return tuple(codeword_list)
        elif codewordType == "int":
            return tuple(codeword_list_int)
        else:
            assert False

    def encoder_top(self, decValue_int, lastState_tuple):
        '''

        :param decValue_int: Value to be encoded
        :param lastState_tuple: Codeword state in the previous one cycle
        :return:
        '''
        assert isinstance(decValue_int, int)
        assert decValue_int >= 0
        newDF_tuple = self.encode_PATCAC(value=decValue_int)
        assert len(newDF_tuple) == len(lastState_tuple)

        xorCodeword_list = []
        for idx_i in range(0, len(newState_tuple)):
            if (newDF_tuple[idx_i]) == 0 and (lastState_tuple[idx_i] == 0):
                xorCodeword_list.append(0)
            elif (newDF_tuple[idx_i]) == 0 and (lastState_tuple[idx_i] == 1):
                xorCodeword_list.append(1)
            elif (newDF_tuple[idx_i]) == 1 and (lastState_tuple[idx_i] == 0):
                xorCodeword_list.append(1)
            elif (newDF_tuple[idx_i]) == 1 and (lastState_tuple[idx_i] == 1):
                xorCodeword_list.append(0)
            else:
                assert False

        xorCodeword_tuple = tuple(copy.deepcopy(xorCodeword_list))

        return xorCodeword_tuple



class PATCAC_Codec(PATCAC_Codec_LJP20241213):
    def __init__(self, len_cw):
        '''

        :param len_cw: Codeword bit-width
        '''
        super().__init__(n_cw=len_cw)