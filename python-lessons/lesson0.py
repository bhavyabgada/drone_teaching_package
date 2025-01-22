# Import required packages
from drone_teaching_package.simulated_tello import EasyTelloToSimulatedDrone
from drone_teaching_package.real_tello import EasyTelloRealDrone
import json
from time import sleep
import threading
from datetime import datetime
import math
import random

def get_drone():
    """
    Prompt user to select between simulated or real drone
    Returns:
        drone: Instance of either EasyTelloToSimulatedDrone or EasyTelloRealDrone
    """
    print("Select drone mode:")
    print("1. Simulated Drone")
    print("2. Real Tello Drone")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        simulator_key = "77f9202d-3aed-4981-a31b-6eb8933fa4ee"
        return EasyTelloToSimulatedDrone(simulator_key=simulator_key)
    elif choice == "2":
        return EasyTelloRealDrone()
    else:
        print("Invalid choice, please select either 1 or 2.")
        return get_drone()

# Initialize drone
drone = get_drone()

# ---------------------------
# LESSON 0: Python Fundamentals
# ---------------------------

# 0.1: Variables
print("\n=== 0.1: Variables ===")
drone_name = "Tello"
current_height = 50  # in cm
battery = drone.get_battery()

print(f"Drone Name: {drone_name}")
print(f"Target Height: {current_height}cm")
print(f"Battery Level: {battery}")

# 0.2: Input/Output
print("\n=== 0.2: Input/Output ===")
print("Available commands: up, down, left, right, forward, back, cw, ccw")
command = input("Enter a drone command (e.g., 'up 50'): ")

try:
    action, value = command.split()
    value = int(value)
    
    # Execute actual drone command
    if action == "up":
        drone.up(value)
    elif action == "down":
        drone.down(value)
    elif action == "left":
        drone.left(value)
    elif action == "right":
        drone.right(value)
    elif action == "forward":
        drone.forward(value)
    elif action == "back":
        drone.back(value)
    elif action == "cw":
        drone.cw(value)
    elif action == "ccw":
        drone.ccw(value)
except Exception as e:
    print(f"Error executing command: {str(e)}")

# 0.3: Conditionals
print("\n=== 0.3: Conditionals ===")
battery = drone.get_battery()
try:
    battery_level = int(battery.replace('%', ''))
    if battery_level > 20:
        print("Battery sufficient for flight")
        drone.takeoff()
        sleep(2)
        drone.land()
    else:
        print("Warning: Recharge needed")
except ValueError:
    print("Could not parse battery level")

# 0.4: Loops
print("\n=== 0.4: Loops ===")
print("Executing square pattern flight...")

try:
    # Take off first
    drone.takeoff()
    sleep(2)
    
    # Fly in a square pattern
    for _ in range(4):
        drone.forward(50)
        sleep(2)
        drone.cw(90)
        sleep(2)
    
    # Land after pattern is complete
    drone.land()
except Exception as e:
    print(f"Error during flight pattern: {str(e)}")
    drone.land()  # Emergency landing

# 0.5: Functions
print("\n=== 0.5: Functions ===")

def safe_takeoff():
    """Safe takeoff with battery check"""
    battery = drone.get_battery()
    try:
        if int(battery.replace('%', '')) > 20:
            drone.takeoff()
            return True
        return False
    except ValueError:
        return False

def execute_flip(direction):
    """Execute a flip in specified direction"""
    try:
        drone.flip(direction)  # 'l', 'r', 'f', 'b'
        return True
    except Exception as e:
        print(f"Flip failed: {str(e)}")
        return False

def fly_triangle(size):
    """Fly in a triangle pattern"""
    try:
        for _ in range(3):
            drone.forward(size)
            sleep(2)
            drone.ccw(120)
            sleep(2)
        return True
    except Exception:
        return False

# 0.6: Lists
print("\n=== 0.6: Lists ===")

# List of commands to execute in sequence
flight_sequence = [
    ("takeoff", None),
    ("up", 50),
    ("forward", 30),
    ("cw", 90),
    ("forward", 30),
    ("land", None)
]

try:
    for command, value in flight_sequence:
        if command == "takeoff":
            drone.takeoff()
        elif command == "land":
            drone.land()
        elif command == "up":
            drone.up(value)
        elif command == "forward":
            drone.forward(value)
        elif command == "cw":
            drone.cw(value)
        sleep(2)  # Wait between commands
except Exception as e:
    print(f"Error in sequence: {str(e)}")
    drone.land()

# 0.7: Dictionaries
print("\n=== 0.7: Dictionaries ===")

# Store flight patterns
flight_patterns = {
    "square": [
        ("forward", 50),
        ("cw", 90),
        ("forward", 50),
        ("cw", 90),
        ("forward", 50),
        ("cw", 90),
        ("forward", 50)
    ],
    "triangle": [
        ("forward", 50),
        ("ccw", 120),
        ("forward", 50),
        ("ccw", 120),
        ("forward", 50)
    ]
}

def execute_pattern(pattern_name):
    """Execute a predefined flight pattern"""
    if pattern_name not in flight_patterns:
        return False
    
    try:
        drone.takeoff()
        sleep(2)
        
        for command, value in flight_patterns[pattern_name]:
            if hasattr(drone, command):
                getattr(drone, command)(value)
                sleep(2)
        
        drone.land()
        return True
    except Exception as e:
        print(f"Error executing pattern: {str(e)}")
        drone.land()
        return False

# 0.8: Tuples
print("\n=== 0.8: Tuples ===")

# Define waypoints as tuples (x, y, z, speed)
waypoints = [
    (50, 0, 0, 50),    # Forward 50cm
    (0, 50, 0, 50),    # Right 50cm
    (0, 0, 50, 50)     # Up 50cm
]

try:
    drone.takeoff()
    sleep(2)
    
    for x, y, z, speed in waypoints:
        drone.go(x, y, z, speed)
        sleep(3)  # Wait for movement to complete
    
    drone.land()
except Exception as e:
    print(f"Error navigating waypoints: {str(e)}")
    drone.land()

# 0.9: Strings
print("\n=== 0.9: Strings ===")

def generate_command_log(command, value=None):
    """Generate formatted log string for drone commands"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if value is not None:
        return f"[{timestamp}] Executed: {command}({value})"
    return f"[{timestamp}] Executed: {command}()"

# Execute some commands and log them
command_logs = []
try:
    drone.takeoff()
    command_logs.append(generate_command_log("takeoff"))
    sleep(2)
    
    drone.up(50)
    command_logs.append(generate_command_log("up", 50))
    sleep(2)
    
    drone.land()
    command_logs.append(generate_command_log("land"))
except Exception as e:
    print(f"Error during command sequence: {str(e)}")

print("\nCommand Logs:")
for log in command_logs:
    print(log)

# 0.10: File Handling
print("\n=== 0.10: File Handling ===")

def save_flight_log(logs, filename="flight_log.txt"):
    """Save flight logs to file"""
    try:
        with open(filename, "a") as file:
            file.write("\n=== Flight Session ===\n")
            for log in logs:
                file.write(log + "\n")
        print(f"Logs saved to {filename}")
    except IOError as e:
        print(f"Error saving logs: {str(e)}")

save_flight_log(command_logs)

# 0.11: Exception Handling
print("\n=== 0.11: Exception Handling ===")

def safe_execute_command(command_func, *args):
    """Safely execute a drone command with error handling"""
    try:
        command_func(*args)
        return True
    except AttributeError:
        print(f"Command not available on this drone")
        return False
    except ValueError as e:
        print(f"Invalid value for command: {str(e)}")
        return False
    except Exception as e:
        print(f"Error executing command: {str(e)}")
        return False

# Test safe command execution
commands_to_test = [
    (drone.up, 50),
    (drone.flip, 'r'),
    (drone.forward, 100)
]

for cmd_func, value in commands_to_test:
    safe_execute_command(cmd_func, value)

# 0.12: Modules
print("\n=== 0.12: Modules ===")

def calculate_curve_params(start_point, control_point, end_point):
    """Calculate curve flight parameters using math module"""
    x1, y1, z1 = start_point
    x2, y2, z2 = control_point
    x3, y3, z3 = end_point
    
    # Calculate distances for speed adjustment
    distance = math.sqrt(
        (x3-x1)**2 + (y3-y1)**2 + (z3-z1)**2
    )
    
    # Calculate speed based on distance
    speed = min(100, max(10, int(distance/5)))
    
    return x1, y1, z1, x2, y2, z2, speed

# Execute curve flight
try:
    start = (0, 0, 0)
    control = (50, 50, 50)
    end = (100, 0, 0)
    
    params = calculate_curve_params(start, control, end)
    drone.curve(*params)
except Exception as e:
    print(f"Error executing curve: {str(e)}")

# 0.13: Combined Concepts - Interactive Flight Control
print("\n=== 0.13: Interactive Flight Control ===")

def interactive_flight_control():
    """
    Interactive flight control combining multiple concepts
    """
    commands = {
        'takeoff': drone.takeoff,
        'land': drone.land,
        'up': drone.up,
        'down': drone.down,
        'left': drone.left,
        'right': drone.right,
        'forward': drone.forward,
        'back': drone.back,
        'cw': drone.cw,
        'ccw': drone.ccw
    }
    
    flight_log = []
    
    print("\nInteractive Flight Control")
    print("Available commands:", list(commands.keys()))
    print("Enter 'quit' to end session")
    
    try:
        while True:
            cmd = input("\nEnter command: ").strip().lower()
            if cmd == 'quit':
                break
                
            if cmd in ['takeoff', 'land']:
                commands[cmd]()
                flight_log.append(generate_command_log(cmd))
            else:
                try:
                    action, value = cmd.split()
                    if action in commands:
                        commands[action](int(value))
                        flight_log.append(generate_command_log(action, value))
                except ValueError:
                    print("Invalid command format. Use: <command> <value>")
                except Exception as e:
                    print(f"Error: {str(e)}")
    
    except KeyboardInterrupt:
        print("\nFlight session interrupted")
    finally:
        # Ensure drone lands safely
        drone.land()
        # Save flight log
        save_flight_log(flight_log, "interactive_session.txt")

if __name__ == "__main__":
    try:
        # Run interactive session
        interactive_flight_control()
    except Exception as e:
        print(f"Program error: {str(e)}")
        # Emergency landing
        drone.land()