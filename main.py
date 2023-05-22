import copy
import pygame
import sys
import datetime
import random


class Graphics:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800))
        self.board_graphic = pygame.image.load('graphics/board.png').convert_alpha()
        self.nought_graphic = pygame.image.load('graphics/nought.png').convert_alpha()
        self.cross_graphic = pygame.image.load('graphics/cross.png').convert_alpha()
        self.graphical_board_list = []

    def draw_board(self, screen):
        screen.blit(self.board_graphic, (0, 0))

    def create_rectangles(self):
        #  Rect(left, top, width, height)
        width = 240
        height = 235
        for y in range(3):
            for x in range(3):
                space = pygame.Rect((x * 290) + 5, (y * 295) + 5, width, height)
                self.graphical_board_list.append(space)
        return self.graphical_board_list


class Board:
    def __init__(self):
        self.graphics = Graphics()
        self.logical_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def get_empty_spaces(self, board):
        empty_spaces = []
        for space in range(9):
            if board[space] == 0:
                empty_spaces.append(space)
        return empty_spaces

    def check_win_condition(self, board):
        win_condition = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                         [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        for list in win_condition:
            check_win = []
            for cell in list:
                if board[cell] == 1 or board[cell] == 2:
                    check_win.append(board[cell])
                if len(check_win) == 3:
                    if check_win[0] == check_win[1] and check_win[0] == check_win[2]:
                        if check_win[0] == 1:
                            return 1
                        else:
                            return 2

    def check_draw(self, board):
        for cell in board:
            if board[cell] == 0:
                return False
        return True

    def draw_marks(self, graphical_board):
        index = 0
        for i in self.logical_board:
            if i == 1:
                self.graphics.screen.blit(self.graphics.nought_graphic, graphical_board[index])
            elif i == 2:
                self.graphics.screen.blit(self.graphics.cross_graphic, graphical_board[index])
            index += 1

    def insert_mark(self, board, mark, index):
        board[index] = mark


class GameLogic:
    def __init__(self):
        self.graphics = Graphics()
        self.board = Board()
        self.state = self.start_game_state
        self.player = 1
        self.opponent = 2

    def get_time(self):
        return datetime.datetime.now()

    def start_game_state(self, event):
        self.graphics.draw_board(self.graphics.screen)
        random_num = random.randint(1,2)
        if random_num == 1:
            self.state = self.player_turn
        else:
            self.board.insert_mark(self.board.logical_board, self.opponent, 0)
            self.state = self.player_turn

    def player_turn(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click = pygame.mouse.get_pos()
            index = 0
            for space in self.graphics.graphical_board_list:
                if space.collidepoint(mouse_click) and self.board.logical_board[index] == 0:
                    self.board.insert_mark(self.board.logical_board, self.player, index)

                    self.state = self.opponent_turn
                if self.board.check_win_condition(self.board.logical_board) == self.player \
                        or self.board.check_win_condition(self.board.logical_board) == self.opponent:
                    self.state = self.winner_state
                if not self.board.get_empty_spaces(self.board.logical_board):
                    self.state = self.draw_state

                index += 1

    def opponent_turn(self, event):
        eval, move = self.minimax(self.board.logical_board, False)
        self.board.insert_mark(self.board.logical_board, self.opponent, move)
        self.state = self.player_turn
        if self.board.check_win_condition(self.board.logical_board) == self.player \
                or self.board.check_win_condition(self.board.logical_board) == self.opponent:
            self.state = self.winner_state
        if not self.board.get_empty_spaces(self.board.logical_board):
            self.state = self.draw_state

    def winner_state(self, event):
        print('winner')

    def draw_state(self, event):
        print('draw')

    def minimax(self, board, maximizing):
        case = self.board.check_win_condition(board)

        if case == 1:
            self.state = self.winner_state
            return 1, 1

        if case == 2:
            self.state = self.winner_state
            return -1, -1

        elif not self.board.get_empty_spaces(board):
            self.state = self.draw_state
            return 0, 0

        if maximizing:
            max_eval = -100
            best_move = None
            empty_spaces = self.board.get_empty_spaces(board)

            for space in empty_spaces:
                temp_board = copy.deepcopy(board)
                temp_board[space] = 1
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = space

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_spaces = self.board.get_empty_spaces(board)

            for space in empty_spaces:
                temp_board = copy.deepcopy(board)
                temp_board[space] = 2
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = space

            return min_eval, best_move


def main():
    pygame.init()
    clock = pygame.time.Clock()
    game = GameLogic()
    graphics = game.graphics
    screen_update = pygame.USEREVENT
    pygame.time.set_timer(screen_update, 30)

    graphics.create_rectangles()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game.state(event)
        if event.type == screen_update:
            graphics.draw_board(graphics.screen)
            game.board.draw_marks(game.graphics.graphical_board_list)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()



