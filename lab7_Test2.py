# -*- coding: utf-8 -*-
"""
@author: Joey Roe
Date: 04/30/2019
CS 2302 Data Structures
Professor: Fuentes
TA's: Anindita Nath, Maliheh Zargaran
Assignment: Lab 7
Purpose: The purpose of this lab was to practice graphs, making adjacency lists.
We also used depth first search and breadth first search to find a path to the 
desired destination, the top right corner.
"""

import matplotlib.pyplot as plt
import numpy as np
import random

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
    
    
def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])


def findCompressed(S, i):
    if S[i] < 0:
        return i
    root = findCompressed(S, S[i])   #the compressed version of find
    S[i] = root
    return root


def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j) 
    if ri!=rj: # Do nothing if i and j belong to the same set 
        S[rj] = ri  # Make j's root point to i's root
    
    
def union2(S, i, j):
    ri = findCompressed(S, i)
    rj = findCompressed(S, j)       #the compressed version of union
    if ri != rj:
        S[rj] = ri
      

def numOfSets(S):
    sets = 0
    for i in range(len(S)):
        if S[i] < 0:
            sets += 1
    return sets


def inSameSet(S, a, b):
    if find(S, a) == find(S, b):
        return True
    else:
        return False


def draw_maze(walls,maze_rows,maze_cols, s, cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums == True and s == []:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    
            
    if cell_nums == True and s != []:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r* maze_cols
                if cell in s:                                 #this is how I made the *'s
                    ax.text((c+.5), (r+.5), '*', size = 10,
                            ha="center", va = "center")
    ax.axis('off') 
    ax.set_aspect(1.0)



def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w



#removes a given number of walls 
def wallRemover(wallList, numRemoved, disjointSet):
    
    if numRemoved > len(wallList):#doesn't do anything if the number of walls is greater than the length of the list
        
        return wallList
    
    removedWalls = []
    
    while len(removedWalls) != numRemoved:
                                             #this is where I get the indices that I'm going to remove
        randomIndex = random.randint(0, len(wallList) - 1)
        
        if randomIndex not in removedWalls:   #this is so there won't be any repeated inices
            removedWalls.append(randomIndex)
            
    a = sorted(removedWalls)
    
    for i in range(len(removedWalls)):
        wallList.pop(a[len(a) - 1])  #wallList and a had to be popped so there wouldn't be an out of bounds error
        a.pop()
   
    return wallList
    
          

#prints out if there's a path or not based on the number of walls that 
#were removed
def isThereAPath(wallsRemoved, maze_rows, maze_cols):
    
    if wallsRemoved < (maze_rows * maze_cols) - 1:
        print('A path from source to destination is not guaranteed to exist')


    if wallsRemoved == (maze_rows * maze_cols) - 1:
        print('There is a unique path from source to destination')
    
    
    if wallsRemoved > (maze_rows * maze_cols) - 1:
        print('There is at least one path from source to destination')



def adjacencyListBuilder(originalWalls, modifiedWalls, rows, cols):
    
    numOfCells = rows * cols
    if len(originalWalls) == len(modifiedWalls):
        return [[] for i in range(numOfCells)]  
    
    adj_list = [[] for i in range(numOfCells)]
    wallsRemoved = []
    
    for i in range(len(originalWalls)):
        if originalWalls[i] not in modifiedWalls: #check to see which walls were removed
            wallsRemoved.append(originalWalls[i])  #make a list of all the walls removed
       
    """
    This is where I use the list of all of the walls removed to get the propper
    indices for the adj_list, then I append the other part of the wall to the 
    adj_list. Example, wall [1, 0], 1 would be the an index for the adj_list
    then I would append 0 to adj_list[1] and vice versa.
    """    
    for i in range(len(wallsRemoved)):
        adj_list[wallsRemoved[i][0]].append(wallsRemoved[i][1])#use the walls removed as indices for the adj_list
        adj_list[wallsRemoved[i][1]].append(wallsRemoved[i][0])
            
    return adj_list
            


def breadthFirstSearch(G, startingVertex, end):
    """
    I used a queue to store all of the neighbors of a node. I used a
    normal list to represent a queue by poping (0).  The popped items 
    get put in the visited list.
    """
    visited = []
    Q = [startingVertex]
    
    while Q != []:
        node = Q.pop(0) #acts like a queue
        
        #adds node to the visited list
        if node not in visited:
            visited.append(node)
            
            if node == end:
                return visited
            
            neighbors = G[node]
            
            #adds neighbors to the queue
            for i in neighbors:
                Q.append(i)
                
    return visited



def depthFirstSearch(G, startingVertex, end):
    """
    I used a stack to store all of the neighbors of a node
    when it a node was popped from the stack it'd go into the 
    visited list
    """
    visited = []
    stack = [startingVertex]
    
    while stack != []:
        current = stack.pop()
        for i in G[current]:   #i are the neighbors
            
            if i not in visited:
                
                stack.append(i)
                
        visited.append(current)
        if current == end:   #stops once it reaches its destination
            return visited
        
    return visited





#Main
#Program should disply n, the number of cells, and ask the user for m, the
#Number of walls to remove

plt.close("all") 
maze_rows = 5
maze_cols = 5

walls = wall_list(maze_rows,maze_cols)
wallsCopy = wall_list(maze_rows, maze_cols)  #a copy to store orignail wall list
disjointSet = DisjointSetForest(maze_rows * maze_cols)


#print()
#print('walls before removal ', walls)
#print(len(walls))
#print()


print('number of cells ', maze_rows * maze_cols)
m = int(input('enter the number of walls you wanna remove: '))

isThereAPath(m, maze_rows, maze_cols)

print()
newWalls = wallRemover(walls, m, disjointSet)
#print('walls after removal: ', newWalls)
#print(len(newWalls))

draw_maze(newWalls, maze_rows, maze_cols, [], cell_nums = True)
draw_maze(newWalls, maze_rows, maze_cols, [], cell_nums = False)


adj_list = adjacencyListBuilder(wallsCopy, newWalls, maze_rows, maze_cols)
print('adjacency list: ', adj_list)

print()
bfs = breadthFirstSearch(adj_list, 0, len(adj_list) - 1)
print('breadth first search: ', bfs)

print()
dfs = depthFirstSearch(adj_list, 0, len(adj_list) - 1)
print('depth first search: ', dfs)
print()

print('The third print out is depth first search, and fourth is breadth first search')
print()
draw_maze(newWalls, maze_rows, maze_cols, dfs, cell_nums = True)
draw_maze(newWalls, maze_rows, maze_cols, bfs, cell_nums = True)
