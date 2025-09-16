from enum import Enum
from typing import List, Set
import heapq

class ElevatorState(Enum):
    IDLE = "idle"
    MOVING_UP = "moving_up"
    MOVING_DOWN = "moving_down"
    DOOR_OPEN = "door_open"

class Direction(Enum):
    UP = 1
    DOWN = 0
    IDLE = -1

class OptimizedElevator:
    def __init__(self, num_floors: int = 10, starting_floor: int = 1):
        self.num_floors = num_floors
        self.current_floor = starting_floor
        self.state = ElevatorState.IDLE
        self.direction = Direction.IDLE

        # Use sets for O(1) lookup and heaps for efficient scheduling
        self.up_requests = []  # min heap for upward requests
        self.down_requests = []  # max heap (negated) for downward requests
        self.current_requests = set()  # All active requests

    def add_floor_request(self, floor: int) -> bool:
        """Add a floor request with validation"""
        if not self._is_valid_floor(floor):
            return False

        if floor == self.current_floor:
            return True  # Already at requested floor

        self.current_requests.add(floor)

        if floor > self.current_floor:
            heapq.heappush(self.up_requests, floor)
        else:
            heapq.heappush(self.down_requests, -floor)  # Negate for max heap behavior

        return True

    def add_multiple_requests(self, floors: List[int]) -> List[bool]:
        """Add multiple floor requests"""
        return [self.add_floor_request(floor) for floor in floors]

    def _is_valid_floor(self, floor: int) -> bool:
        """Validate floor number"""
        return 1 <= floor <= self.num_floors

    def _get_next_floor(self) -> int:
        """Get next floor using SCAN algorithm"""
        if self.direction == Direction.UP and self.up_requests:
            return heapq.heappop(self.up_requests)
        elif self.direction == Direction.DOWN and self.down_requests:
            return -heapq.heappop(self.down_requests)
        elif self.up_requests:
            self.direction = Direction.UP
            return heapq.heappop(self.up_requests)
        elif self.down_requests:
            self.direction = Direction.DOWN
            return -heapq.heappop(self.down_requests)
        else:
            self.direction = Direction.IDLE
            return self.current_floor

    def process_requests(self) -> List[str]:
        """Process all requests and return movement log"""
        if not self.current_requests:
            return ["No requests to process"]

        movements = []

        while self.current_requests:
            next_floor = self._get_next_floor()

            if next_floor == self.current_floor:
                break

            # Update state based on movement
            if next_floor > self.current_floor:
                self.state = ElevatorState.MOVING_UP
                self.direction = Direction.UP
            else:
                self.state = ElevatorState.MOVING_DOWN
                self.direction = Direction.DOWN

            movements.append(f"Moving from floor {self.current_floor} to floor {next_floor}")
            self.current_floor = next_floor

            # Remove completed request
            self.current_requests.discard(next_floor)

            # Simulate door operation
            self.state = ElevatorState.DOOR_OPEN
            movements.append(f"Arrived at floor {self.current_floor} - Doors open")

        self.state = ElevatorState.IDLE
        self.direction = Direction.IDLE
        movements.append("All requests completed - Elevator idle")

        return movements

    def get_status(self) -> dict:
        """Get current elevator status"""
        return {
            "current_floor": self.current_floor,
            "state": self.state.value,
            "direction": self.direction.value,
            "pending_requests": sorted(list(self.current_requests)),
            "up_queue": sorted(self.up_requests),
            "down_queue": sorted([-x for x in self.down_requests], reverse=True)
        }

    def clear_requests(self):
        """Clear all pending requests"""
        self.current_requests.clear()
        self.up_requests.clear()
        self.down_requests.clear()
        self.state = ElevatorState.IDLE
        self.direction = Direction.IDLE

def demonstrate_elevator():
    """Demonstrate the optimized elevator functionality"""
    print("=== Optimized Elevator Demonstration ===\n")

    # Test with 4 floors
    elevator = OptimizedElevator(num_floors=4, starting_floor=1)

    print("Test 1: Multiple floor requests")
    print("Starting at floor 1, requesting floors [3, 2, 4, 1]")

    elevator.add_multiple_requests([3, 2, 4, 1])
    print("Status after adding requests:", elevator.get_status())

    movements = elevator.process_requests()
    for movement in movements:
        print(f"  {movement}")

    print(f"Final status: {elevator.get_status()}\n")

    # Test with 10 floors
    print("Test 2: 10-floor elevator")
    big_elevator = OptimizedElevator(num_floors=10, starting_floor=5)

    print("Starting at floor 5, requesting floors [8, 3, 10, 1, 6]")
    big_elevator.add_multiple_requests([8, 3, 10, 1, 6])

    movements = big_elevator.process_requests()
    for movement in movements:
        print(f"  {movement}")

    print(f"Final status: {big_elevator.get_status()}\n")

    # Test error handling
    print("Test 3: Error handling")
    test_elevator = OptimizedElevator(num_floors=4)

    results = test_elevator.add_multiple_requests([1, 5, 3, 0, 2])
    print("Request results for [1, 5, 3, 0, 2]:", results)
    print("Valid requests processed:", test_elevator.get_status()["pending_requests"])

if __name__ == "__main__":
    demonstrate_elevator()