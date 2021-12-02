import random

class SudokuGame:

    def __init__(self):
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.fixedPositions = []


    def ThrowRules(self, row, col, num):

        # Check row
        for i in range(9):
            if self.board[row][i] == num:
                return 1

        # Check column
        for i in range(9):
            if self.board[i][col] == num:
                return 2

        # Check box
        box_x = row // 3
        box_y = col // 3

        for i in range(box_x * 3, box_x * 3 + 3):
            for j in range(box_y * 3, box_y * 3 + 3):
                if self.board[i][j] == num:
                    return 3

        for i in self.fixedPositions:
            if i[0] == row and i[1] == col:
                return 4

        return 0

    def Rules(self, row, col, num):

        # Check row
        for i in range(9):
            if self.board[row][i] == num:
                return False

        # Check column
        for i in range(9):
            if self.board[i][col] == num:
                return False

        # Check box
        box_x = row // 3
        box_y = col // 3

        for i in range(box_x * 3, box_x * 3 + 3):
            for j in range(box_y * 3, box_y * 3 + 3):
                if self.board[i][j] == num:
                    return False

        for i in self.fixedPositions:
            if i[0] == row and i[1] == col:
                return False

        return True

    def Solve(self):

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    for num in range(1, 10):
                        posibilidades = self.Rules(i, j, num)
                        if self.Rules(i, j, num) == True:
                            self.board[i][j] = num
                            if self.Solve():
                                return True
                            self.board[i][j] = 0
                    return False
        return True

    def Print(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - -")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                print(self.board[i][j], end=" ")
            print()

    def Generate(self):

        for i in range(9):
            for j in range(9):
                self.board[i][j] = 0

    def Add(self, row, col, num):

        if self.Rules(row, col, num) == True:
            self.board[row][col] = num
            return True
        else:
            return self.ThrowRules(row, col, num)

    def Valid(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True

    def GenerateFixed(self):

        self.Solve()

        max = random.randint(1, 15)

        for i in range(9):
            for j in range(9):

                if self.board[i][j] != 0 and max > 0:

                    posibility = random.randint(1, 8)

                    if posibility == 1:
                        self.fixedPositions.append([i, j])
                        max -= 1

                    else:
                        self.board[i][j] = 0

                else:

                    self.board[i][j] = 0

    def Delete(self):

        for i in range(9):
            for j in range(9):

                for k in self.fixedPositions:

                    if i != k[0] and j != k[1]:
                        self.board[i][j] = 0


    def Hard(self):

        self.fixedPositions = []

        self.board =    [[8,0,0,0,0,0,0,0,0],
                        [0,0,3,6,0,0,0,0,0],
                        [0,7,0,0,9,0,2,0,0],
                        [0,5,0,0,0,7,0,0,0],
                        [0,0,0,0,4,5,7,0,0],
                        [0,0,0,1,0,0,0,3,0],
                        [0,0,1,0,0,0,0,6,8],
                        [0,0,8,5,0,0,0,1,0],
                        [0,9,0,0,0,0,4,0,0]]

        for i in range(9):
            for j in range(9):

                if self.board[i][j] != 0:
                    self.fixedPositions.append([i, j])


    def Medium(self):

        self.fixedPositions = []

        self.board =    [[0,0,9,0,7,0,4,3,6],
                        [0,0,0,3,8,0,0,0,0],
                        [6,3,2,5,0,0,0,0,0],
                        [7,6,3,8,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,8,2,7,3],
                        [0,0,0,0,0,0,0,0,0],
                        [3,5,8,0,1,0,6,0,0]]

        for i in range(9):
            for j in range(9):

                if self.board[i][j] != 0:
                    self.fixedPositions.append([i, j])

    def Easy(self):

        self.fixedPositions = []

        self.board = [[5,1,7,6,0,0,0,3,4],
                       [2,8,9,0,0,4,0,0,0],
                       [3,4,6,2,0,5,0,9,0],
                       [6,0,2,0,0,0,0,1,0],
                       [0,3,8,0,0,6,0,4,7],
                       [0,0,0,0,0,0,0,0,0],
                       [0,9,0,0,0,0,0,7,8],
                       [7,0,3,4,0,0,5,6,0],
                       [0,0,0,0,0,0,0,0,0]]

        for i in range(9):
            for j in range(9):

                if self.board[i][j] != 0:
                    self.fixedPositions.append([i, j])


