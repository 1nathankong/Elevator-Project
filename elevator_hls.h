#ifndef ELEVATOR_HLS_H
#define ELEVATOR_HLS_H

#include "ap_int.h"

// Hardware-optimized data types
typedef ap_uint<4> floor_t;      // 4 bits: floors 0-15
typedef ap_uint<2> state_t;      // 2 bits: IDLE=0, MOVING=1, DOOR_OPEN=2
typedef ap_int<2> direction_t;   // 2 bits: DOWN=-1, IDLE=0, UP=1

// States
const state_t STATE_IDLE = 0;
const state_t STATE_MOVING = 1;
const state_t STATE_DOOR_OPEN = 2;

// Directions
const direction_t DIR_DOWN = -1;
const direction_t DIR_IDLE = 0;
const direction_t DIR_UP = 1;

// Request structure
struct request_t {
    floor_t floor;
    bool valid;
};

// Top-level function for HLS
void elevator_controller(
    request_t input_request,
    bool reset,
    floor_t &current_floor,
    state_t &current_state,
    direction_t &current_direction,
    bool &request_accepted
);

#endif