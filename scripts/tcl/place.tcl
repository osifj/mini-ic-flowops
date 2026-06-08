# Tcl step: place
set run_dir [lindex $argv 0]
set design_dir [lindex $argv 1]
set metrics_path [lindex $argv 2]
set report_path [lindex $argv 3]

set placed_instances 137
set congestion_score 0.21
set hpwl_um 4200

set fp [open $metrics_path w]
puts $fp "step=place"
puts $fp "placed_instances=$placed_instances"
puts $fp "congestion_score=$congestion_score"
puts $fp "hpwl_um=$hpwl_um"
close $fp

set rp [open $report_path w]
puts $rp "PLACEMENT REPORT"
puts $rp "Placed instances: $placed_instances"
puts $rp "Congestion score: $congestion_score"
puts $rp "HPWL um: $hpwl_um"
close $rp

puts "place completed"

