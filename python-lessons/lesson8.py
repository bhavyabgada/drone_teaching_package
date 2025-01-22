'''
Super() in Python

The implementation includes:

Base drone class demonstrating super() usage
Camera drone extending base with super()
Advanced camera drone with additional features
Professional camera drone with advanced features
Demonstration of super() usage with different drone types
'''


# Import required packages
from drone_teaching_package.simulated_tello import EasyTelloToSimulatedDrone
from drone_teaching_package.real_tello import EasyTelloRealDrone
from time import sleep
from datetime import datetime

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

class DroneBase:
    """Base drone class demonstrating super() usage"""
    
    def __init__(self, name: str, drone_interface):
        self.name = name
        self.drone = drone_interface
        self.battery = 100
        self.altitude = 0
        self.is_flying = False
        print(f"DroneBase.__init__: Initialized {name}")
    
    def takeoff(self):
        """Base takeoff method"""
        self.drone.takeoff()
        self.is_flying = True
        self.altitude = 50
        print(f"DroneBase.takeoff: {self.name} taking off")
    
    def land(self):
        """Base landing method"""
        self.drone.land()
        self.is_flying = False
        self.altitude = 0
        print(f"DroneBase.land: {self.name} landing")
    
    def move(self, distance: int):
        """Base movement method"""
        if self.is_flying:
            self.drone.forward(distance)
            print(f"DroneBase.move: {self.name} moving forward {distance}cm")

class CameraDrone(DroneBase):
    """Camera drone extending base with super()"""
    
    def __init__(self, name: str, drone_interface, resolution: str = "HD"):
        super().__init__(name, drone_interface)
        self.resolution = resolution
        self.recording = False
        print(f"CameraDrone.__init__: Added camera capabilities to {name}")
    
    def takeoff(self):
        """Enhanced takeoff with camera check"""
        print(f"CameraDrone.takeoff: Checking camera systems")
        super().takeoff()
        if self.resolution == "HD":
            self.drone.up(30)  # Extra height for better shots
            self.altitude += 30
    
    def land(self):
        """Enhanced landing with camera shutdown"""
        if self.recording:
            self.stop_recording()
        print(f"CameraDrone.land: Securing camera systems")
        super().land()
    
    def start_recording(self):
        """Start camera recording"""
        self.recording = True
        print(f"CameraDrone: Started recording at {self.resolution}")
    
    def stop_recording(self):
        """Stop camera recording"""
        self.recording = False
        print(f"CameraDrone: Stopped recording")

class AdvancedCameraDrone(CameraDrone):
    """Advanced camera drone with additional features"""
    
    def __init__(self, name: str, drone_interface, resolution: str = "4K"):
        super().__init__(name, drone_interface, resolution)
        self.stabilization = True
        self.photo_mode = "auto"
        print(f"AdvancedCameraDrone.__init__: Enhanced {name} with advanced features")
    
    def takeoff(self):
        """Advanced takeoff with stabilization"""
        print(f"AdvancedCameraDrone.takeoff: Initializing stabilization")
        super().takeoff()
        if self.stabilization:
            self.drone.set_speed(20)  # Slower for stability
    
    def orbit_shot(self, radius: int):
        """Execute orbital camera shot"""
        if not self.is_flying:
            super().takeoff()
        
        print(f"AdvancedCameraDrone: Starting orbit shot")
        self.start_recording()
        
        # Execute orbit pattern
        for _ in range(4):
            self.drone.forward(radius)
            sleep(2)
            self.drone.cw(90)
            sleep(2)
        
        self.stop_recording()
        super().land()

class ProCameraDrone(AdvancedCameraDrone):
    """Professional camera drone with advanced features"""
    
    def __init__(self, name: str, drone_interface, resolution: str = "8K"):
        super().__init__(name, drone_interface, resolution)
        self.tracking_mode = "object"
        self.filters = ["HDR", "ND"]
        print(f"ProCameraDrone.__init__: Professional setup complete for {name}")
    
    def takeoff(self):
        """Professional takeoff sequence"""
        print(f"ProCameraDrone.takeoff: Professional pre-flight checks")
        super().takeoff()
        
        # Execute stabilization hover
        self.drone.up(20)
        sleep(2)
        self.drone.down(20)
        sleep(2)
    
    def cinematic_shot(self, height: int, distance: int):
        """Execute cinematic reveal shot"""
        if not self.is_flying:
            super().takeoff()
        
        print("ProCameraDrone: Starting cinematic shot")
        self.start_recording()
        
        # Rise and pull back
        self.drone.up(height)
        sleep(2)
        self.drone.back(distance)
        sleep(2)
        
        self.stop_recording()
        super().land()

def demonstrate_super():
    """Demonstrate super() usage with different drone types"""
    
    # Basic camera drone
    print("\n=== Testing Camera Drone ===")
    camera = CameraDrone("Camera-1", drone)
    camera.takeoff()
    camera.start_recording()
    camera.move(50)
    camera.land()
    
    # Advanced camera drone
    print("\n=== Testing Advanced Camera Drone ===")
    advanced = AdvancedCameraDrone("Advanced-1", drone)
    advanced.orbit_shot(50)
    
    # Professional camera drone
    print("\n=== Testing Pro Camera Drone ===")
    pro = ProCameraDrone("Pro-1", drone)
    pro.cinematic_shot(100, 50)

if __name__ == "__main__":
    try:
        demonstrate_super()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        drone.land()
    except Exception as e:
        print(f"\nProgram error: {str(e)}")
        drone.land()