'''
Inheritance in Python

The implementation includes:

Base drone class with fundamental capabilities
Delivery drone with cargo handling
Rescue drone with search pattern execution
Racing drone with race mode and lap timing
Demonstration of inheritance and polymorphism
'''


# Import required packages
from drone_teaching_package.simulated_tello import EasyTelloToSimulatedDrone
from drone_teaching_package.real_tello import EasyTelloRealDrone
from time import sleep
from typing import List, Dict

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

class BaseDrone:
    """Base drone class with fundamental capabilities"""
    
    def __init__(self, name: str, drone_interface):
        self.name = name
        self.drone = drone_interface
        self.is_flying = False
        self.battery_level = 100
        self.flight_log = []
    
    def takeoff(self):
        """Base takeoff method"""
        self.drone.takeoff()
        self.is_flying = True
        self._log_action("Takeoff")
    
    def land(self):
        """Base landing method"""
        self.drone.land()
        self.is_flying = False
        self._log_action("Land")
    
    def move_forward(self, distance: int):
        """Base forward movement"""
        self.drone.forward(distance)
        self._log_action(f"Forward {distance}cm")
    
    def _log_action(self, action: str):
        """Protected logging method"""
        self.flight_log.append(action)
    
    def get_status(self) -> Dict:
        """Get drone status"""
        return {
            "name": self.name,
            "flying": self.is_flying,
            "battery": self.drone.get_battery()
        }

class DeliveryDrone(BaseDrone):
    """Specialized drone for delivery operations"""
    
    def __init__(self, name: str, drone_interface):
        super().__init__(name, drone_interface)
        self.cargo_weight = 0
        self.max_cargo = 200  # grams
        self.delivery_log = []
    
    def load_cargo(self, weight: int) -> bool:
        """Load cargo with weight check"""
        if weight <= self.max_cargo:
            self.cargo_weight = weight
            self._log_action(f"Loaded {weight}g cargo")
            return True
        return False
    
    def deliver_package(self, x: int, y: int, z: int):
        """Execute delivery sequence"""
        if not self.cargo_weight:
            return False
        
        self.takeoff()
        sleep(2)
        self.drone.go(x, y, z, 30)
        sleep(2)
        
        # Simulate package drop
        self.cargo_weight = 0
        self.delivery_log.append(f"Delivered to ({x},{y},{z})")
        self._log_action("Package delivered")
        
        self.return_home()
        return True
    
    def return_home(self):
        """Return to starting position"""
        self.drone.go(0, 0, 50, 30)
        sleep(2)
        self.land()

class RescueDrone(BaseDrone):
    """Specialized drone for search and rescue"""
    
    def __init__(self, name: str, drone_interface):
        super().__init__(name, drone_interface)
        self.search_patterns = {
            "grid": [(0,0), (10,0), (10,10), (0,10)],
            "spiral": [(0,0), (10,10), (20,20), (30,30)]
        }
        self.search_log = []
    
    def execute_search_pattern(self, pattern: str):
        """Execute predefined search pattern"""
        if pattern not in self.search_patterns:
            return False
        
        self.takeoff()
        sleep(2)
        
        for x, y in self.search_patterns[pattern]:
            self.drone.go(x, y, 50, 30)
            sleep(2)
            self._scan_area()
        
        self.land()
        return True
    
    def _scan_area(self):
        """Protected method for area scanning"""
        self.drone.cw(360)  # Full rotation scan
        self.search_log.append("Area scanned")
        self._log_action("Scan complete")

class RacingDrone(BaseDrone):
    """Specialized drone for racing"""
    
    def __init__(self, name: str, drone_interface):
        super().__init__(name, drone_interface)
        self.max_speed = 100
        self.race_mode = False
        self.lap_times = []
    
    def enable_race_mode(self):
        """Enable racing configuration"""
        self.race_mode = True
        self.drone.set_speed(self.max_speed)
        self._log_action("Race mode enabled")
    
    def execute_race_lap(self, checkpoints: List[tuple]):
        """Execute racing lap through checkpoints"""
        start_time = time.time()
        
        self.takeoff()
        sleep(1)
        
        for x, y, z in checkpoints:
            self.drone.go(x, y, z, self.max_speed)
            sleep(1)
        
        self.land()
        lap_time = time.time() - start_time
        self.lap_times.append(lap_time)
        self._log_action(f"Lap completed in {lap_time:.2f}s")

def demonstrate_inheritance():
    """Demonstrate inheritance features"""
    
    # Delivery drone demo
    delivery = DeliveryDrone("Delivery-1", drone)
    if delivery.load_cargo(150):
        delivery.deliver_package(100, 100, 50)
    
    # Rescue drone demo
    rescue = RescueDrone("Rescue-1", drone)
    rescue.execute_search_pattern("grid")
    
    # Racing drone demo
    racing = RacingDrone("Racing-1", drone)
    racing.enable_race_mode()
    racing.execute_race_lap([(50,0,50), (50,50,50), (0,50,50)])

if __name__ == "__main__":
    try:
        demonstrate_inheritance()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        drone.land()
    except Exception as e:
        print(f"\nProgram error: {str(e)}")
        drone.land()