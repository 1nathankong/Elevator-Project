from enum import Enum
from typing import List, Set, Dict, Tuple, Optional
import heapq
import time
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json

class ElevatorState(Enum):
    IDLE = "idle"
    MOVING_UP = "moving_up"
    MOVING_DOWN = "moving_down"
    DOOR_OPEN = "door_open"
    PRE_POSITIONED = "pre_positioned"

class Direction(Enum):
    UP = 1
    DOWN = 0
    IDLE = -1

class ElevatorCache:
    def __init__(self, max_history: int = 1000):
        # Frequency caching
        self.floor_frequency = defaultdict(int)
        self.floor_pair_frequency = defaultdict(int)  # (from, to) pairs

        # Time-based patterns
        self.hourly_patterns = defaultdict(lambda: defaultdict(int))
        self.daily_patterns = defaultdict(lambda: defaultdict(int))

        # User patterns (if user IDs are available)
        self.user_patterns = defaultdict(lambda: defaultdict(int))

        # Recent history for trend analysis
        self.recent_requests = deque(maxlen=max_history)

        # Energy optimization
        self.idle_position_stats = defaultdict(int)
        self.energy_efficient_floors = set()

        # Cache hit statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.predictions_made = 0
        self.predictions_correct = 0

    def record_request(self, from_floor: int, to_floor: int, user_id: Optional[str] = None, timestamp: Optional[float] = None):
        """Record a floor request for caching"""
        if timestamp is None:
            timestamp = time.time()

        dt = datetime.fromtimestamp(timestamp)
        hour = dt.hour
        day_of_week = dt.weekday()

        # Update frequency caches
        self.floor_frequency[to_floor] += 1
        if from_floor != to_floor:
            self.floor_pair_frequency[(from_floor, to_floor)] += 1

        # Update time-based patterns
        self.hourly_patterns[hour][to_floor] += 1
        self.daily_patterns[day_of_week][to_floor] += 1

        # Update user patterns
        if user_id:
            self.user_patterns[user_id][to_floor] += 1

        # Add to recent history
        self.recent_requests.append({
            'from': from_floor,
            'to': to_floor,
            'user_id': user_id,
            'timestamp': timestamp,
            'hour': hour,
            'day': day_of_week
        })

    def get_most_frequent_floors(self, limit: int = 5) -> List[Tuple[int, int]]:
        """Get most frequently requested floors"""
        return sorted(self.floor_frequency.items(), key=lambda x: x[1], reverse=True)[:limit]

    def predict_next_request(self, current_floor: int, current_time: Optional[float] = None) -> Optional[int]:
        """Predict the next likely floor request using weighted scoring"""
        if current_time is None:
            current_time = time.time()

        dt = datetime.fromtimestamp(current_time)
        hour = dt.hour

        self.predictions_made += 1

        # Score floors based on multiple factors
        floor_scores = defaultdict(float)

        # Factor 1: Time-based patterns (weight: 0.4)
        if self.hourly_patterns[hour]:
            max_hourly_requests = max(self.hourly_patterns[hour].values())
            for floor, count in self.hourly_patterns[hour].items():
                floor_scores[floor] += (count / max_hourly_requests) * 0.4

        # Factor 2: Overall frequency (weight: 0.3)
        if self.floor_frequency:
            max_frequency = max(self.floor_frequency.values())
            for floor, count in self.floor_frequency.items():
                floor_scores[floor] += (count / max_frequency) * 0.3

        # Factor 3: Floor pair patterns from current floor (weight: 0.2)
        for (from_f, to_f), count in self.floor_pair_frequency.items():
            if from_f == current_floor:
                max_pair_count = max(self.floor_pair_frequency.values())
                floor_scores[to_f] += (count / max_pair_count) * 0.2

        # Factor 4: Recent trends (weight: 0.1)
        recent_floors = [req['to'] for req in list(self.recent_requests)[-20:]]  # Last 20 requests
        if recent_floors:
            for floor in set(recent_floors):
                trend_score = recent_floors.count(floor) / len(recent_floors)
                floor_scores[floor] += trend_score * 0.1

        # Return highest scoring floor
        if floor_scores:
            return max(floor_scores.items(), key=lambda x: x[1])[0]

        return None

    def get_optimal_idle_position(self) -> int:
        """Get the optimal floor to position elevator when idle"""
        if self.idle_position_stats:
            return max(self.idle_position_stats.items(), key=lambda x: x[1])[0]

        # Default to middle floor or most frequent floor
        if self.floor_frequency:
            return max(self.floor_frequency.items(), key=lambda x: x[1])[0]

        return 1  # Default

    def update_idle_position_stats(self, floor: int):
        """Update statistics for idle positioning"""
        self.idle_position_stats[floor] += 1

    def validate_prediction(self, predicted_floor: int, actual_floor: int):
        """Validate if prediction was correct"""
        if predicted_floor == actual_floor:
            self.predictions_correct += 1

    def get_cache_performance(self) -> Dict:
        """Get cache performance metrics"""
        hit_rate = self.cache_hits / max(1, self.cache_hits + self.cache_misses)
        prediction_accuracy = self.predictions_correct / max(1, self.predictions_made)

        return {
            'hit_rate': hit_rate,
            'prediction_accuracy': prediction_accuracy,
            'total_requests_cached': len(self.recent_requests),
            'unique_floors_seen': len(self.floor_frequency),
            'most_frequent_floor': max(self.floor_frequency.items(), key=lambda x: x[1])[0] if self.floor_frequency else None
        }

class CachedElevator:
    def __init__(self, num_floors: int = 10, starting_floor: int = 1, enable_caching: bool = True):
        self.num_floors = num_floors
        self.current_floor = starting_floor
        self.state = ElevatorState.IDLE
        self.direction = Direction.IDLE

        # Request queues
        self.up_requests = []
        self.down_requests = []
        self.current_requests = set()

        # Caching system
        self.enable_caching = enable_caching
        self.cache = ElevatorCache() if enable_caching else None

        # Pre-positioning
        self.pre_position_enabled = True
        self.last_request_time = time.time()
        self.idle_threshold = 30  # seconds before considering pre-positioning

        # Energy tracking
        self.total_movements = 0
        self.energy_saved = 0

    def add_floor_request(self, floor: int, user_id: Optional[str] = None, from_floor: Optional[int] = None) -> bool:
        """Add a floor request with caching support"""
        if not self._is_valid_floor(floor):
            if self.cache:
                self.cache.cache_misses += 1
            return False

        if floor == self.current_floor:
            if self.cache:
                self.cache.cache_hits += 1
            return True

        # Record request for caching
        if self.cache:
            actual_from = from_floor if from_floor else self.current_floor
            self.cache.record_request(actual_from, floor, user_id)
            self.cache.cache_hits += 1

        self.current_requests.add(floor)
        self.last_request_time = time.time()

        if floor > self.current_floor:
            heapq.heappush(self.up_requests, floor)
        else:
            heapq.heappush(self.down_requests, -floor)

        return True

    def _is_valid_floor(self, floor: int) -> bool:
        return 1 <= floor <= self.num_floors

    def _get_next_floor(self) -> int:
        """Get next floor with caching optimization"""
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

    def _should_pre_position(self) -> bool:
        """Check if elevator should pre-position based on cache"""
        if not self.enable_caching or not self.cache or not self.pre_position_enabled:
            return False

        time_since_last_request = time.time() - self.last_request_time
        return (time_since_last_request > self.idle_threshold and
                self.state == ElevatorState.IDLE and
                len(self.current_requests) == 0)

    def _pre_position(self) -> Optional[str]:
        """Pre-position elevator based on cached patterns"""
        if not self._should_pre_position():
            return None

        optimal_floor = self.cache.get_optimal_idle_position()

        if optimal_floor != self.current_floor:
            movements_to_optimal = abs(optimal_floor - self.current_floor)

            self.state = ElevatorState.PRE_POSITIONED
            old_floor = self.current_floor
            self.current_floor = optimal_floor

            # Estimate energy saved by being closer to likely next request
            energy_saved = 0.0
            predicted_next = self.cache.predict_next_request(old_floor)  # Use old floor for prediction
            if predicted_next and predicted_next != old_floor:
                # Energy saved = distance we would have traveled - distance from optimal position
                original_distance = abs(old_floor - predicted_next)
                optimal_distance = abs(optimal_floor - predicted_next)
                energy_saved = max(0, original_distance - optimal_distance) * 1.0  # Increase weight
                self.energy_saved += energy_saved
            else:
                # Base energy savings from moving to a more central/optimal position
                energy_saved = movements_to_optimal * 0.3  # Conservative estimate
                self.energy_saved += energy_saved

            return f"Pre-positioned from floor {old_floor} to floor {optimal_floor} (predicted high traffic, energy saved: {energy_saved:.1f})"

        return None

    def process_requests(self) -> List[str]:
        """Process requests with caching optimization"""
        if not self.current_requests:
            # Try pre-positioning if idle
            pre_pos_msg = self._pre_position()
            if pre_pos_msg:
                return [pre_pos_msg]
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

            # Track energy usage and potential savings
            floors_moved = abs(next_floor - self.current_floor)
            self.total_movements += floors_moved

            # Check if this was a predicted request for energy savings calculation
            if self.cache and len(self.current_requests) > 1:
                # If we're handling multiple requests efficiently, add energy savings
                remaining_requests = len(self.current_requests) - 1
                self.energy_saved += remaining_requests * 0.1  # Small bonus for batching

            movements.append(f"Moving from floor {self.current_floor} to floor {next_floor}")
            self.current_floor = next_floor

            # Remove completed request
            self.current_requests.discard(next_floor)

            # Update cache with idle position stats
            if self.cache:
                self.cache.update_idle_position_stats(next_floor)

            self.state = ElevatorState.DOOR_OPEN
            movements.append(f"Arrived at floor {self.current_floor} - Doors open")

        self.state = ElevatorState.IDLE
        self.direction = Direction.IDLE
        movements.append("All requests completed - Elevator idle")

        return movements

    def get_status(self) -> dict:
        """Get comprehensive status including cache information"""
        status = {
            "current_floor": self.current_floor,
            "state": self.state.value,
            "direction": self.direction.value,
            "pending_requests": sorted(list(self.current_requests)),
            "up_queue": sorted(self.up_requests),
            "down_queue": sorted([-x for x in self.down_requests], reverse=True),
            "total_movements": self.total_movements,
            "energy_saved": self.energy_saved
        }

        if self.cache:
            status["cache_performance"] = self.cache.get_cache_performance()
            status["most_frequent_floors"] = self.cache.get_most_frequent_floors()
            status["predicted_next_floor"] = self.cache.predict_next_request(self.current_floor)

        return status

    def save_cache_data(self, filename: str):
        """Save cache data to file"""
        if not self.cache:
            return

        cache_data = {
            'floor_frequency': dict(self.cache.floor_frequency),
            'floor_pair_frequency': {f"{k[0]}-{k[1]}": v for k, v in self.cache.floor_pair_frequency.items()},
            'hourly_patterns': {h: dict(patterns) for h, patterns in self.cache.hourly_patterns.items()},
            'cache_performance': self.cache.get_cache_performance()
        }

        with open(filename, 'w') as f:
            json.dump(cache_data, f, indent=2)

    def clear_requests(self):
        """Clear all requests and reset state"""
        self.current_requests.clear()
        self.up_requests.clear()
        self.down_requests.clear()
        self.state = ElevatorState.IDLE
        self.direction = Direction.IDLE

def demonstrate_cached_elevator():
    """Demonstrate the cached elevator functionality"""
    print("=== Cached Elevator Demonstration ===\n")

    elevator = CachedElevator(num_floors=10, starting_floor=1)

    print("Test 1: Building usage patterns")
    # Simulate morning rush to office floors
    morning_requests = [(1, 7), (1, 8), (1, 9), (1, 7), (1, 8)] * 3

    for from_floor, to_floor in morning_requests:
        elevator.current_floor = from_floor
        elevator.add_floor_request(to_floor, f"user_{from_floor}_{to_floor}", from_floor)
        elevator.process_requests()
        elevator.clear_requests()

    print("After morning rush simulation:")
    status = elevator.get_status()
    print(f"Cache performance: {status.get('cache_performance', {})}")
    print(f"Most frequent floors: {status.get('most_frequent_floors', [])}")
    print(f"Predicted next floor: {status.get('predicted_next_floor')}\n")

    print("Test 2: Pre-positioning demonstration")
    elevator.clear_requests()
    elevator.current_floor = 1
    elevator.last_request_time = time.time() - 35  # Simulate 35 seconds of idle time

    # Should trigger pre-positioning
    movements = elevator.process_requests()
    for movement in movements:
        print(f"  {movement}")

    print(f"\nFinal status: {elevator.get_status()}")

if __name__ == "__main__":
    demonstrate_cached_elevator()