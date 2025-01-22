'''
Polymorphism in Python

The implementation includes:

Abstract base class for flying objects
Basic drone implementation
Sports drone with enhanced capabilities
Photo drone with specialized methods
Polymorphic function to fly any drone type
Demonstration of polymorphic behavior
'''


# Import required packages
from drone_teaching_package.simulated_tello import EasyTelloToSimulatedDrone
from drone_teaching_package.real_tello import EasyTelloRealDrone
from abc import ABC, abstractmethod
from time import sleep

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

# Base Abstract Class
class FlyingObject(ABC):
    """Abstract base class for flying objects"""
    
    def __init__(self, name: str):
        self.name = name
        self.altitude = 0
        self.is_flying = False
    
    @abstractmethod
    def takeoff(self):
        """Base takeoff method"""
        pass
    
    @abstractmethod
    def land(self):
        """Base landing method"""
        pass
    
    @abstractmethod
    def move_forward(self, distance: int):
        """Base forward movement method"""
        pass
    
    @abstractmethod
    def rotate(self, degrees: int):
        """Base rotation method"""
        pass

# Implementation Classes
class BasicDrone(FlyingObject):
    """Basic drone implementation"""
    
    def __init__(self, name: str, drone_interface):
        super().__init__(name)
        self.drone = drone_interface
    
    def takeoff(self):
        """Implement drone takeoff"""
        if not self.is_flying:
            self.drone.takeoff()
            self.is_flying = True
            self.altitude = 50
            print(f"{self.name} taking off")
    
    def land(self):
        """Implement drone landing"""
        if self.is_flying:
            self.drone.land()
            self.is_flying = False
            self.altitude = 0
            print(f"{self.name} landing")
    
    def move_forward(self, distance: int):
        """Implement forward movement"""
        if self.is_flying:
            self.drone.forward(distance)
            print(f"{self.name} moving forward {distance}cm")
    
    def rotate(self, degrees: int):
        """Implement rotation"""
        if self.is_flying:
            self.drone.cw(degrees)
            print(f"{self.name} rotating {degrees} degrees")

class SportDrone(BasicDrone):
    """Sports drone with enhanced capabilities"""
    
    def __init__(self, name: str, drone_interface):
        super().__init__(name, drone_interface)
        self.speed = 100  # Maximum speed
        
    def takeoff(self):
        """Override with sporty takeoff"""
        super().takeoff()
        if self.is_flying:
            self.drone.up(100)  # Go higher
            self.altitude = 100
            print(f"{self.name} performing sport takeoff")
    
    def move_forward(self, distance: int):
        """Override with high-speed movement"""
        if self.is_flying:
            self.drone.set_speed(self.speed)
            self.drone.forward(distance)
            print(f"{self.name} racing forward {distance}cm")
    
    def perform_flip(self):
        """Sport-specific method"""
        if self.is_flying and self.altitude >= 100:
            self.drone.flip('f')
            print(f"{self.name} performing flip")

class PhotoDrone(BasicDrone):
    """Drone specialized for photography"""
    
    def __init__(self, name: str, drone_interface):
        super().__init__(name, drone_interface)
        self.speed = 30  # Slower for stability
    
    def takeoff(self):
        """Override with stable takeoff"""
        super().takeoff()
        if self.is_flying:
            self.drone.set_speed(self.speed)
            print(f"{self.name} performing stable takeoff")
    
    def move_forward(self, distance: int):
        """Override with smooth movement"""
        if self.is_flying:
            # Move slower for stability
            self.drone.set_speed(self.speed)
            self.drone.forward(distance)
            print(f"{self.name} smoothly moving forward {distance}cm")
    
    def orbit_point(self, radius: int):
        """Photo-specific method"""
        if self.is_flying:
            # Simulate orbiting by making a square
            for _ in range(4):
                self.drone.forward(radius)
                sleep(2)
                self.drone.cw(90)
                sleep(2)
            print(f"{self.name} completed orbit")

def fly_drone(drone_obj: FlyingObject):
    """Polymorphic function to fly any drone type"""
    drone_obj.takeoff()
    sleep(2)
    drone_obj.move_forward(50)
    sleep(2)
    drone_obj.rotate(90)
    sleep(2)
    drone_obj.land()

def demonstrate_polymorphism():
    """Demonstrate polymorphic behavior"""
    
    # Create different drone types
    basic = BasicDrone("Basic-1", drone)
    sport = SportDrone("Sport-1", drone)
    photo = PhotoDrone("Photo-1", drone)
    
    # Test basic polymorphic behavior
    print("\nTesting Basic Drone:")
    fly_drone(basic)
    
    print("\nTesting Sport Drone:")
    fly_drone(sport)
    sport.perform_flip()
    
    print("\nTesting Photo Drone:")
    fly_drone(photo)
    photo.orbit_point(50)

if __name__ == "__main__":
    try:
        demonstrate_polymorphism()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        drone.land()
    except Exception as e:
        print(f"\nProgram error: {str(e)}")
        drone.land()