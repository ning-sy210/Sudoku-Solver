# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

        self.unassignedVarDomain = {}
        self.initialize()

    def getSubGridIndex(self, coords):
        row, col = coords[0], coords[1]
        if row <= 2:
            if col <= 2:
                return 0
            elif col <= 5:
                return 1
            elif col <= 8:
                return 2
        elif row <= 5:
            if col <= 2:
                return 3
            elif col <= 5:
                return 4
            elif col <= 8:
                return 5
        elif row <= 8:
            if col <= 2:
                return 6
            elif col <= 5:
                return 7
            elif col <= 8:
                return 8
        else:
            return -1

    def initialize(self):
        row_inf = []
        col_inf = []
        box_inf = []
        # containers to remember the values that are present in each row, column and 3x3 grid
        for v in range(9):
            row_inf.append(set())
            col_inf.append(set())
            box_inf.append(set())

        for x in range(9):
            for y in range(9):
                value = self.puzzle[x][y]

                if value != 0:                                                      # cells that are already assigned
                    boxNo = self.getSubGridIndex((x, y))

                    # remembers the values that unassigned cells cannot have in their corresponding row, column, and 3x3 grid
                    row_inf[x].add(value)
                    col_inf[y].add(value)
                    box_inf[boxNo].add(value)
                else:                                                               # cells that are unassigned
                    # remembers the coordinates of unassigned cells
                    self.unassignedVarDomain[(x, y)] = None

        for cell in self.unassignedVarDomain.keys():
            self.unassignedVarDomain[cell] = self.computeDomain(cell, row_inf, col_inf, box_inf)

    def undoPreviousUpdate(self, update):
        for cell, val in update.items():
            self.unassignedVarDomain[cell].append(val)

    def updateDomains(self, x, y, v):
        changes = {}

        for cell, domain in self.unassignedVarDomain.items():
            if cell[0] == x or cell[1] == y or self.getSubGridIndex(cell) == self.getSubGridIndex((x, y)):
                if v in domain:
                    domain.remove(v)
                    changes[cell] = v

        return changes

    def computeDomain(self, cell, row_inf, col_inf, box_inf):
        x, y = cell[0], cell[1]
        bn = self.getSubGridIndex((x, y))

        result = {i for i in range(1, 10)}

        # remove values from the domain that are not consistent with all of the current constraints
        return list(result.difference(row_inf[x]).difference(col_inf[y]).difference(box_inf[bn]))

    def pickUnassignedCell(self):
        # puzzle completed
        if len(self.unassignedVarDomain.keys()) == 0:
            return (-1, -1)

        coords = None
        minDomainCardinality = 10

        for cell, domain in self.unassignedVarDomain.items():
            if len(domain) == 0:
                return None

            if len(domain) < minDomainCardinality:
                coords = cell
                minDomainCardinality = len(domain)

        return coords

    def solve(self):
        # pick the cell with the lowest MRV
        cell = self.pickUnassignedCell()

        if cell == (-1, -1):                            # puzzle completed
            # self.ans is a list of lists
            return self.ans

        if cell is None:                    # current assignment does not work, need to backtrack
            return None

        # found an unassigned cell
        domain = self.unassignedVarDomain.pop(cell)
        x, y = cell[0], cell[1]

        # try out each value in the computed domain of (x, y)
        for v in domain:
            self.ans[x][y] = v
            update = self.updateDomains(x, y, v)
            
            # solve the new puzzle assuming the current assignment is correct, with the updated inferences
            result = self.solve()

            if result is not None:
                return result

            # current assignment does not work, backtracking steps
            self.undoPreviousUpdate(update)
            self.ans[x][y] = 0
        
        # none of the domain values work under current assignment and inference, need to backtrack
        self.unassignedVarDomain[cell] = domain
        return None

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            if i % 3 == 0 and i != 0:
                f.write("---------------------\n")
            for j in range(9):
                if j % 3 == 2 and j != 8:
                    f.write(str(ans[i][j]) + " | ")
                else:
                    f.write(str(ans[i][j]) + " ")
            f.write("\n")
