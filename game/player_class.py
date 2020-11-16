#region(do zmiany/modyfikacji)
#Uwaga zmiana pola w self.__board odbywa się poprzez nie zmianę jak to ma być tylko poprzez wstawienie w to miejsce nowego obiektu o wymaganym znaku
#endregion

import os, time
import keyboard
import time

from string import ascii_uppercase
from termcolor import colored, cprint

class Field:
    def __init__(self, sign):
        self.__sign = sign
        self.__hiden = True

    @property
    def sign(self):
        return self.__sign
    @sign.setter
    def sign(self, sign):
        self.__sign = sign
    @property
    def hiden(self):
        return self.__hiden
    @hiden.setter
    def hiden(self, hiden):
        self.__hiden = hiden

class Player:
    def __init__(self, size_map, fleet_size_list):
        self.__nick_name = "test"
        self.__score = None
        self.__board = None
        self.__hiden_board = None
        self.__size_map = size_map
        self.__fleet_size_list = fleet_size_list       

    @property
    def nick_name(self):
        return self.__nick_name

    @property
    def hiden_board(self):
        return self.__hiden_board
    
    @property
    def board(self):
        return self.__board
    
    def set_nick_name(self, nick_name: str = "gamer", min_char: int = 2, max_char: int = 20):        
        if len(nick_name) >= min_char and len(nick_name) <= max_char:
            self.__nick_name = nick_name            
        else:
            print("Ilość znaków musi znajdować się między {} - {}".format(min_char, max_char))

    def __draw_board(self, position_x, position_y, size, board):
        
        letters_of_columns = " ".join([letter for letter in ascii_uppercase if ascii_uppercase.index(letter)<size])
        
        cprint("       {}".format(letters_of_columns), 'white')
        for row in range(size):
            print("{:>5}".format(row+1), end = "  ")
            for column in range(size):
                if position_y == row and position_x == column:
                    cprint(self.__board[row][column].sign, 'red', end =" ")
                    
                else:
                    if not self.__board[row][column].sign == "~":
                        
                        cprint(self.__board[row][column].sign, 'green', end = " ")
                    else:                     
                          
                        cprint(self.__board[row][column].sign, 'blue', end = " ")
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
    def __print_info_about_fleet(self, orientation,empty_fleet_condition):
        if empty_fleet_condition:
            if orientation == 'h':
                orientation = 'horizontally'
            else:
                orientation = 'vertically'
            print()
            print("Rozmieszcz swoje okręty {}".format(self.nick_name))
            print("Wybrane ustawienie układania statków: {}".format(orientation))
            print("Dostępne czteromasztowce: {}".format(self.__fleet_size_list[0]))
            print("Dostępne trójmasztowce: {}".format(self.__fleet_size_list[1]))
            print("Dostępne dwumasztowce: {}".format(self.__fleet_size_list[2]))
            print("Dostępne jednomasztowce: {}".format(self.__fleet_size_list[3]))
        else:
            print("Rozmieszczanie statków zakończone!")
            time.sleep(2)
    def __change_orientation(self, orientation):
        if keyboard.is_pressed('h'):
            orientation = 'h'
            return orientation
        if keyboard.is_pressed('v'):
            orientation = 'v'
            return orientation
        return orientation
    
    def __validation_put_ship_horizontal(self, position_y,position_x, required_field):
        resutl = None
        if position_x + required_field > self.__size_map:              
            resutl = False
        else:
            for i in range(required_field):
                if not self.__board[position_y][position_x + i].sign == "~":
                    resutl = False
                    break
                else:
                    resutl = True
        return resutl
    
    def __validation_put_ship_vertical(self, position_y,position_x, required_field):
        resutl = None
        if position_y + required_field > self.__size_map:
            resutl = False
        else:
            for i in range(required_field):
                if not self.__board[position_y+i][position_x].sign == "~":
                    resutl = False
                    break
                else:
                    resutl = True
        return resutl

    def __reduce_fleet(self, index):
        if self.__fleet_size_list[index] > 0:
            self.__fleet_size_list[index] -= 1

    def __put_ship(self, position_x, position_y, orientation ):
        if keyboard.is_pressed('space'):
            if self.__fleet_size_list[0] > 0:                
                if orientation == 'h':
                    if self.__validation_put_ship_horizontal(position_y, position_x, 4):
                        for mod_x in range(4):
                            self.__board[position_y][position_x+mod_x] = Field("4")
                        self.__reduce_fleet(0)
                else:
                    if self.__validation_put_ship_vertical(position_y,position_x, 4):
                        for mod_y in range(4):
                            self.__board[position_y+mod_y][position_x] = Field("4")
                        self.__reduce_fleet(0)
            elif self.__fleet_size_list[1] > 0:
                if orientation == 'h':
                    if self.__validation_put_ship_horizontal(position_y, position_x, 3):
                        for mod_x in range(3):
                            self.__board[position_y][position_x+mod_x] = Field("3")
                        self.__reduce_fleet(1)
                else:
                    if self.__validation_put_ship_vertical(position_y,position_x, 3):
                        for mod_y in range(3):
                            self.__board[position_y+mod_y][position_x] = Field("3")
                        self.__reduce_fleet(1)
            elif self.__fleet_size_list[2] > 0:
                if orientation == 'h':
                    if self.__validation_put_ship_horizontal(position_y, position_x, 2):
                        for mod_x in range(2):
                            self.__board[position_y][position_x+mod_x] = Field("2")
                        self.__reduce_fleet(2)
                else:
                    if self.__validation_put_ship_vertical(position_y,position_x, 2):
                        for mod_y in range(2):
                            self.__board[position_y+mod_y][position_x] = Field("2")
                        self.__reduce_fleet(2)
            elif self.__fleet_size_list[3] > 0:
                if orientation == 'h':
                    if self.__validation_put_ship_horizontal(position_y, position_x, 1):
                        for mod_x in range(1):
                            self.__board[position_y][position_x+mod_x] = Field("1")
                        self.__reduce_fleet(3)
                else:
                    if self.__validation_put_ship_vertical(position_y,position_x, 1):
                        for mod_y in range(1):
                            self.__board[position_y+mod_y][position_x] = Field("1")
                        self.__reduce_fleet(3)
    
    def __check_empty_fleet(self):
        if sum(self.__fleet_size_list) > 0:
            return True
        else:
            return False

    def set_board(self):
        
        position_x=2
        position_y=3
        orientation = 'h'
        empty_fleet_condition = True
        
        self.__board = [ [Field("~") for columne in range(self.__size_map)] for row in range(self.__size_map)]

        self.__hiden_board = [ [Field('~') for coummne in range(self.__size_map)] for row in range(self.__size_map)]


        while empty_fleet_condition:
            os.system("cls || clear")
            
            empty_fleet_condition = self.__check_empty_fleet()

            self.__draw_board(position_x, position_y, self.__size_map, self.__board)

            position_y = self.__move_cursor_up_down(position_y)
            position_x = self.__move_cursor_left_right(position_x)
            orientation = self.__change_orientation(orientation)

            self.__put_ship(position_x, position_y, orientation)

            self.__print_info_about_fleet(orientation, empty_fleet_condition)         

            time.sleep(0.15)

        