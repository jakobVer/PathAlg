# Important!!!
# Functions are written without while loop because they are inserted in while loop of pygame. If displaying your algorithm performance is not necessary,
# you can combine function with paramaters and serach algorithms function in one function, don't forget to add while loop instead of first if statement


def priorityQueue(Q, Q_dist):
    """

    :param Q: Node
    :param Q_dist: Distance of node to the finish
    :return: Node with the shortest distance from Q
    """
    current_idx = Q_dist.index(min(Q_dist))
    current = Q[current_idx]
    Q.remove(current)
    Q_dist.pop(current_idx)

    return current, Q, Q_dist

def BFS_paramaters(start_y, start_x):
    # Paramaters for Breadth-first search
    Q = []
    discovered = [[start_y, start_x]]
    Q.append([start_y, start_x])
    end = False
    path = []
    current = []
    return Q, discovered, end, path, current

def BFS(Q, discovered, end, path, current, Graph):
    if not end and len(Q) > 0:
        current = Q.pop(0)
        for i in Graph.getSpot(current).edges:
            spot = Graph.getSpot(i)
            if i not in discovered and not spot.isBarrier:
                discovered.append(i)
                Q.append(i)
                spot.parent = current
                if spot.isFinish:
                    end = True
                    # place the finish node in the path list
                    path.append(spot)
                    current = [spot.y, spot.x]
                    break
   # Reconstruct the path
    path, current = reconstructPath(Graph, current, path, end)
    return Q, discovered, end, path, current

def DFS_paramaters(start_y, start_x):
    # Paramaters for Depth-first search
    S = []
    discovered = []
    S.append([start_y, start_x])
    end = False
    S_parent = [[]]
    path = []
    current = []
    return S, S_parent, discovered, end, path, current

def DFS(S, S_parent, discovered, end, path, current, Graph):
    if not end and len(S) > 0:
        vp = S_parent.pop()
        current = S.pop()
        if current not in discovered and not Graph.getSpot(current).isBarrier:
            # set a parent node
            Graph.getSpot(current).parent = vp
            discovered.append(current)
            for i in Graph.getSpot(current).edges:
                S_parent.append(current)
                S.append(i)
                if Graph.getSpot(current).isFinish:
                    end = True
                    path.append(Graph.getSpot(current))
    # Reconstruct the path
    path, current = reconstructPath(Graph, current, path, end)
    return S, S_parent, discovered, end, path, current

def A_star_paramaters(start_y, start_x, Graph):
    openSet = []
    closedSet = []
    openSet.append([start_y, start_x])
    Graph.getSpot([start_y, start_x]).g = 0
    end = False
    path = []
    current = []
    return openSet, closedSet, end, path, current

def A_star(openSet, closedSet, end, path, current, Graph, finish_y, finish_x):
    if not end and len(openSet) > 0:
        current = openSet[0]
        for i in openSet:
            if len(openSet) > 1 and Graph.getSpot(current).f > Graph.getSpot(i).f:
                current = i
        if Graph.getSpot(current).isFinish:
            end = True
            # place the finish node in the path list
            path.append(Graph.getSpot(current))
        else:
            openSet.remove(current)
            closedSet.append(current)
            for i in Graph.getSpot(current).edges:
                # Unweighted/constant weights
                if Graph.weights == False:
                    neighbor = Graph.getSpot(i)
                    if not neighbor.isBarrier:
                        tentative_gScore = Graph.getSpot(current).g + 1
                        if tentative_gScore < neighbor.g:
                            # This path to neighbor is better than any previous one. Record it!
                            neighbor.parent = current
                            neighbor.g = tentative_gScore
                            neighbor.f = neighbor.g + neighbor.heuristic([finish_y, finish_x])
                            if i not in openSet:
                                openSet.append(i)
                # Weighted weights
                elif Graph.weights == True:
                    neighbor = Graph.getSpot(i)
                    if not neighbor.isBarrier:
                        tentative_gScore = Graph.getSpot(current).g + neighbor.weight
                        if tentative_gScore < neighbor.g:
                            # This path to neighbor is better than any previous one. Record it!
                            neighbor.parent = current
                            neighbor.g = tentative_gScore
                            neighbor.f = neighbor.g + neighbor.heuristic([finish_y, finish_x])
                            if i not in openSet:
                                openSet.append(i)
    # Reconstruct the path
    path, current = reconstructPath(Graph, current, path, end)
    return openSet, closedSet, end, path, current

def Dijkstra_paramaters(start_y, start_x, finish_y, finish_x, Graph):
    # Paramaters for Dijsktra's algorithm
    Graph.getSpot([start_y, start_x]).dist = 0
    Graph.getSpot([start_y, start_x]).h = Graph.getSpot([start_y, start_x]).heuristic([finish_y, finish_x])
    Q = []
    Q_dist = []
    for i in Graph.grid:
        for j in i:
            if not j.isBarrier:
                Q.append([j.y, j.x])
                Q_dist.append(j.dist)

    closedSet = []
    openSet = []
    end = False
    path = []
    current = []
    return Q, Q_dist, closedSet, openSet, end, path, current


def Dijkstra(Q, Q_dist, closedSet, openSet, end, path, current, Graph):
    # Dijkstra's algorithm
    if not end and len(Q) > 0:
        current, Q, Q_dist = priorityQueue(Q, Q_dist)
        closedSet.append(current)
        if Graph.getSpot(current).isFinish:
            end = True
            path.append(Graph.getSpot(current))
        else:
            for i in Graph.getSpot(current).edges:
                if i not in closedSet and not Graph.getSpot(i).isBarrier:
                    if(Graph.weights==False):
                        alt = Graph.getSpot(current).dist + 1  # 1 is length to the neighbor, needed to be changed when different distances/weights
                    elif(Graph.weights==True):
                        alt = Graph.getSpot(current).dist + Graph.getSpot(i).weight
                    openSet.append(i)
                    if alt < Graph.getSpot(i).dist:
                        Q_dist[Q.index(i)] = alt
                        Graph.getSpot(i).dist = alt
                        Graph.getSpot(i).parent = current
    # Reconstruct the path
    path, current = reconstructPath(Graph, current, path, end)
    return Q, Q_dist, closedSet, openSet, end, path, current

def greedyBFS_paramaters(start_y, start_x):
    # Paramaters for Greedy BFS
    Q = []
    Q_dist = []
    current = []
    discovered = [[start_y, start_x]]
    Q.append([start_y, start_x])
    Q_dist.append(0)
    end = False
    path = []
    return Q, Q_dist, end, path, discovered, current

def greedyBFS(Q, Q_dist, end, path, discovered, current, Graph, finish_y, finish_x):
    if not end and len(Q) > 0:
        current, Q, Q_dist = priorityQueue(Q, Q_dist)
        if Graph.getSpot(current).isFinish:
            end = True
            # place the finish node in the path list
            path.append(Graph.getSpot(current))
        else:
            for i in Graph.getSpot(current).edges:
                spot = Graph.getSpot(i)
                if i not in discovered and not spot.isBarrier:
                    discovered.append(i)
                    spot.f = spot.heuristic([finish_y, finish_x])
                    Q.append(i)
                    Q_dist.append(spot.f)
                    spot.parent = current
    path, current = reconstructPath(Graph, current, path, end)
    return Q, Q_dist, end, path, discovered, current

def reconstructPath(Graph, current, path, end):
    # Reconstruct the path
    if not Graph.getSpot(current).isStart and end:
        current = Graph.getSpot(current).parent
        path.append(Graph.getSpot(current))
    return path, current