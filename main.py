# main.py
from simulated_tello import EasyTelloToSimulatedDrone
from real_tello import EasyTelloRealDrone


def get_drone():
    print("Select drone mode:")
    print("1. Simulated Drone")
    print("2. Real Tello Drone")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        # simulator_key = input("Enter your simulator key: ")
        simulator_key = "23aa64ee-8dc9-4fa4-b64d-b3bd5a2d4d5c"
        return EasyTelloToSimulatedDrone(simulator_key=simulator_key)
    elif choice == "2":
        return EasyTelloRealDrone()
    else:
        print("Invalid choice, please select either 1 or 2.")
        return get_drone()  # Recursively ask for correct input


# Instantiate the drone based on user input
drone = get_drone()

# ---------------------------
# LESSON 1: Basic Drone Commands
# ---------------------------

# Uncomment the code below to run Lesson 1

drone.connect()         # Connect to the drone
drone.takeoff()         # Take off
drone.up(50)            # Move up 50 cm
drone.forward(100)      # Move forward 100 cm
drone.cw(90)            # Rotate clockwise 90 degrees
drone.flip('l')         # Flip left
drone.land()            # Land the drone


# ---------------------------
# LESSON 2: Advanced Movement Commands
# ---------------------------

# Uncomment the code below to run Lesson 2

# drone.connect()         # Connect to the drone
# drone.takeoff()         # Take off
# drone.left(100)         # Move left 100 cm
# drone.right(100)        # Move right 100 cm
# drone.down(50)          # Move down 50 cm
# drone.back(100)         # Move backward 100 cm
# drone.ccw(90)           # Rotate counterclockwise 90 degrees
# drone.land()            # Land the drone


# ---------------------------
# LESSON 3: Speed and Flipping
# ---------------------------

# Uncomment the code below to run Lesson 3

# drone.connect()         # Connect to the drone
# drone.takeoff()         # Take off
# drone.set_speed(10)     # Set speed to 10 cm/s
# drone.forward(100)      # Move forward 100 cm at the new speed
# drone.flip('f')         # Flip forward
# drone.flip('b')         # Flip backward
# drone.land()            # Land the drone


# ---------------------------
# LESSON 4: Flying to Coordinates (Go and Curve)
# ---------------------------

# Uncomment the code below to run Lesson 4

# drone.connect()         # Connect to the drone
# drone.takeoff()         # Take off
# drone.go(100, 100, 50, 20)   # Fly to coordinates (100, 100, 50) at speed 20 cm/s
# drone.curve(50, 50, 0, 100, 100, 50, 30)  # Fly in a curve from (50, 50, 0) to (100, 100, 50)
# drone.land()            # Land the drone


# ---------------------------
# LESSON 5: Monitoring and Battery
# ---------------------------

# Uncomment the code below to run Lesson 5

# drone.connect()         # Connect to the drone
# drone.takeoff()         # Take off
# battery = drone.get_battery()   # Get the battery level
# print(f"Battery level: {battery}")
# drone.land()            # Land the drone


# ---------------------------
# LESSON 6: Full Control with Rotation and Flipping
# ---------------------------

# Uncomment the code below to run Lesson 6

# drone.connect()         # Connect to the drone
# drone.takeoff()         # Take off
# drone.up(100)           # Move up 100 cm
# drone.cw(180)           # Rotate clockwise 180 degrees
# drone.forward(200)      # Move forward 200 cm
# drone.flip('r')         # Flip right
# drone.ccw(90)           # Rotate counterclockwise 90 degrees
# drone.back(150)         # Move backward 150 cm
# drone.down(50)          # Move down 50 cm
# drone.land()            # Land the drone
