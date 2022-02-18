import pygame
import sys
import random
pygame.init()

# Changeable variables

squaresize = 30
grid = 1
tiny_sqr = 20

sidebarcolor = [100, 100, 100]

leftbar = 170
rightbar = 170
topbar = 120
botbar = 120

bg_color = [0, 0, 0]
grid_color = [255, 255, 255]

das_startup = 250
das = 50

# Dependent Variables

game_w = squaresize * 10 + grid * 11
game_h = squaresize * 20 + grid * 21

win_w = leftbar + game_w + rightbar
win_h = topbar + game_h + botbar

pygame.key.set_repeat(das_startup, das)

# Static Variables

left = 276
right = 275
hard = 273
soft = 274
cw = 102
ccw = 100
hold = 32
pause = 112

hold_opt = 1
ghost_opt = 1

can_hold = 1
holdpce = 0

bag = [0]

level = 1

board = []

gamemode = "sprint"

time = 0
lines = 0
score = 0
b2b = 0
combocount = 0

fps = 60
lock_delay = fps / 2

lock_c = 0
norm_fall = int((0.8 - ((level - 1) * 0.007)) ** (level - 1) / (1 / fps))
soft_fall = int(norm_fall / 20)

lastclear = 0

tspin = 0

for n in range(0, 41):
    board.append(["X", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


class Piece:
    def __init__(self, p):
        global lock_c
        self.p = p
        if p == 1:
            self.name = "I"
            self.color = [0, 255, 255]
            self.one = [4, 0]
            self.two = [self.one[0] + 1, self.one[1]]
            self.three = [self.one[0] + 2, self.one[1]]
            self.four = [self.one[0] + 3, self.one[1]]

        if p == 2:
            self.name = "O"
            self.color = [255, 255, 0]
            self.one = [5, 0]
            self.two = [self.one[0] + 1, self.one[1]]
            self.three = [self.one[0], self.one[1] - 1]
            self.four = [self.one[0] + 1, self.one[1] - 1]

        if p == 3:
            self.name = "T"
            self.color = [255, 0, 255]
            self.one = [4, 0]
            self.two = [self.one[0] + 1, self.one[1]]
            self.three = [self.one[0] + 2, self.one[1]]
            self.four = [self.one[0] + 1, self.one[1] - 1]

        if p == 4:
            self.name = "S"
            self.color = [0, 255, 0]
            self.one = [4, 0]
            self.two = [self.one[0] + 1, self.one[1]]
            self.three = [self.one[0] + 1, self.one[1] - 1]
            self.four = [self.one[0] + 2, self.one[1] - 1]

        if p == 5:
            self.name = "Z"
            self.color = [255, 0, 0]
            self.one = [4, -1]
            self.two = [self.one[0] + 1, self.one[1]]
            self.three = [self.one[0] + 1, self.one[1] + 1]
            self.four = [self.one[0] + 2, self.one[1] + 1]

        if p == 6:
            self.name = "J"
            self.color = [0, 0, 255]
            self.one = [4, -1]
            self.two = [self.one[0], self.one[1] + 1]
            self.three = [self.one[0] + 1, self.one[1] + 1]
            self.four = [self.one[0] + 2, self.one[1] + 1]

        if p == 7:
            self.name = "L"
            self.color = [255, 128, 0]
            self.one = [4, 0]
            self.two = [self.one[0] + 1, self.one[1]]
            self.three = [self.one[0] + 2, self.one[1]]
            self.four = [self.one[0] + 2, self.one[1] - 1]

        self.x1 = leftbar + ((self.one[0] - 1) * (grid + squaresize)) + grid
        self.y1 = topbar + ((self.one[1] - 1) * (grid + squaresize)) + grid
        self.x2 = leftbar + ((self.two[0] - 1) * (grid + squaresize)) + grid
        self.y2 = topbar + ((self.two[1] - 1) * (grid + squaresize)) + grid
        self.x3 = leftbar + ((self.three[0] - 1) * (grid + squaresize)) + grid
        self.y3 = topbar + ((self.three[1] - 1) * (grid + squaresize)) + grid
        self.x4 = leftbar + ((self.four[0] - 1) * (grid + squaresize)) + grid
        self.y4 = topbar + ((self.four[1] - 1) * (grid + squaresize)) + grid

        self.g1 = self.one
        self.gx1 = self.x1
        self.gy1 = self.y1
        self.g2 = self.two
        self.gx2 = self.x2
        self.gy2 = self.y2
        self.g3 = self.three
        self.gx3 = self.x3
        self.gy3 = self.y3
        self.g4 = self.four
        self.gx4 = self.x4
        self.gy4 = self.y4

        self.f_count = 0
        self.lock_count = 0
        lock_c = 0

        self.rot = 1
        self.test = 0

        self.rone = list(self.one)
        self.rtwo = list(self.two)
        self.rthree = list(self.three)
        self.rfour = list(self.four)

        self.lastmove = 0
        self.bigmini = 0

    def xy_update(self):
        self.x1 = leftbar + ((self.one[0] - 1) * (grid + squaresize)) + grid
        self.y1 = topbar + ((self.one[1] - 1) * (grid + squaresize)) + grid
        self.x2 = leftbar + ((self.two[0] - 1) * (grid + squaresize)) + grid
        self.y2 = topbar + ((self.two[1] - 1) * (grid + squaresize)) + grid
        self.x3 = leftbar + ((self.three[0] - 1) * (grid + squaresize)) + grid
        self.y3 = topbar + ((self.three[1] - 1) * (grid + squaresize)) + grid
        self.x4 = leftbar + ((self.four[0] - 1) * (grid + squaresize)) + grid
        self.y4 = topbar + ((self.four[1] - 1) * (grid + squaresize)) + grid

    def norm_fall(self):
        if self.f_count < norm_fall:
            self.f_count += 1
        else:
            self.f_count = 0
            self.one = [self.one[0], self.one[1] + 1]
            self.two = [self.two[0], self.two[1] + 1]
            self.three = [self.three[0], self.three[1] + 1]
            self.four = [self.four[0], self.four[1] + 1]
            self.lastmove = 0
        self.xy_update()

    def soft_fall(self):
        global score
        if self.f_count < soft_fall:
            self.f_count += 1
        else:
            self.f_count = 0
            self.one = [self.one[0], self.one[1] + 1]
            self.two = [self.two[0], self.two[1] + 1]
            self.three = [self.three[0], self.three[1] + 1]
            self.four = [self.four[0], self.four[1] + 1]
            score += 1
            self.lastmove = 0
        self.xy_update()

    def move_left(self):
        global lock_c
        ret = self.leftstop()
        if ret == 0:
            self.one[0] = self.one[0] - 1
            self.two[0] = self.two[0] - 1
            self.three[0] = self.three[0] - 1
            self.four[0] = self.four[0] - 1
            self.lastmove = 0
            lock_c += 1
            if lock_c < 15:
                self.lock_count = 0
        self.xy_update()

    def move_right(self):
        global lock_c
        ret = self.rightstop()
        if ret == 0:
            self.one[0] = self.one[0] + 1
            self.two[0] = self.two[0] + 1
            self.three[0] = self.three[0] + 1
            self.four[0] = self.four[0] + 1
            self.lastmove = 0
            lock_c += 1
            if lock_c < 15:
                self.lock_count = 0
        self.xy_update()

    def leftstop(self):
        if self.one[0] == 1:
            return 1
        if self.two[0] == 1:
            return 1
        if self.three[0] == 1:
            return 1
        if self.four[0] == 1:
            return 1
        for y in range(0, len(board)):
            for x in range(1, len(board[y])):
                if board[y][x] != 0:
                    if self.one[0] - 1 == x and self.one[1] == y - 20:
                        return 1
                    if self.two[0] - 1 == x and self.two[1] == y - 20:
                        return 1
                    if self.three[0] - 1 == x and self.three[1] == y - 20:
                        return 1
                    if self.four[0] - 1 == x and self.four[1] == y - 20:
                        return 1
        return 0

    def rightstop(self):
        if self.one[0] == 10:
            return 1
        if self.two[0] == 10:
            return 1
        if self.three[0] == 10:
            return 1
        if self.four[0] == 10:
            return 1
        for y in range(0, len(board)):
            for x in range(1, len(board[y])):
                if board[y][x] != 0:
                    if self.one[0] + 1 == x and self.one[1] == y - 20:
                        return 1
                    if self.two[0] + 1 == x and self.two[1] == y - 20:
                        return 1
                    if self.three[0] + 1 == x and self.three[1] == y - 20:
                        return 1
                    if self.four[0] + 1 == x and self.four[1] == y - 20:
                        return 1
        return 0

    def stop_fall(self):
        if self.one[1] == 20:
            return 1
        if self.two[1] == 20:
            return 1
        if self.three[1] == 20:
            return 1
        if self.four[1] == 20:
            return 1
        for y in range(0, len(board)):
            for x in range(1, len(board[y])):
                if board[y][x] != 0:
                    if self.one[1] + 1 == y - 20 and self.one[0] == x:
                        return 1
                    if self.two[1] + 1 == y - 20 and self.two[0] == x:
                        return 1
                    if self.three[1] + 1 == y - 20 and self.three[0] == x:
                        return 1
                    if self.four[1] + 1 == y - 20 and self.four[0] == x:
                        return 1
        return 0

    def hard_fall(self):
        global score
        ret = self.stop_fall()
        while ret == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.one = [self.one[0], self.one[1] + 1]
            self.two = [self.two[0], self.two[1] + 1]
            self.three = [self.three[0], self.three[1] + 1]
            self.four = [self.four[0], self.four[1] + 1]
            score += 2
            ret = self.stop_fall()
        self.xy_update()
        self.place()

    def ghost(self):
        global ghost_opt
        if ghost_opt == 1:
            self.g1 = self.one
            self.g2 = self.two
            self.g3 = self.three
            self.g4 = self.four

            ret = self.ghoststop()

            while ret == 0:
                self.g1 = [self.g1[0], self.g1[1] + 1]
                self.g2 = [self.g2[0], self.g2[1] + 1]
                self.g3 = [self.g3[0], self.g3[1] + 1]
                self.g4 = [self.g4[0], self.g4[1] + 1]
                ret = self.ghoststop()

            self.gx1 = leftbar + ((self.g1[0] - 1) * (grid + squaresize)) + grid
            self.gy1 = topbar + ((self.g1[1] - 1) * (grid + squaresize)) + grid
            self.gx2 = leftbar + ((self.g2[0] - 1) * (grid + squaresize)) + grid
            self.gy2 = topbar + ((self.g2[1] - 1) * (grid + squaresize)) + grid
            self.gx3 = leftbar + ((self.g3[0] - 1) * (grid + squaresize)) + grid
            self.gy3 = topbar + ((self.g3[1] - 1) * (grid + squaresize)) + grid
            self.gx4 = leftbar + ((self.g4[0] - 1) * (grid + squaresize)) + grid
            self.gy4 = topbar + ((self.g4[1] - 1) * (grid + squaresize)) + grid

    def ghoststop(self):
        if self.g1[1] == 20:
            return 1
        if self.g2[1] == 20:
            return 1
        if self.g3[1] == 20:
            return 1
        if self.g4[1] == 20:
            return 1
        for y in range(0, len(board)):
            for x in range(1, len(board[y])):
                if board[y][x] != 0:
                    if self.g1[1] + 1 == y - 20 and self.g1[0] == x:
                        return 1
                    if self.g2[1] + 1 == y - 20 and self.g2[0] == x:
                        return 1
                    if self.g3[1] + 1 == y - 20 and self.g3[0] == x:
                        return 1
                    if self.g4[1] + 1 == y - 20 and self.g4[0] == x:
                        return 1
        return 0

    def placecheck(self):
        if self.lock_count < lock_delay:
            self.lock_count += 1
        else:
            return 1
        return 0

    def place(self):
        global piece
        global board
        global can_hold

        self.xy_update()

        board[self.one[1] + 20][self.one[0]] = self.name
        board[self.two[1] + 20][self.two[0]] = self.name
        board[self.three[1] + 20][self.three[0]] = self.name
        board[self.four[1] + 20][self.four[0]] = self.name

        if self.one[1] < 1 and self.two[1] < 1:
            if self.two[1] < 1 and self.three[1] < 1:
                gameover()

        tspintest()

        lineclear()

        bag.pop(0)
        piece = Piece(bag[0])

        for y in range(0, len(board)):
            for x in range(1, len(board[y])):
                if board[y][x] != 0:
                    if piece.one[0] == x and piece.one[1] == y - 20:
                        gameover()
                    if piece.two[0] == x and piece.two[1] == y - 20:
                        gameover()
                    if piece.three[0] == x and piece.three[1] == y - 20:
                        gameover()
                    if piece.four[0] == x and piece.four[1] == y - 20:
                        gameover()

        can_hold = 1

    def rotatecw(self):
        global lock_c
        transx = 0
        transy = 0
        ret = self.rotatetest("cw")
        if ret == 0:
            return
        else:
            self.lastmove = 1
            lock_c += 1
            if lock_c < 15:
                self.lock_count = 0
        if ret == 5:
            self.bigmini = 1
        else:
            self.bigmini = 0
        if ret == 1:
            transx = 0
            transy = 0
        if self.name == "I":
            if self.rot == 1:
                if ret == 2:
                    transx = -2
                    transy = 0
                if ret == 3:
                    transx = 1
                    transy = 0
                if ret == 4:
                    transx = -2
                    transy = 1
                if ret == 5:
                    transx = 1
                    transy = -2
                self.rot = 2
                self.one = list([self.one[0] + 2 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] + transy])
                self.three = list([self.three[0] + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] + 2 + transy])
            elif self.rot == 2:
                if ret == 2:
                    transx = -1
                    transy = 0
                if ret == 3:
                    transx = 2
                    transy = 0
                if ret == 4:
                    transx = -1
                    transy = -2
                if ret == 5:
                    transx = 2
                    transy = 1
                self.rot = 3
                self.one = list([self.one[0] + 1 + transx, self.one[1] + 2 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 2 + transx, self.four[1] - 1 + transy])
            elif self.rot == 3:
                if ret == 2:
                    transx = 2
                    transy = 0
                if ret == 3:
                    transx = -1
                    transy = 0
                if ret == 4:
                    transx = 2
                    transy = -1
                if ret == 5:
                    transx = -1
                    transy = 2
                self.rot = 4
                self.one = list([self.one[0] - 2 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] + transy])
                self.three = list([self.three[0] + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] - 2 + transy])
            elif self.rot == 4:
                if ret == 2:
                    transx = 1
                    transy = 0
                if ret == 3:
                    transx = -2
                    transy = 0
                if ret == 4:
                    transx = 1
                    transy = 2
                if ret == 5:
                    transx = -2
                    transy = -1
                self.rot = 1
                self.one = list([self.one[0] - 1 + transx, self.one[1] - 2 + transy])
                self.two = list([self.two[0] + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 2 + transx, self.four[1] + 1 + transy])
        else:
            if ret == 2:
                if self.rot == 1:
                    transx = -1
                    transy = 0
                if self.rot == 2:
                    transx = 1
                    transy = 0
                if self.rot == 3:
                    transx = 1
                    transy = 0
                if self.rot == 4:
                    transx = -1
                    transy = 0
            if ret == 3:
                if self.rot == 1:
                    transx = -1
                    transy = -1
                if self.rot == 2:
                    transx = 1
                    transy = 1
                if self.rot == 3:
                    transx = 1
                    transy = -1
                if self.rot == 4:
                    transx = -1
                    transy = 1
            if ret == 4:
                if self.rot == 1:
                    transx = 0
                    transy = 2
                if self.rot == 2:
                    transx = 0
                    transy = -2
                if self.rot == 3:
                    transx = 0
                    transy = 2
                if self.rot == 4:
                    transx = 0
                    transy = -2
            if ret == 5:
                if self.rot == 1:
                    transx = -1
                    transy = 2
                if self.rot == 2:
                    transx = 1
                    transy = -2
                if self.rot == 3:
                    transx = 1
                    transy = 2
                if self.rot == 4:
                    transx = -1
                    transy = -2
        if self.name == "J":
            if self.rot == 1:
                self.rot = 2
                self.one = list([self.one[0] + 2 + transx, self.one[1] + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
            elif self.rot == 2:
                self.rot = 3
                self.one = list([self.one[0] + transx, self.one[1] + 2 + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
            elif self.rot == 3:
                self.rot = 4
                self.one = list([self.one[0] - 2 + transx, self.one[1] + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
            elif self.rot == 4:
                self.rot = 1
                self.one = list([self.one[0] + transx, self.one[1] - 2 + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
        if self.name == "L":
            if self.rot == 1:
                self.rot = 2
                self.one = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + transx, self.four[1] + 2 + transy])
            elif self.rot == 2:
                self.rot = 3
                self.one = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] - 2 + transx, self.four[1] + transy])
            elif self.rot == 3:
                self.rot = 4
                self.one = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] + transx, self.four[1] - 2 + transy])
            elif self.rot == 4:
                self.rot = 1
                self.one = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + 2 + transx, self.four[1] + transy])
        if self.name == "S":
            if self.rot == 1:
                self.rot = 2
                self.one = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + transx, self.four[1] + 2 + transy])
            elif self.rot == 2:
                self.rot = 3
                self.one = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] - 2 + transx, self.four[1] + transy])
            elif self.rot == 3:
                self.rot = 4
                self.one = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] + transx, self.four[1] - 2 + transy])
            elif self.rot == 4:
                self.rot = 1
                self.one = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] + 2 + transx, self.four[1] + transy])
        if self.name == "T":
            if self.rot == 1:
                self.rot = 2
                self.one = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
            elif self.rot == 2:
                self.rot = 3
                self.one = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
            elif self.rot == 3:
                self.rot = 4
                self.one = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
            elif self.rot == 4:
                self.rot = 1
                self.one = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
        if self.name == "Z":
            if self.rot == 1:
                self.rot = 2
                self.one = list([self.one[0] + 2 + transx, self.one[1] + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
            elif self.rot == 2:
                self.rot = 3
                self.one = list([self.one[0] + transx, self.one[1] + 2 + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
            elif self.rot == 3:
                self.rot = 4
                self.one = list([self.one[0] - 2 + transx, self.one[1] + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
            elif self.rot == 4:
                self.rot = 1
                self.one = list([self.one[0] + transx, self.one[1] - 2 + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])

    def rotateccw(self):
        global lock_c
        transx = 0
        transy = 0
        ret = self.rotatetest("ccw")
        if ret == 0:
            return
        else:
            self.lastmove = 1
            lock_c += 1
            if lock_c < 15:
                self.lock_count = 0
        if ret == 1:
            transx = 0
            transy = 0
        if ret == 5:
            self.bigmini = 1
        else:
            self.bigmini = 0
        if self.name == "I":
            if self.rot == 2:
                if ret == 2:
                    transx = 2
                    transy = 0
                if ret == 3:
                    transx = -1
                    transy = 0
                if ret == 4:
                    transx = 2
                    transy = -1
                if ret == 5:
                    transx = -1
                    transy = 2
                self.rot = 1
                self.one = list([self.one[0] - 2 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] + transy])
                self.three = list([self.three[0] + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] - 2 + transy])
            elif self.rot == 3:
                if ret == 2:
                    transx = 1
                    transy = 0
                if ret == 3:
                    transx = -2
                    transy = 0
                if ret == 4:
                    transx = 1
                    transy = 2
                if ret == 5:
                    transx = -2
                    transy = -1
                self.rot = 2
                self.one = list([self.one[0] - 1 + transx, self.one[1] - 2 + transy])
                self.two = list([self.two[0] + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 2 + transx, self.four[1] + 1 + transy])
            elif self.rot == 4:
                if ret == 2:
                    transx = -2
                    transy = 0
                if ret == 3:
                    transx = 1
                    transy = 0
                if ret == 4:
                    transx = -2
                    transy = 1
                if ret == 5:
                    transx = 1
                    transy = -2
                self.rot = 3
                self.one = list([self.one[0] + 2 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] + transy])
                self.three = list([self.three[0] + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] + 2 + transy])
            elif self.rot == 1:
                if ret == 2:
                    transx = -1
                    transy = 0
                if ret == 3:
                    transx = 2
                    transy = 0
                if ret == 4:
                    transx = -1
                    transy = -2
                if ret == 5:
                    transx = 2
                    transy = 1
                self.rot = 4
                self.one = list([self.one[0] + 1 + transx, self.one[1] + 2 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 2 + transx, self.four[1] - 1 + transy])
        else:
            if ret == 2:
                if self.rot == 2:
                    transx = 1
                    transy = 0
                if self.rot == 3:
                    transx = -1
                    transy = 0
                if self.rot == 4:
                    transx = -1
                    transy = 0
                if self.rot == 1:
                    transx = 1
                    transy = 0
            if ret == 3:
                if self.rot == 2:
                    transx = 1
                    transy = 1
                if self.rot == 3:
                    transx = -1
                    transy = -1
                if self.rot == 4:
                    transx = -1
                    transy = 1
                if self.rot == 1:
                    transx = 1
                    transy = -1
            if ret == 4:
                if self.rot == 2:
                    transx = 0
                    transy = -2
                if self.rot == 3:
                    transx = 0
                    transy = 2
                if self.rot == 4:
                    transx = 0
                    transy = -2
                if self.rot == 1:
                    transx = 0
                    transy = 2
            if ret == 5:
                if self.rot == 2:
                    transx = 1
                    transy = -2
                if self.rot == 3:
                    transx = -1
                    transy = 2
                if self.rot == 4:
                    transx = -1
                    transy = -2
                if self.rot == 1:
                    transx = 1
                    transy = 2
        if self.name == "J":
            if self.rot == 2:
                self.rot = 1
                self.one = list([self.one[0] - 2 + transx, self.one[1] + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
            elif self.rot == 3:
                self.rot = 2
                self.one = list([self.one[0] + transx, self.one[1] - 2 + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
            elif self.rot == 4:
                self.rot = 3
                self.one = list([self.one[0] + 2 + transx, self.one[1] + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
            elif self.rot == 1:
                self.rot = 4
                self.one = list([self.one[0] + transx, self.one[1] + 2 + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
        if self.name == "L":
            if self.rot == 2:
                self.rot = 1
                self.one = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] + transx, self.four[1] - 2 + transy])
            elif self.rot == 3:
                self.rot = 2
                self.one = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + 2 + transx, self.four[1] + transy])
            elif self.rot == 4:
                self.rot = 3
                self.one = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + transx, self.four[1] + 2 + transy])
            elif self.rot == 1:
                self.rot = 4
                self.one = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] - 2 + transx, self.four[1] + transy])
        if self.name == "S":
            if self.rot == 2:
                self.rot = 1
                self.one = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] + transx, self.four[1] - 2 + transy])
            elif self.rot == 3:
                self.rot = 2
                self.one = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] + 2 + transx, self.four[1] + transy])
            elif self.rot == 4:
                self.rot = 3
                self.one = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + transx, self.four[1] + 2 + transy])
            elif self.rot == 1:
                self.rot = 4
                self.one = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] - 2 + transx, self.four[1] + transy])
        if self.name == "T":
            if self.rot == 2:
                self.rot = 1
                self.one = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
            elif self.rot == 3:
                self.rot = 2
                self.one = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
            elif self.rot == 4:
                self.rot = 3
                self.one = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
            elif self.rot == 1:
                self.rot = 4
                self.one = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                self.two = list([self.two[0] + transx, self.two[1] + transy])
                self.three = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
        if self.name == "Z":
            if self.rot == 2:
                self.rot = 1
                self.one = list([self.one[0] - 2 + transx, self.one[1] + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
            elif self.rot == 3:
                self.rot = 2
                self.one = list([self.one[0] + transx, self.one[1] - 2 + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] - 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
            elif self.rot == 4:
                self.rot = 3
                self.one = list([self.one[0] + 2 + transx, self.one[1] + transy])
                self.two = list([self.two[0] + 1 + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
            elif self.rot == 1:
                self.rot = 4
                self.one = list([self.one[0] + transx, self.one[1] + 2 + transy])
                self.two = list([self.two[0] - 1 + transx, self.two[1] + 1 + transy])
                self.three = list([self.three[0] + transx, self.three[1] + transy])
                self.four = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])

    def rotatetest(self, dire):
        if self.name == "O":
            return 0
        if self.name == "I":
            if dire == "cw":
                # Test 1
                if self.rot == 1:
                    self.rone = list([self.one[0] + 2, self.one[1] - 1])
                    self.rtwo = list([self.two[0] + 1, self.two[1]])
                    self.rthree = list([self.three[0], self.three[1] + 1])
                    self.rfour = list([self.four[0] - 1, self.four[1] + 2])
                elif self.rot == 2:
                    self.rone = list([self.one[0] + 1, self.one[1] + 2])
                    self.rtwo = list([self.two[0], self.two[1] + 1])
                    self.rthree = list([self.three[0] - 1, self.three[1]])
                    self.rfour = list([self.four[0] - 2, self.four[1] - 1])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 2, self.one[1] + 1])
                    self.rtwo = list([self.two[0] - 1, self.two[1]])
                    self.rthree = list([self.three[0], self.three[1] - 1])
                    self.rfour = list([self.four[0] + 1, self.four[1] - 2])
                elif self.rot == 4:
                    self.rone = list([self.one[0] - 1, self.one[1] - 2])
                    self.rtwo = list([self.two[0], self.two[1] - 1])
                    self.rthree = list([self.three[0] + 1, self.three[1]])
                    self.rfour = list([self.four[0] + 2, self.four[1] + 1])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 1
                # Test 2
                if self.rot == 1:
                    self.rone = list([self.one[0] + 2 - 2, self.one[1] - 1])
                    self.rtwo = list([self.two[0] + 1 - 2, self.two[1]])
                    self.rthree = list([self.three[0] - 2, self.three[1] + 1])
                    self.rfour = list([self.four[0] - 1 - 2, self.four[1] + 2])
                elif self.rot == 2:
                    self.rone = list([self.one[0] + 1 - 1, self.one[1] + 2])
                    self.rtwo = list([self.two[0] - 1, self.two[1] + 1])
                    self.rthree = list([self.three[0] - 1 - 1, self.three[1]])
                    self.rfour = list([self.four[0] - 2 - 1, self.four[1] - 1])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 2 + 2, self.one[1] + 1])
                    self.rtwo = list([self.two[0] - 1 + 2, self.two[1]])
                    self.rthree = list([self.three[0] + 2, self.three[1] - 1])
                    self.rfour = list([self.four[0] + 1 + 2, self.four[1] - 2])
                elif self.rot == 4:
                    self.rone = list([self.one[0] - 1 + 1, self.one[1] - 2])
                    self.rtwo = list([self.two[0] + 1, self.two[1] - 1])
                    self.rthree = list([self.three[0] + 1 + 1, self.three[1]])
                    self.rfour = list([self.four[0] + 2 + 1, self.four[1] + 1])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 2
                # Test 3
                if self.rot == 1:
                    self.rone = list([self.one[0] + 2 + 1, self.one[1] - 1])
                    self.rtwo = list([self.two[0] + 1 + 1, self.two[1]])
                    self.rthree = list([self.three[0] + 1, self.three[1] + 1])
                    self.rfour = list([self.four[0] - 1 + 1, self.four[1] + 2])
                elif self.rot == 2:
                    self.rone = list([self.one[0] + 1 + 2, self.one[1] + 2])
                    self.rtwo = list([self.two[0] + 2, self.two[1] + 1])
                    self.rthree = list([self.three[0] - 1 + 2, self.three[1]])
                    self.rfour = list([self.four[0] - 2 + 2, self.four[1] - 1])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 2 - 1, self.one[1] + 1])
                    self.rtwo = list([self.two[0] - 1 - 1, self.two[1]])
                    self.rthree = list([self.three[0] - 1, self.three[1] - 1])
                    self.rfour = list([self.four[0] + 1 - 1, self.four[1] - 2])
                elif self.rot == 4:
                    self.rone = list([self.one[0] - 1 - 2, self.one[1] - 2])
                    self.rtwo = list([self.two[0] - 2, self.two[1] - 1])
                    self.rthree = list([self.three[0] + 1 - 2, self.three[1]])
                    self.rfour = list([self.four[0] + 2 - 2, self.four[1] + 1])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 3
                # Test 4
                if self.rot == 1:
                    self.rone = list([self.one[0] + 2 - 2, self.one[1] - 1 + 1])
                    self.rtwo = list([self.two[0] + 1 - 2, self.two[1] + 1])
                    self.rthree = list([self.three[0] - 2, self.three[1] + 1 + 1])
                    self.rfour = list([self.four[0] - 1 - 2, self.four[1] + 2 + 1])
                elif self.rot == 2:
                    self.rone = list([self.one[0] + 1 - 1, self.one[1] + 2 - 2])
                    self.rtwo = list([self.two[0] - 1, self.two[1] + 1 - 2])
                    self.rthree = list([self.three[0] - 1 - 1, self.three[1] - 2])
                    self.rfour = list([self.four[0] - 2 - 1, self.four[1] - 1 - 2])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 2 + 2, self.one[1] + 1 - 1])
                    self.rtwo = list([self.two[0] - 1 + 2, self.two[1] - 1])
                    self.rthree = list([self.three[0] + 2, self.three[1] - 1 - 1])
                    self.rfour = list([self.four[0] + 1 + 2, self.four[1] - 2 - 1])
                elif self.rot == 4:
                    self.rone = list([self.one[0] - 1 + 1, self.one[1] - 2 + 2])
                    self.rtwo = list([self.two[0] + 1, self.two[1] - 1 + 2])
                    self.rthree = list([self.three[0] + 1 + 1, self.three[1] + 2])
                    self.rfour = list([self.four[0] + 2 + 1, self.four[1] + 1 + 2])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 4
                # Test 5
                if self.rot == 1:
                    self.rone = list([self.one[0] + 2 + 1, self.one[1] - 1 - 2])
                    self.rtwo = list([self.two[0] + 1 + 1, self.two[1] - 2])
                    self.rthree = list([self.three[0] + 1, self.three[1] + 1 - 2])
                    self.rfour = list([self.four[0] - 1 + 1, self.four[1] + 2 - 2])
                elif self.rot == 2:
                    self.rone = list([self.one[0] + 1 + 2, self.one[1] + 2 + 1])
                    self.rtwo = list([self.two[0] + 2, self.two[1] + 1 + 1])
                    self.rthree = list([self.three[0] - 1 + 2, self.three[1] + 1])
                    self.rfour = list([self.four[0] - 2 + 2, self.four[1] - 1 + 1])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 2 - 1, self.one[1] + 1 + 2])
                    self.rtwo = list([self.two[0] - 1 - 1, self.two[1] + 2])
                    self.rthree = list([self.three[0] - 1, self.three[1] - 1 + 2])
                    self.rfour = list([self.four[0] + 1 - 1, self.four[1] - 2 + 2])
                elif self.rot == 4:
                    self.rone = list([self.one[0] - 1 - 2, self.one[1] - 2 - 1])
                    self.rtwo = list([self.two[0] - 2, self.two[1] - 1 - 1])
                    self.rthree = list([self.three[0] + 1 - 2, self.three[1] - 1])
                    self.rfour = list([self.four[0] + 2 - 2, self.four[1] + 1 - 1])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 5
                else:
                    return 0
            if dire == "ccw":
                # Test 1
                if self.rot == 2:
                    self.rone = list([self.one[0] - 2, self.one[1] + 1])
                    self.rtwo = list([self.two[0] - 1, self.two[1]])
                    self.rthree = list([self.three[0], self.three[1] - 1])
                    self.rfour = list([self.four[0] + 1, self.four[1] - 2])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 1, self.one[1] - 2])
                    self.rtwo = list([self.two[0], self.two[1] - 1])
                    self.rthree = list([self.three[0] + 1, self.three[1]])
                    self.rfour = list([self.four[0] + 2, self.four[1] + 1])
                elif self.rot == 4:
                    self.rone = list([self.one[0] + 2, self.one[1] - 1])
                    self.rtwo = list([self.two[0] + 1, self.two[1]])
                    self.rthree = list([self.three[0], self.three[1] + 1])
                    self.rfour = list([self.four[0] - 1, self.four[1] + 2])
                elif self.rot == 1:
                    self.rone = list([self.one[0] + 1, self.one[1] + 2])
                    self.rtwo = list([self.two[0], self.two[1] + 1])
                    self.rthree = list([self.three[0] - 1, self.three[1]])
                    self.rfour = list([self.four[0] - 2, self.four[1] - 1])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 1
                # Test 2
                if self.rot == 2:
                    self.rone = list([self.one[0] - 2 + 2, self.one[1] + 1])
                    self.rtwo = list([self.two[0] - 1 + 2, self.two[1]])
                    self.rthree = list([self.three[0] + 2, self.three[1] - 1])
                    self.rfour = list([self.four[0] + 1 + 2, self.four[1] - 2])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 1 + 1, self.one[1] - 2])
                    self.rtwo = list([self.two[0] + 1, self.two[1] - 1])
                    self.rthree = list([self.three[0] + 1 + 1, self.three[1]])
                    self.rfour = list([self.four[0] + 2 + 1, self.four[1] + 1])
                elif self.rot == 4:
                    self.rone = list([self.one[0] + 2 - 2, self.one[1] - 1])
                    self.rtwo = list([self.two[0] + 1 - 2, self.two[1]])
                    self.rthree = list([self.three[0] - 2, self.three[1] + 1])
                    self.rfour = list([self.four[0] - 1 - 2, self.four[1] + 2])
                elif self.rot == 1:
                    self.rone = list([self.one[0] + 1 - 1, self.one[1] + 2])
                    self.rtwo = list([self.two[0] - 1, self.two[1] + 1])
                    self.rthree = list([self.three[0] - 1 - 1, self.three[1]])
                    self.rfour = list([self.four[0] - 2 - 1, self.four[1] - 1])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 2
                # Test 3
                if self.rot == 2:
                    self.rone = list([self.one[0] - 2 - 1, self.one[1] + 1])
                    self.rtwo = list([self.two[0] - 1 - 1, self.two[1]])
                    self.rthree = list([self.three[0] - 1, self.three[1] - 1])
                    self.rfour = list([self.four[0] + 1 - 1, self.four[1] - 2])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 1 - 2, self.one[1] - 2])
                    self.rtwo = list([self.two[0] - 2, self.two[1] - 1])
                    self.rthree = list([self.three[0] + 1 - 2, self.three[1]])
                    self.rfour = list([self.four[0] + 2 - 2, self.four[1] + 1])
                elif self.rot == 4:
                    self.rone = list([self.one[0] + 2 + 1, self.one[1] - 1])
                    self.rtwo = list([self.two[0] + 1 + 1, self.two[1]])
                    self.rthree = list([self.three[0] + 1, self.three[1] + 1])
                    self.rfour = list([self.four[0] - 1 + 1, self.four[1] + 2])
                elif self.rot == 1:
                    self.rone = list([self.one[0] + 1 + 2, self.one[1] + 2])
                    self.rtwo = list([self.two[0] + 2, self.two[1] + 1])
                    self.rthree = list([self.three[0] - 1 + 2, self.three[1]])
                    self.rfour = list([self.four[0] - 2 + 2, self.four[1] - 1])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 3
                # Test 4
                if self.rot == 2:
                    self.rone = list([self.one[0] - 2 + 2, self.one[1] + 1 - 1])
                    self.rtwo = list([self.two[0] - 1 + 2, self.two[1] - 1])
                    self.rthree = list([self.three[0] + 2, self.three[1] - 1 - 1])
                    self.rfour = list([self.four[0] + 1 + 2, self.four[1] - 2 - 1])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 1 + 1, self.one[1] - 2 + 2])
                    self.rtwo = list([self.two[0] + 1, self.two[1] - 1 + 2])
                    self.rthree = list([self.three[0] + 1 + 1, self.three[1] + 2])
                    self.rfour = list([self.four[0] + 2 + 1, self.four[1] + 1 + 2])
                elif self.rot == 4:
                    self.rone = list([self.one[0] + 2 - 2, self.one[1] - 1 + 1])
                    self.rtwo = list([self.two[0] + 1 - 2, self.two[1] + 1])
                    self.rthree = list([self.three[0] - 2, self.three[1] + 1 + 1])
                    self.rfour = list([self.four[0] - 1 - 2, self.four[1] + 2 + 1])
                elif self.rot == 1:
                    self.rone = list([self.one[0] + 1 - 1, self.one[1] + 2 - 2])
                    self.rtwo = list([self.two[0] - 1, self.two[1] + 1 - 2])
                    self.rthree = list([self.three[0] - 1 - 1, self.three[1] - 2])
                    self.rfour = list([self.four[0] - 2 - 1, self.four[1] - 1 - 2])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 4
                # Test 5
                if self.rot == 2:
                    self.rone = list([self.one[0] - 2 - 1, self.one[1] + 1 + 2])
                    self.rtwo = list([self.two[0] - 1 - 1, self.two[1] + 2])
                    self.rthree = list([self.three[0] - 1, self.three[1] - 1 + 2])
                    self.rfour = list([self.four[0] + 1 - 1, self.four[1] - 2 + 2])
                elif self.rot == 3:
                    self.rone = list([self.one[0] - 1 - 2, self.one[1] - 2 - 1])
                    self.rtwo = list([self.two[0] - 2, self.two[1] - 1 - 1])
                    self.rthree = list([self.three[0] + 1 - 2, self.three[1] - 1])
                    self.rfour = list([self.four[0] + 2 - 2, self.four[1] + 1 - 1])
                elif self.rot == 4:
                    self.rone = list([self.one[0] + 2 + 1, self.one[1] - 1 - 2])
                    self.rtwo = list([self.two[0] + 1 + 1, self.two[1] - 2])
                    self.rthree = list([self.three[0] + 1, self.three[1] + 1 - 2])
                    self.rfour = list([self.four[0] - 1 + 1, self.four[1] + 2 - 2])
                elif self.rot == 1:
                    self.rone = list([self.one[0] + 1 + 2, self.one[1] + 2 + 1])
                    self.rtwo = list([self.two[0] + 2, self.two[1] + 1 + 1])
                    self.rthree = list([self.three[0] - 1 + 2, self.three[1] + 1])
                    self.rfour = list([self.four[0] - 2 + 2, self.four[1] - 1 + 1])
                can_rot = 1
                if self.rone[0] < 1 or self.rone[0] > 10:
                    can_rot = 0
                if self.rone[1] > 20:
                    can_rot = 0
                if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                    can_rot = 0
                if self.rtwo[1] > 20:
                    can_rot = 0
                if self.rthree[0] < 1 or self.rthree[0] > 10:
                    can_rot = 0
                if self.rthree[1] > 20:
                    can_rot = 0
                if self.rfour[0] < 1 or self.rfour[0] > 10:
                    can_rot = 0
                if self.rfour[1] > 20:
                    can_rot = 0
                for y in range(0, len(board)):
                    for x in range(1, len(board[y])):
                        if board[y][x] != 0:
                            if self.rone[0] == x and self.rone[1] == y - 20:
                                can_rot = 0
                            if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                                can_rot = 0
                            if self.rthree[0] == x and self.rthree[1] == y - 20:
                                can_rot = 0
                            if self.rfour[0] == x and self.rfour[1] == y - 20:
                                can_rot = 0
                if can_rot == 1:
                    return 5
                else:
                    return 0
        else:
            transx = 0
            transy = 0
            if dire == "cw":
                if self.name == "J":
                    if self.rot == 1:
                        self.rone = list([self.one[0] + 2 + transx, self.one[1] + transy])
                        self.rtwo = list([self.two[0] + 1 + transx, self.two[1] - 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
                    elif self.rot == 2:
                        self.rone = list([self.one[0] + transx, self.one[1] + 2 + transy])
                        self.rtwo = list([self.two[0] + 1 + transx, self.two[1] + 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] - 2 + transx, self.one[1] + transy])
                        self.rtwo = list([self.two[0] - 1 + transx, self.two[1] + 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] + transx, self.one[1] - 2 + transy])
                        self.rtwo = list([self.two[0] - 1 + transx, self.two[1] - 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
                if self.name == "L":
                    if self.rot == 1:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + transx, self.four[1] + 2 + transy])
                    elif self.rot == 2:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] - 2 + transx, self.four[1] + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] + transx, self.four[1] - 2 + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + 2 + transx, self.four[1] + transy])
                if self.name == "S":
                    if self.rot == 1:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + transx, self.four[1] + 2 + transy])
                    elif self.rot == 2:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] - 2 + transx, self.four[1] + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] + transx, self.four[1] - 2 + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] + 2 + transx, self.four[1] + transy])
                if self.name == "T":
                    if self.rot == 1:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
                    elif self.rot == 2:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
                if self.name == "Z":
                    if self.rot == 1:
                        self.rone = list([self.one[0] + 2 + transx, self.one[1] + transy])
                        self.rtwo = list([self.two[0] + 1 + transx, self.two[1] + 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
                    elif self.rot == 2:
                        self.rone = list([self.one[0] + transx, self.one[1] + 2 + transy])
                        self.rtwo = list([self.two[0] - 1 + transx, self.two[1] + 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] - 2 + transx, self.one[1] + transy])
                        self.rtwo = list([self.two[0] - 1 + transx, self.two[1] - 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] + transx, self.one[1] - 2 + transy])
                        self.rtwo = list([self.two[0] + 1 + transx, self.two[1] - 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
            if dire == "ccw":
                if self.name == "J":
                    if self.rot == 2:
                        self.rone = list([self.one[0] - 2 + transx, self.one[1] + transy])
                        self.rtwo = list([self.two[0] - 1 + transx, self.two[1] + 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] + transx, self.one[1] - 2 + transy])
                        self.rtwo = list([self.two[0] - 1 + transx, self.two[1] - 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] + 2 + transx, self.one[1] + transy])
                        self.rtwo = list([self.two[0] + 1 + transx, self.two[1] - 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
                    elif self.rot == 1:
                        self.rone = list([self.one[0] + transx, self.one[1] + 2 + transy])
                        self.rtwo = list([self.two[0] + 1 + transx, self.two[1] + 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
                if self.name == "L":
                    if self.rot == 2:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] + transx, self.four[1] - 2 + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + 2 + transx, self.four[1] + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + transx, self.four[1] + 2 + transy])
                    elif self.rot == 1:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] - 2 + transx, self.four[1] + transy])
                if self.name == "S":
                    if self.rot == 2:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] + transx, self.four[1] - 2 + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] + 2 + transx, self.four[1] + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + transx, self.four[1] + 2 + transy])
                    elif self.rot == 1:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] - 2 + transx, self.four[1] + transy])
                if self.name == "T":
                    if self.rot == 2:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] - 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] + 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] - 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] + 1 + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
                    elif self.rot == 1:
                        self.rone = list([self.one[0] + 1 + transx, self.one[1] + 1 + transy])
                        self.rtwo = list([self.two[0] + transx, self.two[1] + transy])
                        self.rthree = list([self.three[0] - 1 + transx, self.three[1] - 1 + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
                if self.name == "Z":
                    if self.rot == 2:
                        self.rone = list([self.one[0] - 2 + transx, self.one[1] + transy])
                        self.rtwo = list([self.two[0] - 1 + transx, self.two[1] - 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] - 1 + transy])
                    elif self.rot == 3:
                        self.rone = list([self.one[0] + transx, self.one[1] - 2 + transy])
                        self.rtwo = list([self.two[0] + 1 + transx, self.two[1] - 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] + 1 + transx, self.four[1] + 1 + transy])
                    elif self.rot == 4:
                        self.rone = list([self.one[0] + 2 + transx, self.one[1] + transy])
                        self.rtwo = list([self.two[0] + 1 + transx, self.two[1] + 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] + 1 + transy])
                    elif self.rot == 1:
                        self.rone = list([self.one[0] + transx, self.one[1] + 2 + transy])
                        self.rtwo = list([self.two[0] - 1 + transx, self.two[1] + 1 + transy])
                        self.rthree = list([self.three[0] + transx, self.three[1] + transy])
                        self.rfour = list([self.four[0] - 1 + transx, self.four[1] - 1 + transy])
            # Test 1
            can_rot = 1
            if self.rone[0] < 1 or self.rone[0] > 10:
                can_rot = 0
            if self.rone[1] > 20:
                can_rot = 0
            if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                can_rot = 0
            if self.rtwo[1] > 20:
                can_rot = 0
            if self.rthree[0] < 1 or self.rthree[0] > 10:
                can_rot = 0
            if self.rthree[1] > 20:
                can_rot = 0
            if self.rfour[0] < 1 or self.rfour[0] > 10:
                can_rot = 0
            if self.rfour[1] > 20:
                can_rot = 0
            for y in range(0, len(board)):
                for x in range(1, len(board[y])):
                    if board[y][x] != 0:
                        if self.rone[0] == x and self.rone[1] == y - 20:
                            can_rot = 0
                        if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                            can_rot = 0
                        if self.rthree[0] == x and self.rthree[1] == y - 20:
                            can_rot = 0
                        if self.rfour[0] == x and self.rfour[1] == y - 20:
                            can_rot = 0
            if can_rot == 1:
                return 1
            # Test 2
            if dire == "cw":
                if self.rot == 1:
                    transx = -1
                    transy = 0
                if self.rot == 2:
                    transx = 1
                    transy = 0
                if self.rot == 3:
                    transx = 1
                    transy = 0
                if self.rot == 4:
                    transx = -1
                    transy = 0
            if dire == "ccw":
                if self.rot == 2:
                    transx = 1
                    transy = 0
                if self.rot == 3:
                    transx = -1
                    transy = 0
                if self.rot == 4:
                    transx = -1
                    transy = 0
                if self.rot == 1:
                    transx = 1
                    transy = 0
            self.rone = list([self.rone[0] + transx, self.rone[1] + transy])
            self.rtwo = list([self.rtwo[0] + transx, self.rtwo[1] + transy])
            self.rthree = list([self.rthree[0] + transx, self.rthree[1] + transy])
            self.rfour = list([self.rfour[0] + transx, self.rfour[1] + transy])
            can_rot = 1
            if self.rone[0] < 1 or self.rone[0] > 10:
                can_rot = 0
            if self.rone[1] > 20:
                can_rot = 0
            if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                can_rot = 0
            if self.rtwo[1] > 20:
                can_rot = 0
            if self.rthree[0] < 1 or self.rthree[0] > 10:
                can_rot = 0
            if self.rthree[1] > 20:
                can_rot = 0
            if self.rfour[0] < 1 or self.rfour[0] > 10:
                can_rot = 0
            if self.rfour[1] > 20:
                can_rot = 0
            for y in range(0, len(board)):
                for x in range(1, len(board[y])):
                    if board[y][x] != 0:
                        if self.rone[0] == x and self.rone[1] == y - 20:
                            can_rot = 0
                        if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                            can_rot = 0
                        if self.rthree[0] == x and self.rthree[1] == y - 20:
                            can_rot = 0
                        if self.rfour[0] == x and self.rfour[1] == y - 20:
                            can_rot = 0
            if can_rot == 1:
                return 2
            self.rone = list([self.rone[0] - transx, self.rone[1] - transy])
            self.rtwo = list([self.rtwo[0] - transx, self.rtwo[1] - transy])
            self.rthree = list([self.rthree[0] - transx, self.rthree[1] - transy])
            self.rfour = list([self.rfour[0] - transx, self.rfour[1] - transy])
            # Test 3
            if dire == "cw":
                if self.rot == 1:
                    transx = -1
                    transy = -1
                if self.rot == 2:
                    transx = 1
                    transy = 1
                if self.rot == 3:
                    transx = 1
                    transy = -1
                if self.rot == 4:
                    transx = -1
                    transy = 1
            if dire == "ccw":
                if self.rot == 2:
                    transx = 1
                    transy = 1
                if self.rot == 3:
                    transx = -1
                    transy = -1
                if self.rot == 4:
                    transx = -1
                    transy = 1
                if self.rot == 1:
                    transx = 1
                    transy = -1
            self.rone = list([self.rone[0] + transx, self.rone[1] + transy])
            self.rtwo = list([self.rtwo[0] + transx, self.rtwo[1] + transy])
            self.rthree = list([self.rthree[0] + transx, self.rthree[1] + transy])
            self.rfour = list([self.rfour[0] + transx, self.rfour[1] + transy])
            can_rot = 1
            if self.rone[0] < 1 or self.rone[0] > 10:
                can_rot = 0
            if self.rone[1] > 20:
                can_rot = 0
            if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                can_rot = 0
            if self.rtwo[1] > 20:
                can_rot = 0
            if self.rthree[0] < 1 or self.rthree[0] > 10:
                can_rot = 0
            if self.rthree[1] > 20:
                can_rot = 0
            if self.rfour[0] < 1 or self.rfour[0] > 10:
                can_rot = 0
            if self.rfour[1] > 20:
                can_rot = 0
            for y in range(0, len(board)):
                for x in range(1, len(board[y])):
                    if board[y][x] != 0:
                        if self.rone[0] == x and self.rone[1] == y - 20:
                            can_rot = 0
                        if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                            can_rot = 0
                        if self.rthree[0] == x and self.rthree[1] == y - 20:
                            can_rot = 0
                        if self.rfour[0] == x and self.rfour[1] == y - 20:
                            can_rot = 0
            if can_rot == 1:
                return 3
            self.rone = list([self.rone[0] - transx, self.rone[1] - transy])
            self.rtwo = list([self.rtwo[0] - transx, self.rtwo[1] - transy])
            self.rthree = list([self.rthree[0] - transx, self.rthree[1] - transy])
            self.rfour = list([self.rfour[0] - transx, self.rfour[1] - transy])
            # Test 4
            if dire == "cw":
                if self.rot == 1:
                    transx = 0
                    transy = 2
                if self.rot == 2:
                    transx = 0
                    transy = -2
                if self.rot == 3:
                    transx = 0
                    transy = 2
                if self.rot == 4:
                    transx = 0
                    transy = -2
            if dire == "ccw":
                if self.rot == 2:
                    transx = 0
                    transy = -2
                if self.rot == 3:
                    transx = 0
                    transy = 2
                if self.rot == 4:
                    transx = 0
                    transy = -2
                if self.rot == 1:
                    transx = 0
                    transy = 2
            self.rone = list([self.rone[0] + transx, self.rone[1] + transy])
            self.rtwo = list([self.rtwo[0] + transx, self.rtwo[1] + transy])
            self.rthree = list([self.rthree[0] + transx, self.rthree[1] + transy])
            self.rfour = list([self.rfour[0] + transx, self.rfour[1] + transy])
            can_rot = 1
            if self.rone[0] < 1 or self.rone[0] > 10:
                can_rot = 0
            if self.rone[1] > 20:
                can_rot = 0
            if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                can_rot = 0
            if self.rtwo[1] > 20:
                can_rot = 0
            if self.rthree[0] < 1 or self.rthree[0] > 10:
                can_rot = 0
            if self.rthree[1] > 20:
                can_rot = 0
            if self.rfour[0] < 1 or self.rfour[0] > 10:
                can_rot = 0
            if self.rfour[1] > 20:
                can_rot = 0
            for y in range(0, len(board)):
                for x in range(1, len(board[y])):
                    if board[y][x] != 0:
                        if self.rone[0] == x and self.rone[1] == y - 20:
                            can_rot = 0
                        if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                            can_rot = 0
                        if self.rthree[0] == x and self.rthree[1] == y - 20:
                            can_rot = 0
                        if self.rfour[0] == x and self.rfour[1] == y - 20:
                            can_rot = 0
            if can_rot == 1:
                return 4
            self.rone = list([self.rone[0] - transx, self.rone[1] - transy])
            self.rtwo = list([self.rtwo[0] - transx, self.rtwo[1] - transy])
            self.rthree = list([self.rthree[0] - transx, self.rthree[1] - transy])
            self.rfour = list([self.rfour[0] - transx, self.rfour[1] - transy])
            # Test 5
            if dire == "cw":
                if self.rot == 1:
                    transx = -1
                    transy = 2
                if self.rot == 2:
                    transx = 1
                    transy = -2
                if self.rot == 3:
                    transx = 1
                    transy = 2
                if self.rot == 4:
                    transx = -1
                    transy = -2
            if dire == "ccw":
                if self.rot == 2:
                    transx = 1
                    transy = -2
                if self.rot == 3:
                    transx = -1
                    transy = 2
                if self.rot == 4:
                    transx = -1
                    transy = -2
                if self.rot == 1:
                    transx = 1
                    transy = 2
            self.rone = list([self.rone[0] + transx, self.rone[1] + transy])
            self.rtwo = list([self.rtwo[0] + transx, self.rtwo[1] + transy])
            self.rthree = list([self.rthree[0] + transx, self.rthree[1] + transy])
            self.rfour = list([self.rfour[0] + transx, self.rfour[1] + transy])
            can_rot = 1
            if self.rone[0] < 1 or self.rone[0] > 10:
                can_rot = 0
            if self.rone[1] > 20:
                can_rot = 0
            if self.rtwo[0] < 1 or self.rtwo[0] > 10:
                can_rot = 0
            if self.rtwo[1] > 20:
                can_rot = 0
            if self.rthree[0] < 1 or self.rthree[0] > 10:
                can_rot = 0
            if self.rthree[1] > 20:
                can_rot = 0
            if self.rfour[0] < 1 or self.rfour[0] > 10:
                can_rot = 0
            if self.rfour[1] > 20:
                can_rot = 0
            for y in range(0, len(board)):
                for x in range(1, len(board[y])):
                    if board[y][x] != 0:
                        if self.rone[0] == x and self.rone[1] == y - 20:
                            can_rot = 0
                        if self.rtwo[0] == x and self.rtwo[1] == y - 20:
                            can_rot = 0
                        if self.rthree[0] == x and self.rthree[1] == y - 20:
                            can_rot = 0
                        if self.rfour[0] == x and self.rfour[1] == y - 20:
                            can_rot = 0
            self.rone = list([self.rone[0] - transx, self.rone[1] - transy])
            self.rtwo = list([self.rtwo[0] - transx, self.rtwo[1] - transy])
            self.rthree = list([self.rthree[0] - transx, self.rthree[1] - transy])
            self.rfour = list([self.rfour[0] - transx, self.rfour[1] - transy])
            if can_rot == 1:
                return 5
            else:
                return 0


win = pygame.display.set_mode([win_w, win_h])
clock = pygame.time.Clock()
pygame.display.set_caption("Stris")
piece = Piece(1)


def game():
    global left
    global right
    global hard
    global soft
    global cw
    global ccw
    global hold
    global pause
    global can_hold
    global bag
    global piece
    global time
    global lines
    global score
    global level
    global norm_fall
    global soft_fall
    global tspin

    while 1:
        mouse = pygame.mouse.get_pos()
        clock.tick(fps)
        time += clock.get_time()
        drawgame()
        pygame.display.update()

        if len(bag) < 14:
            randomizer()

        stopfall = piece.stop_fall()

        if stopfall == 0:
            if pygame.key.get_pressed()[soft]:
                piece.soft_fall()
            else:
                piece.norm_fall()

        if stopfall == 1:
            ret = piece.placecheck()
            if ret == 1:
                piece.place()

        levelgoal = level * 10
        if lines >= levelgoal:
            level += 1
            norm_fall = int((0.8 - ((level - 1) * 0.007)) ** (level - 1) / (1 / fps))
            soft_fall = int(norm_fall / 20)

        if gamemode == "marathon":
            if lines >= 150:
                winscreen()
        if gamemode == "sprint":
            if lines >= 40:
                winscreen()
        if gamemode == "ultra":
            if time >= 180000:
                winscreen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == left:
                    piece.move_left()
                if event.key == right:
                    piece.move_right()
                if event.key == hard:
                    piece.hard_fall()
                if event.key == cw:
                    piece.rotatecw()
                if event.key == ccw:
                    piece.rotateccw()
                if event.key == hold:
                    holdf()
                if event.key == pause:
                    pausemenu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                            topbar + game_h + 10 <= mouse[1] <= topbar + game_h + 10 + 50):
                        pausemenu()


def drawgame():
    global piece
    global board
    global gamemode
    global time
    win.fill(bg_color)

    mouse = pygame.mouse.get_pos()

    for n in range(1, 12):
        pygame.draw.rect(win, grid_color, [leftbar + ((grid + squaresize) * (n - 1)),
                                           topbar, grid, game_h])

    for n in range(1, 22):
        pygame.draw.rect(win, grid_color, [leftbar, topbar + ((grid + squaresize) * (n - 1)),
                                           game_w, grid])

    piece.ghost()

    g1s = pygame.Surface([squaresize, squaresize])
    g2s = pygame.Surface([squaresize, squaresize])
    g3s = pygame.Surface([squaresize, squaresize])
    g4s = pygame.Surface([squaresize, squaresize])

    pygame.draw.rect(g1s, piece.color, [0, 0, squaresize, squaresize])
    pygame.draw.rect(g2s, piece.color, [0, 0, squaresize, squaresize])
    pygame.draw.rect(g3s, piece.color, [0, 0, squaresize, squaresize])
    pygame.draw.rect(g4s, piece.color, [0, 0, squaresize, squaresize])

    g1s.set_alpha(50)
    g2s.set_alpha(50)
    g3s.set_alpha(50)
    g4s.set_alpha(50)

    win.blit(g1s, [piece.gx1, piece.gy1])
    win.blit(g2s, [piece.gx2, piece.gy2])
    win.blit(g3s, [piece.gx3, piece.gy3])
    win.blit(g2s, [piece.gx4, piece.gy4])

    for y in range(0, len(board)):
        for x in range(1, len(board[y])):
            if board[y][x] != 0:
                if board[y][x] == "I":
                    clr = [0, 255, 255]
                elif board[y][x] == "O":
                    clr = [255, 255, 0]
                elif board[y][x] == "T":
                    clr = [255, 0, 255]
                elif board[y][x] == "S":
                    clr = [0, 255, 0]
                elif board[y][x] == "Z":
                    clr = [255, 0, 0]
                elif board[y][x] == "J":
                    clr = [0, 0, 255]
                elif board[y][x] == "L":
                    clr = [255, 128, 0]
                else:
                    clr = [255, 255, 255]
                pygame.draw.rect(win, clr, [leftbar + ((x - 1) * (squaresize + grid)),
                                            topbar + ((y - 21) * (squaresize + grid)),
                                            squaresize, squaresize])

    piece.xy_update()

    pygame.draw.rect(win, piece.color, [piece.x1, piece.y1, squaresize, squaresize])
    pygame.draw.rect(win, piece.color, [piece.x2, piece.y2, squaresize, squaresize])
    pygame.draw.rect(win, piece.color, [piece.x3, piece.y3, squaresize, squaresize])
    pygame.draw.rect(win, piece.color, [piece.x4, piece.y4, squaresize, squaresize])

    pygame.draw.rect(win, sidebarcolor, [0, 0, leftbar, win_h])
    pygame.draw.rect(win, sidebarcolor, [leftbar + game_w, 0, rightbar, win_h])

    holdfont = pygame.font.Font("Chunkfive.otf", 20)
    holdtext = holdfont.render("Hold", 1, [0, 0, 0])
    win.blit(holdtext, [leftbar - ((tiny_sqr + grid) * 5) + ((tiny_sqr + grid) * 4) / 2 - holdtext.get_rect()[2] / 2,
                        topbar + 10])
    pygame.draw.rect(win, [0, 0, 0], [leftbar - ((tiny_sqr + grid) * 5), topbar + 5 + holdtext.get_rect()[3] + 1,
                                      (tiny_sqr + grid) * 4 + grid, (tiny_sqr + grid) * 4 + grid])
    if holdpce != 0:
        if holdpce.name == "I":
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + (tiny_sqr + grid) * 1,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + (tiny_sqr + grid) * 3,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2,
                                                  tiny_sqr, tiny_sqr])
        if holdpce.name == "O":
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + (tiny_sqr + grid) * 1,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 +
                                                  grid + (tiny_sqr + grid) * 1,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 +
                                                  grid + (tiny_sqr + grid) * 1,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + (tiny_sqr + grid) * 1,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 +
                                                  grid + (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 +
                                                  grid + (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
        if holdpce.name == "J":
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
        if holdpce.name == "L":
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
        if holdpce.name == "T":
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
        if holdpce.name == "S":
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  tiny_sqr + grid,
                                                  tiny_sqr, tiny_sqr])
        if holdpce.name == "Z":
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  tiny_sqr + grid,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, holdpce.color, [leftbar - ((tiny_sqr + grid) * 5) + grid + tiny_sqr / 2 +
                                                  (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2,
                                                  tiny_sqr, tiny_sqr])

    nextfont = pygame.font.Font("Chunkfive.otf", 20)
    nexttext = nextfont.render("Next", 1, [0, 0, 0])
    win.blit(nexttext, [leftbar + game_w + ((tiny_sqr + grid) * 1) +
                        ((tiny_sqr + grid) * 4) / 2 - nexttext.get_rect()[2] / 2,
                        topbar + 10])
    pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1),
                                      topbar + 5 + nexttext.get_rect()[3] + 1,
                                      (tiny_sqr + grid) * 4 + grid, (tiny_sqr + grid) * 4 + grid])

    if bag[1] == 1:
        pygame.draw.rect(win, [0, 255, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [0, 255, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + (tiny_sqr + grid) * 1,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [0, 255, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + (tiny_sqr + grid) * 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [0, 255, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + (tiny_sqr + grid) * 3,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2,
                                              tiny_sqr, tiny_sqr])
    if bag[1] == 2:
        pygame.draw.rect(win, [255, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + (tiny_sqr + grid) * 1,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 +
                                              grid + (tiny_sqr + grid) * 1,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + (tiny_sqr + grid) * 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 +
                                              grid + (tiny_sqr + grid) * 1,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + (tiny_sqr + grid) * 1,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 +
                                              grid + (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + (tiny_sqr + grid) * 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 +
                                              grid + (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
    if bag[1] == 6:
        pygame.draw.rect(win, [0, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [0, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [0, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              tiny_sqr + grid,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [0, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              (tiny_sqr + grid) * 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
    if bag[1] == 7:
        pygame.draw.rect(win, [255, 128, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              (tiny_sqr + grid) * 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 128, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 128, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              tiny_sqr + grid,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 128, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              (tiny_sqr + grid) * 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
    if bag[1] == 3:
        pygame.draw.rect(win, [255, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              tiny_sqr + grid,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              tiny_sqr + grid,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              (tiny_sqr + grid) * 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
    if bag[1] == 4:
        pygame.draw.rect(win, [0, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              tiny_sqr + grid,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [0, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [0, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              tiny_sqr + grid,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [0, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              (tiny_sqr + grid) * 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              tiny_sqr + grid,
                                              tiny_sqr, tiny_sqr])
    if bag[1] == 5:
        pygame.draw.rect(win, [255, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              tiny_sqr + grid,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              tiny_sqr + grid,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              tiny_sqr + grid,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])
        pygame.draw.rect(win, [255, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1) + grid + tiny_sqr / 2 +
                                              (tiny_sqr + grid) * 2,
                                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                              (tiny_sqr + grid) * 2,
                                              tiny_sqr, tiny_sqr])

    for i in range(2, 7):
        pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2),
                                          topbar + 5 + nexttext.get_rect()[3] + 1 +
                                          (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                          (tiny_sqr + grid) * 4 + grid, (tiny_sqr + grid) * 4 + grid])
        if bag[i] == 1:
            pygame.draw.rect(win, [0, 255, 255],
                             [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2 +
                              (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [0, 255, 255],
                             [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + (tiny_sqr + grid) * 1,
                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                              ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2 +
                              (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                              tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [0, 255, 255],
                             [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + (tiny_sqr + grid) * 2,
                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                              ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2 +
                              (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                              tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [0, 255, 255],
                             [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + (tiny_sqr + grid) * 3,
                              topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                              ((tiny_sqr + grid) * 4) / 2 - tiny_sqr / 2 +
                              (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                              tiny_sqr, tiny_sqr])
        if bag[i] == 2:
            pygame.draw.rect(win, [255, 255, 0],
                             [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + (tiny_sqr + grid) * 1,
                              topbar + 5 + holdtext.get_rect()[3] + 1 +
                              grid + (tiny_sqr + grid) * 1 + (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                              tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 255, 0],
                             [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + (tiny_sqr + grid) * 2,
                              topbar + 5 + holdtext.get_rect()[3] + 1 +
                              grid + (tiny_sqr + grid) * 1 + (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                              tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 255, 0],
                             [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + (tiny_sqr + grid) * 1,
                              topbar + 5 + holdtext.get_rect()[3] + 1 +
                              grid + (tiny_sqr + grid) * 2 + (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                              tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 255, 0],
                             [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + (tiny_sqr + grid) * 2,
                              topbar + 5 + holdtext.get_rect()[3] + 1 +
                              grid + (tiny_sqr + grid) * 2 + (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                              tiny_sqr, tiny_sqr])
        if bag[i] == 6:
            pygame.draw.rect(win, [0, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [0, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                (tiny_sqr + grid) * 2 +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [0, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                tiny_sqr + grid,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                (tiny_sqr + grid) * 2 +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [0, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                (tiny_sqr + grid) * 2,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                (tiny_sqr + grid) * 2 +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
        if bag[i] == 7:
            pygame.draw.rect(win, [255, 128, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                  (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid +
                                                  (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 128, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2 +
                                                  (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 128, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2 +
                                                  (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 128, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                  (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2 +
                                                  (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                  tiny_sqr, tiny_sqr])
        if bag[i] == 3:
            pygame.draw.rect(win, [255, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid +
                                                  (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2 +
                                                  (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                  tiny_sqr + grid,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2 +
                                                  (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                  tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 0, 255], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                  (tiny_sqr + grid) * 2,
                                                  topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                  (tiny_sqr + grid) * 2 +
                                                  (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                  tiny_sqr, tiny_sqr])
        if bag[i] == 4:
            pygame.draw.rect(win, [0, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                tiny_sqr + grid,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [0, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                (tiny_sqr + grid) * 2 +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [0, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                tiny_sqr + grid,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                (tiny_sqr + grid) * 2 +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [0, 255, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                (tiny_sqr + grid) * 2,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                tiny_sqr + grid +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
        if bag[i] == 5:
            pygame.draw.rect(win, [255, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                tiny_sqr + grid,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid + tiny_sqr + grid +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                tiny_sqr + grid + (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                tiny_sqr + grid,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                (tiny_sqr + grid) * 2 +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])
            pygame.draw.rect(win, [255, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2) + grid + tiny_sqr / 2 +
                                                (tiny_sqr + grid) * 2,
                                                topbar + 5 + holdtext.get_rect()[3] + 1 + grid +
                                                (tiny_sqr + grid) * 2 +
                                                (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                                tiny_sqr, tiny_sqr])

    pygame.draw.rect(win, sidebarcolor, [0, 0, win_w, topbar])
    pygame.draw.rect(win, sidebarcolor, [0, topbar + game_h, win_w, botbar])

    pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50, topbar + game_h + 10, 100, 50])
    if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
            topbar + game_h + 10 <= mouse[1] <= topbar + game_h + 10 + 50):
        pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 50 + 5, topbar + game_h + 10 + 5, 90, 40])
    else:
        pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5, topbar + game_h + 10 + 5, 90, 40])
    pausefont = pygame.font.Font("Chunkfive.otf", 28)
    pausetext = pausefont.render("Pause", 1, [0, 0, 0])
    win.blit(pausetext, [win_w / 2 - pausetext.get_rect()[2] / 2,
                         topbar + game_h + 10 + 25 - pausetext.get_rect()[3] / 2 + 4])

    stris = pygame.Surface([500, 500])
    stris.fill([10, 10, 10])
    stris.set_colorkey([10, 10, 10])
    strisfont = pygame.font.Font("Chunkfive.otf", 75)
    stext = strisfont.render("S", 0, [0, 255, 0])
    tritext = strisfont.render("tri", 0, [0, 0, 0])
    stris.blit(stext, [0, 0])
    stris.blit(tritext, [stext.get_rect()[2], 0])
    stris.blit(stext, [stext.get_rect()[2] + tritext.get_rect()[2], 0])

    win.blit(stris, [win_w / 2 - (stext.get_rect()[2] + stext.get_rect()[2] + tritext.get_rect()[2]) / 2, 10])

    if gamemode == "marathon":
        gamemodefont = pygame.font.Font("opensans.ttf", 30)
        gamemodetext = gamemodefont.render("- Marathon -", 1, [0, 0, 0])
        win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])
    if gamemode == "ultra":
        gamemodefont = pygame.font.Font("opensans.ttf", 30)
        gamemodetext = gamemodefont.render("- Ultra -", 1, [0, 0, 0])
        win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])
    if gamemode == "sprint":
        gamemodefont = pygame.font.Font("opensans.ttf", 30)
        gamemodetext = gamemodefont.render("- Sprint -", 1, [0, 0, 0])
        win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])
    if gamemode == "endless":
        gamemodefont = pygame.font.Font("opensans.ttf", 30)
        gamemodetext = gamemodefont.render("- Endless -", 1, [0, 0, 0])
        win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])

    pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid - 5, win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 5,
                                            (tiny_sqr + grid) * 6 + 10, (squaresize + 5 + grid) * 8 + 10])
    pygame.draw.rect(win, [0, 0, 0], [tiny_sqr + grid, win_h - topbar - 10 - (squaresize + 5 + grid) * 8,
                                            (tiny_sqr + grid) * 6, (squaresize + 5 + grid) * 8])
    pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                            win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5,
                                            (tiny_sqr + grid) * 6, 1])
    pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                            win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5 +
                                            (grid + squaresize + 5) * 1,
                                            (tiny_sqr + grid) * 6, 1])
    pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                            win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5 +
                                            (grid + squaresize + 5) * 3,
                                            (tiny_sqr + grid) * 6, 1])
    pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                            win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5 +
                                            (grid + squaresize + 5) * 5,
                                            (tiny_sqr + grid) * 6, 1])
    levellabelfont = pygame.font.Font("Chunkfive.otf", 25)
    levellabeltext = levellabelfont.render("Level:", 1, [255, 255, 255])
    win.blit(levellabeltext, [tiny_sqr + grid + 3, win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 8])
    levelfont = pygame.font.Font("opensans.ttf", 23)
    leveltext = levelfont.render(str(level), 1, [255, 255, 255])
    win.blit(leveltext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - leveltext.get_rect()[2] - 2),
                              win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + 3])
    lineslabelfont = pygame.font.Font("Chunkfive.otf", 25)
    lineslabeltext = lineslabelfont.render("Lines:", 1, [255, 255, 255])
    win.blit(lineslabeltext, [tiny_sqr + grid + 3,
                              win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2])
    lns = str(lines)
    if lines >= 999:
        lns = str(999)
    linesfont = pygame.font.Font("opensans.ttf", 23)
    linestext = linesfont.render(lns, 1, [255, 255, 255])
    win.blit(linestext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - linestext.get_rect()[2] - 2),
                         win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 + 3])
    scorelabelfont = pygame.font.Font("Chunkfive.otf", 25)
    scorelabeltext = scorelabelfont.render("Score:", 1, [255, 255, 255])
    win.blit(scorelabeltext, [tiny_sqr + grid + 3,
                              win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                              (grid + squaresize + 5) * 1])
    scr = str(score)
    if score >= 999999:
        scr = str(999999)
    scorefont = pygame.font.Font("opensans.ttf", 30)
    scoretext = scorefont.render(scr, 1, [255, 255, 255])
    win.blit(scoretext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - scoretext.get_rect()[2]) - 8,
                         win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 +
                         (grid + squaresize + 5) * 2 - 8])
    bestlabelfont = pygame.font.Font("Chunkfive.otf", 25)
    bestlabeltext = bestlabelfont.render("Best:", 1, [255, 255, 255])
    win.blit(bestlabeltext, [tiny_sqr + grid + 3,
                              win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                              (grid + squaresize + 5) * 3])
    bestlist = get_scores()
    if gamemode == "sprint":
        if bestlist[1] == -1:
            besty = "--:--:---"
        else:
            besty = milliseconds(bestlist[1])
            if len(str(besty[0])) < 2:
                minutes = "0" + str(besty[0])
            else:
                minutes = str(besty[0])
            if len(str(besty[1])) < 2:
                seconds = "0" + str(besty[1])
            else:
                seconds = str(besty[1])
            if len(str(besty[2])) == 2:
                milli = "0" + str(besty[2])
            elif len(str(besty[2])) < 2:
                milli = "00" + str(besty[2])
            else:
                milli = str(besty[2])
            besty = minutes + ":" + seconds + ":" + milli
    elif gamemode == "marathon":
        if bestlist[0] == -1:
            besty = "0"
        else:
            besty = str(bestlist[0])
    elif gamemode == "ultra":
        if bestlist[2] == -1:
            besty = "0"
        else:
            besty = str(bestlist[2])
    else:
        if bestlist[3] == -1:
            besty = "0"
        else:
            besty = str(bestlist[3])
    if gamemode != "sprint":
        if int(besty) >= 999999:
            besty = str(999999)
    if gamemode == "sprint" and bestlist[1] != -1:
        bestfont = pygame.font.Font("opensans.ttf", 25)
        besttext = bestfont.render(besty, 1, [255, 255, 255])
        win.blit(besttext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - besttext.get_rect()[2]) - 8 + 4,
                            win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 +
                            (grid + squaresize + 5) * 4 - 8 + 4])
    else:
        bestfont = pygame.font.Font("opensans.ttf", 30)
        besttext = bestfont.render(besty, 1, [255, 255, 255])
        win.blit(besttext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - besttext.get_rect()[2]) - 8,
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 +
                             (grid + squaresize + 5) * 4 - 8])
    timestr = milliseconds(time)
    if len(str(timestr[0])) < 2:
        minutes = "0" + str(timestr[0])
    else:
        minutes = str(timestr[0])
    if len(str(timestr[1])) < 2:
        seconds = "0" + str(timestr[1])
    else:
        seconds = str(timestr[1])
    if len(str(timestr[2])) == 2:
        milli = "0" + str(timestr[2])
    elif len(str(timestr[2])) < 2:
        milli = "00" + str(timestr[2])
    else:
        milli = str(timestr[2])
    timestr1 = minutes + ":" + seconds
    timestr2 = milli
    timestr1font = pygame.font.Font("opensans.ttf", 40)
    timestr1text = timestr1font.render(timestr1, 1, [255, 255, 255])
    win.blit(timestr1text, [tiny_sqr + grid + ((tiny_sqr + grid) * 6) / 2 - timestr1text.get_rect()[2] / 2,
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                             (grid + squaresize + 5) * 5 - 8])
    timestr2font = pygame.font.Font("opensans.ttf", 25)
    timestr2text = timestr2font.render(timestr2, 1, [255, 255, 255])
    timestr2surf = pygame.Surface([100, 100])
    timestr2surf.set_colorkey([0, 0, 0])
    timestr2surf.blit(timestr2text, [0, 0])
    timestr2surf.set_alpha(100)
    win.blit(timestr2surf, [tiny_sqr + grid + ((tiny_sqr + grid) * 6) / 2 + 5,
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                             (grid + squaresize + 5) * 5 - 8 + 40])

    pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid - 5,
                                            win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 5 -
                                            (squaresize + 5 + grid) - (squaresize + grid),
                                            (tiny_sqr + grid) * 6 + 10,
                                            (squaresize + 5 + grid) + 10])

    pygame.draw.rect(win, [0, 0, 0], [tiny_sqr + grid,
                                      win_h - topbar - 10 - (squaresize + 5 + grid) * 8 -
                                      (squaresize + 5 + grid) - (squaresize + grid),
                                      (tiny_sqr + grid) * 6,
                                      (squaresize + 5 + grid)])

    combolabelfont = pygame.font.Font("Chunkfive.otf", 23)
    combolabeltext = combolabelfont.render("Combo:", 1, [255, 255, 255])
    win.blit(combolabeltext, [tiny_sqr + grid + 3,
                              win_h - topbar - 10 - (squaresize + 5 + grid) * 8 -
                              (squaresize + 5 + grid) - (squaresize + grid) + 8])
    combofont = pygame.font.Font("opensans.ttf", 30)
    combotext = combolabelfont.render(str(combocount), 1, [255, 255, 255])
    win.blit(combotext, [tiny_sqr + grid + (tiny_sqr + grid) * 6 - combotext.get_rect()[2] - 3,
                         win_h - topbar - 10 - (squaresize + 5 + grid) * 8 -
                         (squaresize + 5 + grid) - (squaresize + grid) + 8])

    if lastclear != 0:
        if b2b > 1:
            b2bfont = pygame.font.Font("Chunkfive.otf", 20)
            b2btext = b2bfont.render("Back-to-Back", 1, [0, 0, 0])
            win.blit(b2btext, [leftbar / 2 - b2btext.get_rect()[2] / 2, 250])
        clearfont = pygame.font.Font("Chunkfive.otf", 30)
        cleartext = clearfont.render(lastclear, 1, [0, 0, 0])
        win.blit(cleartext, [leftbar / 2 - cleartext.get_rect()[2] / 2, 275])

    tspinfont = pygame.font.Font("Chunkfive.otf", 20)
    minifont = pygame.font.Font("Chunkfive.otf", 15)
    tspintext = tspinfont.render("T-Spin", 1, [0, 0, 0])
    minitext = minifont.render("mini", 1, [0, 0, 0])

    if lastclear != 0:
        if tspin == 1:
            win.blit(tspintext, [leftbar / 2 - tspintext.get_rect()[2] / 2, 310])
            win.blit(minitext, [leftbar / 2 - minitext.get_rect()[2] / 2, 335])
        if tspin == 2:
            win.blit(tspintext, [leftbar / 2 - tspintext.get_rect()[2] / 2, 310])

    """
    testfont = pygame.font.SysFont("0", 20)

    for i in range(0, len(board)):
        for x in range(0, len(board[i])):
            testtext = testfont.render(str(board[i][x]), 1, [255, 255, 255])
            win.blit(testtext, [(x - 1) * (squaresize + grid), (i - 21) * (squaresize + grid)])
    """

    """
    testfont = pygame.font.SysFont("0", 20)
    test1 = testfont.render("1", 1, [0, 0, 0])
    test2 = testfont.render("2", 1, [0, 0, 0])
    test3 = testfont.render("3", 1, [0, 0, 0])
    test4 = testfont.render("4", 1, [0, 0, 0])

    win.blit(test1, [piece.x1, piece.y1])
    win.blit(test2, [piece.x2, piece.y2])
    win.blit(test3, [piece.x3, piece.y3])
    win.blit(test4, [piece.x4, piece.y4])
    """


def randomizer():
    global bag
    temp1 = [1, 2, 3, 4, 5, 6, 7]
    temp2 = list(temp1)

    random.shuffle(temp1)
    random.shuffle(temp2)

    for pce in temp1:
        bag.append(pce)

    for pce in temp2:
        bag.append(pce)


def lineclear():
    global board
    global lines
    global b2b
    global score
    global level
    global combocount
    global lastclear
    global tspin

    linesl = []

    for y in range(0, len(board)):
        clear = 1
        for x in range(0, len(board[y])):
            if board[y][x] == 0:
                clear = 0
        if clear == 1:
            linesl.append(y)

    for i in linesl:
        board[i] = ["X", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    drop = []

    for i in range(0, 41):
        drop.append(0)

    for i in linesl:
        for x in range(0, i + 1):
            drop[x] += 1

    new_board = []

    for i in range(0, 41):
        new_board.append(["X", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    new_board.append("bottom")
    new_board.append("bottom")
    new_board.append("bottom")
    new_board.append("bottom")

    for i in range(0, len(board)):
        new_board[i + drop[i]] = board[i]

    board = list(new_board)
    board.pop(-1)
    board.pop(-1)
    board.pop(-1)
    board.pop(-1)

    lines += len(linesl)

    if tspin == 1:
        if b2b == 0:
            score += 100 * level
        else:
            score += 150 * level

    if tspin == 2:
        score += 400 * level

    if len(linesl) == 1:
        score += 100 * level
        score += 20 * combocount * level
        combocount += 1
        lastclear = "Single"
        if tspin == 2:
            if b2b == 0:
                score += 300 * level
            else:
                score += 700 * level
    elif len(linesl) == 2:
        score += 300 * level
        score += 50 * combocount * level
        combocount += 1
        lastclear = "Double"
        if tspin == 2:
            if b2b == 0:
                score += 500 * level
            else:
                score += 1100 * level
    elif len(linesl) == 3:
        score += 500 * level
        score += 50 * combocount * level
        combocount += 1
        lastclear = "Triple"
        if tspin == 2:
            if b2b == 0:
                score += 700 * level
            else:
                score += 1500 * level
    elif len(linesl) >= 4:
        if b2b == 0:
            score += 800 * level
        else:
            score += 1200 * level
        score += 50 * combocount * level
        combocount += 1
        lastclear = "Tetris"
    else:
        combocount = 0
        lastclear = 0

    if len(linesl) > 0:
        if len(linesl) >= 4:
            b2b += 1
        elif tspin == 1:
            b2b += 1
        elif tspin == 2:
            b2b += 1
        else:
            b2b = 0
    elif tspin == 1:
        b2b += 1
    elif tspin == 2:
        b2b += 1


def tspintest():
    global tspin
    global piece
    if piece.name == "T":
        if piece.lastmove == 1:
            spn = []
            if piece.two[1] + 1 > 20 or piece.two[0] + 1 > 10:
                spn.append(1)
            else:
                if board[piece.two[1] + 20 + 1][piece.two[0] + 1] != 0:
                    spn.append(1)
            if piece.two[1] + 1 > 20 or piece.two[0] - 1 < 1:
                spn.append(1)
            else:
                if board[piece.two[1] + 20 + 1][piece.two[0] - 1] != 0:
                    spn.append(1)
            if piece.two[0] + 1 > 10:
                spn.append(1)
            else:
                if board[piece.two[1] + 20 - 1][piece.two[0] + 1] != 0:
                    spn.append(1)
            if piece.two[0] - 1 < 1:
                spn.append(1)
            else:
                if board[piece.two[1] + 20 - 1][piece.two[0] - 1] != 0:
                    spn.append(1)
            if len(spn) >= 3:
                tspin = 1
            else:
                tspin = 0
        else:
            tspin = 0
    else:
        tspin = 0

    if tspin == 1:
        minitest = []
        if piece.rot == 1:
            # Facing up
            if piece.four[0] + 1 > 10:
                minitest.append(1)
            else:
                if board[piece.four[1] + 20][piece.four[0] + 1] != 0:
                    minitest.append(1)
            if piece.four[0] - 1 < 1:
                minitest.append(1)
            else:
                if board[piece.four[1] + 20][piece.four[0] - 1] != 0:
                    minitest.append(1)
        if piece.rot == 2:
            # Facing right
            if piece.four[1] + 1 > 20:
                minitest.append(1)
            else:
                if board[piece.four[1] + 20 + 1][piece.four[0]] != 0:
                    minitest.append(1)
            if board[piece.four[1] + 20 - 1][piece.four[0]] != 0:
                minitest.append(1)
        if piece.rot == 3:
            # Facing down
            if piece.four[0] + 1 > 10:
                minitest.append(1)
            else:
                if board[piece.four[1] + 20][piece.four[0] + 1] != 0:
                    minitest.append(1)
            if piece.four[0] - 1 < 1:
                minitest.append(1)
            else:
                if board[piece.four[1] + 20][piece.four[0] - 1] != 0:
                    minitest.append(1)
        if piece.rot == 4:
            # Facing left
            if piece.four[1] + 1 > 20:
                minitest.append(1)
            else:
                if board[piece.four[1] + 20 + 1][piece.four[0]] != 0:
                    minitest.append(1)
            if board[piece.four[1] + 20 - 1][piece.four[0]] != 0:
                minitest.append(1)
        if len(minitest) >= 2:
            tspin = 2

    if tspin == 1:
        if piece.bigmini == 1:
            tspin = 2


def holdf():
    global holdpce
    global piece
    global bag
    global can_hold
    global hold_opt

    if hold_opt == 1:
        if can_hold == 1:
            if holdpce == 0:
                holdpce = Piece(piece.p)
                bag.pop(0)
                piece = Piece(bag[0])
            else:
                bag[0] = holdpce.p
                holdpce = Piece(piece.p)
                piece = Piece(bag[0])
        can_hold = 0


def gameover():
    while 1:
        clock.tick(fps)
        mouse = pygame.mouse.get_pos()

        piece.xy_update()
        if piece.one[1] > 0:
            pygame.draw.rect(win, piece.color, [piece.x1, piece.y1, squaresize, squaresize])
        if piece.two[1] > 0:
            pygame.draw.rect(win, piece.color, [piece.x2, piece.y2, squaresize, squaresize])
        if piece.three[1] > 0:
            pygame.draw.rect(win, piece.color, [piece.x3, piece.y3, squaresize, squaresize])
        if piece.four[1] > 0:
            pygame.draw.rect(win, piece.color, [piece.x4, piece.y4, squaresize, squaresize])

        pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                topbar + game_h / 2 - 126, 282, 252])
        pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140, topbar + game_h / 2 - 100 - 25, 280, 200 + 50])
        pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                topbar + game_h / 2 - 100 + 5 - 25, 270, 190 + 50])
        gameoverfont = pygame.font.Font("Chunkfive.otf", 48)
        gameovertext = gameoverfont.render("Game Over", 1, [0, 0, 0])
        win.blit(gameovertext, [win_w / 2 - gameovertext.get_rect()[2] / 2, topbar + game_h / 2 - 100 + 5 + 50 - 40])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50,
                                          topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 - 25,
                                          100, 50])
        if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                (topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 - 25 <= mouse[1] <=
                    topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 - 25)):
                pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 50 + 5,
                                                       topbar + game_h / 2 - 100 + 5 + 50 +
                                                       gameovertext.get_rect()[3] + 10 + 5 - 25,
                                                       90, 40])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   gameovertext.get_rect()[3] + 10 + 5 - 25,
                                                   90, 40])
        menufont = pygame.font.Font("Chunkfive.otf", 30)
        menutext = menufont.render("Menu", 1, [0, 0, 0])
        win.blit(menutext, [win_w / 2 - menutext.get_rect()[2] / 2,
                               topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 12 - 25])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50,
                                          topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 +
                                          50 + 15 - 25,
                                          100, 50])
        if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                (topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 + 15 - 25 <= mouse[1] <=
                 topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 + 50 + 15 - 25)):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   gameovertext.get_rect()[3] + 10 + 5 + 50 + 15 - 25,
                                                   90, 40])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   gameovertext.get_rect()[3] + 10 + 5 + 50 + 15 - 25,
                                                   90, 40])
        restartfont = pygame.font.Font("Chunkfive.otf", 25)
        restarttext = restartfont.render("Restart", 1, [0, 0, 0])
        win.blit(restarttext, [win_w / 2 - restarttext.get_rect()[2] / 2,
                            topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 14 + 50 + 15 - 25])

        if gamemode == "endless":
            pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                    topbar + game_h / 2 - 126 - 110, 282, 100])
            pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140,
                                              topbar + game_h / 2 - 125 - 110, 280, 98])
            pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                    topbar + game_h / 2 - 125 - 110 + 5, 270, 88])
            scorelabelfont = pygame.font.Font("Chunkfive.otf", 35)
            scorelabeltext = scorelabelfont.render("Score:", 1, [0, 0, 0])
            win.blit(scorelabeltext, [win_w / 2 - scorelabeltext.get_rect()[2] / 2,
                                                    topbar + game_h / 2 - 125 - 110 + 5 + 10])
            scorefont = pygame.font.Font("opensans.ttf", 30)
            scoretext = scorefont.render(str(score), 1, [0, 0, 0])
            win.blit(scoretext, [win_w / 2 - scoretext.get_rect()[2] / 2,
                                      topbar + game_h / 2 - 125 - 110 + 5 + 10 + 30])
            bestlist = get_scores()
            if bestlist[3] == -1 or score > bestlist[3]:
                pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                        topbar + game_h / 2 - 126 - 110 +
                                                        100 + 10 + 252 + 10, 282, 100])
                pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140,
                                                  topbar + game_h / 2 - 125 - 110 +
                                                  100 + 10 + 252 + 10, 280, 98])
                pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                        topbar + game_h / 2 - 125 - 110 + 5 +
                                                        100 + 10 + 252 + 10, 270, 88])
                congratsfont = pygame.font.Font("Chunkfive.otf", 30)
                congratstext = congratsfont.render("Congratulations!", 1, [0, 0, 0])
                win.blit(congratstext, [win_w / 2 - congratstext.get_rect()[2] / 2,
                                          topbar + game_h / 2 - 125 - 110 + 5 + 10 + 100 + 10 + 252 + 10])
                beatfont = pygame.font.Font("Chunkfive.otf", 20)
                beattext = beatfont.render("You beat the high score!", 1, [0, 0, 0])
                win.blit(beattext, [win_w / 2 - beattext.get_rect()[2] / 2,
                                        topbar + game_h / 2 - 125 - 110 + 5 + 10 + 100 + 10 + 252 + 10 + 40])

                update_scores(score, gamemode, bestlist)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                            (topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 - 25 <= mouse[1] <=
                             topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 - 25)):
                        mainmenu()
                    if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                            (topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 + 15 - 25 <=
                             mouse[1] <=
                             topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 + 50 + 15 - 25)):
                        newgame()


def newgame():
    global can_hold
    global holdpce
    global bag
    global level
    global norm_fall
    global soft_fall
    global board
    global time
    global lines
    global score
    global piece
    global b2b
    global combocount
    global lastclear
    global tspin

    apply_options()

    can_hold = 1
    holdpce = 0

    bag = []

    level = 1

    norm_fall = int((0.8 - ((level - 1) * 0.007)) ** (level - 1) / (1 / fps))
    soft_fall = int(norm_fall / 20)

    board = []

    for n in range(0, 41):
        board.append(["X", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    time = 0
    lines = 0
    score = 0
    b2b = 0
    combocount = 0
    tspin = 0
    lastclear = 0

    randomizer()
    piece = Piece(bag[0])

    threefont = pygame.font.Font("Chunkfive.otf", 100)
    twofont = pygame.font.Font("Chunkfive.otf", 100)
    onefont = pygame.font.Font("Chunkfive.otf", 100)
    threetext = threefont.render("3", 1, [255, 0, 0])
    twotext = twofont.render("2", 1, [255, 128, 0])
    onetext = onefont.render("1", 1, [0, 255, 0])
    framecount = 0

    while 1:
        clock.tick(fps)
        drawgame()

        if framecount < 30:
            win.blit(threetext, [win_w / 2 - threetext.get_rect()[2] / 2, win_h / 2 - threetext.get_rect()[3] / 2])
        elif framecount < 60:
            win.blit(twotext, [win_w / 2 - twotext.get_rect()[2] / 2, win_h / 2 - twotext.get_rect()[3] / 2])
        elif framecount < 90:
            win.blit(onetext, [win_w / 2 - onetext.get_rect()[2] / 2, win_h / 2 - onetext.get_rect()[3] / 2])

        if framecount >= 90:
            game()
        else:
            framecount += 1

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


def pausemenu():
    while 1:
        clock.tick(fps)
        mouse = pygame.mouse.get_pos()

        win.fill(bg_color)

        mouse = pygame.mouse.get_pos()

        for n in range(1, 12):
            pygame.draw.rect(win, grid_color, [leftbar + ((grid + squaresize) * (n - 1)),
                                               topbar, grid, game_h])

        for n in range(1, 22):
            pygame.draw.rect(win, grid_color, [leftbar, topbar + ((grid + squaresize) * (n - 1)),
                                               game_w, grid])

        pygame.draw.rect(win, sidebarcolor, [0, 0, leftbar, win_h])
        pygame.draw.rect(win, sidebarcolor, [leftbar + game_w, 0, rightbar, win_h])

        holdfont = pygame.font.Font("Chunkfive.otf", 20)
        holdtext = holdfont.render("Hold", 1, [0, 0, 0])
        win.blit(holdtext,
                 [leftbar - ((tiny_sqr + grid) * 5) + ((tiny_sqr + grid) * 4) / 2 - holdtext.get_rect()[2] / 2,
                  topbar + 10])
        pygame.draw.rect(win, [0, 0, 0], [leftbar - ((tiny_sqr + grid) * 5), topbar + 5 + holdtext.get_rect()[3] + 1,
                                          (tiny_sqr + grid) * 4 + grid, (tiny_sqr + grid) * 4 + grid])

        nextfont = pygame.font.Font("Chunkfive.otf", 20)
        nexttext = nextfont.render("Next", 1, [0, 0, 0])
        win.blit(nexttext, [leftbar + game_w + ((tiny_sqr + grid) * 1) +
                            ((tiny_sqr + grid) * 4) / 2 - nexttext.get_rect()[2] / 2,
                            topbar + 10])
        pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1),
                                          topbar + 5 + nexttext.get_rect()[3] + 1,
                                          (tiny_sqr + grid) * 4 + grid, (tiny_sqr + grid) * 4 + grid])

        pygame.draw.rect(win, sidebarcolor, [0, 0, win_w, topbar])
        pygame.draw.rect(win, sidebarcolor, [0, topbar + game_h, win_w, botbar])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50, topbar + game_h + 10, 100, 50])
        pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5, topbar + game_h + 10 + 5, 90, 40])
        pausefont = pygame.font.Font("Chunkfive.otf", 28)
        pausetext = pausefont.render("Pause", 1, [0, 0, 0])
        win.blit(pausetext, [win_w / 2 - pausetext.get_rect()[2] / 2,
                             topbar + game_h + 10 + 25 - pausetext.get_rect()[3] / 2 + 4])

        for i in range(2, 7):
            pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2),
                                              topbar + 5 + nexttext.get_rect()[3] + 1 +
                                              (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                              (tiny_sqr + grid) * 4 + grid, (tiny_sqr + grid) * 4 + grid])

        pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                topbar + game_h / 2 - 126 - 60, 282, 252 + 60])
        pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140, topbar + game_h / 2 - 100 - 25 - 60,
                                          280, 200 + 50 + 60])
        pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                topbar + game_h / 2 - 100 + 5 - 25 - 60, 270, 190 + 50 + 60])
        pausefont = pygame.font.Font("Chunkfive.otf", 48)
        pausetext = pausefont.render("Pause", 1, [0, 0, 0])
        win.blit(pausetext, [win_w / 2 - pausetext.get_rect()[2] / 2, topbar + game_h / 2 - 100 + 5 + 50 - 40 - 60])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50,
                                          topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 - 25 - 65,
                                          100, 50])
        if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                (topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 - 25 - 65 <= mouse[1] <=
                 topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 + 50 - 25 - 65)):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   pausetext.get_rect()[3] + 10 + 5 - 25 - 65,
                                                   90, 40])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   pausetext.get_rect()[3] + 10 + 5 - 25 - 65,
                                                   90, 40])
        resumefont = pygame.font.Font("Chunkfive.otf", 22)
        resumetext = resumefont.render("Resume", 1, [0, 0, 0])
        win.blit(resumetext, [win_w / 2 - resumetext.get_rect()[2] / 2,
                              topbar + game_h / 2 - 100 + 5 + 50 +
                              pausetext.get_rect()[3] + 10 + 5 - 25 - 55])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50,
                                          topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 - 25,
                                          100, 50])
        if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                (topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 - 25 <= mouse[1] <=
                 topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 + 50 - 25)):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   pausetext.get_rect()[3] + 10 + 5 - 25,
                                                   90, 40])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   pausetext.get_rect()[3] + 10 + 5 - 25,
                                                   90, 40])
        menufont = pygame.font.Font("Chunkfive.otf", 30)
        menutext = menufont.render("Menu", 1, [0, 0, 0])
        win.blit(menutext, [win_w / 2 - menutext.get_rect()[2] / 2,
                            topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 + 12 - 25])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50,
                                          topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 +
                                          50 + 15 - 25,
                                          100, 50])
        if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                (topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 + 50 + 15 - 25 <= mouse[1] <=
                 topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 + 50 + 50 + 15 - 25)):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   pausetext.get_rect()[3] + 10 + 5 + 50 + 15 - 25,
                                                   90, 40])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   pausetext.get_rect()[3] + 10 + 5 + 50 + 15 - 25,
                                                   90, 40])
        restartfont = pygame.font.Font("Chunkfive.otf", 25)
        restarttext = restartfont.render("Restart", 1, [0, 0, 0])
        win.blit(restarttext, [win_w / 2 - restarttext.get_rect()[2] / 2,
                               topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[
                                   3] + 10 + 14 + 50 + 15 - 25])

        stris = pygame.Surface([500, 500])
        stris.fill([10, 10, 10])
        stris.set_colorkey([10, 10, 10])
        strisfont = pygame.font.Font("Chunkfive.otf", 75)
        stext = strisfont.render("S", 0, [0, 255, 0])
        tritext = strisfont.render("tri", 0, [0, 0, 0])
        stris.blit(stext, [0, 0])
        stris.blit(tritext, [stext.get_rect()[2], 0])
        stris.blit(stext, [stext.get_rect()[2] + tritext.get_rect()[2], 0])

        win.blit(stris, [win_w / 2 - (stext.get_rect()[2] + stext.get_rect()[2] + tritext.get_rect()[2]) / 2, 10])

        if gamemode == "marathon":
            gamemodefont = pygame.font.Font("opensans.ttf", 30)
            gamemodetext = gamemodefont.render("- Marathon -", 1, [0, 0, 0])
            win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])
        if gamemode == "ultra":
            gamemodefont = pygame.font.Font("opensans.ttf", 30)
            gamemodetext = gamemodefont.render("- Ultra -", 1, [0, 0, 0])
            win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])
        if gamemode == "sprint":
            gamemodefont = pygame.font.Font("opensans.ttf", 30)
            gamemodetext = gamemodefont.render("- Sprint -", 1, [0, 0, 0])
            win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])
        if gamemode == "endless":
            gamemodefont = pygame.font.Font("opensans.ttf", 30)
            gamemodetext = gamemodefont.render("- Endless -", 1, [0, 0, 0])
            win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])

        pygame.draw.rect(win, [255, 255, 255],
                         [tiny_sqr + grid - 5, win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 5,
                          (tiny_sqr + grid) * 6 + 10, (squaresize + 5 + grid) * 8 + 10])
        pygame.draw.rect(win, [0, 0, 0], [tiny_sqr + grid, win_h - topbar - 10 - (squaresize + 5 + grid) * 8,
                                          (tiny_sqr + grid) * 6, (squaresize + 5 + grid) * 8])
        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5,
                                                (tiny_sqr + grid) * 6, 1])
        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5 +
                                                (grid + squaresize + 5) * 1,
                                                (tiny_sqr + grid) * 6, 1])
        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5 +
                                                (grid + squaresize + 5) * 3,
                                                (tiny_sqr + grid) * 6, 1])
        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5 +
                                                (grid + squaresize + 5) * 5,
                                                (tiny_sqr + grid) * 6, 1])
        levellabelfont = pygame.font.Font("Chunkfive.otf", 25)
        levellabeltext = levellabelfont.render("Level:", 1, [255, 255, 255])
        win.blit(levellabeltext, [tiny_sqr + grid + 3, win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 8])
        levelfont = pygame.font.Font("opensans.ttf", 23)
        leveltext = levelfont.render(str(level), 1, [255, 255, 255])
        win.blit(leveltext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - leveltext.get_rect()[2] - 2),
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + 3])
        lineslabelfont = pygame.font.Font("Chunkfive.otf", 25)
        lineslabeltext = lineslabelfont.render("Lines:", 1, [255, 255, 255])
        win.blit(lineslabeltext, [tiny_sqr + grid + 3,
                                  win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2])
        lns = str(lines)
        if lines >= 999:
            lns = str(999)
        linesfont = pygame.font.Font("opensans.ttf", 23)
        linestext = linesfont.render(lns, 1, [255, 255, 255])
        win.blit(linestext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - linestext.get_rect()[2] - 2),
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 + 3])
        scorelabelfont = pygame.font.Font("Chunkfive.otf", 25)
        scorelabeltext = scorelabelfont.render("Score:", 1, [255, 255, 255])
        win.blit(scorelabeltext, [tiny_sqr + grid + 3,
                                  win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                                  (grid + squaresize + 5) * 1])
        scr = str(score)
        if score >= 999999:
            scr = str(999999)
        scorefont = pygame.font.Font("opensans.ttf", 30)
        scoretext = scorefont.render(scr, 1, [255, 255, 255])
        win.blit(scoretext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - scoretext.get_rect()[2]) - 8,
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 +
                             (grid + squaresize + 5) * 2 - 8])
        bestlabelfont = pygame.font.Font("Chunkfive.otf", 25)
        bestlabeltext = bestlabelfont.render("Best:", 1, [255, 255, 255])
        win.blit(bestlabeltext, [tiny_sqr + grid + 3,
                                 win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                                 (grid + squaresize + 5) * 3])
        bestlist = get_scores()
        if gamemode == "sprint":
            if bestlist[1] == -1:
                besty = "--:--:---"
            else:
                besty = milliseconds(bestlist[1])
                if len(str(besty[0])) < 2:
                    minutes = "0" + str(besty[0])
                else:
                    minutes = str(besty[0])
                if len(str(besty[1])) < 2:
                    seconds = "0" + str(besty[1])
                else:
                    seconds = str(besty[1])
                if len(str(besty[2])) == 2:
                    milli = "0" + str(besty[2])
                elif len(str(besty[2])) < 2:
                    milli = "00" + str(besty[2])
                else:
                    milli = str(besty[2])
                besty = minutes + ":" + seconds + ":" + milli
        elif gamemode == "marathon":
            if bestlist[0] == -1:
                besty = "0"
            else:
                besty = str(bestlist[0])
        elif gamemode == "ultra":
            if bestlist[2] == -1:
                besty = "0"
            else:
                besty = str(bestlist[2])
        else:
            if bestlist[3] == -1:
                besty = "0"
            else:
                besty = str(bestlist[3])
        if gamemode != "sprint":
            if int(besty) >= 999999:
                besty = str(999999)
        bestfont = pygame.font.Font("opensans.ttf", 30)
        besttext = bestfont.render(besty, 1, [255, 255, 255])
        win.blit(besttext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - besttext.get_rect()[2]) - 8,
                            win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 +
                            (grid + squaresize + 5) * 4 - 8])
        timestr = milliseconds(time)
        if len(str(timestr[0])) < 2:
            minutes = "0" + str(timestr[0])
        else:
            minutes = str(timestr[0])
        if len(str(timestr[1])) < 2:
            seconds = "0" + str(timestr[1])
        else:
            seconds = str(timestr[1])
        if len(str(timestr[2])) == 2:
            milli = "0" + str(timestr[2])
        elif len(str(timestr[2])) < 2:
            milli = "00" + str(timestr[2])
        else:
            milli = str(timestr[2])
        timestr1 = minutes + ":" + seconds
        timestr2 = milli
        timestr1font = pygame.font.Font("opensans.ttf", 40)
        timestr1text = timestr1font.render(timestr1, 1, [255, 255, 255])
        win.blit(timestr1text, [tiny_sqr + grid + ((tiny_sqr + grid) * 6) / 2 - timestr1text.get_rect()[2] / 2,
                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                                (grid + squaresize + 5) * 5 - 8])
        timestr2font = pygame.font.Font("opensans.ttf", 25)
        timestr2text = timestr2font.render(timestr2, 1, [255, 255, 255])
        timestr2surf = pygame.Surface([100, 100])
        timestr2surf.set_colorkey([0, 0, 0])
        timestr2surf.blit(timestr2text, [0, 0])
        timestr2surf.set_alpha(100)
        win.blit(timestr2surf, [tiny_sqr + grid + ((tiny_sqr + grid) * 6) / 2 + 5,
                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                                (grid + squaresize + 5) * 5 - 8 + 40])

        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid - 5,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 5 -
                                                (squaresize + 5 + grid) - (squaresize + grid),
                                                (tiny_sqr + grid) * 6 + 10,
                                                (squaresize + 5 + grid) + 10])

        pygame.draw.rect(win, [0, 0, 0], [tiny_sqr + grid,
                                          win_h - topbar - 10 - (squaresize + 5 + grid) * 8 -
                                          (squaresize + 5 + grid) - (squaresize + grid),
                                          (tiny_sqr + grid) * 6,
                                          (squaresize + 5 + grid)])

        combolabelfont = pygame.font.Font("Chunkfive.otf", 23)
        combolabeltext = combolabelfont.render("Combo:", 1, [255, 255, 255])
        win.blit(combolabeltext, [tiny_sqr + grid + 3,
                                  win_h - topbar - 10 - (squaresize + 5 + grid) * 8 -
                                  (squaresize + 5 + grid) - (squaresize + grid) + 8])
        combofont = pygame.font.Font("opensans.ttf", 30)
        combotext = combolabelfont.render(str(combocount), 1, [255, 255, 255])
        win.blit(combotext, [tiny_sqr + grid + (tiny_sqr + grid) * 6 - combotext.get_rect()[2] - 3,
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 -
                             (squaresize + 5 + grid) - (squaresize + grid) + 8])

        if lastclear != 0:
            if b2b > 1:
                b2bfont = pygame.font.Font("Chunkfive.otf", 20)
                b2btext = b2bfont.render("Back-to-Back", 1, [0, 0, 0])
                win.blit(b2btext, [leftbar / 2 - b2btext.get_rect()[2] / 2, 250])
            clearfont = pygame.font.Font("Chunkfive.otf", 30)
            cleartext = clearfont.render(lastclear, 1, [0, 0, 0])
            win.blit(cleartext, [leftbar / 2 - cleartext.get_rect()[2] / 2, 275])

        tspinfont = pygame.font.Font("Chunkfive.otf", 20)
        minifont = pygame.font.Font("Chunkfive.otf", 15)
        tspintext = tspinfont.render("T-Spin", 1, [0, 0, 0])
        minitext = minifont.render("mini", 1, [0, 0, 0])

        if lastclear != 0:
            if tspin == 1:
                win.blit(tspintext, [leftbar / 2 - tspintext.get_rect()[2] / 2, 310])
                win.blit(minitext, [leftbar / 2 - minitext.get_rect()[2] / 2, 335])
            if tspin == 2:
                win.blit(tspintext, [leftbar / 2 - tspintext.get_rect()[2] / 2, 310])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                            (topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 + 50 + 15 - 25 <= mouse[
                                1] <=
                             topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 + 50 + 50 + 15 - 25)):
                        newgame()
                    if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                            (topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 - 25 <= mouse[1] <=
                             topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 + 50 - 25)):
                        mainmenu()
                    if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                            (topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 - 25 - 65 <= mouse[1] <=
                             topbar + game_h / 2 - 100 + 5 + 50 + pausetext.get_rect()[3] + 10 + 50 - 25 - 65)):
                        resume()
                        return
            if event.type == pygame.KEYDOWN:
                if event.key == pause:
                    resume()
                    return


def resume():
    threefont = pygame.font.Font("Chunkfive.otf", 100)
    twofont = pygame.font.Font("Chunkfive.otf", 100)
    onefont = pygame.font.Font("Chunkfive.otf", 100)
    threetext = threefont.render("3", 1, [255, 0, 0])
    twotext = twofont.render("2", 1, [255, 128, 0])
    onetext = onefont.render("1", 1, [0, 255, 0])
    framecount = 0
    while 1:
        clock.tick(fps)

        win.fill(bg_color)

        for n in range(1, 12):
            pygame.draw.rect(win, grid_color, [leftbar + ((grid + squaresize) * (n - 1)),
                                               topbar, grid, game_h])

        for n in range(1, 22):
            pygame.draw.rect(win, grid_color, [leftbar, topbar + ((grid + squaresize) * (n - 1)),
                                               game_w, grid])

        pygame.draw.rect(win, sidebarcolor, [0, 0, leftbar, win_h])
        pygame.draw.rect(win, sidebarcolor, [leftbar + game_w, 0, rightbar, win_h])

        holdfont = pygame.font.Font("Chunkfive.otf", 20)
        holdtext = holdfont.render("Hold", 1, [0, 0, 0])
        win.blit(holdtext,
                 [leftbar - ((tiny_sqr + grid) * 5) + ((tiny_sqr + grid) * 4) / 2 - holdtext.get_rect()[2] / 2,
                  topbar + 10])
        pygame.draw.rect(win, [0, 0, 0], [leftbar - ((tiny_sqr + grid) * 5), topbar + 5 + holdtext.get_rect()[3] + 1,
                                          (tiny_sqr + grid) * 4 + grid, (tiny_sqr + grid) * 4 + grid])

        nextfont = pygame.font.Font("Chunkfive.otf", 20)
        nexttext = nextfont.render("Next", 1, [0, 0, 0])
        win.blit(nexttext, [leftbar + game_w + ((tiny_sqr + grid) * 1) +
                            ((tiny_sqr + grid) * 4) / 2 - nexttext.get_rect()[2] / 2,
                            topbar + 10])
        pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 1),
                                          topbar + 5 + nexttext.get_rect()[3] + 1,
                                          (tiny_sqr + grid) * 4 + grid, (tiny_sqr + grid) * 4 + grid])

        pygame.draw.rect(win, sidebarcolor, [0, 0, win_w, topbar])
        pygame.draw.rect(win, sidebarcolor, [0, topbar + game_h, win_w, botbar])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50, topbar + game_h + 10, 100, 50])
        pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5, topbar + game_h + 10 + 5, 90, 40])
        pausefont = pygame.font.Font("Chunkfive.otf", 28)
        pausetext = pausefont.render("Pause", 1, [0, 0, 0])
        win.blit(pausetext, [win_w / 2 - pausetext.get_rect()[2] / 2,
                             topbar + game_h + 10 + 25 - pausetext.get_rect()[3] / 2 + 4])

        for i in range(2, 7):
            pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w + ((tiny_sqr + grid) * 2),
                                              topbar + 5 + nexttext.get_rect()[3] + 1 +
                                              (tiny_sqr + grid) * 4 + grid + 15 + (100 * (i - 2)),
                                              (tiny_sqr + grid) * 4 + grid, (tiny_sqr + grid) * 4 + grid])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if framecount < 30:
            win.blit(threetext, [win_w / 2 - threetext.get_rect()[2] / 2, win_h / 2 - threetext.get_rect()[3] / 2])
        elif framecount < 60:
            win.blit(twotext, [win_w / 2 - twotext.get_rect()[2] / 2, win_h / 2 - twotext.get_rect()[3] / 2])
        elif framecount < 90:
            win.blit(onetext, [win_w / 2 - onetext.get_rect()[2] / 2, win_h / 2 - onetext.get_rect()[3] / 2])

        if framecount >= 90:
            return
        else:
            framecount += 1

        stris = pygame.Surface([500, 500])
        stris.fill([10, 10, 10])
        stris.set_colorkey([10, 10, 10])
        strisfont = pygame.font.Font("Chunkfive.otf", 75)
        stext = strisfont.render("S", 0, [0, 255, 0])
        tritext = strisfont.render("tri", 0, [0, 0, 0])
        stris.blit(stext, [0, 0])
        stris.blit(tritext, [stext.get_rect()[2], 0])
        stris.blit(stext, [stext.get_rect()[2] + tritext.get_rect()[2], 0])

        win.blit(stris, [win_w / 2 - (stext.get_rect()[2] + stext.get_rect()[2] + tritext.get_rect()[2]) / 2, 10])

        if gamemode == "marathon":
            gamemodefont = pygame.font.Font("opensans.ttf", 30)
            gamemodetext = gamemodefont.render("- Marathon -", 1, [0, 0, 0])
            win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])
        if gamemode == "ultra":
            gamemodefont = pygame.font.Font("opensans.ttf", 30)
            gamemodetext = gamemodefont.render("- Ultra -", 1, [0, 0, 0])
            win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])
        if gamemode == "sprint":
            gamemodefont = pygame.font.Font("opensans.ttf", 30)
            gamemodetext = gamemodefont.render("- Sprint -", 1, [0, 0, 0])
            win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])
        if gamemode == "endless":
            gamemodefont = pygame.font.Font("opensans.ttf", 30)
            gamemodetext = gamemodefont.render("- Endless -", 1, [0, 0, 0])
            win.blit(gamemodetext, [win_w / 2 - gamemodetext.get_rect()[2] / 2, 10 + stext.get_rect()[2] + 10])

        pygame.draw.rect(win, [255, 255, 255],
                         [tiny_sqr + grid - 5, win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 5,
                          (tiny_sqr + grid) * 6 + 10, (squaresize + 5 + grid) * 8 + 10])
        pygame.draw.rect(win, [0, 0, 0], [tiny_sqr + grid, win_h - topbar - 10 - (squaresize + 5 + grid) * 8,
                                          (tiny_sqr + grid) * 6, (squaresize + 5 + grid) * 8])
        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5,
                                                (tiny_sqr + grid) * 6, 1])
        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5 +
                                                (grid + squaresize + 5) * 1,
                                                (tiny_sqr + grid) * 6, 1])
        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5 +
                                                (grid + squaresize + 5) * 3,
                                                (tiny_sqr + grid) * 6, 1])
        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + squaresize + 5 +
                                                (grid + squaresize + 5) * 5,
                                                (tiny_sqr + grid) * 6, 1])
        levellabelfont = pygame.font.Font("Chunkfive.otf", 25)
        levellabeltext = levellabelfont.render("Level:", 1, [255, 255, 255])
        win.blit(levellabeltext, [tiny_sqr + grid + 3, win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 8])
        levelfont = pygame.font.Font("opensans.ttf", 23)
        leveltext = levelfont.render(str(level), 1, [255, 255, 255])
        win.blit(leveltext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - leveltext.get_rect()[2] - 2),
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + 3])
        lineslabelfont = pygame.font.Font("Chunkfive.otf", 25)
        lineslabeltext = lineslabelfont.render("Lines:", 1, [255, 255, 255])
        win.blit(lineslabeltext, [tiny_sqr + grid + 3,
                                  win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2])
        lns = str(lines)
        if lines >= 999:
            lns = str(999)
        linesfont = pygame.font.Font("opensans.ttf", 23)
        linestext = linesfont.render(lns, 1, [255, 255, 255])
        win.blit(linestext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - linestext.get_rect()[2] - 2),
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 + 3])
        scorelabelfont = pygame.font.Font("Chunkfive.otf", 25)
        scorelabeltext = scorelabelfont.render("Score:", 1, [255, 255, 255])
        win.blit(scorelabeltext, [tiny_sqr + grid + 3,
                                  win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                                  (grid + squaresize + 5) * 1])
        scr = str(score)
        if score >= 999999:
            scr = str(999999)
        scorefont = pygame.font.Font("opensans.ttf", 30)
        scoretext = scorefont.render(scr, 1, [255, 255, 255])
        win.blit(scoretext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - scoretext.get_rect()[2]) - 8,
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 +
                             (grid + squaresize + 5) * 2 - 8])
        bestlabelfont = pygame.font.Font("Chunkfive.otf", 25)
        bestlabeltext = bestlabelfont.render("Best:", 1, [255, 255, 255])
        win.blit(bestlabeltext, [tiny_sqr + grid + 3,
                                 win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                                 (grid + squaresize + 5) * 3])
        bestlist = get_scores()
        if gamemode == "sprint":
            if bestlist[1] == -1:
                besty = "--:--:---"
            else:
                besty = milliseconds(bestlist[1])
                if len(str(besty[0])) < 2:
                    minutes = "0" + str(besty[0])
                else:
                    minutes = str(besty[0])
                if len(str(besty[1])) < 2:
                    seconds = "0" + str(besty[1])
                else:
                    seconds = str(besty[1])
                if len(str(besty[2])) == 2:
                    milli = "0" + str(besty[2])
                elif len(str(besty[2])) < 2:
                    milli = "00" + str(besty[2])
                else:
                    milli = str(besty[2])
                besty = minutes + ":" + seconds + ":" + milli
        elif gamemode == "marathon":
            if bestlist[0] == -1:
                besty = "0"
            else:
                besty = str(bestlist[0])
        elif gamemode == "ultra":
            if bestlist[2] == -1:
                besty = "0"
            else:
                besty = str(bestlist[2])
        else:
            if bestlist[3] == -1:
                besty = "0"
            else:
                besty = str(bestlist[3])
        if gamemode != "sprint":
            if int(besty) >= 999999:
                besty = str(999999)
        bestfont = pygame.font.Font("opensans.ttf", 30)
        besttext = bestfont.render(besty, 1, [255, 255, 255])
        win.blit(besttext, [tiny_sqr + grid + ((tiny_sqr + grid) * 6 - besttext.get_rect()[2]) - 8,
                            win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 1 + squaresize + 5 +
                            (grid + squaresize + 5) * 4 - 8])
        timestr = milliseconds(time)
        if len(str(timestr[0])) < 2:
            minutes = "0" + str(timestr[0])
        else:
            minutes = str(timestr[0])
        if len(str(timestr[1])) < 2:
            seconds = "0" + str(timestr[1])
        else:
            seconds = str(timestr[1])
        if len(str(timestr[2])) == 2:
            milli = "0" + str(timestr[2])
        elif len(str(timestr[2])) < 2:
            milli = "00" + str(timestr[2])
        else:
            milli = str(timestr[2])
        timestr1 = minutes + ":" + seconds
        timestr2 = milli
        timestr1font = pygame.font.Font("opensans.ttf", 40)
        timestr1text = timestr1font.render(timestr1, 1, [255, 255, 255])
        win.blit(timestr1text, [tiny_sqr + grid + ((tiny_sqr + grid) * 6) / 2 - timestr1text.get_rect()[2] / 2,
                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                                (grid + squaresize + 5) * 5 - 8])
        timestr2font = pygame.font.Font("opensans.ttf", 25)
        timestr2text = timestr2font.render(timestr2, 1, [255, 255, 255])
        timestr2surf = pygame.Surface([100, 100])
        timestr2surf.set_colorkey([0, 0, 0])
        timestr2surf.blit(timestr2text, [0, 0])
        timestr2surf.set_alpha(100)
        win.blit(timestr2surf, [tiny_sqr + grid + ((tiny_sqr + grid) * 6) / 2 + 5,
                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 + 6 + squaresize + 5 + 2 +
                                (grid + squaresize + 5) * 5 - 8 + 40])

        pygame.draw.rect(win, [255, 255, 255], [tiny_sqr + grid - 5,
                                                win_h - topbar - 10 - (squaresize + 5 + grid) * 8 - 5 -
                                                (squaresize + 5 + grid) - (squaresize + grid),
                                                (tiny_sqr + grid) * 6 + 10,
                                                (squaresize + 5 + grid) + 10])

        pygame.draw.rect(win, [0, 0, 0], [tiny_sqr + grid,
                                          win_h - topbar - 10 - (squaresize + 5 + grid) * 8 -
                                          (squaresize + 5 + grid) - (squaresize + grid),
                                          (tiny_sqr + grid) * 6,
                                          (squaresize + 5 + grid)])

        combolabelfont = pygame.font.Font("Chunkfive.otf", 23)
        combolabeltext = combolabelfont.render("Combo:", 1, [255, 255, 255])
        win.blit(combolabeltext, [tiny_sqr + grid + 3,
                                  win_h - topbar - 10 - (squaresize + 5 + grid) * 8 -
                                  (squaresize + 5 + grid) - (squaresize + grid) + 8])
        combofont = pygame.font.Font("opensans.ttf", 30)
        combotext = combolabelfont.render(str(combocount), 1, [255, 255, 255])
        win.blit(combotext, [tiny_sqr + grid + (tiny_sqr + grid) * 6 - combotext.get_rect()[2] - 3,
                             win_h - topbar - 10 - (squaresize + 5 + grid) * 8 -
                             (squaresize + 5 + grid) - (squaresize + grid) + 8])

        if lastclear != 0:
            if b2b > 1:
                b2bfont = pygame.font.Font("Chunkfive.otf", 20)
                b2btext = b2bfont.render("Back-to-Back", 1, [0, 0, 0])
                win.blit(b2btext, [leftbar / 2 - b2btext.get_rect()[2] / 2, 250])
            clearfont = pygame.font.Font("Chunkfive.otf", 30)
            cleartext = clearfont.render(lastclear, 1, [0, 0, 0])
            win.blit(cleartext, [leftbar / 2 - cleartext.get_rect()[2] / 2, 275])

        tspinfont = pygame.font.Font("Chunkfive.otf", 20)
        minifont = pygame.font.Font("Chunkfive.otf", 15)
        tspintext = tspinfont.render("T-Spin", 1, [0, 0, 0])
        minitext = minifont.render("mini", 1, [0, 0, 0])

        if lastclear != 0:
            if tspin == 1:
                win.blit(tspintext, [leftbar / 2 - tspintext.get_rect()[2] / 2, 310])
                win.blit(minitext, [leftbar / 2 - minitext.get_rect()[2] / 2, 335])
            if tspin == 2:
                win.blit(tspintext, [leftbar / 2 - tspintext.get_rect()[2] / 2, 310])

        pygame.display.update()


def get_scores():
    records = open("records.txt", "r")
    rec = records.readlines()

    marathon_best = rec[1]
    marathon_best.strip()
    marathon_best.strip("\\")
    marathon_best.strip("n")
    marathon_best = int(marathon_best)

    sprint_best = rec[3]
    sprint_best.strip()
    sprint_best.strip("\\")
    sprint_best.strip("n")
    sprint_best = int(sprint_best)

    ultra_best = rec[5]
    ultra_best.strip()
    ultra_best.strip("\\")
    ultra_best.strip("n")
    ultra_best = int(ultra_best)

    endless_best = rec[7]
    endless_best.strip()
    endless_best.strip("\\")
    endless_best.strip("n")
    endless_best = int(endless_best)

    records.close()

    return [marathon_best, sprint_best, ultra_best, endless_best]


def update_scores(score, mode, best):
    records = open("records.txt", "r")
    rec = records.readlines()
    records.close()
    records = open("records.txt", "w")

    if mode == "marathon":
        if int(best[0]) == -1 or int(score) > int(best[0]):
            rec[1] = str(score) + "\n"
            records.writelines(rec)
    if mode == "sprint":
        if int(best[1]) == -1 or int(score) < int(best[1]):
            rec[3] = str(score) + "\n"
            records.writelines(rec)
    if mode == "ultra":
        if int(best[2]) == -1 or int(score) > int(best[2]):
            rec[5] = str(score) + "\n"
            records.writelines(rec)
    if mode == "endless":
        if int(best[3]) == -1 or int(score) > int(best[3]):
            rec[7] = str(score) + "\n"
            records.writelines(rec)

    records.close()


def milliseconds(milli):
    mil = milli % 1000
    seconds = milli // 1000
    sec = seconds % 60
    minu = seconds // 60

    if minu >= 100:
        minu = 99
        sec = 59
        mil = 999

    return([minu, sec, mil])


def winscreen():
    while 1:
        clock.tick(fps)
        mouse = pygame.mouse.get_pos()

        pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                topbar + game_h / 2 - 126, 282, 252])
        pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140, topbar + game_h / 2 - 100 - 25, 280, 200 + 50])
        pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                topbar + game_h / 2 - 100 + 5 - 25, 270, 190 + 50])
        gameoverfont = pygame.font.Font("Chunkfive.otf", 48)
        gameovertext = gameoverfont.render("You win!", 1, [0, 0, 0])
        win.blit(gameovertext, [win_w / 2 - gameovertext.get_rect()[2] / 2, topbar + game_h / 2 - 100 + 5 + 50 - 40])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50,
                                          topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 - 25,
                                          100, 50])
        if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                (topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 - 25 <= mouse[1] <=
                 topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 - 25)):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   gameovertext.get_rect()[3] + 10 + 5 - 25,
                                                   90, 40])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   gameovertext.get_rect()[3] + 10 + 5 - 25,
                                                   90, 40])
        menufont = pygame.font.Font("Chunkfive.otf", 30)
        menutext = menufont.render("Menu", 1, [0, 0, 0])
        win.blit(menutext, [win_w / 2 - menutext.get_rect()[2] / 2,
                            topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 12 - 25])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 50,
                                          topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 +
                                          50 + 15 - 25,
                                          100, 50])
        if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                (topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 + 15 - 25 <= mouse[1] <=
                 topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 + 50 + 15 - 25)):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   gameovertext.get_rect()[3] + 10 + 5 + 50 + 15 - 25,
                                                   90, 40])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 50 + 5,
                                                   topbar + game_h / 2 - 100 + 5 + 50 +
                                                   gameovertext.get_rect()[3] + 10 + 5 + 50 + 15 - 25,
                                                   90, 40])
        restartfont = pygame.font.Font("Chunkfive.otf", 25)
        restarttext = restartfont.render("Restart", 1, [0, 0, 0])
        win.blit(restarttext, [win_w / 2 - restarttext.get_rect()[2] / 2,
                               topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[
                                   3] + 10 + 14 + 50 + 15 - 25])

        bestlist = get_scores()

        if gamemode == "marathon" or gamemode == "ultra":
            pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                    topbar + game_h / 2 - 126 - 110, 282, 100])
            pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140,
                                              topbar + game_h / 2 - 125 - 110, 280, 98])
            pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                    topbar + game_h / 2 - 125 - 110 + 5, 270, 88])
            scorelabelfont = pygame.font.Font("Chunkfive.otf", 35)
            scorelabeltext = scorelabelfont.render("Score:", 1, [0, 0, 0])
            win.blit(scorelabeltext, [win_w / 2 - scorelabeltext.get_rect()[2] / 2,
                                      topbar + game_h / 2 - 125 - 110 + 5 + 10])
            scorefont = pygame.font.Font("opensans.ttf", 30)
            scoretext = scorefont.render(str(score), 1, [0, 0, 0])
            win.blit(scoretext, [win_w / 2 - scoretext.get_rect()[2] / 2,
                                 topbar + game_h / 2 - 125 - 110 + 5 + 10 + 30])
            if gamemode == "marathon":
                if bestlist[0] == -1 or score > bestlist[0]:
                    pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                            topbar + game_h / 2 - 126 - 110 +
                                                            100 + 10 + 252 + 10, 282, 100])
                    pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140,
                                                      topbar + game_h / 2 - 125 - 110 +
                                                      100 + 10 + 252 + 10, 280, 98])
                    pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                            topbar + game_h / 2 - 125 - 110 + 5 +
                                                            100 + 10 + 252 + 10, 270, 88])
                    congratsfont = pygame.font.Font("Chunkfive.otf", 30)
                    congratstext = congratsfont.render("Congratulations!", 1, [0, 0, 0])
                    win.blit(congratstext, [win_w / 2 - congratstext.get_rect()[2] / 2,
                                              topbar + game_h / 2 - 125 - 110 + 5 + 10 + 100 + 10 + 252 + 10])
                    beatfont = pygame.font.Font("Chunkfive.otf", 20)
                    beattext = beatfont.render("You beat the high score!", 1, [0, 0, 0])
                    win.blit(beattext, [win_w / 2 - beattext.get_rect()[2] / 2,
                                            topbar + game_h / 2 - 125 - 110 + 5 + 10 + 100 + 10 + 252 + 10 + 40])

                    update_scores(score, gamemode, bestlist)
            elif gamemode == "ultra":
                if bestlist[2] == -1 or score > bestlist[2]:
                    pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                            topbar + game_h / 2 - 126 - 110 +
                                                            100 + 10 + 252 + 10, 282, 100])
                    pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140,
                                                      topbar + game_h / 2 - 125 - 110 +
                                                      100 + 10 + 252 + 10, 280, 98])
                    pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                            topbar + game_h / 2 - 125 - 110 + 5 +
                                                            100 + 10 + 252 + 10, 270, 88])
                    congratsfont = pygame.font.Font("Chunkfive.otf", 30)
                    congratstext = congratsfont.render("Congratulations!", 1, [0, 0, 0])
                    win.blit(congratstext, [win_w / 2 - congratstext.get_rect()[2] / 2,
                                              topbar + game_h / 2 - 125 - 110 + 5 + 10 + 100 + 10 + 252 + 10])
                    beatfont = pygame.font.Font("Chunkfive.otf", 20)
                    beattext = beatfont.render("You beat the high score!", 1, [0, 0, 0])
                    win.blit(beattext, [win_w / 2 - beattext.get_rect()[2] / 2,
                                            topbar + game_h / 2 - 125 - 110 + 5 + 10 + 100 + 10 + 252 + 10 + 40])

                    update_scores(score, gamemode, bestlist)
        elif gamemode == "sprint":
            timestr = milliseconds(time)
            if len(str(timestr[0])) < 2:
                minutes = "0" + str(timestr[0])
            else:
                minutes = str(timestr[0])
            if len(str(timestr[1])) < 2:
                seconds = "0" + str(timestr[1])
            else:
                seconds = str(timestr[1])
            if len(str(timestr[2])) == 2:
                milli = "0" + str(timestr[2])
            elif len(str(timestr[2])) < 2:
                milli = "00" + str(timestr[2])
            else:
                milli = str(timestr[2])
            timestr1 = minutes + ":" + seconds + ":" + milli
            pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                    topbar + game_h / 2 - 126 - 110, 282, 100])
            pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140,
                                              topbar + game_h / 2 - 125 - 110, 280, 98])
            pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                    topbar + game_h / 2 - 125 - 110 + 5, 270, 88])
            scorelabelfont = pygame.font.Font("Chunkfive.otf", 35)
            scorelabeltext = scorelabelfont.render("Time:", 1, [0, 0, 0])
            win.blit(scorelabeltext, [win_w / 2 - scorelabeltext.get_rect()[2] / 2,
                                      topbar + game_h / 2 - 125 - 110 + 5 + 10])
            scorefont = pygame.font.Font("opensans.ttf", 30)
            scoretext = scorefont.render(timestr1, 1, [0, 0, 0])
            win.blit(scoretext, [win_w / 2 - scoretext.get_rect()[2] / 2,
                                 topbar + game_h / 2 - 125 - 110 + 5 + 10 + 30])
            if bestlist[1] == -1 or time < bestlist[1]:
                pygame.draw.rect(win, [255, 255, 255], [leftbar + game_w / 2 - 140 - 1,
                                                        topbar + game_h / 2 - 126 - 110 +
                                                        100 + 10 + 252 + 10, 282, 100])
                pygame.draw.rect(win, [0, 0, 0], [leftbar + game_w / 2 - 140,
                                                  topbar + game_h / 2 - 125 - 110 +
                                                  100 + 10 + 252 + 10, 280, 98])
                pygame.draw.rect(win, [175, 175, 175], [leftbar + game_w / 2 - 140 + 5,
                                                        topbar + game_h / 2 - 125 - 110 + 5 +
                                                        100 + 10 + 252 + 10, 270, 88])
                congratsfont = pygame.font.Font("Chunkfive.otf", 30)
                congratstext = congratsfont.render("Congratulations!", 1, [0, 0, 0])
                win.blit(congratstext, [win_w / 2 - congratstext.get_rect()[2] / 2,
                                        topbar + game_h / 2 - 125 - 110 + 5 + 10 + 100 + 10 + 252 + 10])
                beatfont = pygame.font.Font("Chunkfive.otf", 20)
                beattext = beatfont.render("You beat the high score!", 1, [0, 0, 0])
                win.blit(beattext, [win_w / 2 - beattext.get_rect()[2] / 2,
                                    topbar + game_h / 2 - 125 - 110 + 5 + 10 + 100 + 10 + 252 + 10 + 40])

                update_scores(time, gamemode, bestlist)



        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                            (topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 - 25 <= mouse[1] <=
                             topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 - 25)):
                        mainmenu()
                    if (win_w / 2 - 50 <= mouse[0] <= win_w / 2 - 50 + 100 and
                            (topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 + 15 - 25 <=
                             mouse[1] <=
                             topbar + game_h / 2 - 100 + 5 + 50 + gameovertext.get_rect()[3] + 10 + 50 + 50 + 15 - 25)):
                        newgame()


def mainmenu():
    while 1:
        clock.tick(30)
        mouse = pygame.mouse.get_pos()

        win.fill([150, 150, 150])

        stris = pygame.Surface([500, 500])
        stris.fill([10, 10, 10])
        stris.set_colorkey([10, 10, 10])
        strisfont = pygame.font.Font("Chunkfive.otf", 200)
        stext = strisfont.render("S", 0, [0, 255, 0])
        tritext = strisfont.render("tri", 0, [0, 0, 0])
        stris.blit(stext, [0, 0])
        stris.blit(tritext, [stext.get_rect()[2], 0])
        stris.blit(stext, [stext.get_rect()[2] + tritext.get_rect()[2], 0])

        win.blit(stris, [win_w / 2 - (stext.get_rect()[2] + stext.get_rect()[2] + tritext.get_rect()[2]) / 2, 50])

        madebyfont = pygame.font.Font("Chunkfive.otf", 40)
        madebytext = madebyfont.render("by Sawyer Scott Stahl", 1, [0, 0, 0])

        win.blit(madebytext, [win_w / 2 - madebytext.get_rect()[2] / 2, 50 + stext.get_rect()[3] - 20])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40,
                                          200, 84])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 1,
                                          200, 84])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 2,
                                          200, 84])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 3,
                                          200, 84])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 4,
                                          200, 84])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 <= mouse[1] <=
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 7,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 7,
                                                   186, 70])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 1 <= mouse[1] <=
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84 + 100 * 1):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 +
                                                   madebytext.get_rect()[3] + 40 + 7 + 100 * 1,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 +
                                                   madebytext.get_rect()[3] + 40 + 7 + 100 * 1,
                                                   186, 70])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 2 <= mouse[1] <=
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84 + 100 * 2):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 +
                                                   madebytext.get_rect()[3] + 40 + 7 + 100 * 2,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 +
                                                   madebytext.get_rect()[3] + 40 + 7 + 100 * 2,
                                                   186, 70])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 3 <= mouse[1] <=
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84 + 100 * 3):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 +
                                                   madebytext.get_rect()[3] + 40 + 7 + 100 * 3,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 +
                                                   madebytext.get_rect()[3] + 40 + 7 + 100 * 3,
                                                   186, 70])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 4 <= mouse[1] <=
                50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84 + 100 * 4):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 +
                                                   madebytext.get_rect()[3] + 40 + 7 + 100 * 4,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + stext.get_rect()[3] - 20 +
                                                   madebytext.get_rect()[3] + 40 + 7 + 100 * 4,
                                                   186, 70])

        playfont = pygame.font.Font("Chunkfive.otf", 40)
        optionsfont = pygame.font.Font("Chunkfive.otf", 40)
        highscoresfont = pygame.font.Font("Chunkfive.otf", 30)
        aboutfont = pygame.font.Font("Chunkfive.otf", 40)
        quitfont = pygame.font.Font("Chunkfive.otf", 40)

        playtext = playfont.render("Play", 1, [0, 0, 0])
        optionstext = optionsfont.render("Options", 1, [0, 0, 0])
        highscorestext = highscoresfont.render("High Scores", 1, [0, 0, 0])
        abouttext = aboutfont.render("About", 1, [0, 0, 0])
        quittext = quitfont.render("Quit", 1, [0, 0, 0])

        win.blit(playtext, [win_w / 2 - playtext.get_rect()[2] / 2,
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40
                            + 42 - playtext.get_rect()[3] / 2 + 4])

        win.blit(optionstext, [win_w / 2 - optionstext.get_rect()[2] / 2,
                               50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 1
                               + 42 - optionstext.get_rect()[3] / 2 + 4])

        win.blit(highscorestext, [win_w / 2 - highscorestext.get_rect()[2] / 2,
                                  50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 2
                                  + 42 - highscorestext.get_rect()[3] / 2 + 3])

        win.blit(abouttext, [win_w / 2 - abouttext.get_rect()[2] / 2,
                             50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 3 +
                             42 - abouttext.get_rect()[3] / 2 + 4])

        win.blit(quittext, [win_w / 2 - quittext.get_rect()[2] / 2,
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 4 +
                            42 - quittext.get_rect()[3] / 2 + 4])

        pygame.display.update()

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 <= mouse[1] <=
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84):
                        playmenu()

                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 1 <= mouse[1] <=
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84 + 100 * 1):
                        optionsmenu()

                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 2 <= mouse[1] <=
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84 + 100 * 2):
                        highscoremenu()

                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 3 <= mouse[1] <=
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84 + 100 * 3):
                        aboutmenu()

                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 100 * 4 <= mouse[1] <=
                            50 + stext.get_rect()[3] - 20 + madebytext.get_rect()[3] + 40 + 84 + 100 * 4):
                        sys.exit()


def playmenu():
    global gamemode

    while 1:
        clock.tick(30)
        mouse = pygame.mouse.get_pos()

        win.fill([150, 150, 150])

        playfont = pygame.font.Font("Chunkfive.otf", 200)
        playtext = playfont.render("Play", 0, [0, 0, 0])

        win.blit(playtext, [win_w / 2 - playtext.get_rect()[2] / 2, 50])

        choosefont = pygame.font.Font("Chunkfive.otf", 40)
        choosetext = choosefont.render("Choose a gamemode:", 1, [0, 0, 0])

        win.blit(choosetext, [win_w / 2 - choosetext.get_rect()[2] / 2, 50 + playtext.get_rect()[3] - 20 + 15])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40,
                                          200, 84])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 1,
                                          200, 84])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 2,
                                          200, 84])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 3,
                                          200, 84])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100,
                                          50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 4,
                                          200, 84])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 <= mouse[1] <=
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 7,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 7,
                                                   186, 70])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 1 <= mouse[1] <=
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84 + 100 * 1):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 +
                                                   choosetext.get_rect()[3] + 40 + 7 + 100 * 1,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 +
                                                   choosetext.get_rect()[3] + 40 + 7 + 100 * 1,
                                                   186, 70])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 2 <= mouse[1] <=
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84 + 100 * 2):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 +
                                                   choosetext.get_rect()[3] + 40 + 7 + 100 * 2,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 +
                                                   choosetext.get_rect()[3] + 40 + 7 + 100 * 2,
                                                   186, 70])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 3 <= mouse[1] <=
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84 + 100 * 3):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 +
                                                   choosetext.get_rect()[3] + 40 + 7 + 100 * 3,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 +
                                                   choosetext.get_rect()[3] + 40 + 7 + 100 * 3,
                                                   186, 70])

        if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 4 <= mouse[1] <=
                50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84 + 100 * 4):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 +
                                                   choosetext.get_rect()[3] + 40 + 7 + 100 * 4,
                                                   186, 70])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7,
                                                   50 + playtext.get_rect()[3] - 20 +
                                                   choosetext.get_rect()[3] + 40 + 7 + 100 * 4,
                                                   186, 70])

        marfont = pygame.font.Font("Chunkfive.otf", 35)
        sprfont = pygame.font.Font("Chunkfive.otf", 40)
        ultfont = pygame.font.Font("Chunkfive.otf", 40)
        endfont = pygame.font.Font("Chunkfive.otf", 40)
        backfont = pygame.font.Font("Chunkfive.otf", 40)

        martext = marfont.render("Marathon", 1, [0, 0, 0])
        sprtext = sprfont.render("Sprint", 1, [0, 0, 0])
        ulttext = ultfont.render("Ultra", 1, [0, 0, 0])
        endtext = endfont.render("Endless", 1, [0, 0, 0])
        backtext = backfont.render("Back", 1, [0, 0, 0])

        win.blit(martext, [win_w / 2 - martext.get_rect()[2] / 2,
                           50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40
                           + 42 - martext.get_rect()[3] / 2 + 4])

        win.blit(sprtext, [win_w / 2 - sprtext.get_rect()[2] / 2,
                           50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 1
                           + 42 - sprtext.get_rect()[3] / 2 + 4])

        win.blit(ulttext, [win_w / 2 - ulttext.get_rect()[2] / 2,
                           50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 2
                           + 42 - ulttext.get_rect()[3] / 2 + 3])

        win.blit(endtext, [win_w / 2 - endtext.get_rect()[2] / 2,
                           50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 3 +
                           42 - endtext.get_rect()[3] / 2 + 4])

        win.blit(backtext, [win_w / 2 - backtext.get_rect()[2] / 2,
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 4 +
                            42 - backtext.get_rect()[3] / 2 + 4])

        pygame.display.update()

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 <= mouse[1] <=
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84):
                        gamemode = "marathon"
                        newgame()

                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 1 <= mouse[1] <=
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84 + 100 * 1):
                        gamemode = "sprint"
                        newgame()

                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 2 <= mouse[1] <=
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84 + 100 * 2):
                        gamemode = "ultra"
                        newgame()

                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 3 <= mouse[1] <=
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84 + 100 * 3):
                        gamemode = "endless"
                        newgame()

                    if (win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 100 * 4 <= mouse[1] <=
                            50 + playtext.get_rect()[3] - 20 + choosetext.get_rect()[3] + 40 + 84 + 100 * 4):
                        mainmenu()


def optionsmenu():
    optlist = get_options()
    optlistog = list(optlist)
    saved = "Changes saved!"
    change = 0
    while 1:
        clock.tick(30)
        mouse = pygame.mouse.get_pos()

        win.fill([150, 150, 150])

        titlefont = pygame.font.Font("Chunkfive.otf", 80)
        titletext = titlefont.render("Options", 1, [0, 0, 0])
        win.blit(titletext, [win_w / 2 - titletext.get_rect()[2] / 2, 40])

        if optlist == optlistog:
            saved = "Changes saved!"
        else:
            saved = "Changes not saved!"

        savedfont = pygame.font.Font("Chunkfive.otf", 20)
        savedtext = savedfont.render(saved, 1, [0, 0, 0])
        win.blit(savedtext, [win_w / 2 - savedtext.get_rect()[2] / 2, 120])

        hgfont = pygame.font.Font("Chunkfive.otf", 40)
        holdopttext = hgfont.render("Hold", 1, [0, 0, 0])
        win.blit(holdopttext, [65, 175])

        pygame.draw.rect(win, [0, 0, 0], [185, 164, 50, 50])
        pygame.draw.rect(win, [0, 0, 0], [245, 164, 50, 50])

        if optlist[0] == 1:
            pygame.draw.rect(win, [0, 200, 0], [185, 164, 50, 50])
        elif optlist[0] == 0:
            pygame.draw.rect(win, [0, 200, 0], [245, 164, 50, 50])

        pygame.draw.rect(win, [0, 0, 0], [win_w - 115, 164, 50, 50])
        pygame.draw.rect(win, [0, 0, 0], [win_w - 175, 164, 50, 50])

        if optlist[1] == 1:
            pygame.draw.rect(win, [0, 200, 0], [win_w - 175, 164, 50, 50])
        elif optlist[1] == 0:
            pygame.draw.rect(win, [0, 200, 0], [win_w - 115, 164, 50, 50])

        ghostopttext = hgfont.render("Ghost", 1, [0, 0, 0])
        win.blit(ghostopttext, [win_w - 185 - 130, 175])

        dastitlefont = pygame.font.Font("Chunkfive.otf", 50)
        dastitletext = dastitlefont.render("DAS", 1, [0, 0, 0])
        win.blit(dastitletext, [win_w / 2 - dastitletext.get_rect()[2] / 2, 240])

        dasfont = pygame.font.Font("Chunkfive.otf", 40)
        startuptext = dasfont.render("Startup", 1, [0, 0 ,0])
        intervaltext = dasfont.render("Interval", 1, [0, 0, 0])

        win.blit(startuptext, [50, 305])

        pygame.draw.rect(win, [0, 0, 0], [210, 295, 100, 50])

        pygame.draw.rect(win, [0, 0, 0], [win_w - 50 - 110, 295, 100, 50])

        win.blit(intervaltext, [325, 305])

        usescrollfont = pygame.font.Font("Chunkfive.otf", 20)
        usescrolltext = usescrollfont.render("Use mouse scroll to change (listed in milliseconds)", 1, [0, 0, 0])

        win.blit(usescrolltext, [win_w / 2 - usescrolltext.get_rect()[2] / 2, 350])

        controltitlefont = pygame.font.Font("Chunkfive.otf", 50)
        controltitletext = controltitlefont.render("Controls", 1, [0, 0, 0])
        win.blit(controltitletext, [win_w / 2 - controltitletext.get_rect()[2] / 2, 400])

        controlfont = pygame.font.Font("Chunkfive.otf", 30)
        lefttext = controlfont.render("Left", 1, [0, 0, 0])
        righttext = controlfont.render("Right", 1, [0, 0, 0])
        hardtext = controlfont.render("Hard drop", 1, [0, 0, 0])
        softtext = controlfont.render("Soft drop", 1, [0, 0, 0])
        cwtext = controlfont.render("Rotate CW", 1, [0, 0, 0])
        ccwtext = controlfont.render("Rotate CCW", 1, [0, 0, 0])
        holdtext = controlfont.render("Hold", 1, [0, 0, 0])
        pausetext = controlfont.render("Pause", 1, [0, 0, 0])

        win.blit(lefttext, [35, 465])
        win.blit(righttext, [win_w / 2, 465])
        win.blit(hardtext, [35, 525])
        win.blit(softtext, [win_w / 2, 525])
        win.blit(cwtext, [35, 585])
        win.blit(ccwtext, [win_w / 2, 585])
        win.blit(holdtext, [35, 645])
        win.blit(pausetext, [win_w / 2, 645])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 10 - 100, 455, 100, 40])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 10 - 100, 515, 100, 40])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 10 - 100, 575, 100, 40])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 10 - 100, 635, 100, 40])

        pygame.draw.rect(win, [0, 0, 0], [win_w - 10 - 135, 455, 100, 40])
        pygame.draw.rect(win, [0, 0, 0], [win_w - 10 - 135, 515, 100, 40])
        pygame.draw.rect(win, [0, 0, 0], [win_w - 10 - 135, 575, 100, 40])
        pygame.draw.rect(win, [0, 0, 0], [win_w - 10 - 135, 635, 100, 40])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100, 710, 200, 60])
        pygame.draw.rect(win, [0, 0, 0], [win_w /2 - 100, 780, 200, 60])

        if change == 0:
            # Hold toggle on
            if 185 <= mouse[0] <= 185 + 50 and 164 <= mouse[1] <= 164 + 50:
                pygame.draw.rect(win, [200, 200, 50], [190, 169, 40, 40])
            else:
                pygame.draw.rect(win, [245, 245, 50], [190, 169, 40, 40])

            # Hold toggle off
            if 245 <= mouse[0] <= 245 + 50 and 164 <= mouse[1] <= 164 + 50:
                pygame.draw.rect(win, [200, 200, 50], [250, 169, 40, 40])
            else:
                pygame.draw.rect(win, [245, 245, 50], [250, 169, 40, 40])

            # Ghost toggle off
            if win_w - 115 <= mouse[0] <= win_w - 115 + 50 and 164 <= mouse[1] <= 164 + 50:
                pygame.draw.rect(win, [200, 200, 50], [win_w - 110, 169, 40, 40])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w - 110, 169, 40, 40])

            # Ghost toggle on
            if win_w - 175 <= mouse[0] <= win_w - 175 + 50 and 164 <= mouse[1] <= 164 + 50:
                pygame.draw.rect(win, [200, 200, 50], [win_w - 170, 169, 40, 40])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w - 170, 169, 40, 40])

            # Das Startup
            if 210 <= mouse[0] <= 210 + 100 and 295 <= mouse[1] <= 295 + 50:
                pygame.draw.rect(win, [200, 200, 50], [215, 300, 90, 40])
            else:
                pygame.draw.rect(win, [245, 245, 50], [215, 300, 90, 40])

            # Das Interval
            if win_w - 50 - 110 <= mouse[0] <= win_w - 50 - 110 + 100 and 295 <= mouse[1] <= 295 + 50:
                pygame.draw.rect(win, [200, 200, 50], [win_w - 50 - 105, 300, 90, 40])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w - 50 - 105, 300, 90, 40])

            # Left
            if win_w / 2 - 10 - 100 <= mouse[0] <= win_w / 2 - 10 - 100 + 100 and 455 <= mouse[1] <= 455 + 40:
                pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 10 - 100 + 5, 455 + 5, 90, 30])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 10 - 100 + 5, 455 + 5, 90, 30])

            # Hard drop
            if win_w / 2 - 10 - 100 <= mouse[0] <= win_w / 2 - 10 - 100 + 100 and 515 <= mouse[1] <= 515 + 40:
                pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 10 - 100 + 5, 515 + 5, 90, 30])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 10 - 100 + 5, 515 + 5, 90, 30])

            # Rotate CW
            if win_w / 2 - 10 - 100 <= mouse[0] <= win_w / 2 - 10 - 100 + 100 and 575 <= mouse[1] <= 575 + 40:
                pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 10 - 100 + 5, 575 + 5, 90, 30])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 10 - 100 + 5, 575 + 5, 90, 30])

            # Hold
            if win_w / 2 - 10 - 100 <= mouse[0] <= win_w / 2 - 10 - 100 + 100 and 635 <= mouse[1] <= 635 + 40:
                pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 10 - 100 + 5, 635 + 5, 90, 30])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 10 - 100 + 5, 635 + 5, 90, 30])

            # Right
            if win_w - 10 - 135 <= mouse[0] <= win_w - 10 - 135 + 100 and 455 <= mouse[1] <= 455 + 40:
                pygame.draw.rect(win, [200, 200, 50], [win_w - 10 - 135 + 5, 455 + 5, 90, 30])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w - 10 - 135 + 5, 455 + 5, 90, 30])

            # Soft Drop
            if win_w - 10 - 135 <= mouse[0] <= win_w - 10 - 135 + 100 and 515 <= mouse[1] <= 515 + 40:
                pygame.draw.rect(win, [200, 200, 50], [win_w - 10 - 135 + 5, 515 + 5, 90, 30])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w - 10 - 135 + 5, 515 + 5, 90, 30])

            # Rotate CCW
            if win_w - 10 - 135 <= mouse[0] <= win_w - 10 - 135 + 100 and 575 <= mouse[1] <= 575 + 40:
                pygame.draw.rect(win, [200, 200, 50], [win_w - 10 - 135 + 5, 575 + 5, 90, 30])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w - 10 - 135 + 5, 575 + 5, 90, 30])

            # Pause
            if win_w - 10 - 135 <= mouse[0] <= win_w - 10 - 135 + 100 and 635 <= mouse[1] <= 635 + 40:
                pygame.draw.rect(win, [200, 200, 50], [win_w - 10 - 135 + 5, 635 + 5, 90, 30])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w - 10 - 135 + 5, 635 + 5, 90, 30])

            # Apply
            if win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and 710 <= mouse[1] <= 710 + 60:
                pygame.draw.rect(win, [75, 155, 0], [win_w / 2 - 100 + 5, 710 + 5, 190, 50])
            else:
                pygame.draw.rect(win, [128, 255, 0], [win_w / 2 - 100 + 5, 710 + 5, 190, 50])

            # Menu
            if win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and 780 <= mouse[1] <= 780 + 60:
                pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 5, 780 + 5, 190, 50])
            else:
                pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 5, 780 + 5, 190, 50])
        else:
            pygame.draw.rect(win, [245, 245, 50], [190, 169, 40, 40])
            pygame.draw.rect(win, [245, 245, 50], [250, 169, 40, 40])
            pygame.draw.rect(win, [245, 245, 50], [win_w - 110, 169, 40, 40])
            pygame.draw.rect(win, [245, 245, 50], [win_w - 170, 169, 40, 40])
            pygame.draw.rect(win, [245, 245, 50], [215, 300, 90, 40])
            pygame.draw.rect(win, [245, 245, 50], [win_w - 50 - 105, 300, 90, 40])
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 10 - 100 + 5, 455 + 5, 90, 30])
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 10 - 100 + 5, 515 + 5, 90, 30])
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 10 - 100 + 5, 575 + 5, 90, 30])
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 10 - 100 + 5, 635 + 5, 90, 30])
            pygame.draw.rect(win, [245, 245, 50], [win_w - 10 - 135 + 5, 455 + 5, 90, 30])
            pygame.draw.rect(win, [245, 245, 50], [win_w - 10 - 135 + 5, 515 + 5, 90, 30])
            pygame.draw.rect(win, [245, 245, 50], [win_w - 10 - 135 + 5, 575 + 5, 90, 30])
            pygame.draw.rect(win, [245, 245, 50], [win_w - 10 - 135 + 5, 635 + 5, 90, 30])
            pygame.draw.rect(win, [128, 255, 0], [win_w / 2 - 100 + 5, 710 + 5, 190, 50])
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 5, 780 + 5, 190, 50])

        applyfont = pygame.font.Font("Chunkfive.otf", 40)
        applytext = applyfont.render("Apply", 1, [0, 0, 0])
        win.blit(applytext, [win_w / 2 - applytext.get_rect()[2] / 2, 720])

        menufont = pygame.font.Font("Chunkfive.otf", 40)
        menutext = menufont.render("Menu", 1, [0, 0, 0])
        win.blit(menutext, [win_w / 2 - menutext.get_rect()[2] / 2, 795])

        togglefont = pygame.font.Font("opensans.ttf", 20)
        ontext = togglefont.render("ON", 1, [0, 0, 0])
        offtext = togglefont.render("OFF", 1, [0, 0, 0])

        win.blit(ontext, [185 + 8, 164 + 10])
        win.blit(offtext, [245 + 5, 164 + 10])

        win.blit(ontext, [win_w - 175 + 8, 164 + 10])
        win.blit(offtext, [win_w - 115 + 5, 164 + 10])

        dasnumfont = pygame.font.Font("opensans.ttf", 20)
        dasstarttext = dasnumfont.render(str(optlist[2]), 1, [0, 0, 0])
        dasinttext = dasnumfont.render(str(optlist[3]), 1, [0, 0, 0])

        win.blit(dasstarttext, [215 + 45 - dasstarttext.get_rect()[2] / 2,
                                300 + 20 - dasstarttext.get_rect()[3] / 2])

        win.blit(dasinttext, [win_w - 50 - 105 + 45 - dasinttext.get_rect()[2] / 2,
                              300 + 20 - dasinttext.get_rect()[3] / 2])

        if change == 0:
            leftctext = pygame.key.name(optlist[4])
            rightctext = pygame.key.name(optlist[5])
            hardctext = pygame.key.name(optlist[6])
            softctext = pygame.key.name(optlist[7])
            cwctext = pygame.key.name(optlist[8])
            ccwctext = pygame.key.name(optlist[9])
            holdctext = pygame.key.name(optlist[10])
            pausectext = pygame.key.name(optlist[11])
        elif change == 4:
            leftctext = "press key"
            rightctext = pygame.key.name(optlist[5])
            hardctext = pygame.key.name(optlist[6])
            softctext = pygame.key.name(optlist[7])
            cwctext = pygame.key.name(optlist[8])
            ccwctext = pygame.key.name(optlist[9])
            holdctext = pygame.key.name(optlist[10])
            pausectext = pygame.key.name(optlist[11])
        elif change == 5:
            leftctext = pygame.key.name(optlist[4])
            rightctext = "press key"
            hardctext = pygame.key.name(optlist[6])
            softctext = pygame.key.name(optlist[7])
            cwctext = pygame.key.name(optlist[8])
            ccwctext = pygame.key.name(optlist[9])
            holdctext = pygame.key.name(optlist[10])
            pausectext = pygame.key.name(optlist[11])
        elif change == 6:
            leftctext = pygame.key.name(optlist[4])
            rightctext = pygame.key.name(optlist[5])
            hardctext = "press key"
            softctext = pygame.key.name(optlist[7])
            cwctext = pygame.key.name(optlist[8])
            ccwctext = pygame.key.name(optlist[9])
            holdctext = pygame.key.name(optlist[10])
            pausectext = pygame.key.name(optlist[11])
        elif change == 7:
            leftctext = pygame.key.name(optlist[4])
            rightctext = pygame.key.name(optlist[5])
            hardctext = pygame.key.name(optlist[6])
            softctext = "press key"
            cwctext = pygame.key.name(optlist[8])
            ccwctext = pygame.key.name(optlist[9])
            holdctext = pygame.key.name(optlist[10])
            pausectext = pygame.key.name(optlist[11])
        elif change == 8:
            leftctext = pygame.key.name(optlist[4])
            rightctext = pygame.key.name(optlist[5])
            hardctext = pygame.key.name(optlist[6])
            softctext = pygame.key.name(optlist[7])
            cwctext = "press key"
            ccwctext = pygame.key.name(optlist[9])
            holdctext = pygame.key.name(optlist[10])
            pausectext = pygame.key.name(optlist[11])
        elif change == 9:
            leftctext = pygame.key.name(optlist[4])
            rightctext = pygame.key.name(optlist[5])
            hardctext = pygame.key.name(optlist[6])
            softctext = pygame.key.name(optlist[7])
            cwctext = pygame.key.name(optlist[8])
            ccwctext = "press key"
            holdctext = pygame.key.name(optlist[10])
            pausectext = pygame.key.name(optlist[11])
        elif change == 10:
            leftctext = pygame.key.name(optlist[4])
            rightctext = pygame.key.name(optlist[5])
            hardctext = pygame.key.name(optlist[6])
            softctext = pygame.key.name(optlist[7])
            cwctext = pygame.key.name(optlist[8])
            ccwctext = pygame.key.name(optlist[9])
            holdctext = "press key"
            pausectext = pygame.key.name(optlist[11])
        elif change == 11:
            leftctext = pygame.key.name(optlist[4])
            rightctext = pygame.key.name(optlist[5])
            hardctext = pygame.key.name(optlist[6])
            softctext = pygame.key.name(optlist[7])
            cwctext = pygame.key.name(optlist[8])
            ccwctext = pygame.key.name(optlist[9])
            holdctext = pygame.key.name(optlist[10])
            pausectext = "press key"

        contfont = pygame.font.Font("opensans.ttf", 15)
        leftcont = contfont.render(leftctext, 1, [0, 0, 0])
        rightcont = contfont.render(rightctext, 1, [0, 0, 0])
        hardcont = contfont.render(hardctext, 1, [0, 0, 0])
        softcont = contfont.render(softctext, 1, [0, 0, 0])
        cwcont = contfont.render(cwctext, 1, [0, 0, 0])
        ccwcont = contfont.render(ccwctext, 1, [0, 0, 0])
        holdcont = contfont.render(holdctext, 1, [0, 0, 0])
        pausecont = contfont.render(pausectext, 1, [0, 0, 0])

        win.blit(leftcont, [win_w / 2 - 10 - 100 + 5 + 45 - leftcont.get_rect()[2] / 2,
                            455 + 5 + 15 - leftcont.get_rect()[3] / 2])

        win.blit(rightcont, [win_w - 10 - 135 + 5 + 45 - rightcont.get_rect()[2] / 2,
                            455 + 5 + 15 - rightcont.get_rect()[3] / 2])

        win.blit(hardcont, [win_w / 2 - 10 - 100 + 5 + 45 - hardcont.get_rect()[2] / 2,
                             515 + 5 + 15 - hardcont.get_rect()[3] / 2])

        win.blit(softcont, [win_w - 10 - 135 + 5 + 45 - softcont.get_rect()[2] / 2,
                            515 + 5 + 15 - softcont.get_rect()[3] / 2])

        win.blit(cwcont, [win_w / 2 - 10 - 100 + 5 + 45 - cwcont.get_rect()[2] / 2,
                            575 + 5 + 15 - cwcont.get_rect()[3] / 2])

        win.blit(ccwcont, [win_w - 10 - 135 + 5 + 45 - ccwcont.get_rect()[2] / 2,
                          575 + 5 + 15 - ccwcont.get_rect()[3] / 2])

        win.blit(holdcont, [win_w / 2 - 10 - 100 + 5 + 45 - holdcont.get_rect()[2] / 2,
                           635 + 5 + 15 - holdcont.get_rect()[3] / 2])

        win.blit(pausecont, [win_w - 10 - 135 + 5 + 45 - pausecont.get_rect()[2] / 2,
                            635 + 5 + 15 - pausecont.get_rect()[3] / 2])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if change == 0:
                        if win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and 710 <= mouse[1] <= 710 + 60:
                            write_options(optlist)
                            apply_options()
                            optlist = get_options()
                            optlistog = list(optlist)
                        if win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and 780 <= mouse[1] <= 780 + 60:
                            mainmenu()
                        if 185 <= mouse[0] <= 185 + 50 and 164 <= mouse[1] <= 164 + 50:
                            optlist[0] = 1
                        if 245 <= mouse[0] <= 245 + 50 and 164 <= mouse[1] <= 164 + 50:
                            optlist[0] = 0
                        if win_w - 115 <= mouse[0] <= win_w - 115 + 50 and 164 <= mouse[1] <= 164 + 50:
                            optlist[1] = 0
                        if win_w - 175 <= mouse[0] <= win_w - 175 + 50 and 164 <= mouse[1] <= 164 + 50:
                            optlist[1] = 1
                        if win_w / 2 - 10 - 100 <= mouse[0] <= win_w / 2 - 10 - 100 + 100 and 455 <= mouse[1] <= 455 + 40:
                            # left 4
                            optlist[4] = "change"
                            change = 4
                        if win_w / 2 - 10 - 100 <= mouse[0] <= win_w / 2 - 10 - 100 + 100 and 515 <= mouse[1] <= 515 + 40:
                            # hard drop 6
                            optlist[6] = "change"
                            change = 6
                        if win_w / 2 - 10 - 100 <= mouse[0] <= win_w / 2 - 10 - 100 + 100 and 575 <= mouse[1] <= 575 + 40:
                            # rotatecw 8
                            optlist[8] = "change"
                            change = 8
                        if win_w / 2 - 10 - 100 <= mouse[0] <= win_w / 2 - 10 - 100 + 100 and 635 <= mouse[1] <= 635 + 40:
                            # hold 10
                            optlist[10] = "change"
                            change = 10
                        if win_w - 10 - 135 <= mouse[0] <= win_w - 10 - 135 + 100 and 455 <= mouse[1] <= 455 + 40:
                            # right 5
                            optlist[5] = "change"
                            change = 5
                        if win_w - 10 - 135 <= mouse[0] <= win_w - 10 - 135 + 100 and 515 <= mouse[1] <= 515 + 40:
                            # soft drop 7
                            optlist[7] = "change"
                            change = 7
                        if win_w - 10 - 135 <= mouse[0] <= win_w - 10 - 135 + 100 and 575 <= mouse[1] <= 575 + 40:
                            # rotate ccw 9
                            optlist[9] = "change"
                            change = 9
                        if win_w - 10 - 135 <= mouse[0] <= win_w - 10 - 135 + 100 and 635 <= mouse[1] <= 635 + 40:
                            # pause 11
                            optlist[11] = "change"
                            change = 11

                if event.button == 4:
                    if change == 0:
                        if 210 <= mouse[0] <= 210 + 100 and 295 <= mouse[1] <= 295 + 50:
                            if optlist[2] <= 1000:
                                optlist[2] += 1
                        if win_w - 50 - 110 <= mouse[0] <= win_w - 50 - 110 + 100 and 295 <= mouse[1] <= 295 + 50:
                            if optlist[3] <= 1000:
                                optlist[3] += 1
                if event.button == 5:
                    if change == 0:
                        if 210 <= mouse[0] <= 210 + 100 and 295 <= mouse[1] <= 295 + 50:
                            if optlist[2] >= 1:
                                optlist[2] -= 1
                        if win_w - 50 - 110 <= mouse[0] <= win_w - 50 - 110 + 100 and 295 <= mouse[1] <= 295 + 50:
                            if optlist[3] >= 1:
                                optlist[3] -=  1
            if event.type == pygame.KEYDOWN:
                if change != 0:
                    controllist = [optlist[4], optlist[5], optlist[6], optlist[7], optlist[8],
                                   optlist[9], optlist[10], optlist[11]]
                    if event.key not in controllist:
                        optlist[change] = event.key
                        change = 0


def highscoremenu():
    bestlist = get_scores()
    if bestlist[0] == -1:
        marscore = "0"
    else:
        marscore = str(bestlist[0])
    if int(marscore) >= 9999999999:
        marscore = str(9999999999)
    if bestlist[1] == -1:
        sprscore = "--:--:---"
    else:
        sprscore = milliseconds(bestlist[1])
        if len(str(sprscore[0])) < 2:
            minutes = "0" + str(sprscore[0])
        else:
            minutes = str(sprscore[0])
        if len(str(sprscore[1])) < 2:
            seconds = "0" + str(sprscore[1])
        else:
            seconds = str(sprscore[1])
        if len(str(sprscore[2])) == 2:
            milli = "0" + str(sprscore[2])
        elif len(str(sprscore[2])) < 2:
            milli = "00" + str(sprscore[2])
        else:
            milli = str(sprscore[2])
        sprscore = minutes + ":" + seconds + ":" + milli
    if bestlist[2] == -1:
        ultscore = "0"
    else:
        ultscore = str(bestlist[2])
    if int(ultscore) >= 9999999999:
        ultscore = str(9999999999)
    if bestlist[3] == -1:
        endscore = "0"
    else:
        endscore = str(bestlist[3])
    if int(endscore) >= 9999999999:
        endscore = str(9999999999)

    while 1:
        clock.tick(30)
        mouse = pygame.mouse.get_pos()

        win.fill([150, 150, 150])

        titlefont = pygame.font.Font("Chunkfive.otf", 90)
        titletext = titlefont.render("High Scores", 1, [0, 0, 0])
        win.blit(titletext, [win_w / 2 - titletext.get_rect()[2] / 2, 100])

        font1 = pygame.font.Font("Chunkfive.otf", 40)
        text1 = font1.render("Marathon: " + marscore, 1, [0, 0, 0])
        win.blit(text1, [win_w / 2 - text1.get_rect()[2] / 2, 270])

        font2 = pygame.font.Font("Chunkfive.otf", 40)
        text2 = font2.render("Sprint: " + sprscore, 1, [0, 0, 0])
        win.blit(text2, [win_w / 2 - text2.get_rect()[2] / 2, 370])

        font3 = pygame.font.Font("Chunkfive.otf", 40)
        text3 = font3.render("Ultra: " + ultscore, 1, [0, 0, 0])
        win.blit(text3, [win_w / 2 - text3.get_rect()[2] / 2, 470])

        font4 = pygame.font.Font("Chunkfive.otf", 40)
        text4 = font4.render("Endless: " + endscore, 1, [0, 0, 0])
        win.blit(text4, [win_w / 2 - text4.get_rect()[2] / 2, 570])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100, 700, 200, 80])

        if win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and 700 <= mouse[1] <= 780:
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7, 700 + 7, 200 - 14, 80 - 14])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7, 700 + 7, 200 - 14, 80 - 14])

        backfont = pygame.font.Font("Chunkfive.otf", 50)
        backtext = backfont.render("Back", 1, [0, 0, 0])
        win.blit(backtext, [win_w / 2 - backtext.get_rect()[2] / 2, 700 + backtext.get_rect()[3] / 2 - 7])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and 700 <= mouse[1] <= 780:
                        mainmenu()


def aboutmenu():
    while 1:
        clock.tick(30)
        mouse = pygame.mouse.get_pos()

        win.fill([150, 150, 150])

        aboutfont = pygame.font.Font("Chunkfive.otf", 100)
        abouttext = aboutfont.render("About", 1, [0, 0, 0])
        win.blit(abouttext, [win_w / 2 - abouttext.get_rect()[2] / 2, 100])

        font1 = pygame.font.Font("Chunkfive.otf", 40)
        text1 = font1.render("Welcome to StriS!", 1, [0, 0, 0])
        win.blit(text1, [win_w / 2 - text1.get_rect()[2] / 2, 300])

        font2 = pygame.font.Font("Chunkfive.otf", 40)
        text2 = font2.render("This is a Tetris clone", 1, [0, 0, 0])
        win.blit(text2, [win_w / 2 - text2.get_rect()[2] / 2, 350])

        font3 = pygame.font.Font("Chunkfive.otf", 40)
        text3 = font3.render("made in Python using Pygame.", 1, [0, 0, 0])
        win.blit(text3, [win_w / 2 - text3.get_rect()[2] / 2, 400])

        font4 = pygame.font.Font("Chunkfive.otf", 40)
        text4 = font4.render("It was made using the", 1, [0, 0, 0])
        win.blit(text4, [win_w / 2 - text4.get_rect()[2] / 2, 450])

        font5 = pygame.font.Font("Chunkfive.otf", 40)
        text5 = font5.render("Tetris Guideline, SRS and all!", 1, [0, 0, 0])
        win.blit(text5, [win_w / 2 - text5.get_rect()[2] / 2, 500])

        font6 = pygame.font.Font("Chunkfive.otf", 40)
        text6 = font6.render("Have fun!", 1, [0, 0, 0])
        win.blit(text6, [win_w / 2 - text6.get_rect()[2] / 2, 600])

        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 100, 700, 200, 80])

        if win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and 700 <= mouse[1] <= 780:
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 100 + 7, 700 + 7, 200 - 14, 80 - 14])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 100 + 7, 700 + 7, 200 - 14, 80 - 14])

        backfont = pygame.font.Font("Chunkfive.otf", 50)
        backtext = backfont.render("Back", 1, [0, 0, 0])
        win.blit(backtext, [win_w / 2 - backtext.get_rect()[2] / 2, 700 + backtext.get_rect()[3] / 2 - 7])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if win_w / 2 - 100 <= mouse[0] <= win_w / 2 - 100 + 200 and 700 <= mouse[1] <= 780:
                        mainmenu()


def get_options():
    options = open("options.txt", "r")
    opt = options.readlines()

    hold = opt[1]
    hold.strip()
    hold.strip("\\")
    hold.strip("n")
    hold = int(hold)

    ghost = opt[3]
    ghost.strip()
    ghost.strip("\\")
    ghost.strip("n")
    ghost = int(ghost)

    dasstart = opt[5]
    dasstart.strip()
    dasstart.strip("\\")
    dasstart.strip("n")
    dasstart = int(dasstart)

    das = opt[7]
    das.strip()
    das.strip("\\")
    das.strip("n")
    das = int(das)

    left = opt[9]
    left.strip()
    left.strip("\\")
    left.strip("n")
    left = int(left)

    right = opt[11]
    right.strip()
    right.strip("\\")
    right.strip("n")
    right = int(right)

    hard = opt[13]
    hard.strip()
    hard.strip("\\")
    hard.strip("n")
    hard = int(hard)

    soft = opt[15]
    soft.strip()
    soft.strip("\\")
    soft.strip("n")
    soft = int(soft)

    cw = opt[17]
    cw.strip()
    cw.strip("\\")
    cw.strip("n")
    cw = int(cw)

    ccw = opt[19]
    ccw.strip()
    ccw.strip("\\")
    ccw.strip("n")
    ccw = int(ccw)

    holdkey = opt[21]
    holdkey.strip()
    holdkey.strip("\\")
    holdkey.strip("n")
    holdkey = int(holdkey)

    pause = opt[23]
    pause.strip()
    pause.strip("\\")
    pause.strip("n")
    pause = int(pause)

    options.close()

    return [hold, ghost, dasstart, das, left, right, hard, soft, cw, ccw, holdkey, pause]


def write_options(opts):
    options = open("options.txt", "w")
    options.write("hold\n")
    options.write(str(opts[0]) + "\n")
    options.write("ghost\n")
    options.write(str(opts[1]) + "\n")
    options.write("das_start\n")
    options.write(str(opts[2]) + "\n")
    options.write("das\n")
    options.write(str(opts[3]) + "\n")
    options.write("left\n")
    options.write(str(opts[4]) + "\n")
    options.write("right\n")
    options.write(str(opts[5]) + "\n")
    options.write("hard\n")
    options.write(str(opts[6]) + "\n")
    options.write("soft\n")
    options.write(str(opts[7]) + "\n")
    options.write("cw\n")
    options.write(str(opts[8]) + "\n")
    options.write("ccw\n")
    options.write(str(opts[9]) + "\n")
    options.write("holdkey\n")
    options.write(str(opts[10]) + "\n")
    options.write("pause\n")
    options.write(str(opts[11]) + "\n")
    options.close()


def apply_options():
    global hold_opt
    global ghost_opt
    global das_startup
    global das
    global left
    global right
    global hard
    global soft
    global cw
    global ccw
    global hold
    global pause

    opt_list = get_options()

    hold_opt = opt_list[0]
    ghost_opt = opt_list[1]
    das_startup = opt_list[2]
    das = opt_list[3]
    left = opt_list[4]
    right = opt_list[5]
    hard = opt_list[6]
    soft = opt_list[7]
    cw = opt_list[8]
    ccw = opt_list[9]
    hold = opt_list[10]
    pause = opt_list[11]

    pygame.key.set_repeat(das_startup, das)

mainmenu()
