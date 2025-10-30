# quantum-hamiltonian-circuit

The goal of this project is to create a full stack application enabling a user to input a small graph, and dynamically create a quantum circuit (oracle included) that determines if a Hamiltonian circuit exists in the graph using Grover's search. This is an exploration of how quantum search can speed up NP-complete problems by providing quadratic speed-up over classical brute force.

## todo

- [ ] determine a polynomial quantum circuit (in gates) that determines if a given circuit (cycle) is a Hamilton cycle
    - [x] determine how to check if a given edge is contained in the edge set E
    - [ ] determine how to check if ALL edges are contained in the edge set E
    - [ ] determine how to check that no vertex is given twice in the circuit
    - [ ] determine how to check that all vertices in the graph are in the circuit
    - [ ] determine how to check that the first vertex is also the last vertex 
    - [ ] ensure this is polynomial
- [ ] implement a general oracle $O$ for any graph
- [ ] implement Grover's around this oracle $O$ 
- [ ] implement the circuit and run on quantum simualtor (perhaps `qsim`?)
    - [x] implemented circuit to check if (v1, v2) is in E for a given E
- [ ] build the interface etc
    - [ ] web dev magic w/ drag and drop nodes (on the order of 5 vertices max depending on how # qubits grows w.r.t V, E)


# Edge Checking
## Iteration 1

![Circuit for edge checking](edgeCheckingCircuit.png)
The image shows the circuit for a graph for $e=2$ edges with an input of $n=2$ vertices ($m=1$ bits each), corresponding to $m*n + n + e+1=n(m+1)+e+1$ qubits. There are 38 (non-barrier) gates. 

For each $Check$ operation which checks the validity of proposed edge $(v_i, v_j)$ we have to return the register `edgeResultQubits` back to the original state for the next pair $(v_{i+1}, v_{j+1})$ to be checked (reducing ancillas). Thus we are trading the need for more qubits for a longer circuit. Since $Check$ is just one of a few subroutines in the oracle, we should investigate shortening the length of the circuit. Later subroutines will want to reuse a subset of the qubits for their own purpose. Thus we explore mid-circuit measurements and qubit resets as as possible avenue for both shortening the length of the circuit as well as reducing the number of ancillas.

## Iteration 2

![Circuit for edge checking iteration 2](edgeCheckingCircuitit2.png)

This (dynamic) circuit includes mid-circuit resets on all `edgeResultQubits` between each pair of vertices (i.e. edge) being checked. This circuit now uses 26 gates, a 32% reduction in gates for the same number of ancillas.