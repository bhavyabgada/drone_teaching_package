from drone_teaching_package.simulated_tello import EasyTelloToSimulatedDrone
from drone_teaching_package.real_tello import EasyTelloRealDrone
import json
from time import sleep
import threading
from datetime import datetime

def get_drone():
    print("Select drone mode:")
    print("1. Simulated Drone")
    print("2. Real Tello Drone")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        # simulator_key = input("Enter your simulator key: ")
        simulator_key = "edafb6aa-f195-450e-a68f-0795f6712085"
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

# drone.connect()         # Connect to the drone
# drone.takeoff()         # Take off
# drone.up(50)            # Move up 50 cm
# drone.forward(100)      # Move forward 100 cm
# drone.cw(90)            # Rotate clockwise 90 degrees
# drone.flip('l')         # Flip left
# drone.land()            # Land the drone


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

# ---------------------------
# LESSON 7: Telemetry, Emergency Monitoring, and Boundary Checking
# ---------------------------

# Define the boundary box for drone movement (in cm)
BOUNDARY_BOX = {
    "x_min": 0,
    "x_max": 100,
    "y_min": 0,
    "y_max": 100,
    "z_min": 0,
    "z_max": 80
}

# Function to collect telemetry data and append it to the JSON file
def collect_telemetry_data(x, y, z):
    # Create telemetry data entry with timestamp
    telemetry_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "x": x,
        "y": y,
        "z": z
    }

    # Try to read the existing JSON file
    try:
        with open('telemetry_data.json', 'r') as file:
            telemetry_log = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, initialize an empty list
        telemetry_log = []

    # Append the new telemetry entry
    telemetry_log.append(telemetry_entry)

    # Write the updated log back to the JSON file
    with open('telemetry_data.json', 'w') as file:
        json.dump(telemetry_log, file, indent=4)

    print(f"Telemetry data logged at {telemetry_entry['timestamp']}")

# Boundary check function
def check_boundary(x, y, z):
    return (x < BOUNDARY_BOX["x_min"] or x > BOUNDARY_BOX["x_max"] or
            y < BOUNDARY_BOX["y_min"] or y > BOUNDARY_BOX["y_max"] or
            z < BOUNDARY_BOX["z_min"] or z > BOUNDARY_BOX["z_max"])

# Emergency landing function with automatic fallback
def emergency_landing():
    print("Emergency condition detected! Preparing for emergency landing...")

    # Set up a thread to wait for user input for 10 seconds
    user_input = []

    def ask_user_input():
        choice = input("Enter 'human' for manual control or 'automatic' for auto landing (10 sec to choose): ")
        user_input.append(choice)

    input_thread = threading.Thread(target=ask_user_input)
    input_thread.start()

    # Wait for the input or timeout after 10 seconds
    input_thread.join(timeout=10)

    # Check if user provided input, otherwise default to 'automatic'
    if user_input and user_input[0].lower() == "human":
        print("Human control selected.")
        human_control()
    else:
        print("Automatic emergency landing!")
        drone.land()

# Human control function
def human_control():
    while True:
        key = input("Enter command (w/a/s/d for movement, t for takeoff, l for landing): ").strip().lower()
        if key == "t":
            drone.takeoff()
        elif key == "l":
            drone.land()
            break
        elif key == "w":
            drone.forward(20)
        elif key == "s":
            drone.back(20)
        elif key == "a":
            drone.left(20)
        elif key == "d":
            drone.right(20)

# Lesson 7: Drone Boundary Monitoring with Continuous Telemetry Update and Timestamp Logging
def lesson_7():
    drone.connect()
    drone.takeoff()

    telemetry_data = {
        "x": 0,
        "y": 0,
        "z": 50  # Start at 50 cm altitude
    }

    # Simulate drone movements and update telemetry
    for _ in range(10):  # Example: Move drone in 10 steps
        telemetry_data["x"] += 50  # Move 50 cm in x-direction
        telemetry_data["y"] += 50  # Move 50 cm in y-direction
        telemetry_data["z"] += 10  # Move 10 cm in z-direction

        # Write updated telemetry data to JSON file (appending with timestamp)
        collect_telemetry_data(telemetry_data["x"], telemetry_data["y"], telemetry_data["z"])

        # Check if the drone is outside the boundary
        if check_boundary(telemetry_data["x"], telemetry_data["y"], telemetry_data["z"]):
            emergency_landing()
            break  # Exit if emergency occurs

        # Simulate drone movement
        drone.go(telemetry_data["x"], telemetry_data["y"], telemetry_data["z"], 20)
        sleep(1)  # Wait before next move

    drone.land()  # Safely land the drone after the lesson

# Run Lesson 7
lesson_7()
