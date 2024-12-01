import matplotlib.pyplot as plt
from copy import deepcopy
from collections import deque
from queue import PriorityQueue 
# from heapq import heappush, heappop


# level 1
B_matrix1 = [
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 3, 0, 0, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 0, 0, 0, 1, 1, 5, 0, 0, 1, 1],
    [1, 1, 2, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
]


#level 2

# B_matrix1 = [
#        [0, 1,  1,  1,  1,  0,  0,  0,  0, 1, 1], 
#        [1, 1,  2,  0,  1,  1,  1,  1,  1, 1, 0], 
#        [1, 0,  0,  0,  0,  0,  1,  0,  1, 1, 0], 
#        [1, 0,  4,  0,  1,  0,  1,  7,  0, 1, 0], 
#        [1, 1,  0,  5,  1,  0,  0,  3,  0, 1, 0], 
#        [0, 1,  1,  0,  1,  0,  0,  0,  1, 1, 0], 
#        [0, 0,  1,  1,  1,  1,  1,  6,  1, 0, 0], 
#        [0, 0,  0,  1,  0,  0,  1,  1,  1, 0, 0]
# ]

# level 3
# B_matrix1 = [
#     [0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1], 
#     [1, 1, 2, 0, 1, 1, 1, 1, 1, 1, 0], 
#     [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0], 
#     [1, 0, 4, 0, 1, 0, 1, 7, 0, 1, 0], 
#     [1, 1, 0, 5, 1, 0, 0, 3, 1, 1, 1], 
#     [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1], 
#     [0, 0, 1, 1, 1, 1, 1, 6, 1, 0, 1], 
#     [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1]
# ]


#________________________________________________________
# هدف كلاس الحالة بناء حالة واستخدم ضمن توابعه الdeep_copy لعدم التحديث على المصفوفة الحالية
class state:
    def __init__(self, B_matrix):
        self.B_matrix = B_matrix


# ----------------
    def moving(self, direct):
        B_matrix_copy = deepcopy(self.B_matrix)
        location = [(i, j) for i in range(len(B_matrix_copy)) for j in range(len(B_matrix_copy[0])) if B_matrix_copy[i][j] in [2, 3, 6]]

        for (i, j) in location:
            n_i, n_j = i, j
            while self.can_moving(B_matrix_copy, n_i, n_j, direct):
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

# ----------------
# فحص امكانية التنقل بين المربعات 
    def can_moving(self, B_matrix, n, m, direct):
        if direct == 'right':
             return m + 1 < len(B_matrix[0]) and B_matrix[n][m + 1] not in [1, 2, 3, 6]


        elif direct == 'left':
            return m - 1 >= 0 and B_matrix[n][m - 1] not in [1, 2, 3, 6]


        elif direct == 'down':
            return n - 1 >= 0 and B_matrix[n - 1][m] not in [1, 2, 3, 6]

            
        elif direct == 'up':
            return n + 1 < len(B_matrix) and B_matrix[n + 1][m] not in [1, 2, 3, 6]
        return False

# ----------------
# فحص هدف المربع
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
# -----------------
# التحقق من ربح المرحلة
    def if_win(self):
      
        return all(cell == 0 for row in self.B_matrix for cell in row if cell in [4, 5, 7])



#____________________________________________
class GUI:
    def __init__(self, ax, state,method_name='Algorithm'):
    # def __init__(self, state):
        self.state = state
        # لنقسم الواجهة لخمس اقسام وحدة منن الرئيسية والاربعة للحالات التالية
    #     # self.figm, self.ax = plt.subplots(1, 5, figsize=(20, 5))
    #     self.figm, self.ax = plt.subplots(1, 1, figsize=(5, 5)) 
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

# ----------------

# لتحديث الرسمة
    def update_board(self):
        self.ax.clear()
        self.print_B_matrix( self.ax,self.state.B_matrix)
        # self.ax.set_title('Current')
        self.ax.set_title(self.method_name)
        # self.next_state()
        plt.draw()
# --------------------
# يجرب الاربع اتجاهات ويرسمهم مع عنوان كل وحدة
    def next_state(self):
        next_states_objects = []
        directs = ['right', 'left', 'down', 'up']

        for idx, direct in enumerate(directs, start=1):
            the_new_state = self.state.moving(direct)  
            next_states_objects.append(the_new_state) 
            # self.print_B_matrix(self.ax[idx],the_new_state.B_matrix)  
            # self.ax[idx].set_title(direct.capitalize())

        return next_states_objects  

# --------------
# رسم مصفوفة الحالة 
    def print_B_matrix(self, ax, B_matrix):
     color_map = {1: 'black', 2: 'red', 3: 'blue', 6: 'green'}
     border_map = {4: 'red', 5: 'blue', 7: 'green'}
    #   نجلب عرض وطول المصفوفة 
     rows, cols = len(B_matrix), len(B_matrix[0])
     for i in range(rows):
        for j in range(cols):
            value = B_matrix[i][j]
            color = color_map.get(value, 'white')  
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))

            if value in border_map:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, edgecolor=border_map[value], facecolor='none', linewidth=2))

     ax.set_xlim(0, cols)
     ax.set_ylim(0, rows)
     ax.set_xticks([])
     ax.set_yticks([])

#_________________________________________________
# كلاس اللعب فيه خوارزميات اللعب وفيه تابع اللعب من قبل المستخدم 
class Play:
    def __init__(self, B_matrix, ax, method_name='Algorithm'):
        self.current_B_matrix = B_matrix
        self.history = []
        self.state = state(self.current_B_matrix)
        # self.game_ui = GUI(self.state)
        # self.figm = self.game_ui.figm
        # self.figm.canvas.mpl_connect('key_press_event', self.press)
        self.game_ui = GUI(ax, self.state, method_name=method_name)
        # self.game_ui = GUI(ax, self.state)
#--------------------- 
    def hill_climbing(self):
     current_state = self.state
     current_cost = self.heuristic(current_state.B_matrix)
     visited = set()
     visited_count = 0

     while True:
        visited.add(tuple(map(tuple, current_state.B_matrix)))
        next_state = None
        next_cost = 5555555
        visited_count += 1

        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            new_state = current_state.moving(direction)
            new_key = tuple(map(tuple, new_state.B_matrix))
            
            if new_key in visited:
                continue
            
            new_cost = self.heuristic(new_state.B_matrix)
            
           
            if new_cost < next_cost:
                next_state = new_state
                next_cost = new_cost

       
        if next_state is None or next_cost >= current_cost:
            break

        
        current_state = next_state
        current_cost = next_cost
        self.state = current_state
        self.game_ui.state = self.state
        self.game_ui.update_board()
        plt.pause(0.8)

  
     if current_state.if_win():
        print("Solution found with Hill Climbing!")
     else:
        print("Hill Climbing stopped")
        print(f"Visited nodes: {visited_count}")


# --------------------
    def heuristic(self, B_matrix):
     
        targets = {4: [], 5: [], 7: []}
        movers = {2: [], 3: [], 6: []}

     
        for i, row in enumerate(B_matrix):
            for j, value in enumerate(row):
                if value in targets:
                    targets[value].append((i, j))
                elif value in movers:
                    movers[value].append((i, j))

      
        distance = 0
        for mover, targte_num in zip([2, 3, 6], [4, 5, 7]):
            for mx, my in movers[mover]:
                distances = [abs(mx - tx) + abs(my - ty) for tx, ty in targets[targte_num]]
                if distances:
                     distance += sum(distances)

        return distance
# ---------------------
    def dfs_recursive(self, init_state):
        def dfs_r(the_current_state, the_path, visites):
            
            key = tuple(map(tuple, the_current_state.B_matrix))

           
            if key in visites:
                return None
            visites.add(key)

            if the_current_state.if_win():
                return the_path

            
            directs = ['up', 'down', 'left', 'right']
            for direct in directs:
               
                the_new_state = the_current_state.moving(direct)
                result = dfs_r(the_new_state, the_path + [direct], visites)
                if result is not None:
                    return result

           

        visites = set()
        return dfs_r(init_state, [], visites)
# -------------------
# تابع الخوارزميات حسب اسم الخوارزمية التي امررها يعمل 
    def search(self, method='bfs'):
        start_state = self.state
        if method == 'bfs':
            queue = deque([(start_state, [])])  
            visites = set()
            while queue:
                the_current_state, the_path = queue.popleft()
                key = tuple(map(tuple, the_current_state.B_matrix))

                if key in visites:
                    continue
                visites.add(key)

                if the_current_state.if_win():
                    print("Solution found with BFS ,the_Path:", the_path)
                    return the_path

                directs = ['up', 'down', 'left', 'right']
                for direct in directs:
                    the_new_state = the_current_state.moving(direct)
                    new_key = tuple(map(tuple, the_new_state.B_matrix))
                    
                    if new_key not in visites:
                        queue.append((the_new_state, the_path + [direct]))

            print("No solution ", queue)
            return None

        elif method == 'dfs':
            stack = [(start_state, [])]
            visites = set()
            while stack:
                the_current_state, the_path = stack.pop()
                key = tuple(map(tuple, the_current_state.B_matrix))

                if key in visites:
                    continue
                visites.add(key)

                if the_current_state.if_win():
                    print("Solution found with DFS ,the_Path:", the_path)
                    return the_path

                directs = ['up', 'down', 'left', 'right']
                for direct in directs:
                    the_new_state = the_current_state.moving(direct)
                    new_key = tuple(map(tuple, the_new_state.B_matrix))
                    
                    if new_key not in visites:
                        stack.append((the_new_state, the_path + [direct]))

            print("No solution ", stack)
            return None

        elif method == 'ucs':

            pq = PriorityQueue()
            pq.put((0, id(start_state), start_state, []))
            visites = set()

            while not pq.empty():
                cost, _, the_current_state, the_path = pq.get()
                key = tuple(map(tuple, the_current_state.B_matrix))

                if key in visites:
                    continue
                visites.add(key)

                if the_current_state.if_win():
                    print("Solution found with UCS! the_Path:", the_path)
                    return the_path

                directs = ['up', 'down', 'left', 'right']
                for direct in directs:
                    the_new_state = the_current_state.moving(direct)
                    new_key = tuple(map(tuple, the_new_state.B_matrix))

                    if new_key not in visites:
                        new_cost = cost + 1
                        pq.put((new_cost, id(the_new_state), the_new_state, the_path + [direct]))

            print("No solution ")
            return None
        
        elif method == 'astar':
          pq = PriorityQueue()
          pq.put((0, 0, id(start_state), start_state, []))  
          visited = set()
          total_cost = 0 
          visited_count = 0 
 
          while not pq.empty():
           f_cost, g_cost, _, current_state, path = pq.get()
           current_key = tuple(map(tuple, current_state.B_matrix))

           if current_key in visited:
            continue
           visited.add(current_key)
           visited_count += 1

           if current_state.if_win():
            print("Solution found with A*!")
            print(f"Path: {path}")
            print(f"Total cost: {g_cost}")
            print(f"Visited nodes: {visited_count}")
            return path

           directions = ['up', 'down', 'left', 'right']
           for direction in directions:
             new_state = current_state.moving(direction)
             new_key = tuple(map(tuple, new_state.B_matrix))

             if new_key not in visited:
                new_g_cost = g_cost + 1  
                h_cost = self.heuristic(new_state.B_matrix)  
                new_f_cost = new_g_cost + h_cost  
                pq.put((new_f_cost, new_g_cost, id(new_state), new_state, path + [direction]))

        print("No solution found with A*.")
        return None

# --------------
# تابع اللعب من المستخدم
    def press(self, event):
        if event.key in ['right', 'left', 'up', 'down']:
            old_B_matrix = deepcopy(self.current_B_matrix)
            the_new_state = self.state.moving(event.key) 

            if self.check_equals(old_B_matrix, the_new_state.B_matrix):
                return  

            self.state = the_new_state  
            self.game_ui.state = self.state 
            self.game_ui.update_board()

            self.current_B_matrix = the_new_state.B_matrix
            self.history.append(old_B_matrix)
# لعرض الحركة التي تسبق الحالية مع رقمها
            # if self.history: 
            #     last_moving = self.history[-1]
            #     moving_number = len(self.history)  
            #     print(f"Moving {moving_number}:")
            #     for row in last_moving:
            #      print(row)
              
# -----------------
    def show_solution(self, solution_path):
        if solution_path:
            for moving in solution_path: 
                the_new_state = self.state.moving(moving)
                self.state = the_new_state
                self.game_ui.state = self.state
                self.game_ui.update_board()
                plt.pause(0.8) 
                plt.draw
                
        else:
            print("No solution ")


# -------------
    def check_equals(self, old_B_matrix, new_B_matrix):
        if old_B_matrix == new_B_matrix:
            print('It\'s the same moving')
            return True


# game = Play(B_matrix1)


# ازالة التعليق عن احداها لتشغيل احد الخوارزميات
# ____________________________________________________________________________________

# 1
# لتشغيل bfs&dfs استتخدم 





# figm, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))



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

#_________________________________________________________________
# 2
# استخدم DFS Recursive) لتشغيل




# figm, ax = plt.subplots(1, 1, figsize=(8, 8))
# game = Play(B_matrix1, ax)


# solution_path = game.dfs_recursive(game.state)
# if solution_path:
#     print("Solution Path (DFS Recursive):", solution_path)
#     game.show_solution(solution_path)  
# else:
#     print("No solution ")


# _________________________________________________________________
# 3
# لتشغيل ucsاستخدم




# figm, ax = plt.subplots(1, 1, figsize=(8, 8))
# game = Play(B_matrix1, ax)
# ax.set_title("ucs Algorithm")
# solution_path_ucs = game.search(method='ucs')
# if solution_path_ucs:
    
#     game.show_solution(solution_path_ucs)
# else:
#     print("No solution ")


# _____________________________________________
# figm, ax = plt.subplots(1, 1, figsize=(8, 8))
# game = Play(B_matrix1, ax)
# solution_path_astar = game.search(method='astar') 

# if solution_path_astar:
#     game.show_solution(solution_path_astar) 
# else:
#     print("No solution found with A*.")
figm, ax = plt.subplots(1, 1, figsize=(8, 8))
game = Play(B_matrix1, ax)
game.hill_climbing()
