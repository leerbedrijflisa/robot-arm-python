import RobotArm

with RobotArm.RobotArm("127.0.0.1", 9876) as robot_arm:
    robot_arm.timeout = 10
    robot_arm.speed = 1.0


    robot_arm.grab()

    robot_arm.move_left()

    if robot_arm.scan() == "red":
        robot_arm.drop()
    else:
        robot_arm.move_left()
        robot_arm.drop()

    robot_arm.move_right()