import matplotlib.pyplot as plt
from copy import deepcopy
from collections import deque
import time

# level 1
# B_matrix1 = [
#     [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
#     [1, 1, 2, 0, 0, 1, 1, 1, 1, 1, 0],
#     [1, 0, 0, 0, 6, 1, 1, 0, 0, 1, 0],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
#     [1, 0, 5, 0, 7, 1, 1, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 4, 0, 3, 0, 1, 1],
#     [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
#     [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
# ]


#level 2

B_matrix1 = [
    [0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 2, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 4, 0, 1, 0, 0, 7, 1],
    [1, 1, 0, 5, 1, 0, 3, 0, 1],
    [0, 1, 1, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 1, 1, 1, 1, 6, 1],
    [0, 0, 0, 1, 0, 0, 1, 1, 1]
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
            B_matrix[i][j] = 0

        if B_matrix[i][j] == 3 and B_matrix[n][m] == 5:
            B_matrix[n][m] = 0
            B_matrix[i][j] = 0

        if B_matrix[i][j] == 6 and B_matrix[n][m] == 7:
            B_matrix[n][m] = 0
            B_matrix[i][j] = 0


    def if_win(self):
      
        return all(cell == 0 for row in self.B_matrix for cell in row if cell in [4, 5, 7])



#____________________________________________
class GUI:
    # def __init__(self, state):
    #     self.state = state
    #     # self.fig, self.ax = plt.subplots(1, 5, figsize=(20, 5))
    #     self.fig, self.ax = plt.subplots(1, 1, figsize=(5, 5)) 
    #     self.update_board()
    def __init__(self, ax, state,method_name='Algorithm'):
        self.state = state
        self.ax = ax
        self.method_name = method_name
        self.update_board()

#التابع ليعمل واجهة فيها عدة اقسام غير الرئيسي
    # def update_board(self):
    #     for ax in self.ax:
    #         ax.clear() 
    #     self.print_B_matrix( self.ax[0],self.state.B_matrix)
    #     self.ax[0].set_title('Current')
    #     self.next_state()
    #     plt.draw()




    def update_board(self):
        self.ax.clear()
        self.print_B_matrix( self.ax,self.state.B_matrix)
        # self.ax.set_title('Current')
        self.ax.set_title(self.method_name)
        # self.next_state()
        plt.draw()


    def next_state(self):
        next_states_objects = []
        directs = ['right', 'left', 'down', 'up']

        for idx, direct in enumerate(directs, start=1):
            new_state = self.state.move(direct)  
            next_states_objects.append(new_state) 
            # self.print_B_matrix(self.ax[idx],new_state.B_matrix)  
            # self.ax[idx].set_title(direct.capitalize())

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
    def __init__(self, B_matrix, ax, method_name='Algorithm'):
        self.current_B_matrix = B_matrix
        self.history = []
        self.state = state(self.current_B_matrix)
        # self.game_ui = GUI(self.state)
        # self.fig = self.game_ui.fig
        # self.fig.canvas.mpl_connect('key_press_event', self.press)
        self.game_ui = GUI(ax, self.state, method_name=method_name)
        # self.game_ui = GUI(ax, self.state)
 

    def dfs_recursive(self, initial_state):
        def dfs_r(current_state, path, visited):
            
            current_key = tuple(map(tuple, current_state.B_matrix))

           
            if current_key in visited:
                return None
            visited.add(current_key)

            if current_state.if_win():
                return path

            
            directions = ['up', 'down', 'left', 'right']
            for direction in directions:
               
                new_state = current_state.move(direction)
                result = dfs_r(new_state, path + [direction], visited)
                if result is not None:
                    return result

            return None

        visited = set()
        return dfs_r(initial_state, [], visited)


    def search(self, method='bfs'):
        start_state = self.state
        if method == 'bfs':
            queue = deque([(start_state, [])])  
            visited = set()
            while queue:
                current_state, path = queue.popleft()
                current_key = tuple(map(tuple, current_state.B_matrix))

                if current_key in visited:
                    continue
                visited.add(current_key)

                if current_state.if_win():
                    print("Solution found with BFS ,Path:", path)
                    return path

                directions = ['up', 'down', 'left', 'right']
                for direction in directions:
                    new_state = current_state.move(direction)
                    new_key = tuple(map(tuple, new_state.B_matrix))
                    
                    if new_key not in visited:
                        queue.append((new_state, path + [direction]))

            print("No solution found.", queue)
            return None

        elif method == 'dfs':
            stack = [(start_state, [])]
            visited = set()
            while stack:
                current_state, path = stack.pop()
                current_key = tuple(map(tuple, current_state.B_matrix))

                if current_key in visited:
                    continue
                visited.add(current_key)

                if current_state.if_win():
                    print("Solution found with DFS ,Path:", path)
                    return path

                directions = ['up', 'down', 'left', 'right']
                for direction in directions:
                    new_state = current_state.move(direction)
                    new_key = tuple(map(tuple, new_state.B_matrix))
                    
                    if new_key not in visited:
                        stack.append((new_state, path + [direction]))

            print("No solution found.", stack)
            return None


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

            # if self.history: 
            #     last_move = self.history[-1]
            #     move_number = len(self.history)  
            #     print(f"Move {move_number}:")
            #     for row in last_move:
            #      print(row)
              

    def show_solution(self, solution_path):
        if solution_path:
            for move in solution_path: 
                new_state = self.state.move(move)
                self.state = new_state
                self.game_ui.state = self.state
                self.game_ui.update_board()
                plt.pause(0.8) 
                plt.draw
                
        else:
            print("No solution to show.")



    def check_equals(self, old_B_matrix, new_B_matrix):
        if old_B_matrix == new_B_matrix:
            print('It\'s the same move')
            return True


# game = Play(B_matrix1)

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))



# game_bfs = Play(B_matrix1, ax1, method_name='BFS Algorithm')
# ax1.set_title("BFS Algorithm")

# game_dfs = Play(B_matrix1, ax2, method_name='DFS Algorithm')
# ax2.set_title("DFS Algorithm")


# solution_path_bfs = game_bfs.search(method='bfs')
# solution_path_dfs = game_dfs.search(method='dfs')

# game_bfs.show_solution(solution_path_bfs)
# game_dfs.show_solution(solution_path_dfs)



# plt.show()
# plt.close('all')


fig, ax = plt.subplots(1, 1, figsize=(8, 8))
game = Play(B_matrix1, ax)

# استدعاء DFS باستخدام الحالة الأولى
solution_path = game.dfs_recursive(game.state)
if solution_path:
    print("Solution Path (DFS Recursive):", solution_path)
    game.show_solution(solution_path)  
else:
    print("No solution found.")
