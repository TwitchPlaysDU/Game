import mousepresser
import time

score_coords = [50, 40]
boards_coords = [50, 175]
boards_y_offset = 105
bench_coords = [440, 950]
bench_x_offset = 148
board_coords = [560, 750]
board_x_offset = 114
board_y_offset = 100
board_x_start_d = 20
board_x_offset_d = 6
items_coords = [1790, 370]
items_x_offset = 65
items_y_offset = 65
close_coords = [1820, 120]
main_menu_coords = [1850, 1030]
play_coords = [200, 990]
ranked_coords = [1450, 600]
yo_coords = [960, 5]

single_commands = ['score', 'play', 'main menu', 'mainmenu']
arg_commands = ['board', 'b', 'c']
arg2_commands = ['b', 'c', 'i']

def index_to_bench(index):
    return (bench_coords[0] + (index - 1) * bench_x_offset, bench_coords[1])
    
def index_to_item(index):
    index = index - 1
    col = index // 6
    row = index - col * 6
    return (items_coords[0] - items_x_offset * col, items_coords[1] + items_y_offset * row)
    
def index_to_cell(index):
    index = 32 - index
    col = index // 8
    row = 7 - (index - col * 8)
    x = board_coords[0] + board_x_start_d * col + (board_x_offset - board_x_offset_d * col) * row
    y = board_coords[1] - board_y_offset * col
    return (x, y)

def command(c):

    if c in single_commands:
        if c == 'score':
            mousepresser.click(*score_coords)
            return True
        elif c == 'play' or c == 'main menu' or c == 'mainmenu':
            mousepresser.click(*close_coords)
            time.sleep(1.8)
            mousepresser.click(*main_menu_coords)
            mousepresser.click(*main_menu_coords)
            time.sleep(1.8)
            mousepresser.click(*play_coords)
            time.sleep(0.25)
            mousepresser.click(*ranked_coords)
            mousepresser.click(*ranked_coords)
            return True
        elif c == 'yo':
            mousepresser.click(*yo_coords)
            time.sleep(0.1)
            mousepresser.click(*yo_coords)
            return True
    
    elif ' ' in c:
        parts = c.split()
        if len(parts) == 2:
            if parts[0] in arg_commands and parts[1].isdigit() and int(parts[1]) >= 1:
                if parts[0] == 'board' and int(parts[1]) <= 8:
                    mousepresser.click(boards_coords[0], boards_coords[1] + (int(parts[1]) - 1) * boards_y_offset)
                    return True
                elif parts[0] == 'b' and int(parts[1]) <= 8:
                    mousepresser.click(*index_to_bench(int(parts[1])))
                    return True
                elif parts[0] == 'c' and int(parts[1]) <= 32:
                    mousepresser.click(*index_to_cell(int(parts[1])))
                    return True
        
        elif len(parts) == 4:
            if parts[0] in arg2_commands and parts[2] in arg2_commands and parts[1].isdigit() and parts[3].isdigit() and int(parts[1]) >= 1 and int(parts[3]) >= 1:
                x1 = y1 = x2 = y2 = -1
                
                if parts[0] == 'b' and int(parts[1]) <= 8:
                    x1, y1 = index_to_bench(int(parts[1]))
                elif parts[0] == 'c' and int(parts[1]) <= 32:
                    x1, y1 = index_to_cell(int(parts[1]))
                elif parts[0] == 'i' and int(parts[1]) <= 14:
                    x1, y1 = index_to_item(int(parts[1]))
                
                if x1 == -1 or y1 == -1:
                    return False
                
                if parts[2] == 'b' and int(parts[3]) <= 8:
                    x2, y2 = index_to_bench(int(parts[3]))
                elif parts[2] == 'c' and int(parts[3]) <= 32:
                    x2, y2 = index_to_cell(int(parts[3]))
                
                if x2 == -1 or y2 == -1:
                    return False
                    
                mousepresser.drag(x1, y1, x2, y2)
                return True    
    
    return False
    

#score 50,40            boards 50,175     +105                   bench 440,950         +148                     board 560,750   x +114(-6 per y)   y-100(x+20)