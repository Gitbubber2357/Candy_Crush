import numpy as np
import time

# ==========================================================================================
# preparing CODE

def eliminate(matrix):
    edge = len(matrix)
    matrix_clone = np.array(matrix)
    
    # eliminate the rows
    for i in range(edge):
        for j in range(1,edge-1):
            if matrix[i,j] == matrix[i,j-1] and matrix[i,j] == matrix[i,j+1]:
                matrix_clone[i,j-1] = matrix_clone[i,j] = matrix_clone[i,j+1] = 0

    # eliminate the cols
    for i in range(edge):
        for j in range(1,edge-1):
            if matrix[j,i] == matrix[j-1,i] and matrix[j,i] == matrix[j+1,i]:
                matrix_clone[j-1,i] = matrix_clone[j,i] = matrix_clone[j+1,i] = 0
                
    return matrix_clone


def score(eli_matrix, matrix, score):
    types = len(score)
    
    score_matrix = matrix - eli_matrix
    for i in range(types):
        score[i] += np.count_nonzero(score_matrix == i+1)
    
    for i in range(types):
        print ("Type %d scores %d points." %(i+1, score[i]))
    
    return score


def drop(matrix, types):
    edge = len(matrix)
    matrix_clone = np.array(matrix)
    
    # drop in col direction and fill it up
    for i in range(edge):
        rest = np.array([])
        for j in range(edge):
            if matrix[j,i] != 0:
                rest = np.append(rest,matrix[j,i])
        fill_up = np.random.randint(1, types+1, (edge-len(rest)))
        matrix_clone[::,i] = np.append(fill_up,rest)
    
    return matrix_clone


def switch(matrix, start, end):
    matrix_clone = np.array(matrix)
    
    if start[0] == end[0] and np.abs(start[1] - end[1]) == 1:
        matrix_clone[end] = matrix[start]
        matrix_clone[start] = matrix[end]
        return matrix_clone
    
    elif start[1] == end[1] and np.abs(start[0] - end[0]) == 1:
        matrix_clone[end] = matrix[start]
        matrix_clone[start] = matrix[end]
        return matrix_clone
    
    else:
        print("Operation Fail")
        
        
def stop(matrix, types):
    matrix_clone = np.array(matrix)
    abs_ = np.abs(drop(eliminate(matrix_clone), types) - matrix).sum()
    
    while abs_ != 0:
        matrix_clone = np.array(matrix)
        matrix = drop(eliminate(matrix), types)
        abs_ = np.abs(drop(eliminate(matrix_clone), types) - matrix).sum()
        
    return matrix_clone


def Initi(size, types):
    matrix =  np.random.randint(1, types+1, (size,size))
    score = np.zeros((types))
    
    return stop(matrix, types), score


def goal(score, target):
    types = len(score)
    
    if (score >= target).sum() == types:
        print( "Congratulations!!" )
        return True
    
    elif (score >= target).sum() > types/2:
        print( "Almost there!" )
        return False
    
    elif (score >= target).sum() > 0:
        print( "Keep going." )
        return False
    
    else:
        return False
    

def print_normal(matrix):
    edge = len(matrix)
    
    for i in range(edge):
        for j in range(edge):
            print("", matrix[i,j], "", end = "")
        print()
        
        
def print_finger(matrix, i_, j_):
    edge = len(matrix)
    
    for i in range(edge):
        for j in range(edge):
            if i == i_ and j == j_:
                print([matrix[i,j]], end = "")
            else:
                print("", matrix[i,j], "", end = "")
        print()
                
                
def require(parser, require_hint, exception_hint = None):
    while True:
        try:
            input_str = input(require_hint)
            if input_str == "Quit" or input_str == "quit" or input_str == "Q" or input_str == "q":
                require = None
            else:
                require = parser(input_str)
            break
        
        except:
            if exception_hint is not None:
                print(exception_hint)
    
    if require is None:
        raise ValueError
    return require

# ==========================================================================================
# GAME CODE (Candy Crush)

def Candy_Crush():
    print("Game start!")
    input("Press Enter to continue...")
    
    name = input("What is your name:")
    print("Welcome " + name + "!")
    
    size = require(int, "What size of the table do you want in this game:",
                        "Please input an integer for the size of the table.")
    types = require(int, "How many types of candy do you want in this time:",
                         "Please input an integer for the number of types of the fruits.")
    target = require(int, "What is your target for each candy in this game:",
                          "Please input an integer for the target in this game.")
    
    print("Okay, we now prepare a %d by %d table for you as followed." %(size, size))
    
    initi_matrix, SCORE = Initi(size = size, types = types)
    print_normal(initi_matrix)
    
    times = 0
    
    def parser_row(input_str):
        Row = int(input_str) - 1
        if Row > size - 1 or Row < 0:
            raise ValuError
        return Row
    
    def parser_col(input_str):
        Col = int(input_str) - 1
        if Col > size - 1 or Col < 0:
            raise ValueError
        return Col
        
    def parser_dir(input_str):
        if input_str == "U" and Row > 0:
            end = (Row-1, Col)

        elif input_str == "D" and Row < size-1:
            end = (Row+1, Col)

        elif input_str == "L" and Col > 0:
            end = (Row, Col-1)

        elif input_str == "R" and Col < size-1:
            end = (Row, Col+1)

        else:
            if input_str == "U" or input_str == "D" or input_str == "L" or input_str == "R":
                print("You have been already on the boundary of the table.")
                
            else:
                print("Please input U, D, L or R representing for up, down, left and right.")
            
            raise ValueError
        return end

    
    while goal(SCORE, target) == False:
        Row = require(parser_row, "Choose an arbitrary row on the table:",
                                  "Please input an integer between 1 and %d." %(size))
        
        Col = require(parser_col, "Choose an arbitrary column on the table:",
                                  "Please input an integer between 1 and %d." %(size))
        
        start = (Row, Col)
        
        end = require(parser_dir, "Choose a direction to move the candy (U/D/L/R):")
        
        switch_matrix = switch(matrix = initi_matrix, start = start, end = end)
        print_normal(switch_matrix)
        time.sleep(0.5)
        print()
        
        eliminate_matrix = eliminate(matrix = switch_matrix)
        print_normal(eliminate_matrix)
        time.sleep(0.5)
        print()
        
        drop_matrix = drop(matrix = eliminate_matrix, types =types)
        print_normal(drop_matrix)
        
        SCORE = score(eli_matrix = eliminate_matrix, matrix = switch_matrix, score = SCORE)
        
        while np.abs(eliminate(drop_matrix) - drop_matrix).sum() != 0:
            mid_matrix = np.array(drop_matrix)
            eliminate_matrix = eliminate(matrix = mid_matrix)
            print_normal(eliminate_matrix)
            time.sleep(0.5)
            print()
            
            drop_matrix = drop(matrix = eliminate_matrix, types =types)
            print_normal(drop_matrix)
            
            SCORE = score(eli_matrix = eliminate_matrix, matrix = mid_matrix, score = SCORE)
        
        initi_matrix = drop_matrix
        times += 1
    if times == 1:
        print( name + " make only %d move to finish the Candy Crush." %(times))
    else:
        print( name + " make %d moves to finish the Candy Crush." %(times)) 
        
# ==========================================================================================
# GAME CODE (Tower of Saviors)

def ToS():
    print("Game start!")
    input("Press Enter to continue...")
    
    name = input("What is your name:")
    print("Welcome " + name + "!")
    
    size = require(int, "What size of the table do you want in this game:",
                        "Please input an integer for the size of the table.")
    types = require(int, "How many types of element do you want in this time:",
                         "Please input an integer for the number of types of the fruits.")
    target = require(int, "What is your target for each element in this game:",
                          "Please input an integer for the target in this game.")
    
    print("Okay, we now prepare a %d by %d table for you as followed." %(size, size))
    
    initi_matrix, SCORE = Initi(size = size, types = types)
    print_normal(initi_matrix)
    
    times = 0
    
    def parser_row(input_str):
        Row = int(input_str) - 1
        if Row > size - 1 or Row < 0:
            raise ValuError
        return Row

    def parser_col(input_str):
        Col = int(input_str) - 1
        if Col > size - 1 or Col < 0:
            raise ValueError
        return Col
        
    def parser_dir(input_str):
        if input_str == "U" and start[0] > 0:
            end = (start[0] - 1, start[1])

        elif input_str == "D" and start[0] < size-1:
            end = (start[0] + 1, start[1])

        elif input_str == "L" and start[1] > 0:
            end = (start[0], start[1] - 1)

        elif input_str == "R" and start[1] < size-1:
            end = (start[0], start[1] + 1)
        
        elif input_str == "stop":
            end = False
        else:
            if input_str == "U" or input_str == "D" or input_str == "L" or input_str == "R":
                print("You have been already on the boundary of the table.")
                
            else:
                print("Please input U, D, L or R representing for up, down, left and right.")
            
            raise ValueError
        return end
    
    while goal(SCORE, target) == False:
        Row = require(parser_row, "Choose an arbitrary row on the table:",
                                  "Please input an integer between 1 and %d." %(size))
        
        Col = require(parser_col, "Choose an arbitrary column on the table:",
                                  "Please input an integer between 1 and %d." %(size))
        
        start = (Row, Col)
        
        end = True
        
        while end != False:
            end = require(parser_dir, "Choose a direction to move the candy (U/D/L/R):")
            if end == False:
                pass
            else:
                switch_matrix = switch(matrix = initi_matrix, start = start, end = end)
                print_finger(switch_matrix, end[0], end[1])
                time.sleep(0.5)
                print()
                start = tuple(end)
                initi_matrix = np.array(switch_matrix)
        
        eliminate_matrix = eliminate(matrix = switch_matrix)
        print_normal(eliminate_matrix)
        time.sleep(0.5)
        print()
        
        drop_matrix = drop(matrix = eliminate_matrix, types =types)
        print_normal(drop_matrix)
        
        SCORE = score(eli_matrix = eliminate_matrix, matrix = switch_matrix, score = SCORE)
        
        while np.abs(eliminate(drop_matrix) - drop_matrix).sum() != 0:
            mid_matrix = np.array(drop_matrix)
            eliminate_matrix = eliminate(matrix = mid_matrix)
            print_normal(eliminate_matrix)
            time.sleep(0.5)
            print()
            
            drop_matrix = drop(matrix = eliminate_matrix, types =types)
            print_normal(drop_matrix)
            
            SCORE = score(eli_matrix = eliminate_matrix, matrix = mid_matrix, score = SCORE)
        
        initi_matrix = drop_matrix
        times += 1
    if times == 1:
        print( name + " make only %d move to finish the Tower of Saviors." %(times))
    else:
        print( name + " make %d moves to finish the Tower of Saviors." %(times)) 