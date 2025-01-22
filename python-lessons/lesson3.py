'''
Decorators in Python

The implementation includes:

Log action decorator for movement tracking
Battery check decorator for safety
Safety check decorator for flight status
Coordinate validation decorator
Two drone classes demonstrating decorator usage
Example usage with actual drone commands
'''


# Import required packages
from drone_teaching_package.simulated_tello import EasyTelloToSimulatedDrone
from drone_teaching_package.real_tello import EasyTelloRealDrone
from datetime import datetime
from time import sleep
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_drone():
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
# LESSON 3: Decorators
# ---------------------------

# 3.1: Basic Action Logging Decorator
def log_action(func):
    """Decorator to log drone actions"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        action_name = func.__name__.replace('_', ' ').title()
        timestamp = datetime.now().strftime("%H:%M:%S")
        logger.info(f"{timestamp} - Drone {self.name}: {action_name}")
        return func(self, *args, **kwargs)
    return wrapper

# 3.2: Battery Check Decorator
def battery_check(min_battery=20):
    """Decorator to check battery level before actions"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            battery = self.drone.get_battery()
            try:
                battery_level = int(battery.replace('%', ''))
                if battery_level < min_battery:
                    raise ValueError(f"Battery too low ({battery_level}%) for {func.__name__}")
                return func(self, *args, **kwargs)
            except ValueError as e:
                logger.error(str(e))
                return None
        return wrapper
    return decorator

# 3.3: Safety Check Decorator
def safety_check(func):
    """Decorator to perform safety checks before flight"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'is_flying'):
            self.is_flying = False
            
        if func.__name__ == 'takeoff' and self.is_flying:
            logger.warning("Already flying - takeoff prevented")
            return None
            
        if func.__name__ != 'takeoff' and not self.is_flying:
            logger.warning("Not flying - command prevented")
            return None
            
        return func(self, *args, **kwargs)
    return wrapper

class DecoratedDrone:
    """Drone class demonstrating decorator usage"""
    
    def __init__(self, name: str, drone_interface):
        self.name = name
        self.drone = drone_interface
        self.is_flying = False
    
    @log_action
    @battery_check(min_battery=20)
    @safety_check
    def takeoff(self):
        """Execute takeoff with all safety checks"""
        self.drone.takeoff()
        self.is_flying = True
    
    @log_action
    @battery_check(min_battery=15)
    @safety_check
    def land(self):
        """Execute landing with all safety checks"""
        self.drone.land()
        self.is_flying = False
    
    @log_action
    @battery_check(min_battery=30)
    @safety_check
    def flip(self, direction: str):
        """Execute flip with safety checks"""
        self.drone.flip(direction)
    
    @log_action
    @battery_check(min_battery=25)
    @safety_check
    def move_sequence(self, moves):
        """Execute a sequence of moves"""
        for move, value in moves:
            if hasattr(self.drone, move):
                getattr(self.drone, move)(value)
                sleep(2)

# Advanced Movement Decorator
def validate_coordinates(func):
    """Decorator to validate coordinate inputs"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            for coord in args:
                if isinstance(coord, (int, float)):
                    if abs(coord) > 500:
                        raise ValueError(f"Coordinate {coord} exceeds safe limit (500)")
            return func(self, *args, **kwargs)
        except ValueError as e:
            logger.error(str(e))
            return None
    return wrapper

class AdvancedDecoratedDrone(DecoratedDrone):
    """Drone with advanced decorated methods"""
    
    @log_action
    @battery_check(min_battery=40)
    @safety_check
    @validate_coordinates
    def go_to_point(self, x: int, y: int, z: int, speed: int):
        """Go to specific point with validation"""
        self.drone.go(x, y, z, speed)
    
    @log_action
    @battery_check(min_battery=50)
    @safety_check
    @validate_coordinates
    def fly_curve(self, x1: int, y1: int, z1: int, 
                  x2: int, y2: int, z2: int, speed: int):
        """Execute curve movement with validation"""
        self.drone.curve(x1, y1, z1, x2, y2, z2, speed)

def demonstrate_decorators():
    """Demonstrate decorated drone operations"""
    
    # Basic decorated drone
    print("\n=== Basic Decorated Drone Demo ===")
    dec_drone = DecoratedDrone("Dec-1", drone)
    
    # Test takeoff and landing
    dec_drone.takeoff()
    sleep(3)
    dec_drone.land()
    
    # Test movement sequence
    moves = [
        ('up', 50),
        ('forward', 30),
        ('cw', 90)
    ]
    dec_drone.takeoff()
    sleep(2)
    dec_drone.move_sequence(moves)
    dec_drone.land()
    
    # Advanced decorated drone
    print("\n=== Advanced Decorated Drone Demo ===")
    adv_drone = AdvancedDecoratedDrone("Adv-1", drone)
    
    # Test coordinated movement
    adv_drone.takeoff()
    sleep(2)
    adv_drone.go_to_point(50, 50, 50, 30)
    sleep(3)
    adv_drone.land()

if __name__ == "__main__":
    try:
        demonstrate_decorators()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        drone.land()
    except Exception as e:
        print(f"\nProgram error: {str(e)}")
        drone.land()