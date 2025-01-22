'''
Classes in Python

The implementation includes:

BasicDrone Class

Basic attributes and methods
Simple flight controls
Status tracking and logging


MissionDrone Class (inherits from BasicDrone)

Predefined flight patterns (square, triangle)
Mission status tracking
Enhanced logging


AdvancedDrone Class (inherits from MissionDrone)

Advanced movement capabilities (go, curve)
Flip functionality
Detailed movement logging


SafeDrone Class (inherits from AdvancedDrone)

Battery safety checks
Safe mission execution
Enhanced error handling



Each class uses only the available drone commands:

takeoff()
land()
up/down/left/right/forward/back
cw/ccw (rotation)
flip
go (coordinate movement)
curve (curved paths)
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
# LESSON 1: Classes
# ---------------------------

# 1.1: Basic Drone Class with Attributes
class BasicDrone:
    """A simple drone class implementing basic drone operations"""
    
    def __init__(self, name, drone_interface):
        """
        Initialize drone with basic attributes
        
        Args:
            name: Name identifier for the drone
            drone_interface: Instance of EasyTelloToSimulatedDrone or EasyTelloRealDrone
        """
        self.name = name
        self.drone = drone_interface
        self.is_flying = False
        self.flight_log = []
        print(f"Initialized drone: {self.name}")
    
    def takeoff(self):
        """Execute takeoff sequence"""
        try:
            self.drone.takeoff()
            self.is_flying = True
            self._log_action("takeoff")
        except Exception as e:
            print(f"Takeoff error: {str(e)}")
    
    def land(self):
        """Execute landing sequence"""
        try:
            self.drone.land()
            self.is_flying = False
            self._log_action("land")
        except Exception as e:
            print(f"Landing error: {str(e)}")
    
    def _log_action(self, action: str):
        """Log drone actions with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.flight_log.append(f"{timestamp}: {action}")
    
    def get_status(self):
        """Get current drone status"""
        battery = self.drone.get_battery()
        status = f"Drone: {self.name}\n"
        status += f"Battery: {battery}\n"
        status += f"Flying: {self.is_flying}"
        return status

# 1.2: Mission Capable Drone
class MissionDrone(BasicDrone):
    """Enhanced drone class with mission capabilities"""
    
    def __init__(self, name, drone_interface):
        """Initialize mission-capable drone"""
        super().__init__(name, drone_interface)
        self.current_mission = None
        self.mission_status = "idle"
    
    def execute_square_mission(self, side_length: int):
        """
        Execute a square flight pattern
        
        Args:
            side_length: Length of square sides in cm
        """
        try:
            self.current_mission = "square"
            self.mission_status = "active"
            
            # Takeoff
            self.takeoff()
            sleep(2)
            
            # Fly in square pattern
            for _ in range(4):
                self.drone.forward(side_length)
                sleep(2)
                self.drone.cw(90)
                sleep(2)
                self._log_action(f"forward {side_length}cm, rotate 90°")
            
            # Land
            self.land()
            self.mission_status = "completed"
            
        except Exception as e:
            print(f"Mission failed: {str(e)}")
            self.mission_status = "failed"
            self.land()
    
    def execute_triangle_mission(self, side_length: int):
        """
        Execute a triangular flight pattern
        
        Args:
            side_length: Length of triangle sides in cm
        """
        try:
            self.current_mission = "triangle"
            self.mission_status = "active"
            
            # Takeoff
            self.takeoff()
            sleep(2)
            
            # Fly in triangular pattern
            for _ in range(3):
                self.drone.forward(side_length)
                sleep(2)
                self.drone.ccw(120)
                sleep(2)
                self._log_action(f"forward {side_length}cm, rotate 120°")
            
            # Land
            self.land()
            self.mission_status = "completed"
            
        except Exception as e:
            print(f"Mission failed: {str(e)}")
            self.mission_status = "failed"
            self.land()

# 1.3: Advanced Movement Drone
class AdvancedDrone(MissionDrone):
    """Drone class with advanced movement capabilities"""
    
    def __init__(self, name, drone_interface):
        """Initialize advanced drone"""
        super().__init__(name, drone_interface)
        self.movement_log = []
    
    def fly_to_point(self, x: int, y: int, z: int, speed: int):
        """
        Fly to specific coordinates
        
        Args:
            x, y, z: Target coordinates in cm
            speed: Flight speed in cm/s
        """
        try:
            self.drone.go(x, y, z, speed)
            self._log_action(f"flew to ({x}, {y}, {z}) at {speed}cm/s")
        except Exception as e:
            print(f"Navigation error: {str(e)}")
    
    def fly_curve(self, x1: int, y1: int, z1: int, 
                  x2: int, y2: int, z2: int, speed: int):
        """
        Execute curved flight path
        
        Args:
            x1, y1, z1: First point coordinates
            x2, y2, z2: Second point coordinates
            speed: Flight speed
        """
        try:
            self.drone.curve(x1, y1, z1, x2, y2, z2, speed)
            self._log_action(f"flew curve through ({x1},{y1},{z1}) to ({x2},{y2},{z2})")
        except Exception as e:
            print(f"Curve flight error: {str(e)}")
    
    def perform_flip(self, direction: str):
        """
        Perform flip in specified direction
        
        Args:
            direction: 'l' (left), 'r' (right), 'f' (forward), 'b' (back)
        """
        try:
            self.drone.flip(direction)
            self._log_action(f"performed {direction} flip")
        except Exception as e:
            print(f"Flip error: {str(e)}")

# 1.4: Safety-Enhanced Drone
class SafeDrone(AdvancedDrone):
    """Drone with enhanced safety features"""
    
    def __init__(self, name, drone_interface):
        """Initialize safety-enhanced drone"""
        super().__init__(name, drone_interface)
        self.safety_checks_enabled = True
        self.minimum_battery = 20
    
    def _check_battery(self):
        """Check if battery level is safe"""
        try:
            battery = int(self.drone.get_battery().replace('%', ''))
            return battery > self.minimum_battery
        except:
            return False
    
    def safe_takeoff(self):
        """Execute takeoff with safety checks"""
        if not self.safety_checks_enabled:
            return super().takeoff()
            
        if self._check_battery():
            super().takeoff()
        else:
            print("Takeoff denied: Battery too low")
    
    def safe_mission(self, mission_type: str, size: int):
        """
        Execute mission with safety checks
        
        Args:
            mission_type: 'square' or 'triangle'
            size: Size of pattern in cm
        """
        if not self.safety_checks_enabled:
            if mission_type == "square":
                self.execute_square_mission(size)
            else:
                self.execute_triangle_mission(size)
            return
            
        if self._check_battery():
            if mission_type == "square":
                self.execute_square_mission(size)
            else:
                self.execute_triangle_mission(size)
        else:
            print("Mission denied: Battery too low")

def demonstrate_classes():
    """Demonstrate the usage of different drone classes"""
    
    # Basic Drone Demo
    print("\n=== Basic Drone Demo ===")
    basic = BasicDrone("Basic-1", drone)
    print(basic.get_status())
    basic.takeoff()
    sleep(2)
    basic.land()
    
    # Mission Drone Demo
    print("\n=== Mission Drone Demo ===")
    mission = MissionDrone("Mission-1", drone)
    mission.execute_square_mission(50)  # 50cm sides
    
    # Advanced Drone Demo
    print("\n=== Advanced Drone Demo ===")
    advanced = AdvancedDrone("Advanced-1", drone)
    advanced.takeoff()
    sleep(2)
    advanced.fly_to_point(50, 0, 50, 30)  # Fly to point
    sleep(2)
    advanced.perform_flip('l')  # Left flip
    sleep(2)
    advanced.land()
    
    # Safety Drone Demo
    print("\n=== Safety Drone Demo ===")
    safe = SafeDrone("Safe-1", drone)
    safe.safe_takeoff()
    sleep(2)
    safe.safe_mission("triangle", 60)  # 60cm sides

if __name__ == "__main__":
    try:
        demonstrate_classes()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        drone.land()  # Emergency landing
    except Exception as e:
        print(f"\nProgram error: {str(e)}")
        drone.land()  # Emergency landing