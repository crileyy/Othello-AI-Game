#!/usr/local/bin/python3
import pygame

#This sets up all the colors for the board
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (0, 51, 0)
GREEN = (0, 153, 0)
RED = (202,0,42)

RADIUS = 17
WIDTH = 36
HEIGHT = 36

con = 0 
flashred = False
pygame.font.init()
font = pygame.font.SysFont('Cambria', 20,True,True)
text2 = font.render("Not Possible", True, WHITE)
 
# This sets the margin between each cell
MARGIN = 6
 
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell
 
# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [(MARGIN + WIDTH) * 8 + MARGIN,((MARGIN + HEIGHT) * 8 + MARGIN)+75]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#First grid positions set
grid[4][3]=-1
grid[3][4]=-1
grid[4][4]=1
grid[3][3]=1


#Setting up variables for whose turn it is 
ltb = 1


#This has all the possible row and column changes for the squares around an origin
g_list = [([-1,-1]),([-1,0]),([-1,1]),([0,-1]),([0,1]),([1,-1]),([1,0]),([1,1])]

#An empty list to help find if there is a possible move
pm_list =[]

	
#Programs

	#flips valid squares by setting grid to current player color
def flip(g_item,row,column):
	if grid[(row+g_list[g_item][0])][(column+g_list[g_item][1])]==ltb:
		return ('done')
	else:
		grid[(row+g_list[g_item][0])][(column+g_list[g_item][1])]=ltb
		return (flip(g_item,row+g_list[g_item][0],column+g_list[g_item][1]))
	
	#goes through the possible moves to see if there are any valid flips
def which_flip(row,column):
	global grid
	global pm_list
	global ltb
	for g_item in range (0,8):
		if pm_list[g_item] == True:
			flip(g_item,row,column)

	#checks a block next to center to see if it's valid. Reports True or False
def vm (r,c,x,y,color,n):
	if (r+x) == -1 or (r+x) == 8 or (y+c) ==-1 or (c+y) == 8:
		return (False)
	elif grid [r+x][c+y] == 0:
		return (False)
	elif n == 0 and grid [r+x][c+y] == (color):
		return False
	elif grid [r+x][c+y] == -(color):
		return vm((r+x),(c+y),(x),(y),(color),(5))
	elif grid [r+x][c+y] == (color):
		return True

	#Uses vm above to check all surrounding blocks. Reports list of True or False from above		
def fullvm (r,c,color):
	for i in g_list:
		pm_list.append(vm(r,c,i[0],i[1],color,0))
		
	#goes through each square, and counts the blocks that are equal to the input (i=color) 
def count(ltb):
	o = 0
	for x in range (0,8):
		for y in range (0,8):
			if grid[x][y]==ltb:
				o = o+1
	return (o)

	#displays the current score

def disp_score():
	screen.fill(GREEN)
	screen.blit((font.render(("White:" + str(count(-1))), True, WHITE)), [10,350])
	screen.blit((font.render("Black:" + str(count(1)), True, WHITE)), [10, 375])
	
game = True
	#counts white and black and reports number of white and black and who won
def gameover():
	global game
	game = False
	done = True
	if (count(-1)) == (count(1)):
		screen.fill(GREY)
		screen.blit(font.render('it is a tie!', False, RED), [100,360])
	elif count(-1) > count(1):
		screen.fill(WHITE)
		screen.blit(font.render(str(count(-1)) + ' White. ' + str(count(1)) + ' Black. White Wins!', False, RED), [50,360])
	else:
		(print ('in else'))
		screen.fill(BLACK)
		screen.blit(font.render(str(count(-1))+ ' White. ' + str(count(1)) + ' Black. Black Wins!', False, RED), [50,360])
	done = True

#looks at current player to make sure there is a possible move. If there is no move, it
	#looks at the other player to see if they have a move.		

def posmove():
	global pm_list
	global ltb
	for x in range (0,8):
		for y in range (0,8):
			if grid[x][y]==0:
				fullvm(x,y,ltb)
				if True in pm_list:
					pm_list=[]
					return True
				else:
					pm_list=[]	
	for x in range (0,8):
		for y in range (0,8):
			if grid[x][y]==0:
				fullvm(x,y,-(ltb))
				if True in pm_list:
					pm_list=[]
					font.render(str(ltb) + 'forfit turn.' + (str(-ltb)) + 'your turn', True, WHITE)
					ltb = -ltb
					return True
				else:
					pm_list=[]
	gameover()
		
def set_status(x,y,color):
	global flashred
	global notposs
	global pm_list
	global ltb
	if grid[x][y]== -1 or grid[x][y]== 1:
		flashred=True
		return (False)
	else:
		fullvm(x,y,color)
		if True in pm_list:
			which_flip(x,y)
			disp_score()
			pm_list = []
			grid[x][y]=color
			ltb=-(ltb)
			posmove()
			return True
		else:
			pm_list=[]
			flashred=True
			screen.blit(text2, [100,360])
			return False

# -------- Main Program Loop -----------

while done == False:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to zero
            set_status(row,column,ltb)
            #print("Click ", pos, "Grid coordinates: ", row, column)
            
    
    # Draw the grid
    
    if flashred and con < 30:
    	screen.fill(RED)
    	screen.blit(text2,[100,360])
    	con = con+1
    elif game == True:
    	screen.fill(GREEN)
    	con = 0
    	flashred = False
    	disp_score()
    	
    #screen.fill(GREEN)
    # Things changed here
    # Draw the grid
    for row in range(8):
        for column in range(8):
            for iteration in range (0, 12): #C reates increasingly smaller, increasingly lighter green rectangles
                pygame.draw.rect(screen,
                                ((60 - 5 * iteration), (153 - 6 * iteration), (48 - 4 * iteration)),
                                [(MARGIN + WIDTH) * column + (MARGIN + iteration)/2,
                                (MARGIN + HEIGHT) * row + (MARGIN + iteration)/2,
                                WIDTH + MARGIN - iteration,
                                HEIGHT + MARGIN - iteration])
            if not grid[row][column] == 0: # Circle takes inputs (background, color, [X center, Y center], radius)
                for iteration in range (0, 12): #C reates increasingly smaller, increasingly darker/lighter black/white tiles
                    color = 85 * (1 - grid[row][column]) + 7 * iteration #If grid[row][column] is positive, color is some shade of black
                    pygame.draw.circle(screen,
                                      (color, color, color),
                                      [int((MARGIN + WIDTH) * (column + 0.5) + MARGIN/2 - iteration/8), # X coordinate of center. Iteration/8 gives it a 3D effect
                                      int((MARGIN + HEIGHT) * (row + 0.5) + MARGIN/2 - iteration/4)], # Y coordinate of center. Iteration/4 is cosmetic
                                      RADIUS-iteration)         
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()