
def calc_codeword_number(n_bit: int, cw_rule) -> tuple:
    '''
    Calculate the number of CAC codewords. The CAC rules should be selected from the pre-defined set.
    :param n_bit:
    :param cw_rule:
    :return:
    '''
    assert cw_rule in ('FPF', 'FTF', 'ringFPF', 'ringFTF', 'ring2CTrans', 'ring3CTrans')
    assert isinstance(n_bit, int) and n_bit > 2
    cnt_all = 0
    cnt_sat = 0
    for dec_value in range(0, (2 ** n_bit)):
        bin_str = bin(dec_value)[2:].zfill(n_bit)
        bin_list = []
        for char_i in bin_str:
            if char_i == "0":
                bin_list.append(0)
            elif char_i == "1":
                bin_list.append(1)
            else:
                assert False
        bin_list.reverse()
        bin_tuple = tuple(bin_list)
        cnt_all = cnt_all + 1
        # Check
        if cw_rule == 'FTF':
            is_sat = FTFCAC_cw_check(cw_tuple=bin_tuple)
        elif cw_rule == 'FPF':
            is_sat = FPFCAC_cw_check(cw_tuple=bin_tuple)
        elif cw_rule == 'ringFTF':
            is_sat = ringFTFCAC_cw_check(cw_tuple=bin_tuple)
        elif cw_rule == 'ringFPF':
            is_sat = ringFPFCAC_cw_check(cw_tuple=bin_tuple)
        elif cw_rule == 'ring2CTrans':
            is_sat = ringCAC_trans_check(trans_tuple=bin_tuple, max_xtalk=2)
        elif cw_rule == 'ring3CTrans':
            is_sat = ringCAC_trans_check(trans_tuple=bin_tuple, max_xtalk=3)
        else:
            assert False

        print("{}-No.{}-{}-{}".format(cw_rule, cnt_all, is_sat, bin_tuple))
        if is_sat:
            cnt_sat = cnt_sat + 1
    print("###{} / {}".format(cnt_sat, cnt_all))
    return cnt_sat, cnt_all

def calc_codeword_number_all(n_bit: int) -> tuple:
    '''
    Calculate the number of the CAC codewords.
    :param n_bit:
    :return:
    '''
    assert isinstance(n_bit, int) and n_bit > 2
    cntList_ruleName = ['FPF', 'FTF', 'ringFPF', 'ringFTF', 'ring2CTrans', 'ring3CTrans']
    cntList_sat = [0, 0, 0, 0, 0, 0]
    cnt_all = 0
    for dec_value in range(0, (2 ** n_bit)):
        bin_str = bin(dec_value)[2:].zfill(n_bit)
        bin_list = []
        for char_i in bin_str:
            if char_i == "0":
                bin_list.append(0)
            elif char_i == "1":
                bin_list.append(1)
            else:
                assert False
        bin_list.reverse()
        bin_tuple = tuple(bin_list)
        cnt_all = cnt_all + 1
        # Check
        for idx_ruleName in range(0, len(cntList_ruleName)):
            iter_ruleName = cntList_ruleName[idx_ruleName]
            if iter_ruleName == 'FTF':
                is_sat = FTFCAC_cw_check(cw_tuple=bin_tuple)
            elif iter_ruleName == 'FPF':
                is_sat = FPFCAC_cw_check(cw_tuple=bin_tuple)
            elif iter_ruleName == 'ringFTF':
                is_sat = ringFTFCAC_cw_check(cw_tuple=bin_tuple)
            elif iter_ruleName == 'ringFPF':
                is_sat = ringFPFCAC_cw_check(cw_tuple=bin_tuple)
            elif iter_ruleName == 'ring2CTrans':
                is_sat = ringCAC_trans_check(trans_tuple=bin_tuple, max_xtalk=2)
            elif iter_ruleName == 'ring3CTrans':
                is_sat = ringCAC_trans_check(trans_tuple=bin_tuple, max_xtalk=3)
            else:
                assert False

            if is_sat is True:
                cntList_sat[idx_ruleName] = cntList_sat[idx_ruleName] + 1
            else:
                assert is_sat is False

        print("No.{}--{}".format(cnt_all, cntList_sat))
    print("###ALL={}\n SAT={}\n RuleName={}".format(cnt_all, cntList_sat, cntList_ruleName))
    return cnt_all, cntList_sat, cntList_ruleName

def FTFCAC_cw_check(cw_tuple: tuple[int, ...]) -> bool:
    '''
    If the input codeword follows the FTF-CAC rules.
    :param cw_tuple:
    :return:
    '''
    assert isinstance(cw_tuple, tuple)
    is_sat = True
    for idx_i in range(0, len(cw_tuple)-1):
        assert cw_tuple[idx_i] in (0, 1)
        if (idx_i % 2 == 1) and (cw_tuple[idx_i] == 0) and (cw_tuple[idx_i + 1] == 1):
            is_sat = False
        if (idx_i % 2 == 0) and (cw_tuple[idx_i] == 1) and (cw_tuple[idx_i + 1] == 0):
            is_sat = False
    return is_sat

def ringFTFCAC_cw_check(cw_tuple: tuple[int, ...]) -> bool:
    '''
    If the input codeword follows the ring-FTF-CAC rules. (FTF-CAC rules + addition restriction on cw_tuple[0] and cw_tuple[-1]).
    :param cw_tuple:
    :return:
    '''
    assert isinstance(cw_tuple, tuple)
    is_sat = True
    for idx_i in range(0, len(cw_tuple)):
        assert cw_tuple[idx_i] in (0, 1)
        if (idx_i % 2 == 1) and (cw_tuple[idx_i] == 0) and (cw_tuple[idx_i - 1] == 1):
            is_sat = False
        if (idx_i % 2 == 0) and (cw_tuple[idx_i] == 1) and (cw_tuple[idx_i - 1] == 0):
            is_sat = False
    return is_sat

def FPFCAC_cw_check(cw_tuple: tuple[int, ...]) -> bool:
    '''
    If the input codeword follows the FPF-CAC rules.
    :param cw_tuple:
    :return:
    '''
    assert isinstance(cw_tuple, tuple)
    is_sat = True
    assert cw_tuple[0] in (0, 1)
    assert cw_tuple[1] in (0, 1)
    for idx_i in range(2, len(cw_tuple)):
        assert cw_tuple[idx_i] in (0, 1)
        if (cw_tuple[idx_i - 2] == 0) and (cw_tuple[idx_i - 1] == 1) and (cw_tuple[idx_i] == 0):
            is_sat = False
        if (cw_tuple[idx_i - 2] == 1) and (cw_tuple[idx_i - 1] == 0) and (cw_tuple[idx_i] == 1):
            is_sat = False
    return is_sat

def ringFPFCAC_cw_check(cw_tuple: tuple[int, ...]) -> bool:
    '''
    If the input codeword follows the ring-FPF-CAC rules. (FPF-CAC rules + addition restrictions).
    :param cw_tuple:
    :return:
    '''
    assert isinstance(cw_tuple, tuple)
    is_sat = True
    assert cw_tuple[0] in (0, 1)
    assert cw_tuple[1] in (0, 1)
    for idx_i in range(0, len(cw_tuple)):
        assert cw_tuple[idx_i] in (0, 1)
        if (cw_tuple[idx_i - 2] == 0) and (cw_tuple[idx_i - 1] == 1) and (cw_tuple[idx_i] == 0):
            is_sat = False
        if (cw_tuple[idx_i - 2] == 1) and (cw_tuple[idx_i - 1] == 0) and (cw_tuple[idx_i] == 1):
            is_sat = False
    return is_sat

def ringCAC_trans_check(trans_tuple: tuple[int, ...], max_xtalk: int) -> bool:
    '''
    If the input codeword (trans) follows the ring-nC-trans-CAC rules.
    ring-2C-trans-CAC: '11' is forbidden in the ring.
    ring-3C-trans-CAC: '111' is forbidden in the ring.
    :param trans_tuple:
    :param max_xtalk:
    :return:
    '''
    assert max_xtalk in (2, 3)
    assert isinstance(trans_tuple, tuple)
    is_sat = True
    trans_list_extend = list(trans_tuple)
    trans_list_extend.append(trans_tuple[0])
    for idx_i in range(0, len(trans_tuple)):
        assert trans_tuple[idx_i] in (0, 1)
        if max_xtalk == 3 and (trans_tuple[idx_i-1] + trans_tuple[idx_i] + trans_list_extend[idx_i+1]) > 2:
            is_sat = False
        if max_xtalk == 2 and trans_tuple[idx_i] == 1 and (trans_tuple[idx_i-1] + trans_list_extend[idx_i+1]) > 0:
            is_sat = False
    return is_sat