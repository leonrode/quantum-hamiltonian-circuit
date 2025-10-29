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
