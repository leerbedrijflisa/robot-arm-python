import RobotArm

with RobotArm.Controller("127.0.0.1", 9876) as robot_arm:
    robot_arm.timeout = 10
    robot_arm.speed = 1.0

    amount = 30

    nr = 1
    nl = 1
    reds = 0
    greens = 0
    blues = 0
    whites = 0
    right = True

    def clear_stack():
        robot_arm.grab()
        if robot_arm.scan() != RobotArm.Colors.none:
            robot_arm.move_left()
            robot_arm.drop()
            robot_arm.move_right()
            clear_stack()

    def left_or_right(right):
        if right:
            for x in range(0,nr):
                robot_arm.move_right()
        elif not right:
            for x in range(0,nl):
                robot_arm.move_left()

    def scan(right):
        global nr
        global nl
        robot_arm.grab()
        color = robot_arm.scan()
        if right:
            if color == RobotArm.Colors.none:
                robot_arm.move_right()
                scan(right)
                nr += 1
        elif not right:
            if color == RobotArm.Colors.none:
                robot_arm.move_left()
                scan(right)
                nl += 1

    def go_back(right):
        if right:
            for x in range(0,nr):
                robot_arm.move_left()
        elif not right:
            for x in range(0,nl):
                robot_arm.move_right()

    def get_new_block():
        global n
        global right

        left_or_right(right)
        scan(right)
        go_back(right)
    
        right = not right

    def put_block(moves):
        for x in range(0, moves):
            robot_arm.move_right()
        robot_arm.drop()
        for x in range(0, moves):
            robot_arm.move_left()

    def sort_block():
        global reds, greens, blues, whites

        robot_arm.grab()
        color = robot_arm.scan()
        if color == RobotArm.Colors.red:
            reds += 1
            put_block(1)
        if color == RobotArm.Colors.green:
            greens += 1
            put_block(2)
        if color == RobotArm.Colors.blue:
            blues += 1
            put_block(3)
        if color == RobotArm.Colors.white:
            whites += 1
            put_block(4)



    clear_stack()

    for x in range(0, amount):
        get_new_block()
        robot_arm.drop()

    print("made a tower of {0} blocks\n".format(amount))

    for x in range(0, amount):
        sort_block()
    
    print("sorted tower into stacks\n")
    print("red blocks: {0}".format(reds))
    print("green blocks: {0}".format(greens))
    print("blue blocks: {0}".format(blues))
    print("white blocks: {0}".format(whites))