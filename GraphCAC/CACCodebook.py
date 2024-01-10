# The Data Structure of the CAC Codebook
import copy


class _CACCodewordNode:
    '''
    The class for single node in the codebook graph.
    Each node represents one codeword.
    '''
    def __init__(self, node_id: int, codeword: tuple[int, ...]):
        '''
        Initializes the _CACCodewordNode object
        :param node_id: int
        :param codeword: tuple[int, ...]
        '''

        # Properties Init
        self._initializeNodeProperties(node_id=node_id, codeword=codeword)

    def _initializeNodeProperties(self, node_id: int, codeword: tuple[int, ...]):
        # ID & Codeword
        assert isinstance(node_id, int)
        assert isinstance(codeword, tuple)
        for element_cwi in codeword:
            assert element_cwi in (0, 1)
        self._nodeProperty_id = node_id  # Node ID
        self._nodeProperty_codeword = codeword  # The codeword represented by this node.

        # Edges - Note that the edges lists are update by the method provided by the graph class instead of the node class.
        #self._nodeProperty_edgeOutList = []  # The list of outgoing edges coming from this node.
        #self._nodeProperty_edgeInList = []  # The list of incoming edges linked to this node.
        self._nodeProperty_edgeUndirectedList = []  # The list of undirected edges linked to this node.


    ####################################################################################################################
    ### ID & Codeword
    def getProperty_nodeID(self) -> int:
        '''
        Return the node ID associated with this node obj.
        :return: int
        '''
        return copy.deepcopy(self._nodeProperty_id)

    def getProperty_codeword(self) -> tuple[int, ...]:
        '''
        Get the codeword represened by this node obj.
        :return: tuple[int, ...]
        '''
        return copy.deepcopy(self._nodeProperty_codeword)


    ####################################################################################################################
    ### EDGES
    # def getProperty_edgeOutList(self) -> list:
    #     '''
    #     Get the outgoing edges associated with this node obj.
    #     :return: list
    #     '''
    #     return copy.deepcopy(self._nodeProperty_edgeOutList)
    #
    # def getProperty_edgeInList(self) -> list:
    #     '''
    #     Get the incoming edges associated with this node obj.
    #     :return: list
    #     '''
    #     return copy.copy(self._nodeProperty_edgeInList)

    def getProperty_edgeUndirectedList(self) -> list:
        '''
        Get the undirected edges associated with this node obj.
        :return: list
        '''
        return copy.deepcopy(self._nodeProperty_edgeUndirectedList)

    # def updateProperty_edgeOutList_replace(self, newEdgeOutList:list):
    #     '''
    #     Replace the outgoing edges list with a new list.
    #     :param newEdgeOutList: list
    #     :return:
    #     '''
    #     assert isinstance(newEdgeOutList, list)
    #     temp_set_list = set(newEdgeOutList)
    #     assert len(temp_set_list) == len(newEdgeOutList)  # NO duplicate elements are allowed!
    #     self._nodeProperty_edgeOutList = copy.deepcopy(newEdgeOutList)
    #
    # def updateProperty_edgeInList_replace(self, newEdgeInList:list):
    #     '''
    #     Replace the incoming edges list with a new list.
    #     :param newEdgeInList: list
    #     :return:
    #     '''
    #     assert isinstance(newEdgeInList, list)
    #     temp_set_list = set(newEdgeInList)
    #     assert len(temp_set_list) == len(newEdgeInList)  # NO duplicate elements are allowed!
    #     self._nodeProperty_edgeInList = copy.deepcopy(newEdgeInList)

    def updateProperty_edgeUndirected_replace(self, newEdgeList:list):
        '''
        Replace the undirected edges list with a new list.
        :param newEdgeList: list
        :return:
        '''
        assert isinstance(newEdgeList, list)
        temp_set_list = set(newEdgeList)
        assert len(temp_set_list) == len(newEdgeList)  # NO duplicate elements are allowed!
        self._nodeProperty_edgeUndirectedList = copy.deepcopy(newEdgeList)

    def updateProperty_edgeUndirectedList_reset(self):
        '''
        Reset the undirected edges list as [].
        :return:
        '''
        self._nodeProperty_edgeUndirectedList = []

    def updateProperty_edgeUndirectedList_appendOne(self, newEdge:int):
        '''
        Append ONE NEW undirected edge to the list.
        :param newEdge: int
        :return:
        '''
        assert isinstance(newEdge, int)
        assert newEdge not in self._nodeProperty_edgeUndirectedList
        self._nodeProperty_edgeUndirectedList.append(copy.deepcopy(newEdge))

    # def updateProperty_edgeOutList_remove(self, edgeList_2BRemoved:list):
    #     '''
    #     Remove some elements from the outgoing edges list.
    #     Note that the edgeList_2BRemoved is allowed to contain the elements that is not in the current outgoing edge list.
    #     :param edgeList_2BRemoved:
    #     :return:
    #     '''
    #     for edge_i in edgeList_2BRemoved:
    #         if edge_i in self._nodeProperty_edgeOutList:
    #             self._nodeProperty_edgeOutList.remove(edge_i)
    #             assert edge_i not in self._nodeProperty_edgeOutList
    #
    # def updateProperty_edgeInList_remove(self, edgeList_2BRemoved:list):
    #     '''
    #     Remove some elements from the incoming edges list.
    #     Note that the edgeList_2BRemoved is allowed to contain the elements that is not in the current incoming edge list.
    #     :param edgeList_2BRemoved:
    #     :return:
    #     '''
    #     for edge_i in edgeList_2BRemoved:
    #         if edge_i in self._nodeProperty_edgeInList:
    #             self._nodeProperty_edgeInList.remove(edge_i)
    #             assert edge_i not in self._nodeProperty_edgeInList

    def updateProperty_edgeUndirectedList_remove(self, edgeList_2BRemoved:list):
        '''
        Remove some elements from the undirected edges list.
        Note that the edgeList_2BRemoved is allowed to contain the elements that is not in the current incoming edge list.
        :param edgeList_2BRemoved:
        :return:
        '''
        for edge_i in edgeList_2BRemoved:
            if edge_i in self._nodeProperty_edgeUndirectedList:
                self._nodeProperty_edgeUndirectedList.remove(edge_i)
                assert edge_i not in self._nodeProperty_edgeUndirectedList # For DEBUG only. If everything is right, the edge list is supposed to have NO duplicate elements.

    def getNodeProperty_edgeUndirected_number(self) -> int:
        '''
        Get the number of undirected edges connected to this node.
        :return: int
        '''
        return len(self._nodeProperty_edgeUndirectedList)



########################################################################################################################
########################################################################################################################
########################################################################################################################
class CACCodebook:
    '''
    The graph structure of the CAC codebook.
    '''
    def __init__(self, cw_len:int):
        assert isinstance(cw_len, int) and cw_len > 1
        self._codebookProperty_codewordLength = cw_len # The bit-width of codewords.

        # Initialize
        self.initializeCodebook_all()

    ####################################################################################################################
    ### Initialization
    def initializeCodebook_allNodes(self, ):
        '''
        Initialize the ID list and the node object list for the CAC codebook.\n
        Be careful! This will replace the existing data in this codebook with a init one.
        :return:
        '''
        self._codebook_idList = [] # List of the node id.
        self._codebook_nodeObjList = [] # List of the node obj.
        self._removed_idList = []
        self._removed_nodeObjList = []

        # Initialize
        for id_i in range(0, (2 ** self.getCodebookProperty_codewordLength())):
            cw_binStr = bin(id_i)[2:].zfill(self.getCodebookProperty_codewordLength())
            cw_binList = []
            for binStr_i in cw_binStr:
                if binStr_i == '0':
                    cw_binList.append(0)
                elif binStr_i == '1':
                    cw_binList.append(1)
                else:
                    assert False
            self._codebook_idList.append(copy.deepcopy(id_i))
            self._codebook_nodeObjList.append(_CACCodewordNode(node_id=copy.deepcopy(id_i), codeword=copy.deepcopy(cw_binList)))

        # Establish edges
        self._initializeCodebook_allEdgeUndirectedList()

    def _initializeCodebook_allEdgeUndirectedList(self, allow_empty_edgeList = False):
        '''
        This will initialize the undirected edge lists of each node obj in this codebook.\n
        Note that this function should only be automatically called when initializing all node objs, but not called in other locations.\n
        If allow_empty_edgeList is set as False (default), the function will make sure all the current edge lists are empty.\n
        Assume that the crosstalk level between two codewords is no related to their order, i.e., the xtalk level of codeword A --> codeword B is same as that of B --> A.
        So, the xtalk value in the following matrix are symmetric matrix.\n
        ###################################\n
        ###00__01__02__03__04__05...\n
        \n
        00___??__??__??__??__??__??\n
        01___??__??__??__??__??__??\n
        02___??__??__??__??__??__??\n
        03___??__??__??__??__??__??\n
        04___??__??__??__??__??__??\n
        05___??__??__??__??__??__??\n
        .._ \n
        .._ \n
        .._ \n

        :param allow_empty_edgeList: bool
        :return:
        '''
        n_node = len(self._codebook_idList)
        if allow_empty_edgeList is False:
            for idx_aa in range(0, n_node):
                assert self._codebook_nodeObjList[idx_aa].getNodeProperty_edgeUndirected_number() == 0
        for idx_ii in range(0, n_node):
            cwTuple_01 = tuple(self._codebook_nodeObjList[idx_ii].getProperty_codeword())
            for idx_kk in range(idx_ii, n_node):
                cwTuple_02 = tuple(self._codebook_nodeObjList[idx_kk].getProperty_codeword())
                xtalk_if_sat = self.xtalkEvaluaion_transition(cwTuple_01=cwTuple_01, cwTuple_02=cwTuple_02)
                if (xtalk_if_sat is True) and (idx_ii != idx_kk):
                    self._codebook_nodeObjList[idx_ii].updateProperty_edgeUndirectedList_appendOne(newEdge=idx_kk)
                    self._codebook_nodeObjList[idx_kk].updateProperty_edgeUndirectedList_appendOne(newEdge=idx_ii)
                elif (xtalk_if_sat is True) and (idx_ii == idx_kk):
                    self._codebook_nodeObjList[idx_ii].updateProperty_edgeUndirectedList_appendOne(newEdge=idx_kk)
                else:
                    assert xtalk_if_sat is False

    ####################################################################################################################
    ### Crosstalk Evaluation
    def xtalkEvaluaion_transition(self, cwTuple_01: tuple[int, ...], cwTuple_02: tuple[int, ...], evaluation_method = 'Ring2CDefault') -> bool:
        '''
        Evaluate if the xtalk level of the transition cwTuple_01 --> cwTuple_02 is no more than a certain upper bound.\n
        This function is only an interface. The detailed evaluation method and the upper bound is implemented in other functions.\n
        :param cwTuple_01:
        :param cwTuple_02:
        :param evaluation_method:
        :return:
        '''
        if evaluation_method == 'Ring2CDefault':
            return self.xtalkEvaluation_Ring2CDefault(cwTuple_01=cwTuple_01, cwTuple_02=cwTuple_02)


    @staticmethod
    def xtalkEvaluation_Ring2CDefault(cwTuple_01:tuple[int, ...], cwTuple_02:tuple[int, ...]) -> bool:
        '''

        :param cwTuple_01:
        :param cwTuple_02:
        :return:
        '''
        assert isinstance(cwTuple_01, tuple) and isinstance(cwTuple_02, tuple)
        cw_length = len(cwTuple_01)
        assert len(cwTuple_02) == cw_length
        xtalk_is_sat = True
        cwDiffList = []
        for idx_i in range(0, cw_length):
            cwDiffList.append(cwTuple_02[idx_i] - cwTuple_01[idx_i])
        # All bits except MSB & LSB
        for idx_i in range(1, cw_length - 1):
            if cwDiffList[idx_i] in (-1, 1):
                if (abs(cwDiffList[idx_i - 1] - cwDiffList[idx_i]) + abs(cwDiffList[idx_i + 1] - cwDiffList[idx_i])) > 2:
                    xtalk_is_sat = False
                    return False
            else:
                assert cwDiffList[idx_i] == 0
        # MSB
        if cwDiffList[-1] in (-1, 1):
            if (abs(cwDiffList[-2] - cwDiffList[-1]) + abs(cwDiffList[0] - cwDiffList[-1])) > 2:
                xtalk_is_sat = False
                return False
            else:
                assert cwDiffList[-1] == 0
        # LSB
        if cwDiffList[0] in (-1, 1):
            if (abs(cwDiffList[-1] - cwDiffList[0]) + abs(cwDiffList[1] - cwDiffList[0])) > 2:
                xtalk_is_sat = False
                return False
            else:
                assert cwDiffList[0] == 0

        assert xtalk_is_sat is True
        return True

    ####################################################################################################################
    ### Properties
    def getCodebookProperty_codewordLength(self) -> int:
        '''
        Get the bit-width of the codewords.
        :return:
        '''
        return copy.deepcopy(self._codebookProperty_codewordLength)

    def getCodebookProperty_nodeNumber(self) -> int:
        '''
        Get the number of the nodes in the graph.\n
        The nodes in 'removed' state are not taken into account.\n
        :return: int
        '''
        return len(self._codebook_idList)

    ####################################################################################################################
    ### Codebook Pruning
    def codebookPruning_heuristic_main(self, heuristicMethod = "degreeOnly"):
        '''
        The main function of the heuristic algorithm for selected the node to be pruned in next step.\n
        There may be more than one heuristic methods available, and the var heuristicMethod is used to select the heuristic method.\n
        However, the heuristic methods are not implemented in this function.\n
        #####################################################################\n
        The available heuristic methods are as follows:\n

        - degreeOnly:
        The node with the lowest degree should be removed.
        If there are multiple nodes with the lowest degree, remove the one with the lowest ID.
        (Note: The 'degree' means the number of edges connected with a node.)\n

        :param heuristicMethod:
        :return: tuple(int, int) - The first 'int' is the idx in node list and the second 'idx' is the node ID.
        '''
        #######################################
        if heuristicMethod == "degreeOnly":
            candidate_idxAndIDList = [] # Note that each element in this list should be a tuple(int, int), in which the first 'int' is the idx in node list and the second 'idx' is the node ID.
            candidate_degreeValue = self.getCodebookProperty_nodeNumber()
            for idx_i in range(0, self.getCodebookProperty_nodeNumber()):
                nodeDegree_i = self._codebook_nodeObjList[idx_i].getNodeProperty_edgeUndirected_number()
                if nodeDegree_i == candidate_degreeValue:
                    candidate_idxAndIDList.append((idx_i, copy.deepcopy(self._codebook_idList[idx_i])))
                elif nodeDegree_i < candidate_degreeValue:
                    candidate_idxAndIDList = []
                    candidate_degreeValue = nodeDegree_i
                    candidate_idxAndIDList.append((idx_i, copy.deepcopy(self._codebook_idList[idx_i])))
                else:
                    assert nodeDegree_i > candidate_degreeValue
            return copy.deepcopy(candidate_idxAndIDList[0])
        ########################################
        else:
            assert False
