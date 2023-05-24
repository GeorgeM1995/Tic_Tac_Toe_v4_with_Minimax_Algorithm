import copy
import pygame
import sys
import random
import enum


class Mark(enum.IntEnum):
    PLAYER = 1
    OPPONENT = 2
    EMPTY = 0


class Board:
    def __init__(self):
        self._logical_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def insert_mark(self, mark, index):
        self._logical_board[index] = mark
    
    def mark_at(self, index):
        return self._logical_board[index]
    
    def check_win_condition(self):
        win_condition = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                         [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        for condition in win_condition:
            check_win = []
            for cell in condition:
                if self._logical_board[cell] == Mark.PLAYER or self._logical_board[cell] == Mark.OPPONENT:
                    check_win.append(self._logical_board[cell])
                if len(check_win) == 3:
                    if check_win[0] == check_win[1] and check_win[0] == check_win[2]:
                        if check_win[0] == 1:
                            return 1
                        else:
                            return 2
    
    def get_empty_spaces(self):
        empty_spaces = []
        for space in range(9):
            if self._logical_board[space] == Mark.EMPTY:
                empty_spaces.append(space)
        return empty_spaces


class Graphics:
    def __init__(self):
        self._screen = pygame.display.set_mode((800, 800))
        self._board_graphic = pygame.image.load('graphics/board.png').convert_alpha()
        self._nought_graphic = pygame.image.load('graphics/nought.png').convert_alpha()
        self._cross_graphic = pygame.image.load('graphics/cross.png').convert_alpha()
        self._graphical_board_list = []
        
        #  Rect(left, top, width, height)
        width = 240
        height = 235
        for y in range(3):
            for x in range(3):
                space = pygame.Rect((x * 290) + 5, (y * 295) + 5, width, height)
                self._graphical_board_list.append(space)
    
    def get_clicked_index(self, mouse_click):
        for index in range(len(self._graphical_board_list)):
            space = self._graphical_board_list[index]
            if space.collidepoint(mouse_click):
                return index
        return None
    
    def draw(self, board):
        self._screen.blit(self._board_graphic, (0, 0))
        for index in range(len(self._graphical_board_list)):
            if board.mark_at(index) == Mark.PLAYER:
                self._screen.blit(self._nought_graphic, self._graphical_board_list[index])
            elif board.mark_at(index) == Mark.OPPONENT:
                self._screen.blit(self._cross_graphic, self._graphical_board_list[index])
            

class Game:
    def __init__(self):
        self._state = self._state_start_game
        self._board = Board()
        self._graphics = Graphics()
    
    def update(self, event):
        self._state(event)
        self._graphics.draw(self._board)
    
    def _state_start_game(self, event):
        random_num = random.randint(1, 2)
        if random_num == 1:
            self._state = self._state_player_turn
        else:
            self._board.insert_mark(Mark.OPPONENT, 0)
            self._state = self._state_player_turn
    
    def _state_player_turn(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click = pygame.mouse.get_pos()
            index = self._graphics.get_clicked_index(mouse_click)
            if index is not None and self._board.mark_at(index) == Mark.EMPTY:
                self._board.insert_mark(Mark.PLAYER, index)
                self._state = self._state_opponent_turn
            
            if self._board.check_win_condition() == Mark.PLAYER or self._board.check_win_condition() == Mark.OPPONENT:
                self._state = self._state_winner
            if not self._board.get_empty_spaces() and not self._state == self._state_winner:
                self._state = self._state_draw
    
    def _state_opponent_turn(self, event):
        evaluation, move = self._minimax(self._board, False)
        self._board.insert_mark(Mark.OPPONENT, move)
        self._state = self._state_player_turn

        if self._board.check_win_condition() == Mark.PLAYER or self._board.check_win_condition() == Mark.OPPONENT:
            self._state = self._state_winner
        if not self._board.get_empty_spaces() and not self._state == self._state_winner:
            self._state = self._state_draw
    
    def _state_winner(self, event):
        print("winner")
    
    def _state_draw(self, event):
        print("draw")

    def _minimax(self, board, maximizing):
        case = board.check_win_condition()
        
        if case == 1:
            self._state = self._state_winner
            return 1, 1

        if case == 2:
            self._state = self._state_winner
            return -1, -1

        elif not board.get_empty_spaces():
            self._state = self._state_draw
            return 0, 0

        if maximizing:
            max_evaluation = -100
            best_move = None
            empty_spaces = board.get_empty_spaces()

            for space in empty_spaces:
                temp_board = copy.deepcopy(board)
                temp_board.insert_mark(Mark.PLAYER, space)
                evaluation = self._minimax(temp_board, False)[0]
                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    best_move = space

            return max_evaluation, best_move

        else:
            min_evaluation = 100
            best_move = None
            empty_spaces = board.get_empty_spaces()

            for space in empty_spaces:
                temp_board = copy.deepcopy(board)
                temp_board.insert_mark(Mark.OPPONENT, space)
                evaluation = self._minimax(temp_board, True)[0]
                if evaluation < min_evaluation:
                    min_evaluation = evaluation
                    best_move = space

            return min_evaluation, best_move


def main():
    pygame.init()
    clock = pygame.time.Clock()
    game = Game()
    screen_update = pygame.USEREVENT
    pygame.time.set_timer(screen_update, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game.update(event)
            pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
