import pygame
import time
import collections

colour = (100, 100, 100)
colour2 = (0,175,0)
wall = (205,100,0) # COlour of the wall
startColour = (200,0,0)
endColour = (0,200,0)
explored = (255,255,0)
final_path_color = (255,255,0)
x = 0
y = 0
w = 30 # width of one square/cell
size = int(input("What siZe do u want the maZe to be???"))
while size < 1 or size > 30:
    print("INvalid size: Enter a INTEGER value between 1 and 30!")
    size = int(input("What siZe do u want the maZe to be???"))

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Maze...")
screen = pygame.display.set_mode(((size+2)*30,(size+2)*30))
screen.fill(colour)
grid = []
queue = collections.deque([(1,1)])
visited = {(1,1),(size,size)}
graph = {} # This is needed for the bfs. We need it for an adjancency list
tracker = {(1,1): (1,1)}
final_path = set()
path_filled = False

def maze(x,y,w): # Drawing the maze
    for i in range (0,size): # i represents the x-axis or the rows
        x = 30
        y = y + 30
        for j in range (0,size):
            pygame.draw.line(screen, colour2, [x,y], [x + w, y], 2) #<----- This entire block creates each cell
            pygame.draw.line(screen, colour2, [x + w, y], [x + w, y + w], 2)
            pygame.draw.line(screen, colour2, [x + w, y + w], [x, y + w], 2)
            pygame.draw.line(screen, colour2, [x, y + w], [x, y], 2)# ---->
            grid.append((x,y))
            x = x + 30
    pygame.draw.rect(screen, startColour, [32,32,28,28]) # Creating the starting cell 
    pygame.draw.rect(screen, endColour, [size*30 + 2,size*30 + 2, 28, 28]) # Creating the ending cell

maze(x,y,w)

# Making a graph
for r in range(1,size+1):
    for c in range(1,size+1):
        if (c,r) == (0,0) or (c,r) ==(size,size): graph[(c,r)] = True # False means already clicked
        else: graph[(c,r)] = False # True means not clicked

startBFS = False
running = True
clock = pygame.time.Clock()

while running:
    # BFS in Action
    if startBFS and queue:
        # Getting the node
        node = queue.popleft()
        visited.add(node)

        xpos = node[0]
        ypos = node[1]
        # Changing its colour
        pygame.draw.rect(screen, (45,23,190), [xpos*30+2, ypos*30+2, 28, 28])
        
        if not node == (size,size):
            # Getting the child nodes of:

            left = (node[0]-1,node[1])
            right = (node[0]+1,node[1])
            up = (node[0],node[1]-1)
            down = (node[0],node[1]+1)

            if not(left[0] < 1 or left[0] > size):
                if left not in visited and not graph[left]:
                    if left not in queue:
                        queue.append(left)
                        tracker[left] = node #graph[childnode] = parentnode

            if not (right[0] < 1 or right[0] > size):
                if right not in visited and not graph[right]:
                    if right not in queue:
                        queue.append(right)
                        tracker[right] = node #graph[childnode] = parentnode
                        
            if not (up[1] < 1 or up[1] > size):
                if up not in visited and not graph[up]:
                    if up not in queue:
                        queue.append(up)
                        tracker[up] = node #graph[childnode] = parentnode

            if not (down[1] < 1 or down[1] > size):
                if down not in visited and not graph[down]:
                    if down not in queue:
                        queue.append(down)
                        tracker[down] = node#graph[childnode] = parentnode
                        if down == (size,size):
                            print("jpsd")
        else:
            startBFS = False
            
    elif not bool(queue):
        # Showing shortest path
        node = list(tracker.keys())[-1]
        
        if path_filled == False:
            while True:
                final_path.add(node)
                node = tracker[node]

                if node == (1,1):
                    final_path.add(node)
                    path_filled = True
                    break

        for n in final_path:
            xpos = n[0]
            ypos = n[1]
            pygame.draw.rect(screen, final_path_color, [xpos*30+2, ypos*30+2, 28, 28])
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN: # Needed to fill in "holes/cells" in the grid
            pos = pygame.mouse.get_pos()
            xpos = pos[0]//30
            ypos = pos[1]//30
            node = (xpos, ypos)
            print(node)
            
            if xpos > 0 and xpos < size+1 and ypos > 0 and ypos < size+1: #This is when you are in the grid space
                if not graph[node]:
                    pygame.draw.rect(screen, startColour, [xpos*30+2, ypos*30+2, 28, 28])
                    print("Hello world",(xpos, ypos))
                    graph[node] = not graph[node]

                    # Entering the nodes into the visted
                    visited.add(node)
                else:
                    pygame.draw.rect(screen, colour, [xpos*30+2, ypos*30+2, 28, 28])
                    print("Hello world",(xpos, ypos))
                    graph[node] = not graph[node]
                    print(graph[node])

                    # Removing the nodes into the visted
                    visited.remove(node)
            
            elif xpos > 0 and xpos < size+1 and ypos > 0 and ypos < size+1: #Same here but if you touch the wall
                if not graph[node]:
                    pygame.draw.rect(screen, startColour, [xpos*30+2, ypos*30+2, 28, 28])
                    print("Hello world",(xpos, ypos))
                    graph[node] = not graph[node]

                    # Entering the nodes into the visted
                    visited.add(node)
                else:
                    pygame.draw.rect(screen, colour, [xpos*30+2, ypos*30+2, 28, 28])
                    print("Hello world",(xpos, ypos))
                    graph[node] = not graph[node]

                    # Removing the nodes into the visted
                    visited.remove(node)
            else:
                print("U clicked OUTside the maze OR on the maze # 'kratka' #!!!") #Outside the grid
		          #Python (Proton) 1.5SE TRIPLE VALVEs NPCs
                #"u DTM" - DTM - Doing Too Much!!!
                #they're doing a Mr GUNN
                #FOCUS FOCUSSSSSS
                #A* project INCOMING (JK)
        
        elif event.type==pygame.KEYDOWN: # I need this to run the bfs when you have clicked finished colouring your desired grid. It used the Enter button
            if event.key==pygame.K_UP:
                    pos = pygame.mouse.get_pos()
                    # Alright, I understand every thing now, it is actually well designed. Thanks for the simplicity and readablility
                    # print(graph)
                    startBFS = True
                    print(startBFS)
                    node = (1,1) # Starting node
                    queue.append(node)

    clock.tick(5000)
    pygame.display.update()
