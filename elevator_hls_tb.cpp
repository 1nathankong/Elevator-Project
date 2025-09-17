#include "elevator_hls.h"
#include <iostream>
#include <iomanip>

using namespace std;

int main() {
    cout << "=== Minimal HLS Elevator Controller Test ===" << endl;

    // Test variables
    request_t input_request;
    bool reset;
    floor_t current_floor;
    state_t current_state;
    direction_t current_direction;
    bool request_accepted;

    int test_count = 0;
    int pass_count = 0;

    // Helper function for test output
    auto print_status = [&]() {
        cout << "Floor: " << current_floor
             << ", State: " << current_state
             << ", Direction: " << current_direction
             << ", Accepted: " << request_accepted << endl;
    };

    // Test 1: Reset
    cout << "\n--- Test 1: Reset ---" << endl;
    reset = true;
    input_request.valid = false;
    input_request.floor = 0;

    elevator_controller(input_request, reset, current_floor, current_state, current_direction, request_accepted);
    print_status();

    if (current_floor == 1 && current_state == STATE_IDLE && current_direction == DIR_IDLE) {
        cout << "✓ Reset test PASSED" << endl;
        pass_count++;
    } else {
        cout << "✗ Reset test FAILED" << endl;
    }
    test_count++;

    // Test 2: Request floor 3
    cout << "\n--- Test 2: Request floor 3 ---" << endl;
    reset = false;
    input_request.valid = true;
    input_request.floor = 3;

    elevator_controller(input_request, reset, current_floor, current_state, current_direction, request_accepted);
    print_status();

    if (request_accepted && current_state == STATE_MOVING && current_direction == DIR_UP) {
        cout << "✓ Request accepted test PASSED" << endl;
        pass_count++;
    } else {
        cout << "✗ Request accepted test FAILED" << endl;
    }
    test_count++;

    // Test 3: Simulate movement to floor 3
    cout << "\n--- Test 3: Movement simulation ---" << endl;
    input_request.valid = false;  // No new requests

    // Should take 2 cycles to reach floor 3 from floor 1
    for (int cycle = 0; cycle < 5; cycle++) {
        elevator_controller(input_request, reset, current_floor, current_state, current_direction, request_accepted);
        cout << "Cycle " << cycle + 1 << ": ";
        print_status();

        if (current_floor == 3 && current_state == STATE_IDLE) {
            cout << "✓ Reached target floor 3" << endl;
            break;
        }
    }

    if (current_floor == 3 && current_state == STATE_IDLE) {
        cout << "✓ Movement test PASSED" << endl;
        pass_count++;
    } else {
        cout << "✗ Movement test FAILED" << endl;
    }
    test_count++;

    // Test 4: Request floor 1 (downward movement)
    cout << "\n--- Test 4: Request floor 1 (downward) ---" << endl;
    input_request.valid = true;
    input_request.floor = 1;

    elevator_controller(input_request, reset, current_floor, current_state, current_direction, request_accepted);
    print_status();

    if (request_accepted && current_direction == DIR_DOWN) {
        cout << "✓ Downward request test PASSED" << endl;
        pass_count++;
    } else {
        cout << "✗ Downward request test FAILED" << endl;
    }
    test_count++;

    // Test 5: Invalid request (floor 0)
    cout << "\n--- Test 5: Invalid request (floor 0) ---" << endl;
    reset = true;  // Reset first
    elevator_controller(input_request, reset, current_floor, current_state, current_direction, request_accepted);

    reset = false;
    input_request.valid = true;
    input_request.floor = 0;  // Invalid floor

    elevator_controller(input_request, reset, current_floor, current_state, current_direction, request_accepted);
    print_status();

    if (!request_accepted) {
        cout << "✓ Invalid request rejection test PASSED" << endl;
        pass_count++;
    } else {
        cout << "✗ Invalid request rejection test FAILED" << endl;
    }
    test_count++;

    // Final results
    cout << "\n=== Test Results ===" << endl;
    cout << "Passed: " << pass_count << "/" << test_count << endl;

    if (pass_count == test_count) {
        cout << "🎉 All tests PASSED! Ready for synthesis." << endl;
        return 0;
    } else {
        cout << "❌ Some tests FAILED. Check implementation." << endl;
        return 1;
    }
}