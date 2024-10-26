#!/usr/bin/env python3

def works(edge):
    """ Given an edge, represented as a set of vertex indices,
    returns true iff it is a valid cyclic representation of a finite plane.
    """
    n = len(edge) - 1
    num_vertices = n*n + n + 1
    for i in range(1, num_vertices):
            new_edge = {(v+i) % num_vertices for v in edge}
            if len(edge.intersection(new_edge)) != 1:
                    return False
    return True

def find_solution(n):
    """ Iterates through sets {a_i} of the form
    0 <= a_1 < a_2 < ... < a_{n+1} < num_vertices
    and returns the first one which is a valid cyclic representation of
    a finite plane. Adds one to the indices to match the way humans count.
    """
    edge = list(range(n+1))
    num_vertices = n*n + n + 1
    while not works(set(edge)):
        index = n
        edge[index] += 1
        while edge[index] > num_vertices - 1:
            index -= 1
            edge[index] += 1
        for j in range(index, n+1):
            edge[j] = edge[index] + (j - index)
    edge = {v + 1 for v in edge}
    return sorted(edge)

for bleh in range(2,6):
    print(find_solution(bleh))
