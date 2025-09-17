// 10-Floor Elevator Controller - Matches Python Implementation
// Direct correspondence to OptimizedElevator(num_floors=10)
module elevator_controller_10floor (
    input wire clk,
    input wire reset,

    // Floor button inputs (floors 1-10)
    input wire [9:0] floor_buttons,  // floor_buttons[0] = floor 1, [9] = floor 10
    input wire door_close_btn,

    // Direction control
    input wire direction,  // 0 = down, 1 = up

    // Outputs
    output reg [3:0] current_floor,     // 0-9 (floors 1-10)
    output reg [9:0] floor_requests,    // Active floor requests
    output reg moving_up,
    output reg moving_down,
    output reg door_open,
    output reg [3:0] total_movements,   // Movement counter (like Python)

    // Status outputs (matches Python get_status())
    output reg [9:0] up_queue,          // Floors in up direction
    output reg [9:0] down_queue,        // Floors in down direction
    output reg [9:0] pending_requests   // All pending requests
);

// State definitions (matches Python ElevatorState enum)
parameter [2:0] IDLE      = 3'b000;  // ElevatorState.IDLE
parameter [2:0] MOVING_UP = 3'b001;  // ElevatorState.MOVING_UP
parameter [2:0] MOVING_DN = 3'b010;  // ElevatorState.MOVING_DOWN
parameter [2:0] DOOR_OP   = 3'b011;  // ElevatorState.DOOR_OPEN

reg [2:0] current_state, next_state;

// Internal registers (matches Python internal variables)
reg [9:0] floor_buttons_sync;
reg [9:0] floor_buttons_prev;
reg direction_reg;

// Request queues (matches Python heapq implementation)
reg [9:0] up_requests_mask;
reg [9:0] down_requests_mask;

// Movement tracking (matches Python total_movements)
reg [3:0] movement_counter;

// Button edge detection and synchronization
always @(posedge clk or posedge reset) begin
    if (reset) begin
        floor_buttons_sync <= 10'b0000000000;
        floor_buttons_prev <= 10'b0000000000;
    end else begin
        floor_buttons_prev <= floor_buttons_sync;
        floor_buttons_sync <= floor_buttons;
    end
end

// Floor request management (matches Python add_floor_request logic)
always @(posedge clk or posedge reset) begin
    if (reset) begin
        floor_requests <= 10'b0000000000;
        direction_reg <= 1'b0;
        movement_counter <= 4'b0000;
    end else begin
        direction_reg <= direction;

        // Add floor requests on button press (edge detection)
        // Matches Python: self.current_requests.add(floor)
        if (floor_buttons_sync[0] && !floor_buttons_prev[0] && current_floor != 0) floor_requests[0] <= 1'b1;
        if (floor_buttons_sync[1] && !floor_buttons_prev[1] && current_floor != 1) floor_requests[1] <= 1'b1;
        if (floor_buttons_sync[2] && !floor_buttons_prev[2] && current_floor != 2) floor_requests[2] <= 1'b1;
        if (floor_buttons_sync[3] && !floor_buttons_prev[3] && current_floor != 3) floor_requests[3] <= 1'b1;
        if (floor_buttons_sync[4] && !floor_buttons_prev[4] && current_floor != 4) floor_requests[4] <= 1'b1;
        if (floor_buttons_sync[5] && !floor_buttons_prev[5] && current_floor != 5) floor_requests[5] <= 1'b1;
        if (floor_buttons_sync[6] && !floor_buttons_prev[6] && current_floor != 6) floor_requests[6] <= 1'b1;
        if (floor_buttons_sync[7] && !floor_buttons_prev[7] && current_floor != 7) floor_requests[7] <= 1'b1;
        if (floor_buttons_sync[8] && !floor_buttons_prev[8] && current_floor != 8) floor_requests[8] <= 1'b1;
        if (floor_buttons_sync[9] && !floor_buttons_prev[9] && current_floor != 9) floor_requests[9] <= 1'b1;

        // Clear completed requests (matches Python self.current_requests.discard())
        if (current_state == DOOR_OP) begin
            floor_requests[current_floor] <= 1'b0;
        end

        // Count movements (matches Python self.total_movements)
        if ((current_state == MOVING_UP && next_state != MOVING_UP) ||
            (current_state == MOVING_DN && next_state != MOVING_DN)) begin
            movement_counter <= movement_counter + 1;
        end
    end
end

// Request queue generation (matches Python heapq logic)
always @(*) begin
    // Clear queues
    up_requests_mask = 10'b0000000000;
    down_requests_mask = 10'b0000000000;

    // Populate up/down queues based on current floor (matches Python heappush logic)
    // Floor 0 (floor 1)
    if (floor_requests[0]) begin
        if (0 > current_floor) up_requests_mask[0] = 1'b1;
        else if (0 < current_floor) down_requests_mask[0] = 1'b1;
    end
    // Floor 1 (floor 2)
    if (floor_requests[1]) begin
        if (1 > current_floor) up_requests_mask[1] = 1'b1;
        else if (1 < current_floor) down_requests_mask[1] = 1'b1;
    end
    // Floor 2 (floor 3)
    if (floor_requests[2]) begin
        if (2 > current_floor) up_requests_mask[2] = 1'b1;
        else if (2 < current_floor) down_requests_mask[2] = 1'b1;
    end
    // Floor 3 (floor 4)
    if (floor_requests[3]) begin
        if (3 > current_floor) up_requests_mask[3] = 1'b1;
        else if (3 < current_floor) down_requests_mask[3] = 1'b1;
    end
    // Floor 4 (floor 5)
    if (floor_requests[4]) begin
        if (4 > current_floor) up_requests_mask[4] = 1'b1;
        else if (4 < current_floor) down_requests_mask[4] = 1'b1;
    end
    // Floor 5 (floor 6)
    if (floor_requests[5]) begin
        if (5 > current_floor) up_requests_mask[5] = 1'b1;
        else if (5 < current_floor) down_requests_mask[5] = 1'b1;
    end
    // Floor 6 (floor 7)
    if (floor_requests[6]) begin
        if (6 > current_floor) up_requests_mask[6] = 1'b1;
        else if (6 < current_floor) down_requests_mask[6] = 1'b1;
    end
    // Floor 7 (floor 8)
    if (floor_requests[7]) begin
        if (7 > current_floor) up_requests_mask[7] = 1'b1;
        else if (7 < current_floor) down_requests_mask[7] = 1'b1;
    end
    // Floor 8 (floor 9)
    if (floor_requests[8]) begin
        if (8 > current_floor) up_requests_mask[8] = 1'b1;
        else if (8 < current_floor) down_requests_mask[8] = 1'b1;
    end
    // Floor 9 (floor 10)
    if (floor_requests[9]) begin
        if (9 > current_floor) up_requests_mask[9] = 1'b1;
        else if (9 < current_floor) down_requests_mask[9] = 1'b1;
    end
end

// State machine (matches Python process_requests logic)
always @(posedge clk or posedge reset) begin
    if (reset) begin
        current_state <= IDLE;
        current_floor <= 4'b0000;  // Start at floor 1 (index 0)
    end else begin
        current_state <= next_state;

        // Floor movement logic (matches Python current_floor updates)
        case (current_state)
            MOVING_UP: begin
                if (current_floor < 4'd9)  // If not at top floor (floor 10)
                    current_floor <= current_floor + 1;
            end
            MOVING_DN: begin
                if (current_floor > 4'd0)  // If not at bottom floor (floor 1)
                    current_floor <= current_floor - 1;
            end
            default: begin
                current_floor <= current_floor;  // No movement
            end
        endcase
    end
end

// Next state logic (matches Python _get_next_floor and SCAN algorithm)
always @(*) begin
    next_state = current_state;

    case (current_state)
        IDLE: begin
            // Matches Python: if not self.current_requests: return ["No requests to process"]
            if (floor_requests != 10'b0000000000) begin
                // Matches Python direction logic and SCAN algorithm
                if (direction_reg) begin  // UP direction preferred
                    if (|up_requests_mask)        // Any floors above
                        next_state = MOVING_UP;
                    else if (|down_requests_mask) // Any floors below
                        next_state = MOVING_DN;
                    else
                        next_state = DOOR_OP;     // Already at requested floor
                end else begin  // DOWN direction preferred
                    if (|down_requests_mask)      // Any floors below
                        next_state = MOVING_DN;
                    else if (|up_requests_mask)   // Any floors above
                        next_state = MOVING_UP;
                    else
                        next_state = DOOR_OP;     // Already at requested floor
                end
            end
        end

        MOVING_UP: begin
            // Check if we've reached a requested floor (matches Python heappop logic)
            if (floor_requests[current_floor + 1]) begin
                next_state = DOOR_OP;
            end else if (!|up_requests_mask) begin  // No more up requests
                next_state = IDLE;
            end
        end

        MOVING_DN: begin
            // Check if we've reached a requested floor
            if (floor_requests[current_floor - 1]) begin
                next_state = DOOR_OP;
            end else if (!|down_requests_mask) begin  // No more down requests
                next_state = IDLE;
            end
        end

        DOOR_OP: begin
            // Matches Python door operation logic
            if (door_close_btn) begin
                next_state = IDLE;
            end
        end

        default: next_state = IDLE;
    endcase
end

// Output assignments (matches Python get_status() return values)
always @(*) begin
    // Default outputs
    moving_up = (current_state == MOVING_UP);
    moving_down = (current_state == MOVING_DN);
    door_open = (current_state == DOOR_OP);
    total_movements = movement_counter;

    // Status outputs (matches Python get_status dictionary)
    pending_requests = floor_requests;
    up_queue = up_requests_mask;
    down_queue = down_requests_mask;
end

endmodule