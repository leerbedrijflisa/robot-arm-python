import RobotArm

robot_arm = RobotArm.Controller()
robot_arm.timeout = 1000
robot_arm.speed = 1.0

reds = 0
greens = 0
blues = 0
whites = 0

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
    if color == RobotArm.Colors.none:
        return False

#robot_arm.load_level("bas/tower")
#robot_arm.load_level("tower")
#robot_arm.load_level("random")
#robot_arm.load_level("empty")
robot_arm.load_level("nonexisting/level")

robot_arm.grab()
for i in range(0,1000):
    result = sort_block()
    if result == False:
        break
    
print("sorted tower into stacks\n")
print("red blocks: {0}".format(reds))
print("green blocks: {0}".format(greens))
print("blue blocks: {0}".format(blues))
print("white blocks: {0}".format(whites))