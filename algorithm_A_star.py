"""
Very dirty realization
"""
from queue import PriorityQueue
from bfs import bfs
from random import sample, randint


class _AStarNode():
    def __init__(self, vertex):
        self.vertex = vertex
        self.came_from = None
        self.distance = 0  # distance
        self.hce = 0  # heuristic cost estimate
        self.sum = 0  # sum(x) = distance + hce(x)

    def updateSum(self):
        self.sum = self.hce + self.distance


def _createPath(vertex, node_storage):
    path = list()
    while node_storage[vertex].came_from is not None:
        path.append(vertex)
        vertex = node_storage[vertex].came_from
    path.reverse()
    return path


def _processVertex(processing_vertex, getDistance, getIncidenceList, getHeuristicCostEstimate,
                   processed_vertices, waiting_vertices, node_storage, node_queue):
    waiting_vertices.remove(processing_vertex)
    processed_vertices.add(processing_vertex)

    for incidence_vertex in getIncidenceList(processing_vertex):
        if incidence_vertex not in processed_vertices:
            distance_to_vertex = node_storage[processing_vertex].distance + \
                                 getDistance(processing_vertex, incidence_vertex)

            if (incidence_vertex not in waiting_vertices) or \
                    (distance_to_vertex < node_storage[incidence_vertex].distance):
                waiting_vertices.add(incidence_vertex)

                node_storage[incidence_vertex] = _AStarNode(incidence_vertex)
                node_storage[incidence_vertex].came_from = processing_vertex
                node_storage[incidence_vertex].distance = distance_to_vertex
                node_storage[incidence_vertex].hce = getHeuristicCostEstimate(incidence_vertex)
                node_storage[incidence_vertex].updateSum()
                node_queue.put(tuple(((node_storage[incidence_vertex].sum, -node_queue.unfinished_tasks),
                                             incidence_vertex)))


def findWayByAStar(start, isFinish, getDistance, getIncidenceList, getHeuristicCostEstimate):
    """
    start - start vertex, isFinish - function which returns True only on finish
    getIncidenceList(vertex) - returns incidence list of vertex,
    getDistance(first_vertex, second_vertex) - returns distance from first_vertex to second_vertex,
    getHeuristicCostEstimate(vertex).
    findWayByAStar returns path(list) from start to finish
    """
    processed_vertices = set()
    waiting_vertices = {start, }

    node_queue = PriorityQueue()
    node_storage = dict()

    node_storage[start] = _AStarNode(start)
    node_storage[start].hce = getHeuristicCostEstimate(start)
    node_storage[start].updateSum()
    node_queue.put_nowait(tuple(((node_storage[start].sum, 0), node_storage[start].vertex)))

    while len(waiting_vertices) != 0:
        processing_vertex = node_queue.get()[1]  # item = ((priority number, priority_index), data).
        while processing_vertex in processed_vertices:
            processing_vertex = node_queue.get_nowait()[1]

        if isFinish(processing_vertex):
            return _createPath(processing_vertex, node_storage)

        _processVertex(processing_vertex, getDistance, getIncidenceList, getHeuristicCostEstimate,
                       processed_vertices, waiting_vertices, node_storage, node_queue)

    raise Exception("Path doesn't exist")


#############################-testing-#####################################
def _getRandomGraph(number_of_vertices):
    result = dict()
    for x in range(number_of_vertices):
        result[x] = sample(set(range(number_of_vertices)), randint(0, number_of_vertices // 10))
    return result


def _checkPath(start, finish, path, graph, error_text):
    path.insert(0, start)
    for x in range(len(path) - 1):
        if path[x + 1] not in graph[path[x]]:
            raise Exception(error_text)

    if path[-1] != finish:
        raise Exception(error_text)


def _testWithoutHeuristicCostEstimate():
    number_of_vertices = 100
    for test in range(1000):
        graph = _getRandomGraph(number_of_vertices)

        distance = bfs(0, graph)
        error_text = "Error on test: _testWithoutHeuristicCostEstimate"
        try:
            path = findWayByAStar(0, lambda x: x == number_of_vertices - 1, lambda x, y: 1, lambda x: graph[x],
                                  lambda x: 0)
        except:
            if distance[number_of_vertices - 1] != "Inf":
                raise Exception(error_text)
        else:
            if len(path) != distance[number_of_vertices - 1]:
                raise Exception(error_text)
            _checkPath(0, number_of_vertices - 1, path, graph, error_text)


def _testAStar():
    _testWithoutHeuristicCostEstimate()
    print("All ok")

if __name__ == "__main__":
    _testAStar()
