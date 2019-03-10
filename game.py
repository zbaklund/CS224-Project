import copy
from random import *
class Game:
    def __init__(self, s=3):
        self.size = s
        self.board = [[[0 for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]
        self.turn = 0

    def __repr__(self):
        boardbuf = ""
        boardbuf += "Turn {}\n##########\n".format(self.turn)
        if len(self.board) != self.size:
            boardbuf += "Empty board - Please init_board\n"
        else:
            for level in self.board:
                for row in level:
                    boardbuf += str(row) + "\n"
                boardbuf += "##########\n"
        boardbuf += "\n"
        return boardbuf

    def make_move(self, m):
        x, y, z = m[0], m[1], m[2]
        if self.board[x][y][z]:
            return False
        else:
            self.board[x][y][z] = self.turn % 2 + 1
            self.turn += 1
            return True

    def get_player_turn(self):
        return self.turn % 2 + 1

    def check_win(self):
        for i, grid in enumerate(self.board):
            won = self.check_grid(grid)
            if won:
                won = list(won)
                for cord in won[1]:
                    cord.insert(0, i)
                return won
        for i in range(self.size):
            grid = []
            for j in range(self.size):
                grid.append([self.board[j][k][i] for k in range(self.size)])
            # print(grid)
            won = self.check_grid(grid)
            if won:
                won = list(won)
                for cord in won[1]:
                    cord.append(i)
                return won
        return self.check_mulit_diagonal()
        # TODO add check 3d horizontals

    def check_grid(self, grid):
        checks = [self.check_verticle(grid), self.check_horizontal(grid), self.check_diagonal(grid)]
        for i in checks:
            if i:
                return i
        return 0

    def check_diagonal(self, grid):
        line = [grid[i][i] for i in range(self.size)]
        won = self.check_line(line)
        if won:
            return won, [[i, i] for i in range(self.size)]
        line = [grid[(self.size - 1) - i][i] for i in range(self.size)]
        # print line
        won = self.check_line(line)
        if won:
            return won, [[self.size - 1 - i, i] for i in range(self.size)]
        return 0

    def check_mulit_diagonal(self):
        lines = [[self.board[i][i][i] for i in range(self.size)],
                 [self.board[i][i][(self.size - 1) - i] for i in range(self.size)],
                 [self.board[i][(self.size - 1) - i][i] for i in range(self.size)],
                 [self.board[i][(self.size - 1) - i][(self.size - 1) - i] for i in range(self.size)]]
        cords = [[[i, i, i] for i in range(self.size)],
                 [[i, i, (self.size - 1) - i] for i in range(self.size)],
                 [[i, (self.size - 1) - i, i] for i in range(self.size)],
                 [[i, (self.size - 1) - i, (self.size - 1) - i] for i in range(self.size)]]
        for i, line in enumerate(lines):
            won = self.check_line(line)
            if won:
                return [won, cords[i]]
        return 0

    def check_verticle(self, grid):
        for i in range(self.size):
            line = [grid[j][i] for j in range(len(grid))]  # double check
            won = self.check_line(line)
            if won:
                return won, [[j, i] for j in range(self.size)]
        return 0

    def check_horizontal(self, grid):
        for i in range(self.size):
            won = self.check_line(grid[i])
            if won:
                return won, [[i, j] for j in range(self.size)]
        return 0

    def check_line(self, line):
        temp = line[0]
        for i in line:
            if i != temp:
                return 0
        return temp

    # function for dumb bot to take it's turn, returns a list of the three indexes that are the location it will put
    # its piece. Code assumes bot is always O (2 in the game board)
    def dumb_bot_take_turn(self):
        # get list of all empty spaces
        free_spaces = [[l, r, c] for l in range(len(self.board)) for r in range(len(self.board[l])) for c in range(
            len(self.board[l][r])) if self.board[l][r][c] == 0]
        # for each space in free_spaces check if a move results in a win for bot, if it does make that move.
        for m in free_spaces:
            fake_board = copy.deepcopy(self)
            fake_board.board[m[0]][m[1]][m[2]] = 2
            if fake_board.check_win():
                return m
        # for each space in free_spaces check if a move results in a win for player, if it does block that move
        for m in free_spaces:
            fake_board = copy.deepcopy(self)
            fake_board.board[m[0]][m[1]][m[2]] = 1
            if fake_board.check_win():
                return m
        # there is no wining move for the bot or player, so take a random move from free_spaces
        return free_spaces[randint(0, len(free_spaces)-1)]
