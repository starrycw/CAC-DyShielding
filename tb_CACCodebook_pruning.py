import GraphCAC.CACCodebook

# Graph_01 = GraphCAC.CACCodebook.CACCodebook(cw_len=12, xtalk_evaluation_method="2D2CDefault")
Graph_01 = GraphCAC.CACCodebook.CACCodebook(cw_len=11, xtalk_evaluation_method="Ring2CDefault")
while Graph_01.getCodebookProperty_minimumDegreeValue() > 1:
    Graph_01.codebookPruning_continuousPruningUntilNoGain()
    print("#######")

best_degreeValue01, best_idList01, best_nodeObjList01 = Graph_01.codebookPruning_getBestRecord(recordType='normal_maxDegree')
best_degreeValue02, best_idList02, best_nodeObjList02 = Graph_01.codebookPruning_getBestRecord(recordType='allInterconnected_maxDegree')
print(best_degreeValue01)
print(best_idList01)
print(best_degreeValue02)
print(best_idList02)
print(len(Graph_01.codebookPruing_tryToExtendBestcodebook_extendAllInterconnectedNodes()))