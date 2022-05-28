
from itertools import chain, combinations
import graphviz
# from https://stackoverflow.com/a/1482316
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def isAntichain(elements):
  for x in elements:
    xSet = set(x)
    for y in elements:
      if x != y and xSet.issubset(y):
        return False
  return True
  
def lessThan(antichain1, antichain2):
  antichain1Sets = [set(a) for a in antichain1]
  for b in antichain2:
    foundA = False
    for aSet in antichain1Sets:
      if aSet.issubset(b):
        foundA = True
    if not foundA: return False
  return True
  
def makeAntichains(elements):
  antichains = [x for x in powerset(powerset(elements)) if isAntichain(x)]
  return antichains
  
def makeRedudancyGraph(elements):
  antichains = makeAntichains(elements)
  edges = dict([(i, set()) for i in range(len(antichains))])
  for i, x in enumerate(antichains):
    for j, y in enumerate(antichains):
      if i != j:
        if lessThan(x,y):
          edges[i].add(j)
  
  dot = graphviz.Digraph()
  for i, x in enumerate(antichains):
    dot.node(str(i), str(x).replace(", ", "").replace(",","")[1:-1])
  for i, x in enumerate(antichains):
    for j, y in enumerate(antichains):
      if i != j:
        if lessThan(x,y):
          # if there is k s.t. i->k and k->j then don't render i->j
          foundEdges = False
          for k in range(len(antichains)):
            if k in edges[i] and j in edges[k]:
                foundEdges = True
            if foundEdges: break
          if not foundEdges:
            dot.edge(str(j), str(i))
  return dot
      