# Simplified timing constraint for practice.
create_clock -name clk -period 10.0
set_input_delay 1.0 -clock clk [all_inputs]
set_output_delay 1.0 -clock clk [all_outputs]

