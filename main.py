import curses
from re import S

# TODO:
#   couleur de fond cellule OK
#   voir l entree qu on ecrit OK
#   faire defiler le tableau OK
#   rajouter des cellules qd on fait défiler OK
#   Limite du tableau quand on defile
#   Afficher les axes
#   Afficher menu
#   detecter des commandes
#   Rajouter des couleurs

# INITIALISATION CURSES

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
stdscr.keypad(True)

# COLORS
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
SELECTED_COLOR = curses.color_pair(1)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
DEFALUT_COLOR = curses.color_pair(2)

# VARIABLES
cells = []
cells_size = []
test_cells = 0
running = True
selected_cell_x = 0
selected_cell_y = 0 # column position in the celslelected_cell_y = 0 # line position in the cell
len_cell =  8 # taille d une cellule par defaut
len_current_column = []
sheet_size_c = 20 # taille de la feuille de calcul
sheet_size_l = 20
screen_size_x = 15
screen_size_y = 12
start_cell_draw_x = 0
start_cell_draw_y = 0
selector_x = 0 # selection cursor position on the screen
selector_y = 0
axes_line = []
axes_column = []

# Rempli la feuille de calcule par defaut
for i in range(sheet_size_l):
    inner_list = []
    for y in range(sheet_size_c):
        test_cells = test_cells + 1
        inner_list.append(str(test_cells)+" ")
    cells.append(inner_list)

# Tableau de taille de cellules
for i in range(sheet_size_l):
    inner_list2 = []
    for y in range(sheet_size_c):
        inner_list2.append(len_cell)
    cells_size.append(inner_list2)
# Tableau de taille de colonnes
for i in range(sheet_size_c):
    len_current_column.append(len_cell)
# Tableau des axes
for i in range(1, sheet_size_l-10):
    axes_line.append(str(i))
for i in range(1, sheet_size_c-1):
    axes_column.append(str(i))

# DRAWING THE SHEET
def draw_sheet(p_cells):
    y = 1
    x = 1
    for l in range(screen_size_y):
        x = 1
        for c in range(screen_size_x):
            cc = c + start_cell_draw_x
            ll = l + start_cell_draw_y
            if c == selector_x  and l == selector_y:
                stdscr.addstr(y, x, p_cells[ll][cc], SELECTED_COLOR)
            else:
                stdscr.addstr(y, x, p_cells[ll][cc], DEFALUT_COLOR)            
            x = x + len_current_column[cc]
        y = y + 1
    stdscr.addstr(14,0, "VALEUR CELLULE ACTUELLE : " + str(p_cells[selected_cell_y][selected_cell_x]))
    #stdscr.refresh()


# MENU
def draw_menu():
    pass


# COLORS


# CALCULS



# USER INPUT
def user_input(p_cells):
    curses.echo()
    global len_current_column
    entry = stdscr.getstr(14, 26)
    entry = entry.decode() # !!! getstr renvoie un byte objet qu on decode ici en str
    curses.noecho()
    if len(p_cells[selected_cell_y][selected_cell_x]) < len(entry):
        len_current_column[selected_cell_x] = len(entry)    
    p_cells[selected_cell_y][selected_cell_x] = entry

# FORMATING CELLS TO SAME SIZE
def formating_cells_size(p_cells, p_cells_size):
    #remplir la cellule d espace si le contenu ne prend pas tte la place
    #trouver la plus grande cellule d une colonne
    #ajouster toute la colonne a cette taille
    for l in range(sheet_size_l):
        for c in range(sheet_size_c):
            if len_current_column[c] > len(p_cells[l][c]):
                p_cells_size[l][c] = len_current_column[c]
            current_cell_size = p_cells_size[l][c]
            if len(p_cells[l][c]) <= current_cell_size:
                for i in range(current_cell_size - len(p_cells[l][c])):
                    current_str = p_cells[l][c]
                    current_str = current_str + " "
                    p_cells[l][c] = current_str
                p_cells_size[l][c] = current_cell_size
            elif len(p_cells[l][c]) > current_cell_size:
                new_size = len(p_cells[l][c])
                for l in range(sheet_size_l):
                    p_cells_size[l][c] = new_size
                    
                        

def change_column_size(p_cells, column_to_change, new_column_size):
        stdscr.addstr(16,0, str(column_to_change))
        stdscr.addstr(17,0, str(new_column_size))
        for l in range(sheet_size_l):
            current_cell_size = len(p_cells[l][column_to_change])
            if current_cell_size < new_column_size:
                for y in range(new_column_size - current_cell_size):
                    current_str = p_cells[l][column_to_change]
                    current_str = current_str + " "
                    p_cells[l][column_to_change] = current_str


# KEY PRESSED DETECTION
def key_detection():
    key = stdscr.getch()
    global selected_cell_x, selected_cell_y, selector_x, selector_y
    global start_cell_draw_x, start_cell_draw_y

    if key == curses.KEY_UP:
        if selected_cell_y <= screen_size_y-1 and start_cell_draw_y == 0 and selector_y != 0:
            selector_y = selector_y - 1
            selected_cell_y = selected_cell_y - 1
        elif selected_cell_y <= screen_size_y-1 and start_cell_draw_y != 0 and selector_y == 0:
            selected_cell_y = selected_cell_y -1
            start_cell_draw_y = start_cell_draw_y - 1
        elif selected_cell_y <= screen_size_y-1 and start_cell_draw_y !=0 and selector_y != 0:
            selector_y = selector_y - 1
            selected_cell_y = selected_cell_y - 1
        elif selected_cell_y >= screen_size_y-1 and selector_y == 0:
            selected_cell_y = selected_cell_y - 1
            start_cell_draw_y = start_cell_draw_y -1
        elif selected_cell_y >= screen_size_y-1 and selector_y !=0:
            selector_y = selector_y - 1
            selected_cell_y = selected_cell_y -1
    

    if key == curses.KEY_DOWN:
        if selected_cell_y < screen_size_y-1 and selector_y < screen_size_y-1:
            selector_y = selector_y +1
            selected_cell_y = selected_cell_y +1
        elif selected_cell_y > screen_size_y-1 and selector_y < screen_size_y-1:
            selector_y = selector_y + 1
            selected_cell_y = selected_cell_y +1
        elif selector_y == screen_size_y-1:
            selected_cell_y = selected_cell_y +1
            start_cell_draw_y = start_cell_draw_y +1


    if key == curses.KEY_LEFT:
        if selected_cell_x <= screen_size_x-1 and start_cell_draw_x == 0 and selector_x != 0:
            selector_x = selector_x - 1
            selected_cell_x = selected_cell_x - 1
        elif selected_cell_x <= screen_size_x-1 and start_cell_draw_x != 0 and selector_x == 0:
            selected_cell_x = selected_cell_x -1
            start_cell_draw_x = start_cell_draw_x - 1
        elif selected_cell_x <= screen_size_x-1 and start_cell_draw_x !=0 and selector_x != 0:
            selector_x = selector_x - 1
            selected_cell_x = selected_cell_x - 1
        elif selected_cell_x >= screen_size_x-1 and selector_x == 0:
            selected_cell_x = selected_cell_x - 1
            start_cell_draw_x = start_cell_draw_x -1
        elif selected_cell_x >= screen_size_x-1 and selector_x !=0:
            selector_x = selector_x - 1
            selected_cell_x = selected_cell_x -1
    

    if key == curses.KEY_RIGHT:
        if selected_cell_x <= screen_size_x-1 and selector_x < screen_size_x-1:
            selector_x = selector_x + 1
            selected_cell_x = selected_cell_x +1
        elif selected_cell_x >= screen_size_x-1 and selector_x < screen_size_x-1:
            selector_x = selector_x + 1
            selected_cell_x = selected_cell_x +1
        elif selector_x == screen_size_x-1:
            selected_cell_x = selected_cell_x +1
            start_cell_draw_x = start_cell_draw_x +1

    if key in [10, 13]:
        user_input(cells)
    

# MAIN LOOP
while running:
    #stdscr.nodelay(True)
    stdscr.clear()
    formating_cells_size(cells, cells_size)
    draw_sheet(cells)
    key_detection()
    #stdscr.addstr(16,0, str(selector_x))
    stdscr.refresh()



curses.echo()
curses.curs_set(1)
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
print(cells)
curses.endwin()