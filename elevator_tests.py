import unittest
from optimized_elevator import OptimizedElevator, ElevatorState, Direction

class TestOptimizedElevator(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.elevator = OptimizedElevator(num_floors=4, starting_floor=1)
        self.big_elevator = OptimizedElevator(num_floors=10, starting_floor=5)

    def test_initialization(self):
        """Test elevator initialization"""
        self.assertEqual(self.elevator.current_floor, 1)
        self.assertEqual(self.elevator.num_floors, 4)
        self.assertEqual(self.elevator.state, ElevatorState.IDLE)
        self.assertEqual(self.elevator.direction, Direction.IDLE)

    def test_valid_floor_requests(self):
        """Test adding valid floor requests"""
        self.assertTrue(self.elevator.add_floor_request(3))
        self.assertTrue(self.elevator.add_floor_request(2))
        self.assertTrue(self.elevator.add_floor_request(4))

        status = self.elevator.get_status()
        self.assertEqual(set(status["pending_requests"]), {2, 3, 4})

    def test_invalid_floor_requests(self):
        """Test handling of invalid floor requests"""
        self.assertFalse(self.elevator.add_floor_request(0))  # Below range
        self.assertFalse(self.elevator.add_floor_request(5))  # Above range
        self.assertFalse(self.elevator.add_floor_request(-1)) # Negative

        # Should have no pending requests
        self.assertEqual(len(self.elevator.get_status()["pending_requests"]), 0)

    def test_same_floor_request(self):
        """Test requesting current floor"""
        result = self.elevator.add_floor_request(1)  # Currently on floor 1
        self.assertTrue(result)
        # Should not add to pending requests
        self.assertEqual(len(self.elevator.get_status()["pending_requests"]), 0)

    def test_multiple_requests(self):
        """Test adding multiple requests at once"""
        floors = [2, 4, 3, 1]
        results = self.elevator.add_multiple_requests(floors)

        # Floor 1 should return True but not be added (current floor)
        # Floors 2, 3, 4 should be added
        expected_pending = {2, 3, 4}
        actual_pending = set(self.elevator.get_status()["pending_requests"])
        self.assertEqual(actual_pending, expected_pending)

    def test_elevator_movement_up(self):
        """Test upward movement"""
        self.elevator.add_multiple_requests([2, 4, 3])
        movements = self.elevator.process_requests()

        # Should visit floors in order: 2, 3, 4
        self.assertEqual(self.elevator.current_floor, 4)
        self.assertEqual(self.elevator.state, ElevatorState.IDLE)

        # Check movement log contains expected moves
        movement_text = " ".join(movements)
        self.assertIn("floor 1 to floor 2", movement_text)
        self.assertIn("floor 2 to floor 3", movement_text)
        self.assertIn("floor 3 to floor 4", movement_text)

    def test_elevator_movement_down(self):
        """Test downward movement"""
        # Start at floor 4
        self.elevator.current_floor = 4
        self.elevator.add_multiple_requests([3, 1, 2])
        movements = self.elevator.process_requests()

        # Should visit floors in order: 3, 2, 1
        self.assertEqual(self.elevator.current_floor, 1)

        movement_text = " ".join(movements)
        self.assertIn("floor 4 to floor 3", movement_text)
        self.assertIn("floor 3 to floor 2", movement_text)
        self.assertIn("floor 2 to floor 1", movement_text)

    def test_mixed_direction_requests(self):
        """Test requests in both directions"""
        # Start at floor 2
        self.elevator.current_floor = 2
        self.elevator.add_multiple_requests([4, 1, 3])
        movements = self.elevator.process_requests()

        # Should complete all requests efficiently
        self.assertEqual(len(self.elevator.get_status()["pending_requests"]), 0)

    def test_clear_requests(self):
        """Test clearing all requests"""
        self.elevator.add_multiple_requests([2, 3, 4])
        self.assertEqual(len(self.elevator.get_status()["pending_requests"]), 3)

        self.elevator.clear_requests()
        self.assertEqual(len(self.elevator.get_status()["pending_requests"]), 0)
        self.assertEqual(self.elevator.state, ElevatorState.IDLE)

    def test_large_elevator(self):
        """Test 10-floor elevator functionality"""
        floors = [8, 3, 10, 1, 6]
        self.big_elevator.add_multiple_requests(floors)

        status = self.big_elevator.get_status()
        self.assertEqual(set(status["pending_requests"]), set(floors))

        movements = self.big_elevator.process_requests()
        self.assertEqual(len(self.big_elevator.get_status()["pending_requests"]), 0)

    def test_status_reporting(self):
        """Test status reporting functionality"""
        self.elevator.add_multiple_requests([3, 2, 4])
        status = self.elevator.get_status()

        required_keys = ["current_floor", "state", "direction", "pending_requests", "up_queue", "down_queue"]
        for key in required_keys:
            self.assertIn(key, status)

    def test_edge_cases(self):
        """Test edge cases"""
        # Empty request list
        movements = self.elevator.process_requests()
        self.assertEqual(movements, ["No requests to process"])

        # Duplicate requests
        self.elevator.add_floor_request(3)
        self.elevator.add_floor_request(3)  # Duplicate

        status = self.elevator.get_status()
        self.assertEqual(status["pending_requests"], [3])  # Should only appear once

def run_performance_test():
    """Test performance with large number of requests"""
    print("\n=== Performance Test ===")
    import time

    elevator = OptimizedElevator(num_floors=100, starting_floor=50)

    # Add 1000 random requests
    import random
    floors = [random.randint(1, 100) for _ in range(1000)]

    start_time = time.time()
    results = elevator.add_multiple_requests(floors)
    add_time = time.time() - start_time

    start_time = time.time()
    movements = elevator.process_requests()
    process_time = time.time() - start_time

    print(f"Added 1000 requests in {add_time:.4f} seconds")
    print(f"Processed all requests in {process_time:.4f} seconds")
    print(f"Total movements: {len([m for m in movements if 'Moving from' in m])}")

if __name__ == "__main__":
    # Run unit tests
    print("Running Unit Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)

    # Run performance test
    run_performance_test()