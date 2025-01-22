'''
Access Modifiers in Python

Implementation includes:

Public attributes/methods for general access
Protected attributes/methods with single underscore
Private attributes/methods with double underscore
Security features with password/key verification
Inheritance demonstrating access modifier behavior
All using actual drone commands
'''


# Import required packages
from drone_teaching_package.simulated_tello import EasyTelloToSimulatedDrone
from drone_teaching_package.real_tello import EasyTelloRealDrone
from datetime import datetime
import time
import hashlib

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

class SecureDrone:
    """Demonstrate access modifiers with drone operations"""
    
    def __init__(self, name: str, drone_interface):
        # Public attributes
        self.name = name
        self.drone = drone_interface
        
        # Protected attributes (single underscore)
        self._model = "Tello-EDU"
        self._firmware_version = "2.0.0"
        self._max_altitude = 500  # cm
        
        # Private attributes (double underscore)
        self.__password = "default_pass123"
        self.__security_key = hashlib.sha256(b"drone_key").hexdigest()
        self.__flight_logs = []

    # Public methods
    def get_drone_info(self):
        """Get public drone information"""
        return {
            "name": self.name,
            "model": self._model,
            "firmware": self._firmware_version
        }

    def execute_flight(self, password: str):
        """Execute a simple flight pattern with password verification"""
        if self.__verify_password(password):
            try:
                self.drone.takeoff()
                time.sleep(2)
                self.drone.up(50)
                time.sleep(2)
                self.drone.land()
                self.__log_flight("Simple flight pattern executed")
                return True
            except Exception as e:
                self.__log_flight(f"Flight error: {str(e)}")
                return False
        return False

    # Protected methods (convention)
    def _check_altitude_limit(self, target_altitude: int) -> bool:
        """Check if target altitude is within limits"""
        return 0 <= target_altitude <= self._max_altitude

    def _update_firmware(self, version: str, key: str):
        """Update firmware version with security key"""
        if self.__verify_security_key(key):
            self._firmware_version = version
            return True
        return False

    # Private methods
    def __verify_password(self, password: str) -> bool:
        """Verify access password"""
        return password == self.__password

    def __verify_security_key(self, key: str) -> bool:
        """Verify security key"""
        return hashlib.sha256(key.encode()).hexdigest() == self.__security_key

    def __log_flight(self, message: str):
        """Log flight operations privately"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__flight_logs.append(f"{timestamp}: {message}")

class EnhancedSecureDrone(SecureDrone):
    """Demonstrate inheritance with access modifiers"""
    
    def __init__(self, name: str, drone_interface):
        super().__init__(name, drone_interface)
        self._enhanced_features = ["obstacle_detection", "night_vision"]
        self.__enhanced_key = "enhanced_123"

    def execute_advanced_flight(self, password: str):
        """Execute advanced flight pattern using parent's methods"""
        if self._check_altitude_limit(100):  # Accessing protected method
            return self.execute_flight(password)  # Accessing public method
        return False

    def get_enhanced_info(self):
        """Get enhanced drone information"""
        basic_info = self.get_drone_info()
        basic_info["enhanced_features"] = self._enhanced_features
        return basic_info

def demonstrate_access_modifiers():
    """Demonstrate access modifiers usage"""
    
    # Create secure drone
    secure_drone = SecureDrone("Secure-1", drone)
    
    # Access public methods and attributes
    print("\nPublic Access:")
    print(secure_drone.name)  # Public attribute
    print(secure_drone.get_drone_info())  # Public method
    
    # Access protected attributes (possible but not recommended)
    print("\nProtected Access:")
    print(secure_drone._model)  # Protected attribute
    
    # Try to access private attributes (will raise AttributeError)
    try:
        print(secure_drone.__password)  # Will fail
    except AttributeError as e:
        print("\nPrivate Access Failed:", str(e))
    
    # Execute flight with password
    print("\nExecute Flight:")
    secure_drone.execute_flight("default_pass123")  # Correct password
    secure_drone.execute_flight("wrong_pass")  # Wrong password
    
    # Create enhanced secure drone
    enhanced_drone = EnhancedSecureDrone("Enhanced-1", drone)
    print("\nEnhanced Drone Info:")
    print(enhanced_drone.get_enhanced_info())

if __name__ == "__main__":
    try:
        demonstrate_access_modifiers()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        drone.land()
    except Exception as e:
        print(f"\nProgram error: {str(e)}")
        drone.land()