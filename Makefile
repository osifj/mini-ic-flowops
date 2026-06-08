.PHONY: doctor init ref testchip status qa report

doctor:
	./bin/flowctl doctor

init:
	./bin/flowctl init

ref:
	./bin/flowctl run --design alu --flow ref

testchip:
	./bin/flowctl run --design alu --flow testchip

status:
	./bin/flowctl status

qa:
	./bin/flowctl qa --design alu

report:
	./bin/flowctl report --run latest

