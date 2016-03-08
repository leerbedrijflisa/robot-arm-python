import RobotArm

with RobotArm.RobotArm("127.0.0.1", 9876) as robot_arm:
    robot_arm.timeout = 10
    robot_arm.speed = 1.0

    def go_right():
        robot_arm.move_right()
        robot_arm.grab()
        if robot_arm.scan() == "none":
            zoekblokrechts()
        robot_arm.move_left()

    for x in range(0, 100):
        go_right()
        robot_arm.drop()