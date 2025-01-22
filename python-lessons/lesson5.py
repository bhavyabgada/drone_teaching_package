'''
Properties in Python
Setters and Getters

The implementation includes:

Basic properties for altitude, speed, battery, and position
Enhanced properties for orientation and flight mode
Demonstration of property usage with actual drone commands
'''


# Import required packages
from drone_teaching_package.simulated_tello import EasyTelloToSimulatedDrone
from drone_teaching_package.real_tello import EasyTelloRealDrone
from time import sleep
from typing import Tuple

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

class DroneWithProperties:
    """Demonstrate property usage with drone control"""
    
    def __init__(self, name: str, drone_interface):
        self.name = name
        self.drone = drone_interface
        self._altitude = 0
        self._speed = 10
        self._battery = 100
        self._position = (0, 0, 0)
        self._is_flying = False
    
    @property
    def altitude(self) -> int:
        """Get current altitude"""
        return self._altitude
    
    @altitude.setter
    def altitude(self, value: int):
        """
        Set drone altitude with safety checks
        Args:
            value: Target altitude in cm
        """
        if not 0 <= value <= 500:
            raise ValueError("Altitude must be between 0 and 500 cm")
        
        if self._is_flying:
            current = self._altitude
            if value > current:
                self.drone.up(value - current)
            elif value < current:
                self.drone.down(current - value)
            sleep(2)
            
        self._altitude = value
    
    @property
    def speed(self) -> int:
        """Get current speed"""
        return self._speed
    
    @speed.setter
    def speed(self, value: int):
        """
        Set drone speed with limits
        Args:
            value: Speed in cm/s
        """
        if not 10 <= value <= 100:
            raise ValueError("Speed must be between 10 and 100 cm/s")
        self.drone.set_speed(value)
        self._speed = value
    
    @property
    def battery(self) -> int:
        """Get current battery level"""
        try:
            level = self.drone.get_battery()
            self._battery = int(level.replace('%', ''))
        except:
            pass
        return self._battery
    
    @property
    def position(self) -> Tuple[int, int, int]:
        """Get current position"""
        return self._position
    
    @position.setter
    def position(self, coords: Tuple[int, int, int]):
        """
        Set drone position
        Args:
            coords: (x, y, z) coordinates
        """
        x, y, z = coords
        if not all(-500 <= c <= 500 for c in (x, y, z)):
            raise ValueError("Coordinates must be between -500 and 500")
        
        if self._is_flying:
            self.drone.go(x, y, z, self._speed)
            sleep(2)
            
        self._position = coords
    
    def takeoff(self):
        """Safe takeoff implementation"""
        if not self._is_flying and self.battery > 20:
            self.drone.takeoff()
            self._is_flying = True
            self._altitude = 50  # Default takeoff height
    
    def land(self):
        """Safe landing implementation"""
        if self._is_flying:
            self.drone.land()
            self._is_flying = False
            self._altitude = 0

class EnhancedDroneProperties(DroneWithProperties):
    """Enhanced drone with additional properties"""
    
    def __init__(self, name: str, drone_interface):
        super().__init__(name, drone_interface)
        self._orientation = 0  # Degrees from north
        self._flight_mode = "normal"
    
    @property
    def orientation(self) -> int:
        """Get current orientation in degrees"""
        return self._orientation
    
    @orientation.setter
    def orientation(self, degrees: int):
        """
        Set drone orientation
        Args:
            degrees: Target orientation (0-360)
        """
        degrees = degrees % 360
        if self._is_flying:
            current = self._orientation
            diff = (degrees - current) % 360
            
            if diff <= 180:
                self.drone.cw(diff)
            else:
                self.drone.ccw(360 - diff)
            sleep(2)
            
        self._orientation = degrees
    
    @property
    def flight_mode(self) -> str:
        """Get current flight mode"""
        return self._flight_mode
    
    @flight_mode.setter
    def flight_mode(self, mode: str):
        """
        Set flight mode with validation
        Args:
            mode: Flight mode ('normal', 'sport', 'safe')
        """
        valid_modes = {'normal', 'sport', 'safe'}
        if mode not in valid_modes:
            raise ValueError(f"Mode must be one of {valid_modes}")
        
        if mode == 'sport':
            self.speed = 100
        elif mode == 'safe':
            self.speed = 30
        else:
            self.speed = 50
            
        self._flight_mode = mode

def demonstrate_properties():
    """Demonstrate property usage"""
    
    # Basic properties
    drone_props = DroneWithProperties("Props-1", drone)
    
    # Test altitude control
    drone_props.takeoff()
    drone_props.altitude = 100
    print(f"Current altitude: {drone_props.altitude}")
    
    # Test position control
    drone_props.position = (50, 0, 100)
    print(f"Current position: {drone_props.position}")
    
    # Test speed control
    drone_props.speed = 50
    print(f"Current speed: {drone_props.speed}")
    
    drone_props.land()
    
    # Enhanced properties
    enhanced = EnhancedDroneProperties("Enhanced-1", drone)
    enhanced.takeoff()
    
    # Test orientation
    enhanced.orientation = 90
    print(f"Current orientation: {enhanced.orientation}")
    
    # Test flight mode
    enhanced.flight_mode = 'sport'
    print(f"Current mode: {enhanced.flight_mode}")
    print(f"Speed in sport mode: {enhanced.speed}")
    
    enhanced.land()

if __name__ == "__main__":
    try:
        demonstrate_properties()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        drone.land()
    except Exception as e:
        print(f"\nProgram error: {str(e)}")
        drone.land()