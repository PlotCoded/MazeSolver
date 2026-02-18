"""This file will generate a maze, but this maze is a bit differenct 
from a normal maze, this maze is actually reprsented by circles
instead of squares"""

import pygame, collections,math

# Creating a display screen
width = 1080
height = 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('BFS')

# Running the program
running = True

# fps
clock = pygame.time.Clock()

# Constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RADIUS = 5
SEPERATION = 60 #It is extremely important for this to be a multiple of 10
STARTINGNODE = (30,30)# It is extrmely important for this to be a multiple of 10, both the x and y coord
GREEN = (0,255,0)
FINALPATHCOLOR = (0,255,0)

# The algorithm to use
algo = "BFS"

# Generating the nodes for a dfs or bfs: Unweighted graph
nodes = set()
for w in range(STARTINGNODE[0],width,SEPERATION):
    for h in range(STARTINGNODE[1],height,SEPERATION):
        nodes.add((w,h))

# Getting End node
ENDNODE = (w,h)

# Generating the graph for the grid/maze
graph = {}
visited = set()
tracker = {STARTINGNODE: STARTINGNODE}
previous_node = STARTINGNODE
queue = collections.deque([STARTINGNODE])
final_path = []
path_filled = False
index = 0
drawing_nodes = []
StartBFS = False

def getChildNodes(node,visited):
    # Getting child nodes
    child_nodes = set()

    left_node = (node[0]-SEPERATION, node[1])
    right_node = (node[0]+SEPERATION, node[1])
    up_node = (node[0], node[1]-SEPERATION)
    down_node = (node[0], node[1]+SEPERATION)

    if left_node in nodes and left_node not in visited:
        child_nodes.add(left_node)
    if right_node in nodes and right_node not in visited:
        child_nodes.add(right_node)
    if up_node in nodes and up_node not in visited:
        child_nodes.add(up_node)
    if down_node in nodes and down_node not in visited:
        child_nodes.add(down_node)

    return sorted(child_nodes)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN: # Needed to fill in "holes/cells" in the grid
            pos = pygame.mouse.get_pos()

            x_pos_lower,x_pos_higher = math.floor(pos[0]/10)*10, math.ceil(pos[0]/10)*10
            y_pos_lower,y_pos_higher = math.floor(pos[1]/10)*10, math.ceil(pos[1]/10)*10
            
            for node in [(x_pos_lower,y_pos_lower),(x_pos_lower,y_pos_higher),(x_pos_higher,y_pos_lower),(x_pos_higher,y_pos_higher)]:
                if node in nodes:
                    if node not in visited:
                        visited.add(node)
                    else:
                        visited.remove(node)
                    break
        elif event.type==pygame.KEYDOWN: # I need this to run the bfs when you have clicked finished colouring your desired grid. It used the Enter button
            if event.key==pygame.K_UP:
                if len(queue) == 1:
                    StartBFS = True
                else:
                    StartBFS = False
                    visited = set()
                    tracker = {STARTINGNODE: STARTINGNODE}
                    previous_node = STARTINGNODE
                    queue = collections.deque([STARTINGNODE])
                    final_path = []
                    path_filled = False
                    index = 0
                    drawing_nodes = []
                    GREEN = (0,255,0)

    screen.fill(BLACK)

    # Drawing the grid/maze and performing a bfs
    if algo in {"BFS","DFS"}:
        for centre in nodes: # centre is also know as the node
            if centre not in visited:
                pygame.draw.circle(screen,WHITE, centre,RADIUS,RADIUS)
            else:
                pygame.draw.circle(screen,GREEN, centre,RADIUS,RADIUS)

    # Drawing connections from the parent nodes to the child nodes 
    if queue and StartBFS:
        current_node = queue.popleft()
        subnodes = getChildNodes(current_node,visited)

        for n in subnodes:
            pygame.draw.line(screen, WHITE, current_node, n)
            if n not in queue:
                queue.append(n)

            tracker[n] = current_node #graph[childnode] = parentnode

        visited.add(current_node)

    else:
        if ENDNODE in tracker.keys():
            current_node = ENDNODE
        if StartBFS:
            if path_filled == False:
                while True:
                    final_path.append(current_node)
                    current_node = tracker[current_node]

                    if current_node == STARTINGNODE:
                        final_path.append(current_node)
                        path_filled = True
                        break

            if index < len(final_path) -1:
                GREEN = WHITE
                pygame.draw.circle(screen,FINALPATHCOLOR,final_path[index],RADIUS,RADIUS)
                pygame.draw.line(screen, WHITE, final_path[index], final_path[index+1],)
                drawing_nodes.append(final_path[index])
                index+=1

            for i,n in enumerate(drawing_nodes):
                pygame.draw.circle(screen,FINALPATHCOLOR,final_path[i],RADIUS,RADIUS)
                pygame.draw.line(screen, WHITE, final_path[i], final_path[i+1],)

            pygame.draw.circle(screen,FINALPATHCOLOR,STARTINGNODE,RADIUS,RADIUS)

    # Setting fps
    clock.tick(300)

    pygame.display.update()