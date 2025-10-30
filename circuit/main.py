# Author: Leon Rode

# for any set of edges E, generate a quantum circuit that 
# determines if an edge is an edge in E

from qiskit import QuantumCircuit, QuantumRegister, transpile
from typing import List, Tuple
import math
from qiskit_aer import AerSimulator
from utils import ket_label_q0_first


Vertex = int # v: Vertex -> {0, 1, ..., n - 1}
Edge = Tuple[Vertex, Vertex] # e: Edge -> (v1, v2) where v1, v2: Vertex
Edges = List[Edge]

N = 2
M = math.ceil(math.log2(N))
"""
edges: the set of edges E (length = e)
v1Indices: the qubit indices of the first vertex (length = m where m is the number of bits in the binary representation of the vertex index)
v2Indices: the qubit indices of the second vertex (length = m where m is the number of bits in the binary representation of the vertex index)
resIndices: the qubit indices of the intermediate results (length = e where e is the number of edges in the edge set E)
resIndex: the qubit index of the result

returns: None (directly modifies the input quantum circuit qc)
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
        qc.barrier(label=f"<- edge {edge}")

    # next apply X on all resIndices
    for i in range(len(resIndices)):
        qc.x(resIndices[i])

    qc.barrier()
    # next we apply the MCX on all of resIndices, with target on resIndex
    qc.mcx(resIndices, resIndex)
    qc.x(resIndex)

    qc.barrier()
    # next we apply X on resIndex

    # apply reset on all resIndices
    for i in range(len(resIndices)):
        qc.reset(resIndices[i])



"""
Assumes specific ordering of qubits:
v1...vN take up first N * M qubits
re_i take up next len(edges) qubits
res_check takes up the last qubit

for a total of N*(M+1) + len(edges) + 1 qubits

"""
def checkAll(qc: QuantumCircuit, edges: Edges) -> None:


    RES_EDGES_START_INDEX = N * M
    RES_EDGES_END_INDEX = RES_EDGES_START_INDEX + len(edges) - 1
    
    
    RES_EDGE_INDICES = list(range(RES_EDGES_START_INDEX, RES_EDGES_END_INDEX + 1))
    RES_INDICES = list(range(RES_EDGES_END_INDEX + 1, RES_EDGES_END_INDEX + N + 1))
    
    CHECK_INDEX = RES_EDGES_END_INDEX + N + 1
    # iterate over the pairs

    for i in range(N - 1):

        v1Indices = [i * M + j for j in range(M)]
        v2Indices = [(i + 1) * M + j for j in range(M)]
        RES_INDEX = RES_EDGES_END_INDEX + i + 1

        check(qc, edges, v1Indices, v2Indices, RES_EDGE_INDICES, RES_INDEX)

        qc.barrier()
        qc.barrier()

    # check vn -> v1
    v1Indices = [(N - 1) * M + j for j in range(M)]
    v2Indices = [0 * M + j for j in range(M)]
    RES_INDEX = RES_EDGES_END_INDEX + N
    check(qc, edges, v1Indices, v2Indices, RES_EDGE_INDICES, RES_INDEX)

    qc.barrier()
    qc.barrier()
    qc.mcx(RES_INDICES, CHECK_INDEX)

# test case

#edges = [(0, 1), (1, 2), (2, 3)]
edges = [(0, 1), (1, 0)]

vertexRegs = []
for i in range(N):
    vertexRegs.append(QuantumRegister(M, name=f"vertex{i}"))

edgeResultQubits = QuantumRegister(len(edges), name="edgeResultQubits")
resultQubits = QuantumRegister(N, name="resultQubits")
checkQubit = QuantumRegister(1, name="checkQubit")

qc = QuantumCircuit(*vertexRegs, edgeResultQubits, resultQubits, checkQubit)
# let's simulate the circuit and ensure that it works

# for example, we expect the following circuit to work:
# (0, 1)
# 01
# |01>

qc.x(vertexRegs[1][0])

qc.barrier()


checkAll(qc, edges)

qc.save_statevector()

sim = AerSimulator(method="statevector")

compiled = transpile(qc, sim)

job = sim.run(compiled)
result = job.result()
statevector = result.get_statevector()
print(statevector)
qc.draw(output="mpl", filename=f"edgeCheckingCircuit_{N}_{len(edges)}.png", fold=-1)

print(qc.count_ops())

print(ket_label_q0_first(statevector))