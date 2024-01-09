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

