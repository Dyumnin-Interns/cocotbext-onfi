SIM ?= icarus
TOPLEVEL_LANG ?= verilog


TOPLEVEL?=top


VERILOG_SOURCES += $(PWD)/dummy_dut.v
VERILOG_SOURCES += $(PWD)/nand_controller.v
VERILOG_SOURCES += $(PWD)/top.v


MODULE = test_onfi

onfi:
	$(MAKE) sim MODULE=$(MODULE)

include $(shell cocotb-config --makefiles)/Makefile.sim
