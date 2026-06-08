# Tcl step: floorplan
set run_dir [lindex $argv 0]
set design_dir [lindex $argv 1]
set metrics_path [lindex $argv 2]
set report_path [lindex $argv 3]

set die_width_um 1000
set die_height_um 1000
set core_utilization 0.62
set macro_count 0

set fp [open $metrics_path w]
puts $fp "step=floorplan"
puts $fp "die_width_um=$die_width_um"
puts $fp "die_height_um=$die_height_um"
puts $fp "core_utilization=$core_utilization"
puts $fp "macro_count=$macro_count"
close $fp

set rp [open $report_path w]
puts $rp "FLOORPLAN REPORT"
puts $rp "Die: ${die_width_um}um x ${die_height_um}um"
puts $rp "Core utilization: $core_utilization"
puts $rp "Macro count: $macro_count"
close $rp

puts "floorplan completed"

