import GraphCAC.CACCodebook

Graph_01 = GraphCAC.CACCodebook.CACCodebook(cw_len=11)
while Graph_01.getCodebookProperty_minimumDegreeValue() > 1:
    Graph_01.codebookPruning_continuousPruningUntilNoGain()
    print("#######")

best_degreeValue, best_idList, best_nodeObjList = Graph_01.codebookPruning_getBestRecord()
print(best_degreeValue)
print(best_idList)