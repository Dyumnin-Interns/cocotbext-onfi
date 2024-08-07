module dummy_dut(
    input clk,
    output wire RB_x_n,    
    input wire RE_x_n,
    input wire RE_x_c,
    input wire WR_x_n,
    input wire CE_x_n,
    input wire Vcc,
    input wire VccQ,
    input wire Vss,
    input wire VssQ,
    input wire VREFQ_x,
    input wire Vpp,
    input wire CLE_x,
    input wire ALE_x,
    input wire WE_x_n,
    input wire CLK_x,
    input wire WP_x_n,

    inout wire IO0_0,
    inout wire IO1_0,
    inout wire IO2_0,
    inout wire IO3_0,
    inout wire IO4_0,
    inout wire IO5_0,
    inout wire IO6_0,
    inout wire IO7_0,
    inout wire[7:0] IO_bus,
    inout wire IO8,
    inout wire IO9,
    inout wire IO10,
    inout wire IO11,
    inout wire IO12,
    inout wire IO13,
    inout wire IO14,
    inout wire IO15,

    inout wire IO0_1,
    inout wire IO1_1,
    inout wire IO2_1,
    inout wire IO3_1,
    inout wire IO4_1,
    inout wire IO5_1,
    inout wire IO6_1,
    inout wire IO7_1,

    inout wire DQS,
    inout wire DQS_x_c,
    inout wire DBI_x,

    output wire ENo,
    input wire ENi,
    inout wire VSP_x,
    output wire R,
    output wire RFT,
    inout wire NU,
    inout wire NC,
    inout wire ZQ_x
);
assign IO_bus = {IO7_0, IO6_0, IO5_0, IO4_0, IO3_0, IO2_0, IO1_0, IO0_0};

initial begin
        $display("Dummy DUT");
        $dumpfile("waveform.vcd");
        $dumpvars(0, dummy_dut);
    end
endmodule
