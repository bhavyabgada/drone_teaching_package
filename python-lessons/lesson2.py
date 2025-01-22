'''
Constructors in Python

The implementation includes:

Basic Constructor (DroneWithConstructor)

Simple initialization with name and altitude
Basic attribute setup
Default value demonstration


Multiple Configurations (ConfigurableDrone)

Multiple initialization parameters
Custom drone settings
Configuration application


Position Aware Constructor (PositionAwareDrone)

Home position initialization
Position tracking
Distance calculation


Return Home Constructor (ReturnHomeDrone)

Separate home coordinates
Movement tracking
Return home functionality



Each class uses only the available drone commands:

takeoff()
land()
up/down
go (coordinate movement)
set_speed()
get_battery()
'''


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
        simulator_key = "edafb6aa-f195-450e-a68f-0795f6712085"
        return EasyTelloToSimulatedDrone(simulator_key=simulator_key)
    elif choice == "2":
        return EasyTelloRealDrone()
    else:
        print("Invalid choice, please select either 1 or 2.")
        return get_drone()

# Initialize drone
drone = get_drone()

# ---------------------------
# LESSON 2: Constructors
# ---------------------------

# 2.1: Basic Constructor
class DroneWithConstructor:
    """Demonstrate basic constructor usage"""
    
    def __init__(self, name: str, drone_interface, starting_altitude: int = 50):
        """
        Initialize drone with basic attributes
        
        Args:
            name (str): Identifier for the drone
            drone_interface: The drone control interface
            starting_altitude (int): Default flight altitude in cm
        """
        # Basic attributes
        self.name = name
        self.drone = drone_interface
        self.default_altitude = starting_altitude
        
        # Status attributes
        self.is_flying = False
        self.current_altitude = 0
        
        # Log initialization
        self._log_setup()
    
    def _log_setup(self):
        """Log the initialization of the drone"""
        print(f"Initialized drone '{self.name}' with altitude {self.default_altitude}cm")
    
    def takeoff_to_default(self):
        """Take off and move to default altitude"""
        try:
            self.drone.takeoff()
            sleep(2)
            self.drone.up(self.default_altitude)
            self.is_flying = True
            self.current_altitude = self.default_altitude
        except Exception as e:
            print(f"Takeoff error: {str(e)}")

# 2.2: Multiple Drones with Different Configurations
class ConfigurableDrone:
    """Demonstrate multiple configuration options in constructor"""
    
    def __init__(self, 
                 name: str,
                 drone_interface,
                 home_position: tuple = (0, 0, 0),
                 max_altitude: int = 100,
                 default_speed: int = 30):
        """
        Initialize drone with multiple configuration options
        
        Args:
            name (str): Drone identifier
            drone_interface: Drone control interface
            home_position (tuple): Starting coordinates (x, y, z)
            max_altitude (int): Maximum allowed altitude in cm
            default_speed (int): Default movement speed in cm/s
        """
        # Basic setup
        self.name = name
        self.drone = drone_interface
        
        # Configuration
        self.home_position = home_position
        self.max_altitude = max_altitude
        self.default_speed = default_speed
        
        # Initialize drone settings
        self._configure_drone()
    
    def _configure_drone(self):
        """Apply initial drone configuration"""
        try:
            self.drone.set_speed(self.default_speed)
            print(f"Configured {self.name} with:")
            print(f"Home: {self.home_position}")
            print(f"Max Altitude: {self.max_altitude}cm")
            print(f"Speed: {self.default_speed}cm/s")
        except Exception as e:
            print(f"Configuration error: {str(e)}")
    
    def return_home(self):
        """Return to home position"""
        try:
            x, y, z = self.home_position
            self.drone.go(x, y, z, self.default_speed)
        except Exception as e:
            print(f"Return home error: {str(e)}")

# 2.3: Constructor with Home Position
class PositionAwareDrone:
    """Demonstrate constructor with position tracking"""
    
    def __init__(self, 
                 name: str,
                 drone_interface,
                 home_coordinates: tuple = (0, 0, 0)):
        """
        Initialize position-aware drone
        
        Args:
            name (str): Drone identifier
            drone_interface: Drone control interface
            home_coordinates (tuple): Home position (x, y, z)
        """
        self.name = name
        self.drone = drone_interface
        self.home_coordinates = home_coordinates
        self.current_position = home_coordinates
        self.flight_path = [home_coordinates]
    
    def move_to_position(self, x: int, y: int, z: int):
        """
        Move to specified position and update tracking
        
        Args:
            x, y, z (int): Target coordinates in cm
        """
        try:
            self.drone.go(x, y, z, 30)
            self.current_position = (x, y, z)
            self.flight_path.append((x, y, z))
        except Exception as e:
            print(f"Movement error: {str(e)}")
    
    def get_distance_from_home(self) -> float:
        """Calculate distance from home position"""
        x1, y1, z1 = self.home_coordinates
        x2, y2, z2 = self.current_position
        return math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

# 2.4: Constructor with Return Home Capability
class ReturnHomeDrone:
    """Demonstrate home position and return capability"""
    
    def __init__(self,
                 name: str,
                 drone_interface,
                 home_x: int = 0,
                 home_y: int = 0,
                 home_z: int = 100):
        """
        Initialize drone with separate home coordinates
        
        Args:
            name (str): Drone identifier
            drone_interface: Drone control interface
            home_x (int): Home X coordinate
            home_y (int): Home Y coordinate
            home_z (int): Home Z coordinate
        """
        # Basic setup
        self.name = name
        self.drone = drone_interface
        
        # Home position
        self.home_x = home_x
        self.home_y = home_y
        self.home_z = home_z
        
        # Current position tracking
        self.current_x = home_x
        self.current_y = home_y
        self.current_z = home_z
        
        # Movement history
        self.movements = []
    
    def update_position(self, x: int, y: int, z: int):
        """Update current position after movement"""
        self.current_x = x
        self.current_y = y
        self.current_z = z
        self.movements.append((x, y, z))
    
    def return_home(self):
        """Execute return to home sequence"""
        try:
            print(f"Returning to home position ({self.home_x}, {self.home_y}, {self.home_z})")
            
            # First, rise to safe altitude if needed
            if self.current_z < self.home_z:
                self.drone.up(self.home_z - self.current_z)
                sleep(2)
            
            # Then move to home X,Y coordinates
            self.drone.go(self.home_x, self.home_y, self.home_z, 30)
            sleep(2)
            
            # Update position
            self.update_position(self.home_x, self.home_y, self.home_z)
            print("Successfully returned home")
            
        except Exception as e:
            print(f"Return home error: {str(e)}")

def demonstrate_constructors():
    """Demonstrate the usage of different constructors"""
    
    # 2.1: Basic Constructor Demo
    print("\n=== Basic Constructor Demo ===")
    basic_drone = DroneWithConstructor("Basic-1", drone, starting_altitude=60)
    basic_drone.takeoff_to_default()
    sleep(3)
    drone.land()
    
    # 2.2: Configurable Drone Demo
    print("\n=== Configurable Drone Demo ===")
    config_drone = ConfigurableDrone(
        "Config-1",
        drone,
        home_position=(0, 0, 50),
        max_altitude=120,
        default_speed=40
    )
    
    # 2.3: Position Aware Drone Demo
    print("\n=== Position Aware Drone Demo ===")
    pos_drone = PositionAwareDrone("Position-1", drone, home_coordinates=(0, 0, 50))
    pos_drone.move_to_position(50, 50, 50)
    sleep(3)
    print(f"Distance from home: {pos_drone.get_distance_from_home():.2f}cm")
    
    # 2.4: Return Home Drone Demo
    print("\n=== Return Home Drone Demo ===")
    home_drone = ReturnHomeDrone("Home-1", drone, home_z=80)
    home_drone.update_position(100, 100, 50)  # Simulate movement
    home_drone.return_home()

if __name__ == "__main__":
    try:
        demonstrate_constructors()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        drone.land()  # Emergency landing
    except Exception as e:
        print(f"\nProgram error: {str(e)}")
        drone.land()  # Emergency landing