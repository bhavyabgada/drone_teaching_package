'''
Complex Missions in Python

The implementation includes:

Complex mission planning and execution
Delivery mission with multiple points
Survey mission with defined area
Search mission with different patterns
Demonstration of complex missions with actual drone commands
'''


# Import required packages
from drone_teaching_package.simulated_tello import EasyTelloToSimulatedDrone
from drone_teaching_package.real_tello import EasyTelloRealDrone
from typing import List, Tuple, Dict
from datetime import datetime
from time import sleep
import math
import json

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

class MissionPlanner:
    """Complex mission planning and execution"""
    
    def __init__(self, drone_interface):
        self.drone = drone_interface
        self.mission_log = []
        self.current_mission = None
        self.battery_threshold = 20
    
    def check_battery(self) -> bool:
        """Verify sufficient battery for mission"""
        try:
            battery = int(self.drone.get_battery().replace('%', ''))
            return battery > self.battery_threshold
        except:
            return False
    
    def log_mission(self, action: str):
        """Log mission actions with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mission_log.append(f"{timestamp}: {action}")
    
    def generate_route(self, waypoints: List[Tuple[int, int, int]]) -> List[Dict]:
        """Generate optimized route through waypoints"""
        route = []
        current_pos = (0, 0, 0)
        
        for point in waypoints:
            x, y, z = point
            dx = x - current_pos[0]
            dy = y - current_pos[1]
            dz = z - current_pos[2]
            
            if dz != 0:
                route.append({"up" if dz > 0 else "down": abs(dz)})
            if dx != 0:
                route.append({"forward" if dx > 0 else "back": abs(dx)})
            if dy != 0:
                route.append({"right" if dy > 0 else "left": abs(dy)})
                
            current_pos = point
            
        return route

    def execute_route(self, route: List[Dict]):
        """Execute planned route"""
        try:
            for move in route:
                for command, value in move.items():
                    if hasattr(self.drone, command):
                        getattr(self.drone, command)(value)
                        self.log_mission(f"Executed {command}({value})")
                        sleep(2)
        except Exception as e:
            self.log_mission(f"Route error: {str(e)}")
            raise

class DeliveryMission(MissionPlanner):
    """Specialized delivery mission planning"""
    
    def __init__(self, drone_interface):
        super().__init__(drone_interface)
        self.delivery_points = []
        self.completed_deliveries = []
    
    def add_delivery(self, point: Tuple[int, int, int], package_id: str):
        """Add delivery point to mission"""
        self.delivery_points.append({
            "location": point,
            "package_id": package_id,
            "status": "pending"
        })
    
    def execute_delivery_mission(self):
        """Execute multi-point delivery mission"""
        if not self.check_battery():
            raise ValueError("Insufficient battery for delivery mission")
            
        try:
            self.drone.takeoff()
            self.log_mission("Started delivery mission")
            
            for delivery in self.delivery_points:
                point = delivery["location"]
                route = self.generate_route([point])
                
                self.execute_route(route)
                self.log_mission(f"Delivered package {delivery['package_id']}")
                delivery["status"] = "completed"
                self.completed_deliveries.append(delivery)
                
                # Return to home between deliveries
                home_route = self.generate_route([(0, 0, 50)])
                self.execute_route(home_route)
                
            self.drone.land()
            self.log_mission("Completed delivery mission")
            
        except Exception as e:
            self.log_mission(f"Delivery mission failed: {str(e)}")
            self.drone.land()
            raise

class SurveyMission(MissionPlanner):
    """Aerial survey mission planning"""
    
    def __init__(self, drone_interface):
        super().__init__(drone_interface)
        self.survey_area = []
        self.coverage_spacing = 50  # cm between survey lines
    
    def set_survey_area(self, corners: List[Tuple[int, int, int]]):
        """Define area to survey"""
        if len(corners) != 4:
            raise ValueError("Survey area must have 4 corners")
        self.survey_area = corners
    
    def generate_survey_pattern(self) -> List[Tuple[int, int, int]]:
        """Generate survey waypoints"""
        if not self.survey_area:
            raise ValueError("Survey area not defined")
            
        waypoints = []
        x_min = min(p[0] for p in self.survey_area)
        x_max = max(p[0] for p in self.survey_area)
        y_min = min(p[1] for p in self.survey_area)
        y_max = max(p[1] for p in self.survey_area)
        altitude = self.survey_area[0][2]
        
        # Generate parallel survey lines
        current_y = y_min
        direction = 1
        
        while current_y <= y_max:
            if direction == 1:
                waypoints.append((x_min, current_y, altitude))
                waypoints.append((x_max, current_y, altitude))
            else:
                waypoints.append((x_max, current_y, altitude))
                waypoints.append((x_min, current_y, altitude))
                
            current_y += self.coverage_spacing
            direction *= -1
            
        return waypoints
    
    def execute_survey_mission(self):
        """Execute survey mission"""
        if not self.check_battery():
            raise ValueError("Insufficient battery for survey mission")
            
        try:
            waypoints = self.generate_survey_pattern()
            route = self.generate_route(waypoints)
            
            self.drone.takeoff()
            self.log_mission("Started survey mission")
            
            self.execute_route(route)
            
            self.drone.land()
            self.log_mission("Completed survey mission")
            
        except Exception as e:
            self.log_mission(f"Survey mission failed: {str(e)}")
            self.drone.land()
            raise

class SearchMission(MissionPlanner):
    """Search and rescue mission planning"""
    
    def __init__(self, drone_interface):
        super().__init__(drone_interface)
        self.search_patterns = {
            "spiral": self._generate_spiral,
            "grid": self._generate_grid,
            "expanding": self._generate_expanding_square
        }
    
    def _generate_spiral(self, size: int, spacing: int) -> List[Tuple[int, int, int]]:
        """Generate spiral search pattern"""
        waypoints = []
        x, y = 0, 0
        dx, dy = spacing, 0
        steps = size // spacing
        
        for _ in range(steps):
            if len(waypoints) == 0:
                waypoints.append((x, y, 50))
            
            if abs(dx) > abs(dy):
                dx = dx if dx < 0 else spacing
                dx = -dx if dx > 0 else spacing
            else:
                dy = dy if dy < 0 else spacing
                dy = -dy if dy > 0 else spacing
                
            x += dx
            y += dy
            waypoints.append((x, y, 50))
            
        return waypoints
    
    def _generate_grid(self, size: int, spacing: int) -> List[Tuple[int, int, int]]:
        """Generate grid search pattern"""
        waypoints = []
        for x in range(0, size + spacing, spacing):
            for y in range(0, size + spacing, spacing):
                waypoints.append((x, y, 50))
        return waypoints
    
    def _generate_expanding_square(self, size: int, spacing: int) -> List[Tuple[int, int, int]]:
        """Generate expanding square pattern"""
        waypoints = [(0, 0, 50)]
        current_size = spacing
        
        while current_size <= size:
            x, y = waypoints[-1][0], waypoints[-1][1]
            
            # Add four corners of expanding square
            waypoints.extend([
                (x + current_size, y, 50),
                (x + current_size, y + current_size, 50),
                (x, y + current_size, 50),
                (x, y, 50)
            ])
            
            current_size += spacing
            
        return waypoints
    
    def execute_search_mission(self, pattern: str, size: int, spacing: int):
        """Execute search pattern mission"""
        if pattern not in self.search_patterns:
            raise ValueError(f"Invalid pattern. Choose from: {list(self.search_patterns.keys())}")
            
        if not self.check_battery():
            raise ValueError("Insufficient battery for search mission")
            
        try:
            waypoints = self.search_patterns[pattern](size, spacing)
            route = self.generate_route(waypoints)
            
            self.drone.takeoff()
            self.log_mission(f"Started {pattern} search mission")
            
            self.execute_route(route)
            
            self.drone.land()
            self.log_mission("Completed search mission")
            
        except Exception as e:
            self.log_mission(f"Search mission failed: {str(e)}")
            self.drone.land()
            raise

def demonstrate_complex_missions():
    """Demonstrate various complex missions"""
    
    # Delivery Mission Demo
    delivery = DeliveryMission(drone)
    delivery.add_delivery((100, 0, 50), "PKG001")
    delivery.add_delivery((0, 100, 50), "PKG002")
    delivery.execute_delivery_mission()
    
    # Survey Mission Demo
    survey = SurveyMission(drone)
    survey.set_survey_area([
        (0, 0, 50),
        (100, 0, 50),
        (100, 100, 50),
        (0, 100, 50)
    ])
    survey.execute_survey_mission()
    
    # Search Mission Demo
    search = SearchMission(drone)
    search.execute_search_mission("spiral", 200, 50)

if __name__ == "__main__":
    try:
        demonstrate_complex_missions()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        drone.land()
    except Exception as e:
        print(f"\nProgram error: {str(e)}")
        drone.land()