# Tcl step: synth
set run_dir [lindex $argv 0]
set design_dir [lindex $argv 1]
set metrics_path [lindex $argv 2]
set report_path [lindex $argv 3]

set rtl_files [glob -nocomplain -directory "$design_dir/rtl" *.v]
set rtl_count [llength $rtl_files]
set cell_count [expr {120 + $rtl_count * 17}]
set area_um2 [expr {$cell_count * 6.25}]
set wns_ns 0.18

set fp [open $metrics_path w]
puts $fp "step=synth"
puts $fp "rtl_files=$rtl_count"
puts $fp "cell_count=$cell_count"
puts $fp "area_um2=$area_um2"
puts $fp "wns_ns=$wns_ns"
close $fp

set rp [open $report_path w]
puts $rp "SYNTHESIS REPORT"
puts $rp "Design dir: $design_dir"
puts $rp "RTL files: $rtl_count"
puts $rp "Cell count: $cell_count"
puts $rp "Area um2: $area_um2"
puts $rp "WNS ns: $wns_ns"
close $rp

puts "synth completed"

