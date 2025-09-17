# Simple HLS script for minimal elevator controller
open_project elevator_hls_project
set_top elevator_controller
add_files elevator_hls.cpp
add_files -tb elevator_hls_tb.cpp

open_solution "solution1"
set_part {xc7z020-clg400-1}
create_clock -period 10 -name default

# C Simulation
csim_design

# Optional: Synthesis (uncomment to run)
# csynth_design

# Optional: Co-simulation (uncomment after synthesis)
# cosim_design

exit