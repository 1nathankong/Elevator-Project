#include "elevator_hls.h"

void elevator_controller(
    request_t input_request,
    bool reset,
    floor_t &current_floor,
    state_t &current_state,
    direction_t &current_direction,
    bool &request_accepted
) {
    #pragma HLS INTERFACE ap_ctrl_none port=return
    #pragma HLS INTERFACE ap_none port=input_request
    #pragma HLS INTERFACE ap_none port=reset
    #pragma HLS INTERFACE ap_none port=current_floor
    #pragma HLS INTERFACE ap_none port=current_state
    #pragma HLS INTERFACE ap_none port=current_direction
    #pragma HLS INTERFACE ap_none port=request_accepted

    // Static variables to maintain state between calls
    static floor_t elevator_floor = 1;
    static state_t elevator_state = STATE_IDLE;
    static direction_t elevator_direction = DIR_IDLE;
    static floor_t target_floor = 0;
    static bool has_target = false;

    // Reset functionality
    if (reset) {
        elevator_floor = 1;
        elevator_state = STATE_IDLE;
        elevator_direction = DIR_IDLE;
        target_floor = 0;
        has_target = false;
        request_accepted = false;
    } else {
        // Process new request only if idle and no current target
        if (input_request.valid && !has_target && elevator_state == STATE_IDLE) {
            if (input_request.floor > 0 && input_request.floor <= 15 &&
                input_request.floor != elevator_floor) {
                target_floor = input_request.floor;
                has_target = true;
                request_accepted = true;

                // Determine direction
                if (target_floor > elevator_floor) {
                    elevator_direction = DIR_UP;
                } else {
                    elevator_direction = DIR_DOWN;
                }
                elevator_state = STATE_MOVING;
            } else {
                request_accepted = false;
            }
        } else {
            request_accepted = false;
        }

        // Move elevator if we have a target
        if (has_target && elevator_state == STATE_MOVING) {
            if (elevator_floor < target_floor) {
                elevator_floor++;
                elevator_direction = DIR_UP;
            } else if (elevator_floor > target_floor) {
                elevator_floor--;
                elevator_direction = DIR_DOWN;
            }

            // Check if we've reached the target
            if (elevator_floor == target_floor) {
                elevator_state = STATE_DOOR_OPEN;
                elevator_direction = DIR_IDLE;
                has_target = false;
                // In next cycle, will return to IDLE
            }
        } else if (elevator_state == STATE_DOOR_OPEN) {
            // Simple door operation - just return to idle
            elevator_state = STATE_IDLE;
        }
    }

    // Update output ports
    current_floor = elevator_floor;
    current_state = elevator_state;
    current_direction = elevator_direction;
}