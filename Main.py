import pygame
from Grid import *
from SearchAlgorithms import *
from DrawFunctions import *

# NUM_SQUARES = 50
# start_x = 0
# start_y = 0
# finish_x = 49
# finish_y = 49
#
# # Unweighted example
# Graph = Grid(NUM_SQUARES, [start_y, start_x], [finish_y, finish_x], barrier_per=25)


NUM_SQUARES = 50
start_x = 0
start_y = 0
finish_x = 49
finish_y = 49
# Weighted example
Graph = Grid(NUM_SQUARES, [start_y, start_x], [finish_y, finish_x], barrier_per=50, weights=True, max_weight=4)

st = 0
noSol = False
if __name__ == "__main__":
    #GRID = Graph.grid

    WIDTH = 1000
    HEIGHT = 1000
    width_rect = WIDTH // NUM_SQUARES
    height_rect = HEIGHT // NUM_SQUARES
    running = True
    pygame.init()
    # set a width and height of the display window, making a window named win
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Grid")
    # white background
    win.fill([255, 255, 255])

    run_search = False
    search1 = search2 = search3 = search4 = search5 = False
    end = False
    while running:
        for event in pygame.event.get():
            # Closes the window when exiting
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                # Initializing variables, runs only once when you clik the button
                if not run_search:
                    if  WIDTH/2 - size_X/2 <=  mouse[0] <= WIDTH/2 + size_X/2 and 0 <= mouse[1] <= size_Y:
                        # Paramaters for Greedy BFS
                        openSet, Q_dist, end, path, closedSet, current = greedyBFS_paramaters(start_y, start_x)
                        search1 = True
                        run_search = True
                        # Erasing buttons
                        win.fill([255, 255, 255])
                    elif WIDTH/2 - size_X/2 <=  mouse[0] <= WIDTH/2 + size_X/2 and 2*size_Y <= mouse[1] <= 3*size_Y:
                        # Paramaters for A* search
                        openSet, closedSet, end, path, current = A_star_paramaters(start_y, start_x, Graph)
                        search2 = True
                        run_search = True
                        # Erasing buttons
                        win.fill([255, 255, 255])
                    elif WIDTH/2 - size_X/2 <=  mouse[0] <= WIDTH/2 + size_X/2 and 4*size_Y <= mouse[1] <= 5*size_Y:
                        # Paramaters for Dijsktra's algorithm
                        Q, Q_dist, closedSet, openSet, end, path, current = Dijkstra_paramaters(start_y, start_x, finish_y, finish_x, Graph)
                        search3 = True
                        run_search = True
                        # Erasing buttons
                        win.fill([255, 255, 255])
                    elif WIDTH/2 - size_X/2 <=  mouse[0] <= WIDTH/2 + size_X/2 and 6*size_Y <= mouse[1] <= 7*size_Y:
                        # Paramaters for Breadth-first search
                        Q, discovered, end, path, current = BFS_paramaters(start_y, start_x)
                        search4 = True
                        run_search = True
                        # Erasing buttons
                        win.fill([255, 255, 255])
                    elif WIDTH/2 - size_X/2 <=  mouse[0] <= WIDTH/2 + size_X/2 and 8*size_Y <= mouse[1] <= 9*size_Y:
                        # Paramaters for Depth-first search
                        S, S_parent, discovered, end, path, current = DFS_paramaters(start_y, start_x)
                        search5 = True
                        run_search = True
                        # Erasing buttons
                        win.fill([255, 255, 255])



        if run_search:
            if search1:
                # Greedy BFS
                openSet, Q_dist, end, path, closedSet, current = greedyBFS(openSet, Q_dist, end, path, closedSet, current, Graph, finish_y, finish_x)
            elif search2:
                # A* search
                openSet, closedSet, end, path, current = A_star(openSet, closedSet, end, path, current, Graph, finish_y, finish_x)
            elif search3:
                # Dijsktra's algorithm
                Q, Q_dist, closedSet, openSet, end, path, current = Dijkstra(Q, Q_dist, closedSet, openSet, end, path, current, Graph)
            elif search4:
                # Breadth-first search
                Q, discovered, end, path, current = BFS(Q, discovered, end, path, current, Graph)
            elif search5:
                # Depth-first search
                S, S_parent, discovered, end, path, current = DFS(S, S_parent, discovered, end, path, current, Graph)

            # Draws only when algorithms is working, stops at the end when finish node is found found
            if not end or Graph.weights==False:
                # BFS and DFS
                if search4 or search5:
                    draw_closed_set_BFS_DFS(win, Graph, discovered, finish_y, finish_x, NUM_SQUARES, width_rect, height_rect, current)
                # Dijkstra
                elif search3:
                    draw_open_closed_set_Dijsktra(win, Graph, closedSet, openSet, width_rect, height_rect, finish_y, finish_x, NUM_SQUARES)
                # A* or Greedy BFS
                else:
                    draw_closed_set(win, Graph, closedSet, finish_y, finish_x, NUM_SQUARES, width_rect, height_rect)
                    draw_open_set(win, Graph, openSet, width_rect, height_rect)

            # If there is no solution
            if len(path) == 0:
                noSol = True


            path_dist = 0 # for weighted map
            # Draw a yellow path for unweighted map
            if len(path) > 0 and Graph.weights == False:
                if st == len(path):
                    print("The distance of path:", len(path))
                st+=1
                for i in path:
                    draw_circle_alpha(win, (255, 255, 0, 255),
                                      (i.x * width_rect + width_rect / 2, i.y * width_rect + height_rect / 2),
                                      (height_rect / 2 - 1))

            # If weighted draw a line of path
            elif len(path) > 0 and Graph.weights == True:
                for i in path:
                    if not i.isStart:
                        path_dist += i.weight

                        #print(i.g)
                        r = height_rect / 2 - 1
                        pygame.draw.line(win, (255, 0, 0), (i.x * width_rect + r, i.y * height_rect + r),
                                         (i.parent[1] * width_rect + r, i.parent[0] * height_rect + r), width=3)

                if st == len(path):
                    print("The cost of the path: ", path_dist)
                    print("The distance of path: ", len(path))
                st+=1



        # Draw lines - grid
        # for i in range(NUM_SQUARES):
        #     pygame.draw.line(win, (0, 0, 0), (i * (WIDTH // NUM_SQUARES), 0), (i * (WIDTH // NUM_SQUARES), HEIGHT), width=1)
        #     pygame.draw.line(win, (0, 0, 0), (0, i * (HEIGHT // NUM_SQUARES)), (WIDTH, i * (HEIGHT // NUM_SQUARES)), width=1)

        # Random obstacles
        for i in range(NUM_SQUARES):
            for j in range(NUM_SQUARES):
                if Graph.grid[i][j].isBarrier:
                    if Graph.weights == False:
                        col = (50, 50, 50) # Gray barriers
                    else:
                        col = (128, 0, 128) # Purple barriers
                    pygame.draw.rect(win, col, (Graph.grid[i][j].x * width_rect + 1, Graph.grid[i][j].y * width_rect + 1,
                                                height_rect, width_rect))

        # Random weights for weighted map
        alpha = 50
        for i in range(NUM_SQUARES):
            for j in range(NUM_SQUARES):
                if Graph.grid[i][j].weight is not None:
                    w = Graph.grid[i][j].weight # Get a weight
                    k = 255/Graph.max_weight # koefficient, draw different weights between 0 and 255, for example: 4 different weights mean 4 different shades of grey
                    draw_rect_alpha(win, (255-w*k, 255-w*k, 255-w*k, alpha),
                                     (Graph.grid[i][j].x * width_rect + 1, Graph.grid[i][j].y * width_rect + 1,
                                      height_rect, width_rect))

        for i in range(NUM_SQUARES):
            for j in range(NUM_SQUARES):
                # Draw start node
                if Graph.grid[i][j].isStart:
                    pygame.draw.rect(win, (255, 0, 0),
                                     (Graph.grid[i][j].x * width_rect + 1, Graph.grid[i][j].y * width_rect + 1,
                                      height_rect, width_rect ))
                # Draw finish node
                elif Graph.grid[i][j].isFinish:
                    pygame.draw.rect(win, (0, 0, 255),
                                     (Graph.grid[i][j].x * width_rect + 1, Graph.grid[i][j].y * width_rect + 1, height_rect , width_rect ))

        # Before we start search algorithm
        if not run_search:
            # draw a buttons
            size_X, size_Y = draw_button(win, WIDTH, HEIGHT, (255, 0, 0), (0, 0, 0), but_number=0, title='Greedy BFS')
            draw_button(win, WIDTH, HEIGHT, (255, 0, 0), (0, 0, 0), but_number=1, title='A* Search', offSetX=10)
            draw_button(win, WIDTH, HEIGHT, (255, 0, 0), (0, 0, 0), but_number=2, title='Dijkstra', offSetX=30)

            draw_button(win, WIDTH, HEIGHT, (0, 255, 0), (0, 0, 0), but_number=3, title='BFS', offSetX=50)
            draw_button(win, WIDTH, HEIGHT, (0, 255, 0), (0, 0, 0), but_number=4, title='DFS', offSetX=50)
        # If there is no solution found
        if noSol:
            draw_button(win, WIDTH, HEIGHT, (255, 255, 255), (0, 0, 0), but_number=2, title='No solution found!', offSetX=0, font=24)

        pygame.display.update()
        #pygame.time.delay(100)
    # uninitialize all pygame modules
    pygame.quit()