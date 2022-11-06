#Maze Solver using A*

from simpleai.search import astar, SearchProblem
import math

#SearchProblem:
#simpleai provides a SearchProblem class, that must be inherited
#to override methods like action, result, is_goal, cost and heuristic.
#These methods define the specifics of a problem (help the turtle
#reach the egg).
#Once defined a suitable algorithm (like A*) can be applied
#to find a solution to the problem.


class MazeSolver(SearchProblem) :
    def __init__(self, source):
        #1) load the board
        self.board = []
        #open a file for reading in text mode
        #if the file doesnt exist, FileNotFoundError gets raised
        fh = open(source, 'r')
        #for each line of the file
        for aline in fh:
            #remove the preceeding and trailing spaces, tabs and new line
            aline = aline.strip()
            self.board.append([achar for achar in aline if achar])
        #release the resource
        fh.close()

        #2) find the position of the turtle (x) and of the egg(o)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'x': #turtle
                    self.initial = (i,j)
                elif self.board[i][j] == 'o': #egg
                    self.goal = (i,j)
        #print(self.initial)
        #print(self.goal)

        #3) define the costs and possible movements of the turtle
        cost_regular = 1
        cost_diagonal = 1.7
        self.COSTS = {
            'up': cost_regular,
            'down': cost_regular,
            'left': cost_regular,
            'right': cost_regular,
            'up left': cost_diagonal,
            'up right': cost_diagonal,
            'down left': cost_diagonal,
            'down right': cost_diagonal
        }

        #invoke parent class init
        super(MazeSolver,self).__init__(initial_state=self.initial)

    #This method receices a state and returns a boolean indicating
    #whether the state is the goal_state or not.
    def is_goal(self, state):
        return self.goal == state

    #helper method
    def displayBoard(self):
        print()
        for rows in self.board:
            print()
            for cols in rows:
                print(cols, end='')
        print()

    #This method receives a state and must return a list of actions
    #that can be taken (performed) ahead.
    def actions(self, state):
        possible_moves = []

        for amove in self.COSTS.keys():
            newx,newy = self.result(state, amove)
            if self.board[newx][newy] != '#':
                possible_moves.append(amove)

        return possible_moves

    #This method receives a state and must return the new state
    #that results by application of action.
    def result(self, state, action):
        #fetch the state
        x,y = state

        if action.count('up'):
            y-=1
        if action.count('down'):
            y+=1
        if action.count('left'):
            x-=1
        if action.count('right'):
            x+=1
        return (x,y) #new_state

    #This method receives the state and must return a score
    #that represents an estimated cost
    def heuristic(self, state):
        x,y = state
        gx,gy = self.goal

        #euclidean distance
        p1 = (x-gx)**2
        p2 = (y-gy)**2
        estimated_cost = math.sqrt((p1+p2))

        return estimated_cost

    def cost(self, state, action, state2):
        return self.COSTS[action]

    #application of the algorithm
    def solve(self):
        #solve the maze problem using A*
        result = astar(self,graph_search=True) #graph_search : True avoid exploring repeated states

        #extract route from the result
        route = [x[1] for x in result.path()]
        route.pop(0) #ignore the initial pos
        route.pop(-1) #ignore the goal pos

        for x,y in route:
            self.board[x][y] = '.'  #draw thw breadcrums

def main():
    ms = MazeSolver('D:/parthcomp/temp/maze_boards/3.txt')
    ms.displayBoard()
    ms.solve()
    ms.displayBoard()

main()
