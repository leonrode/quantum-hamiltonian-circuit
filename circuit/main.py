# Author: Leon Rode

# for any set of edges E, generate a quantum circuit that 
# determines if an edge is an edge in E

from qiskit import QuantumCircuit
from typing import List, Tuple
import math

Vertex = int # v: Vertex -> {0, 1, ..., n - 1}
Edge = Tuple[Vertex, Vertex] # e: Edge -> (v1, v2) where v1, v2: Vertex
Edges = List[Edge]

N = 4
M = math.ceil(math.log2(N))
"""
edges: the set of edges E (length = e)
v1Indices: the qubit indices of the first vertex (length = m where m is the number of bits in the binary representation of the vertex index)
v2Indices: the qubit indices of the second vertex (length = m where m is the number of bits in the binary representation of the vertex index)
resIndices: the qubit indices of the intermediate results (length = e where e is the number of edges in the edge set E)
resIndex: the qubit index of the result
"""

def check(qc: QuantumCircuit, edges: Edges, v1Indices: List[int], v2Indices: List[int], resIndices: List[int], resIndex: int) -> None:

    # we need the binary representation of a Vertex v padded to M bits
    # e.g. v = 3 -> 1

    for edgeIndex, edge in enumerate(edges):
        x, y = edge

        xBin = bin(x)[2:].zfill(M) # padded binary representation of x
        yBin = bin(y)[2:].zfill(M) # padded binary representation of y

        # apply X when the binary is 0 
        for i, c in enumerate(xBin):
            if c == '0':
                qc.x(v1Indices[i])
        
        for i, c in enumerate(yBin):
            if c == '0':
                qc.x(v2Indices[i])


        qc.barrier()
        # apply MCX on all of v1Indices and v2Indices, with target on resIndices[edgeIndex]
        print(v1Indices + v2Indices, resIndices[edgeIndex])
        qc.mcx(v1Indices + v2Indices, resIndices[edgeIndex])

        qc.barrier()
        # now we apply the X's again to flip the qubits back
        for i, c in enumerate(xBin):
            if c == '0':
                qc.x(v1Indices[i])
        
        for i, c in enumerate(yBin):
            if c == '0':
                qc.x(v2Indices[i])
        qc.barrier()

    # next apply X on all resIndices
    for i in range(len(resIndices)):
        qc.x(resIndices[i])

    qc.barrier()
    # next we apply the MCX on all of resIndices, with target on resIndex
    qc.mcx(resIndices, resIndex)

    qc.barrier()
    # next we apply X on resIndex
    qc.x(resIndex)

# test case

edges = [(0, 1), (1, 2)]

# for now we just test two vertices
# 2 * 2 + 2 + 1 = 7
qc = QuantumCircuit(2 * M + len(edges) + 1)

print(qc.draw())

check(qc, edges, [0, 1], [2, 3], [4, 5], 6)

print(qc.draw())