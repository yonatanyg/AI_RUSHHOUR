import json
import sys


def create_domain_file(domain_file_name, board_size):

    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    "*** YOUR CODE HERE ***"
    domain_file.write("Propositions:\n")

    ##### FREE_IJ
    for i in range(board_size):
        for j in range(board_size):
            domain_file.write("FREE_{0},{1} ".format(i, j))
            domain_file.write("RED_{0},{1} ".format(i, j))
            domain_file.write("REDVISITED_{0},{1} ".format(i, j))

    #### PARTOF_LENGTH_INDEX_ORIENTATION_I,J
    for car_length in range(1, board_size + 1):
        for index_within in range(car_length):
            for orientation in {"H", "V"}:
                for i in range(board_size):
                    for j in range(board_size):
                        domain_file.write(
                            "PARTOF_{0}_{1}_{2}_{3},{4} ".format(car_length, index_within, orientation, i, j))

    domain_file.write("\nActions:\n")

    for i in range(board_size):
        for j in range(board_size):
            for dir in {"DOWN", "UP", "RIGHT", "LEFT"}:
                for car_length in range(1, board_size):
                    if dir == "DOWN":
                        if i == board_size - 1 or car_length > i + 1:
                            continue
                        # Regular Car
                        domain_file.write("Name: DOWN_{0},{1}_{2}\n".format(i, j, car_length))
                        domain_file.write(f"pre: FREE_{i + 1},{j} PARTOF_{car_length}_{car_length - 1}_V_{i},{j}\n")
                        domain_file.write("add: ")
                        addlist = f"FREE_{i - car_length + 1},{j} "
                        for t in range(car_length):
                            addlist += f"PARTOF_{car_length}_{t}_V_{i - car_length + 2 + t},{j} "
                        domain_file.write(addlist)

                        domain_file.write("\ndelete: ")
                        deletelist = f"FREE_{i + 1},{j} "
                        for t in range(car_length):
                            deletelist += f"PARTOF_{car_length}_{t}_V_{i - car_length + 1 + t},{j} "
                        domain_file.write(deletelist + "\n")

                        # Red Car
                        domain_file.write("Name: DOWN_RED_{0},{1}\n".format(i, j))
                        domain_file.write(f"pre: FREE_{i + 1},{j} RED_{i},{j}\n")
                        domain_file.write(f"add: REDVISITED_{i + 1},{j} RED_{i + 1},{j} FREE_{i},{j}\n")
                        domain_file.write(f"delete: RED_{i},{j} FREE_{i + 1},{j}\n")

                    if dir == "UP":
                        if i == 0 or car_length > board_size - i:
                            continue
                        # Regular Car
                        domain_file.write("Name: UP_{0},{1}_{2}\n".format(i, j, car_length))
                        domain_file.write(f"pre: FREE_{i - 1},{j} PARTOF_{car_length}_{0}_V_{i},{j}\n")
                        domain_file.write("add: ")
                        addlist = f"FREE_{i + car_length - 1},{j} "
                        for t in range(car_length):
                            addlist += f"PARTOF_{car_length}_{t}_V_{i + t - 1},{j} "
                        domain_file.write(addlist)

                        domain_file.write("\ndelete: ")
                        deletelist = f"FREE_{i - 1},{j} "
                        for t in range(car_length):
                            deletelist += f"PARTOF_{car_length}_{t}_V_{i + t},{j} "
                        domain_file.write(deletelist + "\n")

                        # Red Car
                        domain_file.write("Name: UP_RED_{0},{1}\n".format(i, j))
                        domain_file.write(f"pre: FREE_{i - 1},{j} RED_{i},{j}\n")
                        domain_file.write(f"add: REDVISITED_{i - 1},{j} RED_{i - 1},{j} FREE_{i},{j}\n")
                        domain_file.write(f"delete: RED_{i},{j} FREE_{i - 1},{j}\n")

                    if dir == "RIGHT":
                        if j == board_size - 1 or car_length > j + 1:
                            continue
                        # Regular Car
                        domain_file.write("Name: RIGHT_{0},{1}_{2}\n".format(i, j, car_length))
                        domain_file.write(f"pre: FREE_{i},{j + 1} PARTOF_{car_length}_{car_length - 1}_H_{i},{j}\n")
                        domain_file.write("add: ")
                        addlist = f"FREE_{i},{j - car_length + 1} "
                        for t in range(car_length):
                            addlist += f"PARTOF_{car_length}_{t}_H_{i},{j-car_length+t+2} "
                        domain_file.write(addlist)

                        domain_file.write("\ndelete: ")
                        deletelist = f"FREE_{i},{j + 1} "
                        for t in range(car_length):
                            deletelist += f"PARTOF_{car_length}_{t}_H_{i},{j - car_length + 1 + t} "
                        domain_file.write(deletelist + "\n")

                        # Red Car
                        domain_file.write("Name: RIGHT_RED_{0},{1}\n".format(i, j))
                        domain_file.write(f"pre: FREE_{i},{j + 1} RED_{i},{j}\n")
                        domain_file.write(f"add: REDVISITED_{i},{j + 1} RED_{i},{j + 1} FREE_{i},{j}\n")
                        domain_file.write(f"delete: RED_{i},{j} FREE_{i},{j+1}\n")

                    if dir == "LEFT":
                        if j == 0 or car_length > board_size - j:
                            continue
                        # Regular Car
                        domain_file.write("Name: LEFT_{0},{1}_{2}\n".format(i, j, car_length))
                        domain_file.write(f"pre: FREE_{i},{j - 1} PARTOF_{car_length}_{0}_H_{i},{j}\n")
                        domain_file.write("add: ")
                        addlist = f"FREE_{i},{j + car_length - 1} "
                        for t in range(car_length):
                            addlist += f"PARTOF_{car_length}_{t}_H_{i},{j+t-1} "
                        domain_file.write(addlist)

                        domain_file.write("\ndelete: ")
                        deletelist = f"FREE_{i},{j - 1} "
                        for t in range(car_length):
                            deletelist += f"PARTOF_{car_length}_{t}_H_{i},{j + t} "
                        domain_file.write(deletelist + "\n")

                        # Red Car
                        domain_file.write("Name: LEFT_RED_{0},{1}\n".format(i, j))
                        domain_file.write(f"pre: FREE_{i},{j - 1} RED_{i},{j}\n")
                        domain_file.write(f"add: REDVISITED_{i},{j - 1} RED_{i},{j - 1} FREE_{i},{j}\n")
                        domain_file.write(f"delete: RED_{i},{j} FREE_{i},{j - 1}\n")

    domain_file.close()



def create_problem_file(problem_file_name_, json_file_name, board_size, targets):

    vehicles_data = None
    with open(json_file_name, 'r') as f:
        vehicles_data = json.load(f)

    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"
    problem_file.write("Initial state: ")

    available_cells = {(i,j) for j in range(board_size) for i in range(board_size)}

    redcar = None
    ### ISPARTOF
    for car in vehicles_data:
        if car['symbol'] == 'X':
            redcar = car
            continue
        if car['orientation'] == 'vertical':
            car_length = car['length']
            pos = car['position']
            for t in range(car_length):
                problem_file.write(f"PARTOF_{car_length}_{t}_V_{pos[0]+t},{pos[1]} ")
                available_cells.remove((pos[0]+t,pos[1]))
        # handle horizontal
        if car['orientation'] == 'horizontal':
            car_length = car['length']
            pos = car['position']
            for t in range(car_length):
                problem_file.write(f"PARTOF_{car_length}_{t}_H_{pos[0]},{pos[1]+t} ")
                available_cells.remove((pos[0],pos[1]+t))
    ### RED
    redpos = redcar["position"]
    problem_file.write(f"RED_{redpos[0]},{redpos[1]} ")
    available_cells.remove((redpos[0], redpos[1]))
    problem_file.write(f"REDVISITED_{redpos[0]},{redpos[1]} ")
    ### FREE
    for cell in available_cells:
        problem_file.write(f"FREE_{cell[0]},{cell[1]} ")

    problem_file.write("\nGoal state: ")

    ### TARGETS
    for target in targets:
        problem_file.write(f"REDVISITED_{target[0]},{target[1]} ")

    ###RED
    problem_file.write(f"RED_{board_size-1},{board_size-1} ")

    problem_file.close()


if __name__ == '__main__':
    """
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)
    """
    #create_domain_file("Test_Domain.txt", 6)
    #create_problem_file("Test_Problem.txt", "vehicles.json", 6, [(2, 5), (4, 3), (0, 0)])
    create_domain_file("simple_Domain.txt", 4)
    create_problem_file("simple_Problem.txt", "vehicles_empty.json", 4, [(1, 1)])
