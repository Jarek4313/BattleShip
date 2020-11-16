#region(zmienić/poprawić:)
# Uwaga w pliku menu_class w metodzie klasy menu na początku pętli zakomentowane jest rysowanie loga
#endregion

#region(testy/działające rzeczy):
#-działa cały system menu 
#-ustawianie opcji tj. map_size, fleet_size (1-5) 
#endregion

#region lista żeczy do zrobienia, tymczasowych, do poprawy
#nie użyta zmienna five_masted_fleet_size w options_menu
#endregion

import termcolor
import os

from options.map_class import Map
from options.ship_class import Ship
from options.turn_limit_class import Turn

from menu_class import simple_item_menu
from menu_class import min_max_item_menu
from menu_class import Menu

from game_class import Game

if __name__ == "__main__":

    ##############################################################################################
    #region(obiekty do opcji gry, wielkość mapy, wielkość floty, ilość tur w grze)
    map_size = Map()
    turn_limit = Turn()    
    single_mast_fleet_size = Ship()
    two_masted_fleet_size = Ship()
    three_masted_fleet_size = Ship()
    four_masted_fleet_size = Ship()
    five_masted_fleet_size = Ship()#jeszcze nie użyty
    #endregion
    ##############################################################################################
    #region(obiekty składowe do main_menu, options_menu)
    
    #region(zmienne obiektów menu wykorzystywane w main_menu, options_menu)
    new_game_item_menu = simple_item_menu("Nowa gra", 1)
    options_item_menu = simple_item_menu("Opcje", 2)
    quit_game_item_menu = simple_item_menu("Wyjście", 3)

    map_size_item_menu = min_max_item_menu("Wielkość mapy",5,10, map_size)
    turn_limit_item_menu = min_max_item_menu("Limit tór", 20, 50, turn_limit)
    single_mast_fleet_item_menu = min_max_item_menu("Ilość jednomasztowców",1,10,single_mast_fleet_size)
    two_masted_fleet_item_menu = min_max_item_menu("Ilość dwumasztowców",1,6,two_masted_fleet_size)
    three_masted_fleet_item_menu = min_max_item_menu("Ilość trójmasztowców",1,5,three_masted_fleet_size)
    four_masted_fleet_item_menu = min_max_item_menu("Ilość czteromasztowców",1,3,four_masted_fleet_size)

    one_player_game_item_menu = simple_item_menu("Gra jednoosobowa", 11)
    two_player_game_item_menu = simple_item_menu("Gra dwuosobowa", 12)
    #endregion
    
    #region(właściwe obiekty menu, które wyświetlane są w głównej pętli gry)
    main_menu = Menu([
        new_game_item_menu, 
        options_item_menu,
        quit_game_item_menu],
        "battle ship !!!")
    
    options_menu = Menu([
        map_size_item_menu,
        turn_limit_item_menu,
        single_mast_fleet_item_menu,
        two_masted_fleet_item_menu,
        three_masted_fleet_item_menu,
        four_masted_fleet_item_menu,
        quit_game_item_menu,],
        "game options")
    
    new_game_menu = Menu([
        one_player_game_item_menu,
        two_player_game_item_menu,
        quit_game_item_menu],
        "player options")

    #endregion
    
    #endregion
    ##############################################################################################
    #region(obiekty graczy,gry)
    player_one = None
    player_two = None
    game = None #główny obiekt programu, do którego wywysyłane są wszyskie dane z opcji, obiekty graczy, obiekty cpu, i którymi zarządza
    #endregion
    ##############################################################################################
    options = None
    run_game = True
    
    while run_game:

        options = main_menu.use_menu()

        if options == 1:
            options = new_game_menu.use_menu()
            game = Game(
                map_size.map_size, 
                [four_masted_fleet_size.fleet_size,three_masted_fleet_size.fleet_size,
                two_masted_fleet_size.fleet_size,
                single_mast_fleet_size.fleet_size]
                )

            #region(gra jednoosobowa)
            if options == 11:
                pass
            #endregion
            
            #region(gra dwuosobowa)            
            if options == 12:
                game.set_player_one()
                game.set_player_two()

                game.play_game()
                #game.TEST_method_show_about_yourself()
            #endregion
            
            options = 0

        if options == 2:
            options = options_menu.use_menu()
            options = 0
            

        if options == 3:
            run_game = False
    
    input('Exit!')


 