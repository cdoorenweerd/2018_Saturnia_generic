var.doCheckForAllGapColumns=False
a = func.readAndPop('20180226_Saturnia_7Gpr4.nex')
# Now a.taxNames has the list we want

var.nexus_doFastNextTok = False
var.punctuation = var.phylip_punctuation

tMaster = func.readAndPop('RAxML_bipartitions.BestBS')
tSecondary = func.readAndPop('ExaBayes_ConsensusExtendedMajorityRuleNewick.myCons')

tMaster.taxNames = a.taxNames
tSecondary.taxNames = a.taxNames

# Split keys are numerical versions of the 'dot-star' split notation.
# The same split on the two trees would have the same split key.
tMaster.makeSplitKeys()
tSecondary.makeSplitKeys()

# Make a dictionary, so that we can fish out nodes in the secondary tree
# given a split key.  Split keys are found on node branches, here
# n.br.
myDict = {}
for n in tSecondary.iterInternalsNoRoot():
    myDict[n.br.splitKey] = n

for nM in tMaster.iterInternalsNoRoot():
    # Given a split key in the master tree, we can find the
    # corresponding node in the secondary tree, using the split key with
    # the dictionary.
    nS = myDict.get(nM.br.splitKey)
    # If there was none, then nS is None
    if nS:
        nM.name = '%s/%s' % (nM.name, nS.name)
    else:
        nM.name = '%s/-' % nM.name
    #print nM.name
tMaster.writeNexus('combinedSupportsTree.nex')
