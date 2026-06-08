# Tcl step: route
set run_dir [lindex $argv 0]
set design_dir [lindex $argv 1]
set metrics_path [lindex $argv 2]
set report_path [lindex $argv 3]

set routed_nets 86
set drc_violations 0
set antenna_violations 0

set fp [open $metrics_path w]
puts $fp "step=route"
puts $fp "routed_nets=$routed_nets"
puts $fp "drc_violations=$drc_violations"
puts $fp "antenna_violations=$antenna_violations"
close $fp

set rp [open $report_path w]
puts $rp "ROUTE REPORT"
puts $rp "Routed nets: $routed_nets"
puts $rp "DRC violations: $drc_violations"
puts $rp "Antenna violations: $antenna_violations"
close $rp

puts "route completed"

