# Champions League 2024

## Table of Contents

- [Installation](#installation)
- [Champions League 2024](#champions-league-2024)
- [General Problem](#general-problem)
- [License](#license)

## Champions League 2024

The 36 teams will no longer be drawn into groups. Instead, they will all start the competition together in one league, with every team playing against eight others. The 36 teams will be seeded into four pots of nine based on the 2023–24 UEFA club coefficients. Each club plays four matches at home and four matches away, one home and one away match against a team from each of the four pots. The seeding will be based on the following principles:

- Pot 1 will contain the Champions League title holder and the 8 qualified teams with the highest UEFA club coefficient (CC).
- Pots 2, 3 and 4 will contain the remaining qualified teams grouped by highest to lowest club coefficient.

In principle, clubs from the same association will not be drawn against each other in the league phase. Exceptionally, a maximum of one match per club against another club from the same association may be allowed for associations with four or more clubs in the league stage, if this is the only way to avoid a deadlock in the draw. 

Those information are based on the [Wikipedia](https://en.wikipedia.org/wiki/2024%E2%80%9325_UEFA_Champions_League#League_stage) page.

## General Problem

We are given a graph $G=(V,E)$, where the vertices are partitioned into $k$ subsets $V_1, \dots, V_k$. An integer $d$ is given. The goal is to decide whether there exists a subset $F$ of $E$ such that every vertex has $d$ neighbors in $F$ within each $V_i$.

This problem is polynomial, even if $d$ is free (i.e., complexity of the form $O(|V|^a \log^b(d)))$. Indeed, the problem is "separable":


- First problem:

    For each pair of distinct integers  $(i,\, j) \in [\![0, k]\!]^2$, decide whether there exists a subset of edges in the bipartite graph $(V_i\cup V_j,\, E_{ij})$ giving each vertex a degree of $d$, where $E_{ij}$ is the subset of $E$ with one endpoint in $V_i$ and the other in $V_j$. This can be done in polynomial time using a `maximum flow algorithm`.
- Second problem: 

    For each integer $i \in [\![0, k]\!]$, decide whether there exists a subset of edges in the "induced" subgraph $G[V_i] = (V_i,\, E_i)$ giving each vertex a degree of $d$. 
    
    Where $E_i$ is the subset of $E$ with both endpoints in $V_i$. This can be done in polynomial time using an algorithm for `simple d-matchings`. This is a challenging algorithm.

We have a solution if and only if the answer is "yes" for the $\frac{k(k-1)}{2} + k = \frac{k(k+1)}{2}$ previous tests.

The Champions League 2024 format corresponds as the case where $k=4$ and $d=2$ of this problem.


## Installation

Install the requirements by running 

```
pip install requirements.txt 
```
