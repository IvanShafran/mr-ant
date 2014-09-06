import queue


def bfs(start_vertex, graph):
    queue_ = queue.Queue()
    queue_.put_nowait(start_vertex)
    was = list(False for x in range(len(graph)))
    was[start_vertex] = True
    distance = list("Inf" for x in range(len(graph)))
    distance[start_vertex] = 0

    while not queue_.empty():
        vertex = queue_.get()
        for incidence_vertex in graph[vertex]:
            if not was[incidence_vertex]:
                was[incidence_vertex] = True
                distance[incidence_vertex] = distance[vertex] + 1
                queue_.put(incidence_vertex)

    return distance
