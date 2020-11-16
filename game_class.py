#region (zmiany/ dodane rzeczy)
# rozmiar poszczególnych statków jest przekazywany poprzez listę
#endregion
import os
import time
import copy
import keyboard
from game.player_class import Player
from game.player_class import Field
from game.shoot_info_class import Shot_Info

from string import ascii_uppercase
from termcolor import colored, cprint
class Game:
    
    def __init__(
        self, size_map, 
        fleet_size_list
        ):
        self.__size_map = size_map
        self.__fleet_size_list = fleet_size_list
        self.__player_one = None
        self.__player_two = None

    def set_player_one(self):
        player = Player(
            self.__size_map,
            copy.copy(self.__fleet_size_list))
        
        os.system("cls || clear")

        while player.nick_name == None:
            player.set_nick_name(input("Podaj imię pierwszego gracza: "))           
        
        time.sleep(.5)
        
        player.set_board()
        
        self.__player_one = player

    def set_player_two(self):
        player = Player(
            self.__size_map,
            copy.copy(self.__fleet_size_list) )
        
        os.system("cls || clear")

        while player.nick_name == None:
            player.set_nick_name(input("Podaj imię drugiego gracza: "))

        time.sleep(.15)

        player.set_board()

        self.__player_two = player
 
    def TEST_method_show_about_yourself(self):
        print(self.__size_map)
        print(self.__player_one.nick_name)
        print(self.__player_two.nick_name)
        
        input()
    
    def __draw_board(self,position_x, position_y, board):
        size = self.__size_map
        letters_of_columns = " ".join([letter for letter in ascii_uppercase if ascii_uppercase.index(letter)<size])
        cprint("       {}".format(letters_of_columns), 'white')
        for row in range(size):
            print("{:>5}".format(row+1), end = "  ")
            for column in range(size):
                if position_y == row and position_x == column:
                    cprint(board[row][column].sign, 'red', end =" ")
                    
                else:
                    if not board[row][column].sign == "~":
                        cprint(board[row][column].sign, 'green', end = " ")
                    else:
                        if board[row][column].hiden == True:
                            cprint(board[row][column].sign, 'white', end = " ")
                        else:
                            cprint(board[row][column].sign, 'blue', end = " ")
            print()

    def __move_cursor_up_down(self, position_y):
        if keyboard.is_pressed("down"):
            position_y += 1
        if keyboard.is_pressed("up"):
            position_y -= 1
        
        if position_y < 0:
            return 0
        elif position_y > self.__size_map-1:
            return self.__size_map-1
        else:
            return position_y
    def __move_cursor_left_right(self, position_x):
        if keyboard.is_pressed("left"):
            position_x -= 1
        if keyboard.is_pressed("right"):
            position_x += 1
        if position_x < 0:
            return 0
        elif position_x > self.__size_map-1:
            return self.__size_map-1
        else:
            return position_x
    def __print_info_about_game(self, nick_name: str):
        print("Ruch gracza: {}".format(nick_name))
    
    def __check_field(self,position_x, position_y, chooser_player, checked_player):
        shot_info = Shot_Info()

        if keyboard.is_pressed('space'):            
            if checked_player.board[position_y][position_x].sign == "~":
                if chooser_player.hiden_board[position_y][position_x].hiden == True:
                    chooser_player.hiden_board[position_y][position_x].hiden = False
                    shot_info.waste = True            
            elif not checked_player.board[position_y][position_x].sign == "~":
                chooser_player.hiden_board[position_y][position_x].sign = checked_player.board[position_y][position_x].sign
                shot_info.hit = True
            return shot_info
        else:
            return shot_info            
                
    def __check_win_condition(self, chooser_player, checked_player):        
        win_result = True        
        for row in range(self.__size_map):
            for column in range(self.__size_map):
                #print(chooser_player.hiden_board[row][column].sign, checked_player.board[row][column].sign) 
                #time.sleep(.3)
                if not chooser_player.hiden_board[row][column].sign == checked_player.board[row][column].sign:
                    win_result = False
                
        return win_result
                    
    def play_game(self):
        position_x = 2
        position_y = 2

        
        #change_player = False
        shot_info = None
        change_player = True
        while True:
            os.system("cls || clear")

            #tego ifa koniecznie zmienić/uprościć
            if not shot_info == None:
                if shot_info.waste:
                    if change_player:
                        chooser_player = self.__player_two
                        checked_player = self.__player_one
                        change_player = False
                    else:
                        chooser_player = self.__player_one
                        checked_player = self.__player_two    
                        change_player = True
            else:
                chooser_player = self.__player_one
                checked_player = self.__player_two 

            position_y = self.__move_cursor_up_down(position_y)
            position_x = self.__move_cursor_left_right(position_x)

            shot_info = self.__check_field(position_x,position_y,chooser_player, checked_player)
            self.__draw_board(position_x, position_y, chooser_player.hiden_board)
            self.__draw_board(position_x, position_y, checked_player.board)
            self.__print_info_about_game(chooser_player.nick_name)
                        
            if self.__check_win_condition(chooser_player, checked_player):
                print("You win")
                time.sleep(3)
                return 

            
            time.sleep(0.15)

# gm = Game(6,[1,0,1,0])      
# gm.set_player_one() 
# gm.set_player_two()
# gm.play_game()
