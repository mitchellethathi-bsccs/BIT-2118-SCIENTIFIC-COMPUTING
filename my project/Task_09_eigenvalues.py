# Task 09: Eigenvalues and Eigenvectors
# B) Find the dominant eigenpair and centrality scores of a four-node network.
# C) Remove an edge and compare node scores.
# D) Verify the eigenpair residual.
# E) Compute PageRank-style scores for a directed graph.

import numpy as np

A = np.array([[0,1,1,0], [1,0,1,1], [1,1,0,1], [0,1,1,0]], dtype=float)
nodes = ["A", "B", "C", "D"]
def scores(matrix):
	vals, vecs = np.linalg.eig(matrix)
	i = np.argmax(vals.real)
	v = vecs[:, i].real
	return vals[i].real, np.abs(v) / np.abs(v).sum(), v
value, centrality, v = scores(A)
print("Dominant eigenvalue:", value)
for node, score in zip(nodes, centrality): print(node, round(score, 4))
print("Residual:", np.linalg.norm(A @ v - value * v))
A[2, 3] = A[3, 2] = 0
value2, centrality2, _ = scores(A)
print("After removing C-D:", list(zip(nodes, np.round(centrality2, 4))))

M = np.array([[0,1,1,0,0], [1,0,0,1,0], [1,0,0,1,1],
			  [0,1,1,0,1], [0,0,1,1,0]], dtype=float)
n = len(M); damping = .85
P = damping * M / M.sum(axis=0) + (1 - damping) / n
vals, vecs = np.linalg.eig(P)
i = np.argmax(vals.real)
pagerank = np.abs(vecs[:, i].real); pagerank /= pagerank.sum()
print("PageRank:", np.round(pagerank, 4), "eigenvalue:", vals[i].real)
