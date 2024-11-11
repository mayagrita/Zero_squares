import matplotlib.pyplot as plt
from copy import deepcopy

B_matrix1 = [
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 2, 0, 0, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 6, 1, 1, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 5, 0, 7, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 4, 0, 3, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
]



#________________________________________________________
class state:
    def __init__(self, B_matrix):
        self.B_matrix = B_matrix



    def move(self, direct):
        B_matrix_copy = deepcopy(self.B_matrix)
        location = [(i, j) for i in range(len(B_matrix_copy)) for j in range(len(B_matrix_copy[0])) if B_matrix_copy[i][j] in [2, 3, 6]]

        for (i, j) in location:
            n_i, n_j = i, j
            while self.can_move(B_matrix_copy, n_i, n_j, direct):
                if direct == 'right':
                    n_j += 1
                elif direct == 'left':
                    n_j -= 1
                elif direct == 'down':
                    n_i -= 1
                elif direct == 'up':
                    n_i += 1

                self.check_goal(B_matrix_copy, i, j, n_j, n_i)

            if (n_i, n_j) != (i, j):
                B_matrix_copy[n_i][n_j] = B_matrix_copy[i][j]
                B_matrix_copy[i][j] = 0

        return state(B_matrix_copy)



    def can_move(self, B_matrix, n, m, direct):
        if direct == 'right':
             return m + 1 < len(B_matrix[0]) and B_matrix[n][m + 1] not in [1, 2, 3, 6]


        elif direct == 'left':
            return m - 1 >= 0 and B_matrix[n][m - 1] not in [1, 2, 3, 6]


        elif direct == 'down':
            return n - 1 >= 0 and B_matrix[n - 1][m] not in [1, 2, 3, 6]

            
        elif direct == 'up':
            return n + 1 < len(B_matrix) and B_matrix[n + 1][m] not in [1, 2, 3, 6]
        return False



    def check_goal(self, B_matrix, i, j, m, n):
        if B_matrix[i][j] == 2 and B_matrix[n][m] == 4:
            B_matrix[n][m] = 0
        if B_matrix[i][j] == 3 and B_matrix[n][m] == 5:
            B_matrix[n][m] = 0
        if B_matrix[i][j] == 6 and B_matrix[n][m] == 7:
            B_matrix[n][m] = 0




#____________________________________________
class GUI:
    def __init__(self, state):
        self.state = state
        self.fig, self.ax = plt.subplots(1, 5, figsize=(20, 5))
        self.update_board()



    def update_board(self):
        for ax in self.ax:
            ax.clear() 
        self.print_B_matrix( self.ax[0],self.state.B_matrix)
        self.ax[0].set_title('Current')
        self.next_state()
        plt.draw()



    def next_state(self):
        next_states_objects = []
        directs = ['right', 'left', 'down', 'up']

        for idx, direct in enumerate(directs, start=1):
            new_state = self.state.move(direct)  
            next_states_objects.append(new_state) 
            self.print_B_matrix(self.ax[idx],new_state.B_matrix)  
            self.ax[idx].set_title(direct.capitalize())

        return next_states_objects  



    def print_B_matrix(self,ax, B_matrix):
        rows = len(B_matrix)
        cols = len(B_matrix[0])
        for i in range(rows):
            for j in range(cols):
                color = 'white'
                if B_matrix[i][j] == 1:
                    color = 'black'
                elif B_matrix[i][j] == 2:
                    color = 'red'
                elif B_matrix[i][j] == 3:
                    color = 'blue'
                elif B_matrix[i][j] == 6:
                    color = 'green'

                rect = plt.Rectangle((j, i), 1, 1, color=color)
                ax.add_patch(rect)

                if B_matrix[i][j] in [4, 5, 7]:
                    border_color = 'red' if B_matrix[i][j] == 4 else 'blue' if B_matrix[i][j] == 5 else 'green'
                    border_rect = plt.Rectangle((j, i), 1, 1, edgecolor=border_color, facecolor='none', linewidth=2)
                    ax.add_patch(border_rect)

        ax.set_xlim([0, cols])
        ax.set_ylim([0, rows])
        ax.set_xticks([])
        ax.set_yticks([])




#_________________________________________________
class Play:
    def __init__(self, B_matrix):
        self.current_B_matrix = B_matrix
        self.history = []
        self.state = state(self.current_B_matrix)
        self.game_ui = GUI(self.state)
        self.fig = self.game_ui.fig
        self.fig.canvas.mpl_connect('key_press_event', self.press)




    def press(self, event):
        if event.key in ['right', 'left', 'up', 'down']:
            old_B_matrix = deepcopy(self.current_B_matrix)
            new_state = self.state.move(event.key) 

            if self.check_equals(old_B_matrix, new_state.B_matrix):
                return  

            self.state = new_state  
            self.game_ui.state = self.state 
            self.game_ui.update_board()

            self.current_B_matrix = new_state.B_matrix
            self.history.append(old_B_matrix)

            if self.history: 
                last_move = self.history[-1]
                move_number = len(self.history)  
                print(f"Move {move_number}:")
                for row in last_move:
                 print(row)
              



# هون برجع ازا تحرك نفس لحركةواستدعيتو بال press

    def check_equals(self, old_B_matrix, new_B_matrix):
        if old_B_matrix == new_B_matrix:
            print('It\'s the same move')
            return True


game = Play(B_matrix1)
plt.show()