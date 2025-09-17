import time
import random
from typing import List, Tuple
from optimized_elevator import OptimizedElevator
from cached_elevator import CachedElevator

class ElevatorComparison:
    """Compare performance between optimized and cached elevator implementations"""

    def __init__(self):
        self.results = {}

    def simulate_office_building_day(self, elevator, num_employees: int = 100) -> dict:
        """Simulate a full day in an office building"""
        movements = 0
        total_time = 0
        requests_processed = 0

        # Morning rush (8-10 AM) - everyone goes up
        print("  Simulating morning rush...")
        morning_requests = [(1, random.randint(2, 10)) for _ in range(num_employees)]

        start_time = time.time()
        for from_floor, to_floor in morning_requests:
            if hasattr(elevator, 'current_floor'):
                elevator.current_floor = from_floor

            if isinstance(elevator, CachedElevator):
                # Cached elevator method with user_id and from_floor
                elevator.add_floor_request(to_floor, f"emp_{random.randint(1, num_employees)}", from_floor)
            else:
                # Optimized elevator method
                elevator.add_floor_request(to_floor)

            moves = elevator.process_requests()
            movements += len([m for m in moves if "Moving from" in m])
            requests_processed += 1

            if hasattr(elevator, 'clear_requests'):
                elevator.clear_requests()

        morning_time = time.time() - start_time

        # Lunch time (12-1 PM) - mixed movement
        print("  Simulating lunch time...")
        lunch_requests = []
        for _ in range(num_employees // 2):
            # Some go down to lobby
            lunch_requests.append((random.randint(2, 10), 1))
            # Some go to different floors
            lunch_requests.append((random.randint(2, 10), random.randint(2, 10)))

        start_time = time.time()
        for from_floor, to_floor in lunch_requests:
            if hasattr(elevator, 'current_floor'):
                elevator.current_floor = from_floor

            if isinstance(elevator, CachedElevator):
                elevator.add_floor_request(to_floor, f"emp_{random.randint(1, num_employees)}", from_floor)
            else:
                elevator.add_floor_request(to_floor)

            moves = elevator.process_requests()
            movements += len([m for m in moves if "Moving from" in m])
            requests_processed += 1

            if hasattr(elevator, 'clear_requests'):
                elevator.clear_requests()

        lunch_time = time.time() - start_time

        # Evening rush (5-6 PM) - everyone goes down
        print("  Simulating evening rush...")
        evening_requests = [(random.randint(2, 10), 1) for _ in range(num_employees)]

        start_time = time.time()
        for from_floor, to_floor in evening_requests:
            if hasattr(elevator, 'current_floor'):
                elevator.current_floor = from_floor

            if isinstance(elevator, CachedElevator):
                elevator.add_floor_request(to_floor, f"emp_{random.randint(1, num_employees)}", from_floor)
            else:
                elevator.add_floor_request(to_floor)

            moves = elevator.process_requests()
            movements += len([m for m in moves if "Moving from" in m])
            requests_processed += 1

            if hasattr(elevator, 'clear_requests'):
                elevator.clear_requests()

        evening_time = time.time() - start_time

        total_time = morning_time + lunch_time + evening_time

        return {
            'total_movements': movements,
            'total_time': total_time,
            'requests_processed': requests_processed,
            'movements_per_request': movements / max(1, requests_processed),
            'requests_per_second': requests_processed / max(0.001, total_time),
            'morning_time': morning_time,
            'lunch_time': lunch_time,
            'evening_time': evening_time
        }

    def compare_implementations(self) -> dict:
        """Compare all elevator implementations"""
        print("=== Elevator Implementation Comparison ===\n")

        results = {}

        # Test 1: Optimized Elevator
        print("Testing Optimized Elevator...")
        optimized = OptimizedElevator(num_floors=10, starting_floor=1)
        results['optimized'] = self.simulate_office_building_day(optimized)

        # Test 2: Cached Elevator
        print("Testing Cached Elevator...")
        cached = CachedElevator(num_floors=10, starting_floor=1, enable_caching=True)
        results['cached'] = self.simulate_office_building_day(cached)

        # Test 3: Cached Elevator without caching (for comparison)
        print("Testing Cached Elevator (caching disabled)...")
        cached_disabled = CachedElevator(num_floors=10, starting_floor=1, enable_caching=False)
        results['cached_no_cache'] = self.simulate_office_building_day(cached_disabled)

        # Get cache performance if available
        if hasattr(cached, 'cache') and cached.cache:
            cache_status = cached.get_status()
            results['cache_performance'] = cache_status.get('cache_performance', {})
            results['cache_energy_saved'] = cache_status.get('energy_saved', 0)

        return results

    def print_comparison_results(self, results: dict):
        """Print formatted comparison results"""
        print("\n" + "="*80)
        print("ELEVATOR PERFORMANCE COMPARISON RESULTS")
        print("="*80)

        implementations = ['optimized', 'cached', 'cached_no_cache']
        metrics = ['total_movements', 'total_time', 'requests_processed',
                  'movements_per_request', 'requests_per_second']

        # Print table header
        print(f"{'Metric':<25} {'Optimized':<15} {'Cached':<15} {'No Cache':<15} {'Improvement':<15}")
        print("-" * 85)

        for metric in metrics:
            optimized_val = results['optimized'][metric]
            cached_val = results['cached'][metric]
            no_cache_val = results['cached_no_cache'][metric]

            # Calculate improvement (cached vs optimized)
            if metric in ['total_movements', 'total_time', 'movements_per_request']:
                # Lower is better
                improvement = ((optimized_val - cached_val) / optimized_val) * 100 if optimized_val > 0 else 0
                improvement_str = f"{improvement:+.1f}%"
            else:
                # Higher is better
                improvement = ((cached_val - optimized_val) / optimized_val) * 100 if optimized_val > 0 else 0
                improvement_str = f"{improvement:+.1f}%"

            print(f"{metric.replace('_', ' ').title():<25} {optimized_val:<15.3f} {cached_val:<15.3f} {no_cache_val:<15.3f} {improvement_str:<15}")

        # Cache-specific metrics
        if 'cache_performance' in results:
            print("\n" + "="*50)
            print("CACHE PERFORMANCE METRICS")
            print("="*50)

            cache_perf = results['cache_performance']
            for key, value in cache_perf.items():
                if isinstance(value, float):
                    print(f"{key.replace('_', ' ').title():<30}: {value:.3f}")
                else:
                    print(f"{key.replace('_', ' ').title():<30}: {value}")

            if 'cache_energy_saved' in results:
                print(f"{'Energy Saved':<30}: {results['cache_energy_saved']:.2f} units")

    def run_stress_test(self, num_requests: int = 10000) -> dict:
        """Run stress test with many requests"""
        print(f"\n=== Stress Test ({num_requests:,} requests) ===")

        elevators = {
            'optimized': OptimizedElevator(num_floors=50, starting_floor=25),
            'cached': CachedElevator(num_floors=50, starting_floor=25, enable_caching=True)
        }

        results = {}

        for name, elevator in elevators.items():
            print(f"Testing {name} elevator...")

            start_time = time.time()
            requests_processed = 0

            for i in range(num_requests):
                from_floor = random.randint(1, 50)
                to_floor = random.randint(1, 50)

                if hasattr(elevator, 'current_floor'):
                    elevator.current_floor = from_floor

                if isinstance(elevator, CachedElevator):
                    success = elevator.add_floor_request(to_floor, f"user_{i}", from_floor)
                else:
                    success = elevator.add_floor_request(to_floor)

                if success:
                    requests_processed += 1

                # Process every 100 requests to avoid memory issues
                if i % 100 == 0:
                    elevator.process_requests()
                    if hasattr(elevator, 'clear_requests'):
                        elevator.clear_requests()

            total_time = time.time() - start_time
            requests_per_second = requests_processed / total_time

            results[name] = {
                'requests_processed': requests_processed,
                'total_time': total_time,
                'requests_per_second': requests_per_second
            }

            print(f"  Processed {requests_processed:,} requests in {total_time:.2f}s ({requests_per_second:.0f} req/s)")

        return results

def main():
    """Run comprehensive elevator comparison"""
    comparison = ElevatorComparison()

    # Run office building simulation
    results = comparison.compare_implementations()
    comparison.print_comparison_results(results)

    # Run stress test
    stress_results = comparison.run_stress_test(5000)

    print("\n" + "="*50)
    print("STRESS TEST RESULTS")
    print("="*50)
    for name, result in stress_results.items():
        improvement = ""
        if name == 'cached' and 'optimized' in stress_results:
            opt_rps = stress_results['optimized']['requests_per_second']
            cached_rps = result['requests_per_second']
            improvement_pct = ((cached_rps - opt_rps) / opt_rps) * 100
            improvement = f" ({improvement_pct:+.1f}% vs optimized)"

        print(f"{name.title():<15}: {result['requests_per_second']:.0f} requests/second{improvement}")

    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    print("The cached elevator implementation provides:")
    print("• Predictive pre-positioning to reduce wait times")
    print("• Pattern recognition for energy optimization")
    print("• User behavior learning for improved service")
    print("• Performance metrics and analytics")
    print("• Scalable caching architecture")
    print("="*80)

if __name__ == "__main__":
    main()