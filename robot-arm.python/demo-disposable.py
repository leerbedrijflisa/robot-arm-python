import RobotArm

with RobotArm.RobotArm("127.0.0.1", 9876) as robot_arm:
    robot_arm.timeout = 10
    robot_arm.speed = 1.0

    n = 1

    def scan():
        global n
        robot_arm.grab()
        if robot_arm.scan() == "none":
            robot_arm.move_right()
            scan()
            n += 1

    def get_new_block():
        global n

        for x in range(0,n):
            robot_arm.move_right()

        scan()
    
        for x in range(0,n):
            robot_arm.move_left()


    for x in range(0, 100000):
        get_new_block()
        robot_arm.drop()