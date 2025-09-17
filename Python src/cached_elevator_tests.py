import unittest
import time
import tempfile
import os
import random
from cached_elevator import CachedElevator, ElevatorCache, ElevatorState

class TestElevatorCache(unittest.TestCase):

    def setUp(self):
        self.cache = ElevatorCache()

    def test_frequency_caching(self):
        """Test floor frequency caching"""
        # Record multiple requests to floor 5
        for _ in range(5):
            self.cache.record_request(1, 5)

        # Record fewer requests to other floors
        self.cache.record_request(1, 3)
        self.cache.record_request(1, 7)

        most_frequent = self.cache.get_most_frequent_floors(3)
        self.assertEqual(most_frequent[0][0], 5)  # Floor 5 should be most frequent
        self.assertEqual(most_frequent[0][1], 5)  # With 5 requests

    def test_time_based_patterns(self):
        """Test time-based pattern recognition"""
        # Simulate morning rush hour (9 AM)
        morning_time = time.time() - (time.time() % 86400) + 9 * 3600

        for _ in range(3):
            self.cache.record_request(1, 8, timestamp=morning_time)
            self.cache.record_request(1, 9, timestamp=morning_time)

        # Predict at 9 AM should suggest popular morning floors
        prediction = self.cache.predict_next_request(1, morning_time)
        self.assertIn(prediction, [8, 9])

    def test_user_patterns(self):
        """Test user-specific pattern caching"""
        # User "alice" always goes to floor 7
        for _ in range(5):
            self.cache.record_request(1, 7, user_id="alice")

        # Check user pattern was recorded
        self.assertEqual(self.cache.user_patterns["alice"][7], 5)

    def test_idle_position_optimization(self):
        """Test optimal idle position calculation"""
        # Record multiple arrivals at floor 5
        for _ in range(10):
            self.cache.update_idle_position_stats(5)

        # Record fewer at other floors
        self.cache.update_idle_position_stats(3)
        self.cache.update_idle_position_stats(7)

        optimal_floor = self.cache.get_optimal_idle_position()
        self.assertEqual(optimal_floor, 5)

    def test_prediction_validation(self):
        """Test prediction accuracy tracking"""
        # Make some predictions and validate them
        self.cache.predictions_made = 10
        self.cache.predictions_correct = 8

        performance = self.cache.get_cache_performance()
        self.assertEqual(performance['prediction_accuracy'], 0.8)

class TestCachedElevator(unittest.TestCase):

    def setUp(self):
        self.elevator = CachedElevator(num_floors=10, starting_floor=1)

    def test_cache_enabled_initialization(self):
        """Test elevator initializes with caching enabled"""
        self.assertTrue(self.elevator.enable_caching)
        self.assertIsNotNone(self.elevator.cache)

    def test_cache_disabled_initialization(self):
        """Test elevator can be initialized without caching"""
        elevator = CachedElevator(num_floors=10, enable_caching=False)
        self.assertFalse(elevator.enable_caching)
        self.assertIsNone(elevator.cache)

    def test_request_recording(self):
        """Test that requests are properly recorded in cache"""
        self.elevator.add_floor_request(5, user_id="test_user", from_floor=1)

        # Check cache recorded the request
        self.assertEqual(self.elevator.cache.floor_frequency[5], 1)
        self.assertEqual(self.elevator.cache.floor_pair_frequency[(1, 5)], 1)

    def test_cache_hit_miss_tracking(self):
        """Test cache hit/miss statistics"""
        initial_hits = self.elevator.cache.cache_hits

        # Valid request should be a cache hit
        self.elevator.add_floor_request(5)
        self.assertEqual(self.elevator.cache.cache_hits, initial_hits + 1)

        # Invalid request should be a cache miss
        initial_misses = self.elevator.cache.cache_misses
        self.elevator.add_floor_request(15)  # Invalid floor
        self.assertEqual(self.elevator.cache.cache_misses, initial_misses + 1)

    def test_pre_positioning(self):
        """Test pre-positioning functionality"""
        # Set up conditions for pre-positioning
        self.elevator.last_request_time = time.time() - 35  # 35 seconds ago
        self.elevator.current_floor = 1

        # Simulate some cached patterns favoring floor 5
        for _ in range(10):
            self.elevator.cache.update_idle_position_stats(5)

        # Process should trigger pre-positioning
        movements = self.elevator.process_requests()
        self.assertIn("Pre-positioned", movements[0])
        self.assertEqual(self.elevator.current_floor, 5)

    def test_energy_tracking(self):
        """Test energy usage tracking"""
        initial_movements = self.elevator.total_movements

        # Make requests that require movement
        self.elevator.add_floor_request(5)
        self.elevator.add_floor_request(8)
        self.elevator.process_requests()

        # Should have tracked movements
        self.assertGreater(self.elevator.total_movements, initial_movements)

    def test_prediction_integration(self):
        """Test prediction integration in status"""
        # Add some patterns to cache
        for _ in range(5):
            self.elevator.cache.record_request(1, 7)

        status = self.elevator.get_status()

        # Status should include cache information
        self.assertIn('cache_performance', status)
        self.assertIn('most_frequent_floors', status)
        self.assertIn('predicted_next_floor', status)

    def test_comprehensive_caching_workflow(self):
        """Test a complete caching workflow"""
        # Simulate daily usage patterns
        requests = [
            (1, 8, "employee1"),  # Morning rush
            (1, 9, "employee2"),
            (1, 8, "employee1"),  # Repeat user
            (8, 1, "employee1"),  # Return trip
            (9, 1, "employee2"),
        ]

        for from_floor, to_floor, user in requests:
            self.elevator.current_floor = from_floor
            self.elevator.add_floor_request(to_floor, user, from_floor)
            self.elevator.process_requests()
            self.elevator.clear_requests()

        # Check patterns were learned
        status = self.elevator.get_status()
        cache_perf = status['cache_performance']

        self.assertGreater(cache_perf['total_requests_cached'], 0)
        self.assertGreater(len(status['most_frequent_floors']), 0)

    def test_cache_data_persistence(self):
        """Test saving and loading cache data"""
        # Add some data to cache
        for i in range(5):
            self.elevator.add_floor_request(7, f"user_{i}", 1)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name

        try:
            self.elevator.save_cache_data(temp_filename)

            # Verify file was created and contains data
            self.assertTrue(os.path.exists(temp_filename))

            with open(temp_filename, 'r') as f:
                import json
                data = json.load(f)

            self.assertIn('floor_frequency', data)
            self.assertIn('cache_performance', data)

        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

class TestCachingPerformance(unittest.TestCase):
    """Test caching system performance improvements"""

    def test_large_scale_caching(self):
        """Test caching with large number of requests"""
        elevator = CachedElevator(num_floors=50, starting_floor=1)

        # Simulate 1000 requests
        import random
        requests = [(random.randint(1, 50), random.randint(1, 50)) for _ in range(1000)]

        start_time = time.time()
        for from_floor, to_floor in requests:
            elevator.current_floor = from_floor
            elevator.add_floor_request(to_floor, f"user_{random.randint(1, 100)}", from_floor)

        processing_time = time.time() - start_time

        # Should process quickly (less than 1 second for 1000 requests)
        self.assertLess(processing_time, 1.0)

        # Cache should have meaningful data
        status = elevator.get_status()
        self.assertGreater(status['cache_performance']['total_requests_cached'], 900)

    def test_memory_efficiency(self):
        """Test that cache doesn't grow unboundedly"""
        elevator = CachedElevator(num_floors=10)

        # Add more requests than max_history
        for i in range(1500):  # More than default max_history of 1000
            elevator.add_floor_request(random.randint(1, 10))

        # Recent requests should be limited
        self.assertLessEqual(len(elevator.cache.recent_requests), 1000)

def run_caching_benchmarks():
    """Run performance benchmarks for caching system"""
    print("\n=== Caching Performance Benchmarks ===")

    # Test 1: Request processing speed
    elevator = CachedElevator(num_floors=100)

    start_time = time.time()
    for _ in range(10000):
        floor = random.randint(1, 100)
        elevator.add_floor_request(floor)

    request_time = time.time() - start_time
    print(f"10,000 requests processed in {request_time:.4f} seconds")

    # Test 2: Realistic prediction accuracy test
    print("\n=== Prediction Accuracy Test ===")
    elevator = CachedElevator(num_floors=10)

    # Build realistic office building patterns
    print("Building usage patterns...")

    # Morning rush: lobby to office floors
    morning_pattern = [(1, floor) for floor in [7, 8, 9] for _ in range(20)]
    # Lunch: office floors to lobby and cafeteria (floor 2)
    lunch_pattern = [(floor, 1) for floor in [7, 8, 9] for _ in range(10)]
    lunch_pattern += [(floor, 2) for floor in [7, 8, 9] for _ in range(5)]
    # Evening: office floors to lobby
    evening_pattern = [(floor, 1) for floor in [7, 8, 9] for _ in range(20)]

    all_patterns = morning_pattern + lunch_pattern + evening_pattern

    # Train the cache with patterns
    for from_floor, to_floor in all_patterns:
        elevator.current_floor = from_floor
        elevator.add_floor_request(to_floor, f"user_{random.randint(1, 50)}", from_floor)

    # Test predictions against realistic scenarios
    test_scenarios = [
        (1, [7, 8, 9]),  # From lobby, expect office floors
        (7, [1, 2]),     # From office, expect lobby or cafeteria
        (8, [1, 2]),     # From office, expect lobby or cafeteria
        (9, [1, 2]),     # From office, expect lobby or cafeteria
    ]

    correct_predictions = 0
    total_predictions = 0

    for from_floor, expected_floors in test_scenarios:
        for _ in range(25):  # Test each scenario 25 times
            predicted = elevator.cache.predict_next_request(from_floor)
            if predicted in expected_floors:
                correct_predictions += 1
            total_predictions += 1

    accuracy = correct_predictions / total_predictions
    print(f"Realistic prediction accuracy: {accuracy:.2%}")

    # Test 3: Energy savings demonstration
    print(f"\n=== Energy Analysis ===")

    # Simulate pre-positioning scenarios
    elevator.clear_requests()
    elevator.current_floor = 1
    elevator.last_request_time = time.time() - 35  # Trigger pre-positioning

    # Force some idle position stats to demonstrate pre-positioning
    for _ in range(10):
        elevator.cache.update_idle_position_stats(8)  # Office floor likely to be requested

    movements = elevator.process_requests()
    for movement in movements:
        if "Pre-positioned" in movement:
            print(f"Pre-positioning: {movement}")

    print(f"Total energy saved: {elevator.get_status()['energy_saved']:.2f} units")

    # Show cache performance metrics
    cache_perf = elevator.get_status()['cache_performance']
    print(f"\n=== Cache Performance Metrics ===")
    for key, value in cache_perf.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title()}: {value:.3f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    print("Running Cached Elevator Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)

    run_caching_benchmarks()