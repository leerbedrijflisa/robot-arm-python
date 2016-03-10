import RobotArm

with RobotArm.RobotArm("127.0.0.1", 9876) as robot_arm:
    robot_arm.timeout = 10
    robot_arm.speed = 1.0

    nr = 1
    nl = 1
    right = True

    def left_or_right(right):
        if right:
            for x in range(0,nr):
                robot_arm.move_right()
        elif not right:
            for x in range(0,nl):
                robot_arm.move_left()

    def go_back(right):
        if right:
            for x in range(0,nr):
                robot_arm.move_left()
        elif not right:
            for x in range(0,nl):
                robot_arm.move_right()

    def scan(right):
        global nr
        global nl
        robot_arm.grab()
        if right:
            if robot_arm.scan() == "none":
                robot_arm.move_right()
                scan(right)
                nr += 1
        elif not right:
            if robot_arm.scan() == "none":
                robot_arm.move_left()
                scan(right)
                nl += 1

    def get_new_block():
        global n
        global right

        left_or_right(right)

        scan(right)
    
        go_back(right)
    
        right = not right


    for x in range(0, 100000):
        get_new_block()
        robot_arm.drop()