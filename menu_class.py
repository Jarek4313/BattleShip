#region(zmienić/poprawić:)
#       self.__actual_value = min_value + 2 - aby wskazywało środek między min a max/ nie koniecznie jest to istotne/
#       BUG poprawić kursor aby po wybraniu ilość w min_max_item_menu nie przechodził do        ostatniej opcji
#endregion
import os
import keyboard
import time
from options.options_class import Options
from options.map_class import Map
from options.ship_class import Ship
from options.turn_limit_class import Turn

class Menu:
    def __init__(self, list_menu, logo):
        self.__menu_list = list_menu
        self.__menu_logo = logo
        
##############################################################################################
#region(metody do rysowania pozycji menu, logo, kursor)
    def __draw_arrow(self, arrow_counter_in_menu, arrow_indication,menu_option_edit):
        if menu_option_edit:
            print()            
        else:
            if arrow_counter_in_menu == arrow_indication:
                print("<-")
            else:
                print()
            
    def __draw_simple_menu(self, item):
        print("{}".format(item.item_name), end =" ")
    def __draw_min_max_menu(self, item, menu_min_max_edit):
        if menu_min_max_edit:
            print("{} : < {} >".format(item.item_name, item.actual_value), end =" ")
        else:
            print("{} : {}".format(item.item_name, item.actual_value), end =" ")
    #region(__draw_logo(self)
    def __draw_logo(self):
        path = r'c:\BattleShip\ascii_alphabet.txt'
        ascii_logo_to_draw = []
        alpha_ascii_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','w','v','x','y','z',' ','!']
        try:
            with open(path, 'r', encoding="UTF-8") as file:
                content = file.readlines()    
        except FileExistsError:
            print("Plik nie istnieje")
        for i in range(len(content)):
            content[i] = content[i].strip()
        for char_in_logo in self.__menu_logo:
            tmp = 0
            for char in alpha_ascii_list:
                if char == char_in_logo:
                    break            
                tmp += 1        
            i = 0
            if ascii_logo_to_draw == []:
                for i in range(7):
                    ascii_logo_to_draw.append(content[i + (tmp * 7)])
                    i += 1
            else:
                for i in range(7):
                    ascii_logo_to_draw[i] += content[i + (tmp * 7)]
                    i += 1
        for item in ascii_logo_to_draw:
            print(item)
    #endregion
#endregion
##############################################################################################
#region(sterowanie menu, wybór min-max item)
    def __validation_indication_in_menu(self, arrow_indication, size_max, size_min = 0 ):
        if arrow_indication < size_min:
            return size_max 
        elif arrow_indication > size_max:
            return size_min
        else:
            return arrow_indication

    def __menu_user_control(self, arrow_indication, size_max, size_min = 0):
        input_key = True
        while input_key:
            if keyboard.is_pressed('down'):
                arrow_indication += 1
                input_key = False                
                return self.__validation_indication_in_menu(arrow_indication, size_max, size_min)
            if keyboard.is_pressed('up'):
                arrow_indication -= 1
                input_key = False    
                return self.__validation_indication_in_menu(arrow_indication, size_max, size_min)
            if keyboard.is_pressed('left'):
                arrow_indication = 100
                input_key = False    
                return arrow_indication
            if keyboard.is_pressed('right'):
                arrow_indication = -100
                input_key = False    
                return arrow_indication
    
    def __menu_min_max_user_control(self, actual_value, size_max, size_min):
        input_key = True
        while input_key:
            if keyboard.is_pressed('down'):
                actual_value -= 1
                input_key = False                
                if actual_value < size_min:
                    return 0
                else:
                    return -1
            if keyboard.is_pressed('up'):
                actual_value += 1
                input_key = False    
                if actual_value > size_max:
                    return 0
                else:
                    return 1
            if keyboard.is_pressed('right'):
                actual_value = -100
                input_key = False    
                return actual_value        
#endregion
##############################################################################################
#region(główna metoda klasy use_menu)
    def use_menu(self):
        arrow_indication = 0 #domyślna pozycja kursora
        tmp_arrow_indication = 0
        size_menu = len(self.__menu_list) - 1
        run_menu = True
        menu_return_value = None
        menu_min_max_edit = False
        menu_min_max_object = None

        while run_menu:
            os.system("cls || clear")
            self.__draw_logo()

            arrow_counter_in_menu = 0
            for item in self.__menu_list: 
                if isinstance(item, simple_item_menu):
                    self.__draw_simple_menu(item)
                    self.__draw_arrow(arrow_counter_in_menu, arrow_indication,menu_min_max_edit)                
                elif isinstance(item, min_max_item_menu):
                    
                    if arrow_counter_in_menu == arrow_indication and menu_min_max_edit:
                        self.__draw_min_max_menu(item, True)
                    else:
                        self.__draw_min_max_menu(item, False)
                    self.__draw_arrow(arrow_counter_in_menu, arrow_indication,menu_min_max_edit)
                arrow_counter_in_menu += 1

            if menu_min_max_edit:
                tmp_arrow_indication = self.__menu_min_max_user_control(menu_min_max_object.actual_value, menu_min_max_object.max_value, menu_min_max_object.min_value)    
            else:                                
                tmp_arrow_indication = self.__menu_user_control(arrow_indication,size_menu)    
            
            if tmp_arrow_indication >= 100 and not menu_min_max_edit:                
                item = self.__menu_list[arrow_indication]

                if isinstance(item, simple_item_menu):                    
                    menu_return_value = item.item_value
                    run_menu = False
                elif isinstance(item, min_max_item_menu):                    
                    menu_min_max_edit = True
                    menu_min_max_object = item
                    tmp_arrow_indication = 0

            if tmp_arrow_indication <= -100:
                menu_min_max_edit = False

            if menu_min_max_edit:
                menu_min_max_object.actual_value += tmp_arrow_indication                
            else:
                arrow_indication = self.__validation_indication_in_menu(tmp_arrow_indication, size_menu)
                
            time.sleep(0.21)    
            
        return menu_return_value
#endregion            
##############################################################################################
#region(klasy/rodzaje menu)
class simple_item_menu:
    def __init__(self, item_menu_name, menu_return_value):
        self.__item_menu_name = item_menu_name
        self.__item_menu_value = menu_return_value
    @property
    def item_name(self):
        return self.__item_menu_name
    @property
    def item_value(self):
        return self.__item_menu_value

class min_max_item_menu:
    #menu_return_value
    def __init__(self, item_menu_name, min_value, max_value, option_object):
        self.__item_menu_name = item_menu_name        
        self.__min_value = min_value
        self.__max_value = max_value
        self.__option_object = option_object
    @property
    def min_value(self):
        return self.__min_value
    @property
    def max_value(self):
        return self.__max_value
    @property
    def item_name(self):
        return self.__item_menu_name
    
    @property
    def actual_value(self):
        if isinstance(self.__option_object, Map):
            return self.__option_object.map_size   
        if isinstance(self.__option_object, Ship):
            return self.__option_object.fleet_size 
        if isinstance(self.__option_object, Turn):
            return self.__option_object.turn_limit

    @actual_value.setter
    def actual_value(self, value):
        if isinstance(self.__option_object, Map):
            self.__option_object.map_size = value
        if isinstance(self.__option_object, Ship):
            self.__option_object.fleet_size = value
        if isinstance(self.__option_object, Turn):
            self.__option_object.turn_limit = value
#endregion
##############################################################################################


