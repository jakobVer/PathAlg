# DRAW FUNCTIONS
import pygame

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, color, center, radius, width=None):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)

    if width != None:
        pygame.draw.circle(shape_surf, color, (radius, radius), radius, width=width)
    else:
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)

    surface.blit(shape_surf, target_rect)

def draw_button(win, WIDTH, HEIGHT, col_rect, col_text, but_number, title, offSetX=0, font=35):
    size_X = WIDTH // 5
    size_Y = HEIGHT // 10
    pygame.draw.rect(win, col_rect, (WIDTH / 2 - size_X / 2, 2*but_number*size_Y, size_X, size_Y))


    smallfont = pygame.font.SysFont('Corbel', font)
    text = smallfont.render(title, True, col_text)
    win.blit(text, (WIDTH / 2 - size_X / 2 + 0.08 * size_X + offSetX, 0 + 0.75 * size_Y / 2 + 2*but_number*size_Y))
    if but_number == 0:
        return size_X, size_Y

def draw_closed_set(win, Graph, closedSet, finish_y, finish_x, NUM_SQUARES, width_rect, height_rect):
    # Draw closed set
    if len(closedSet) > 0:
        for i in closedSet:
            spot = Graph.getSpot(i)
            spot.h = spot.heuristic([finish_y, finish_x])
            # draw_rect_alpha(win, (190, 100, 190, 60), (spot.x*width_rect + 1 , spot.y*width_rect + 1 , height_rect-1, width_rect-1))
            if (spot.h != None):
                MAX_DIST = 2 * NUM_SQUARES - 1
                draw_circle_alpha(win, ((255 / MAX_DIST) * spot.h, 255 - (255 / MAX_DIST) * spot.h, 0, 50),
                                  (spot.x * width_rect + width_rect / 2, spot.y * width_rect + height_rect / 2),
                                  (height_rect / 2 - 1))

            if not spot.isStart:
                r = height_rect / 2 - 1
                pygame.draw.line(win, (0, 0, 0), (spot.x * width_rect + r, spot.y * height_rect + r),
                                 (spot.parent[1] * width_rect + r, spot.parent[0] * height_rect + r), width=2)

def draw_open_set(win, Graph, openSet, width_rect, height_rect):
    # Draw open set
    for i in openSet:
        spot = Graph.getSpot(i)
        # fill
        draw_circle_alpha(win, (255, 255, 255, 255),
                          (spot.x * width_rect + width_rect / 2, spot.y * width_rect + height_rect / 2),
                          (height_rect / 2 - 1))
        # stroke
        draw_circle_alpha(win, (0, 0, 255, 255),
                          (spot.x * width_rect + width_rect / 2, spot.y * width_rect + height_rect / 2),
                          (height_rect / 2 - 1), width=2)

def draw_open_closed_set_Dijsktra(win, Graph, closedSet, openSet, width_rect, height_rect, finish_y, finish_x, NUM_SQUARES):
    if len(closedSet) > 0:
        # Draw open set
        for i in openSet:
            spot = Graph.getSpot(i)
            # fill
            draw_circle_alpha(win, (255, 255, 255, 255),
                              (spot.x * width_rect + width_rect / 2, spot.y * width_rect + height_rect / 2),
                              (height_rect / 2 - 1))
            # stroke
            draw_circle_alpha(win, (0, 0, 255, 255),
                              (spot.x * width_rect + width_rect / 2, spot.y * width_rect + height_rect / 2),
                              (height_rect / 2 - 1), width=2)

        for i in closedSet:
            spot = Graph.getSpot(i)
            spot.h = spot.heuristic([finish_y, finish_x])
            if (spot.h != None):
                MAX_DIST = 2 * NUM_SQUARES - 1
                draw_circle_alpha(win, ((255 / MAX_DIST) * spot.h, 255 - (255 / MAX_DIST) * spot.h, 0, 255),
                                  (spot.x * width_rect + width_rect / 2, spot.y * width_rect + height_rect / 2),
                                  (height_rect / 2 - 1))
            if not spot.isStart:
                r = height_rect / 2 - 1
                pygame.draw.line(win, (0, 0, 0), (spot.x * width_rect + r, spot.y * height_rect + r),
                                 (spot.parent[1] * width_rect + r, spot.parent[0] * height_rect + r), width=2)

def draw_closed_set_BFS_DFS(win, Graph, discovered, finish_y, finish_x, NUM_SQUARES, width_rect, height_rect, current):
    # Draw closed set
    if len(discovered) > 0:
        for i in discovered:
            spot = Graph.getSpot(i)
            spot.h = spot.heuristic([finish_y, finish_x])
            if (spot.h != None):
                MAX_DIST = 2 * NUM_SQUARES - 1
                if spot.h > MAX_DIST:
                    MAX_DIST = spot.h
                # closer to finish: green
                # further from finish: red
                # 50 is value for transparency
                draw_circle_alpha(win, ((255 / MAX_DIST) * spot.h, 255 - (255 / MAX_DIST) * spot.h, 0, 50),
                                  (spot.x * width_rect + width_rect / 2, spot.y * width_rect + height_rect / 2),
                                  (height_rect / 2 - 1))
            # Drawing connections between nodes
            if not spot.isStart:
                r = height_rect / 2 - 1
                pygame.draw.line(win, (0, 0, 0), (spot.x * width_rect + r, spot.y * height_rect + r),
                                 (spot.parent[1] * width_rect + r, spot.parent[0] * height_rect + r), width=2)
    # Draw open set - only current node
    spot = Graph.getSpot(current)
    # fill
    draw_circle_alpha(win, (0, 0, 255, 255),
                      (spot.x * width_rect + width_rect / 2,
                       spot.y * width_rect + height_rect / 2),
                      (height_rect / 2 - 1))