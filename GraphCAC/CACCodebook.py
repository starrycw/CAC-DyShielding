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
        self._nodeProperty_id = copy.deepcopy(node_id)  # Node ID
        self._nodeProperty_codeword = copy.deepcopy(codeword)  # The codeword represented by this node.

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
        self.initializeCodebook_allNodes()

        # Pruning Vars
        self._varPruning_bestDegreeRecorded = 0
        self._varPruning_bestNodeObjListRecorded = []
        self._varPruning_bestIdListRecorded = []

    ####################################################################################################################
    ### Initialization And Backup
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
        self._backup_codebookIdList = []
        self._backup_codebookNodeObjList = []
        self._backup_removedIdList = []
        self._backup_removedNodeObjList = []

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
            self._codebook_nodeObjList.append(_CACCodewordNode(node_id=copy.deepcopy(id_i), codeword=tuple(cw_binList)))

        # Establish edges
        self._initializeCodebook_allEdgeUndirectedList()

    def _initializeCodebook_allEdgeUndirectedList(self, allow_nonEmpty_edgeList = False):
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

        :param allow_nonEmpty_edgeList: bool
        :return:
        '''
        n_node = len(self._codebook_idList)
        if allow_nonEmpty_edgeList is False:
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

    def _backup_backupCurrentList(self):
        '''
        Copy the current lists:\n
        self._codebook_idList,
        self._codebook_nodeObjList,
        self._removed_idList,
        self._removed_nodeObjList\n
        to\n
        self._backup_codebookIdList,
        self._backup_codebookNodeObjList,
        self._backup_removedIdList,
        self._backup_removedNodeObjList.
        :return:
        '''
        self._backup_codebookIdList = copy.deepcopy(self._codebook_idList)
        self._backup_codebookNodeObjList = copy.deepcopy(self._codebook_nodeObjList)
        self._backup_removedIdList = copy.deepcopy(self._removed_idList)
        self._backup_removedNodeObjList = copy.deepcopy(self._removed_nodeObjList)

    def _backup_backup_restoreBackups(self):
        '''
        Copy the current lists:\n
        self._backup_codebookIdList,
        self._backup_codebookNodeObjList,
        self._backup_removedIdList,
        self._backup_removedNodeObjList\n
        to\n
        self._codebook_idList,
        self._codebook_nodeObjList,
        self._removed_idList,
        self._removed_nodeObjList.
        :return:
        '''
        self._codebook_idList = copy.deepcopy(self._backup_codebookIdList)
        self._codebook_nodeObjList = copy.deepcopy(self._backup_codebookNodeObjList)
        self._removed_idList = copy.deepcopy(self._backup_removedIdList)
        self._removed_nodeObjList = copy.deepcopy(self._backup_removedNodeObjList)

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

    def getCodebookProperty_minimumDegreeValue(self) -> int:
        '''
        Get the minimum degree of nodes.
        :return:
        '''
        var_idxAndIDListOfNodesPruning, var_degreeValueOfNodesPruning = self.codebookPruning_heuristic_main()
        return var_degreeValueOfNodesPruning


    ####################################################################################################################
    ### Codebook Pruning
    def codebookPruning_continuousPruningUntilNoGain(self, pruningCycleLimitation = 0, restoreTheNegativePruning = False):
        '''
        Do pruning continuously, until the next pruning decrease the min degree.\n
        Note that this function does not guarantee that the stop point has the global highest degree.\n
        The better result will be recorded!

        :param pruningCycleLimitation: int - The default value is 0, which means no limitation.
        :param restoreTheNegativePruning: boolean - If True, the node list will be roll back if the last pruning reduces degree.
        :return:
        '''
        assert isinstance(pruningCycleLimitation, int) and (pruningCycleLimitation >= 0)
        flag_stop_pruning = False
        cnt_pruningCycle = 0
        #self._backup_backupCurrentList() # Backup
        var_idxAndIDListOfNodesPruning, var_degreeValueOfNodesPruning = self.codebookPruning_heuristic_main()
        self._varPruning_degreeValueOfNodesPruning_lastCycle = copy.deepcopy(var_degreeValueOfNodesPruning) - 1
        while not flag_stop_pruning:
            cnt_pruningCycle = cnt_pruningCycle + 1
            var_idxAndIDListOfNodesPruning, var_degreeValueOfNodesPruning = self.codebookPruning_heuristic_main()
            if var_degreeValueOfNodesPruning < self._varPruning_degreeValueOfNodesPruning_lastCycle:
                if self._varPruning_degreeValueOfNodesPruning_lastCycle >= self._varPruning_bestDegreeRecorded:
                    self._varPruning_bestDegreeRecorded = copy.deepcopy(self._varPruning_degreeValueOfNodesPruning_lastCycle)
                    self._codebookPruning_recordBetterResult_recordBackups()
                if restoreTheNegativePruning is True:
                    self._backup_backup_restoreBackups()
                flag_stop_pruning = True
                print("[Pruning] Terminated! The min degree after last pruning is {}, which is no larger than that before ({})!".format(var_degreeValueOfNodesPruning, self._varPruning_degreeValueOfNodesPruning_lastCycle))

            else:
                self._backup_backupCurrentList()
                self.codebookPruning_pruningOnce(idxAndIDList_nodes2BPruning=var_idxAndIDListOfNodesPruning)
                self._varPruning_idxAndIDListOfNodesPruning_lastCycle = copy.deepcopy(var_idxAndIDListOfNodesPruning)
                self._varPruning_degreeValueOfNodesPruning_lastCycle = copy.deepcopy(var_degreeValueOfNodesPruning)
                print("[Pruning] Cycle={}, degree of nodes removed={}, number of nodes removed={}".format(cnt_pruningCycle, var_degreeValueOfNodesPruning, len(var_idxAndIDListOfNodesPruning)))

    def _codebookPruning_recordBetterResult_recordBackups(self):
        '''
        Copy the 'backup' lists to the self._varPruning_bestIdListRecorded and self._varPruning_bestNodeObjListRecorded.
        :return:
        '''
        self._varPruning_bestIdListRecorded = copy.deepcopy(self._backup_codebookIdList)
        self._varPruning_bestNodeObjListRecorded = copy.deepcopy(self._backup_codebookNodeObjList)

    def codebookPruning_getBestRecord(self):
        '''
        Return copy.deepcopy(self._varPruning_bestDegreeRecorded), copy.deepcopy(self._varPruning_bestIdListRecorded), copy.deepcopy(self._varPruning_bestNodeObjListRecorded)
        :return:
        '''
        return copy.deepcopy(self._varPruning_bestDegreeRecorded), copy.deepcopy(self._varPruning_bestIdListRecorded), copy.deepcopy(self._varPruning_bestNodeObjListRecorded)

    

    def codebookPruning_pruningOnce(self, idxAndIDList_nodes2BPruning):
        '''
        Pruning once.\n
        Note that the codebook graph will be modified directly after pruning.\n
        Please make sure you have the backups of current graph before pruning.\n
        The pruning result will NOT be evaluated and recorded!
        :param idxAndIDList_nodes2BPruning: list/tuple with one or more elements tuple(int, int), and int - The first 'int' is the idx in node list and the second 'idx' is the node ID.
        :return: Nothing
        '''
        # Get the list containing the nodes to be removed in this pruning.
        # idxAndIDList_nodes2BPruning, degreeValue_nodes2BPruning = self.codebookPruning_heuristic_main(heuristicMethod=heuristicMethod)
        # Removing
        assert isinstance(idxAndIDList_nodes2BPruning, list) or isinstance(idxAndIDList_nodes2BPruning, tuple)
        for idxAndID_tuple_i in idxAndIDList_nodes2BPruning:
            self.codebookPruning_removeOneNode(node2BRemove_index=idxAndID_tuple_i[0], node2BRemove_id=idxAndID_tuple_i[1])


    def codebookPruning_removeOneNode(self, node2BRemove_index = None, node2BRemove_id = None):
        '''
        Remove one node from the graph.\n
        The node2BRemove_index is the idx of the node to be removed in the node list.\n
        The node2BRemove_id is the ID of the node to be removed.\n
        Note that node2BRemove_index OR node2BRemove_id should be assigned a value!\n
        :param node2BRemove_index:
        :param node2BRemove_id:
        :return:
        '''
        # Complete and verify the values of ID and Index.
        if isinstance(node2BRemove_index, int):
            if isinstance(node2BRemove_id, int):
                assert self._codebook_nodeObjList[node2BRemove_index].getProperty_nodeID() == node2BRemove_id
                assert self._codebook_idList[node2BRemove_index] == node2BRemove_id
            else:
                assert node2BRemove_id is None
                node2BRemove_id = self._codebook_idList[node2BRemove_index]
                assert self._codebook_nodeObjList[node2BRemove_index].getProperty_nodeID() == node2BRemove_id
        else:
            assert node2BRemove_index is None
            assert isinstance(node2BRemove_id, int)
            node2BRemove_index = self._codebook_idList.index(node2BRemove_id)
            assert self._codebook_nodeObjList[node2BRemove_index].getProperty_nodeID() == node2BRemove_id

        # Remove the edges in other node objs
        for idx_ii in range(0, self.getCodebookProperty_nodeNumber()):
            if idx_ii != node2BRemove_index:
                self._codebook_nodeObjList[idx_ii].updateProperty_edgeUndirectedList_remove(edgeList_2BRemoved=[node2BRemove_id])
        # Remove this node
        self._removed_idList.append(copy.deepcopy(self._codebook_idList.pop(node2BRemove_index)))
        self._removed_nodeObjList.append(copy.deepcopy(self._codebook_nodeObjList.pop(node2BRemove_index)))




    def codebookPruning_heuristic_main(self, heuristicMethod="degreeOnly"):
        '''
        The main function of the heuristic algorithm for selected the node to be pruned in next step.\n
        There may be more than one heuristic methods available, and the var heuristicMethod is used to select the heuristic method.\n
        However, the heuristic methods are not implemented in this function.\n
        It is important to note that the elements in the return list MUST be ordered by the reversed index!
        #####################################################################\n
        The available heuristic methods are as follows:\n

        - degreeOnly:
        The node with the lowest degree should be removed.
        (Note: The 'degree' means the number of edges connected with a node.)\n

        :param heuristicMethod:
        :return: list with one or more elements tuple(int, int), and int - The first 'int' is the idx in node list and the second 'idx' is the node ID, the finally 'int' is the degree value.
        '''
        #######################################
        if heuristicMethod == "degreeOnly":
            return self.codebookPruning_heuristic_degreeOnly()
        ########################################
        else:
            assert False

    def codebookPruning_heuristic_degreeOnly(self):
        '''
        degreeOnly:\n
        The node with the lowest degree should be removed.
        (Note: The 'degree' means the number of edges connected with a node.)\n

        :return: list with one or more elements tuple(int, int), and int - The first 'int' is the idx in node list and the second 'idx' is the node ID, the finally 'int' is the degree value.
        '''
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
        candidate_idxAndIDList.reverse()
        return copy.deepcopy(candidate_idxAndIDList), candidate_degreeValue

