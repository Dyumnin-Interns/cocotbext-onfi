SIM ?= icarus
TOPLEVEL_LANG ?= verilog

export PYTHONPATH := /home/om/tests/cocotbext-onfi/src/cocotbext/onfi
TOPLEVEL?=top


VERILOG_SOURCES += ../hdl/dummy_dut.v
VERILOG_SOURCES += ../hdl/nand_controller.v
VERILOG_SOURCES += ../hdl/top.v


MODULE = test_onfi

onfi:
	$(MAKE) sim MODULE=$(MODULE)

include $(shell cocotb-config --makefiles)/Makefile.sim
