import RobotArm

robot_arm = RobotArm.Controller()
robot_arm.timeout = 10
robot_arm.speed = 0.5

robot_arm.grab()

color = robot_arm.scan()

if color.name == "green":
    print(color)

while True:
    robot_arm.move_left()