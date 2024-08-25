module top;
    reg clk;
    wire RE_x_n, RE_x_c, WR_x_n, CE_x_n, Vcc, VccQ, Vss, VssQ, VREFQ_x, Vpp;
    wire CLE_x, ALE_x, WE_x_n, CLK_x, WP_x_n;
    wire DQ0_0, IO1_0, IO2_0, IO3_0, IO4_0, IO5_0, IO6_0, IO7_0;
    wire IO8, IO9, IO10, IO11, IO12, IO13, IO14, IO15;
    wire IO0_1, IO1_1, IO2_1, IO3_1, IO4_1, IO5_1, IO6_1, IO7_1;
    wire IOS_x_t, IOS_x_c, DBI_x;
    wire ENo, ENi;
    wire VSP_x, R, RFT, NU, NC, ZQ_x;
    wire RB_x_n;
    wire [7:0] IO_bus;
    wire [7:0] IO0_bus;
    wire RE_0_n, RE_1_n, RE_0_c, RE_1_c, WR_0_n, WR_1_n, CE_0_n, CE_1_n, CLE_0, CLE_1, ALE_0, ALE_1,WE_0_n,WE_1_n, CLK_0, CLK_1, WP_0_n, WP_1_n;
    nand_controller u_nand_controller (
        .clk(clk),
        .RB_x_n(RB_x_n),
        .RE_x_n(RE_x_n),
        .RE_x_c(RE_x_c),
        .WR_x_n(WR_x_n),
        .CE_x_n(CE_x_n),
        .Vcc(Vcc),
        .VccQ(VccQ),
        .Vss(Vss),
        .VssQ(VssQ),
        .VREFQ_x(VREFQ_x),
        .Vpp(Vpp),
        .CLE_x(CLE_x),
        .ALE_x(ALE_x),
        .WE_x_n(WE_x_n),
        .CLK_x(CLK_x),
        .WP_x_n(WP_x_n),
        // LUN-specific signals for multiple LUNs
.RE_0_n(RE_0_n),
.RE_1_n(RE_1_n),
.RE_0_c(RE_0_c),
.RE_1_c(RE_1_c),
.WR_0_n(WR_0_n),
.WR_1_n(WR_1_n),
.CE_0_n(CE_0_n),
.CE_1_n(CE_1_n),
.CLE_0(CLE_0),
.CLE_1(CLE_1),
.ALE_0(ALE_0),
.ALE_1(ALE_1),
.WE_0_n(WE_0_n),
.WE_1_n(WE_1_n),
.CLK_0(CLK_0),
.CLK_1(CLK_1),
.WP_0_n(WP_0_n),
.WP_1_n(WP_1_n),







        // DQ0_0 - IO7_0 series
        .DQ0_0(DQ0_0),
        .IO1_0(IO1_0),
        .IO2_0(IO2_0),
        .IO3_0(IO3_0),
        .IO4_0(IO4_0),
        .IO5_0(IO5_0),
        .IO6_0(IO6_0),
        .IO7_0(IO7_0),
 .IO_bus(IO_bus),
        // IO8 - IO15 series
        .IO8(IO8),
        .IO9(IO9),
        .IO10(IO10),
        .IO11(IO11),
        .IO12(IO12),
        .IO13(IO13),
        .IO14(IO14),
        .IO15(IO15),

        // IO0_1 - IO7_1 series
        .IO0_1(IO0_1),
        .IO1_1(IO1_1),
        .IO2_1(IO2_1),
        .IO3_1(IO3_1),
        .IO4_1(IO4_1),
        .IO5_1(IO5_1),
        .IO6_1(IO6_1),
        .IO7_1(IO7_1),

        .IOS(IOS),
        .IOS_x_c(IOS_x_c),
        .DBI_x(DBI_x),
        .ENo(ENo),
        .ENi(ENi),
        .VSP_x(VSP_x),
        .R(R),
        .RFT(RFT),
        .NU(NU),
        .NC(NC),
        .ZQ_x(ZQ_x)
);

    // Instantiate the dummy_dut
    dummy_dut u_dummy_dut (
        .clk(clk),
	.RB_x_n(RB_x_n),
        .RE_x_n(RE_x_n),
        .RE_x_c(RE_x_c),
        .WR_x_n(WR_x_n),
        .CE_x_n(CE_x_n),
        .Vcc(Vcc),
        .VccQ(VccQ),
        .Vss(Vss),
        .VssQ(VssQ),
        .VREFQ_x(VREFQ_x),
        .Vpp(Vpp),
        .CLE_x(CLE_x),
        .ALE_x(ALE_x),
        .WE_x_n(WE_x_n),
        .CLK_x(CLK_x),
        .WP_x_n(WP_x_n),
// LUN-specific signals for multiple LUNs
.RE_0_n(RE_0_n),
.RE_1_n(RE_1_n),
.RE_0_c(RE_0_c),
.RE_1_c(RE_1_c),
.WR_0_n(WR_0_n),
.WR_1_n(WR_1_n),
.CE_0_n(CE_0_n),
.CE_1_n(CE_1_n),
.CLE_0(CLE_0),
.CLE_1(CLE_1),
.ALE_0(ALE_0),
.ALE_1(ALE_1),
.WE_0_n(WE_0_n),
.WE_1_n(WE_1_n),
.CLK_0(CLK_0),
.CLK_1(CLK_1),
.WP_0_n(WP_0_n),
.WP_1_n(WP_1_n),







        // DQ0_0 - IO7_0 series
        .DQ0_0(DQ0_0),
        .IO1_0(IO1_0),
        .IO2_0(IO2_0),
        .IO3_0(IO3_0),
        .IO4_0(IO4_0),
        .IO5_0(IO5_0),
        .IO6_0(IO6_0),
        .IO7_0(IO7_0),
        .IO_bus(IO_bus),
        // IO8 - IO15 series
        .IO8(IO8),
        .IO9(IO9),
        .IO10(IO10),
        .IO11(IO11),
        .IO12(IO12),
        .IO13(IO13),
        .IO14(IO14),
        .IO15(IO15),

        // IO0_1 - IO7_1 series
        .IO0_1(IO0_1),
        .IO1_1(IO1_1),
        .IO2_1(IO2_1),
        .IO3_1(IO3_1),
        .IO4_1(IO4_1),
        .IO5_1(IO5_1),
        .IO6_1(IO6_1),
        .IO7_1(IO7_1),

        .IOS(IOS),
        .IOS_x_c(IOS_x_c),
        .DBI_x(DBI_x),
        .ENo(ENo),
        .ENi(ENi),
        .VSP_x(VSP_x),
        .R(R),
        .RFT(RFT),
        .NU(NU),
        .NC(NC),
        .ZQ_x(ZQ_x)
);
assign IO0_bus = {DQ0_0, IO1_0, IO2_0, IO3_0, IO4_0, IO5_0, IO6_0, IO7_0};
assign IO_bus = {DQ0_0, IO1_0, IO2_0, IO3_0, IO4_0, IO5_0, IO6_0, IO7_0};
    initial begin
	$display("Top_level");
        $dumpfile("waveform.vcd");  // Specify the output file for waveform data
        $dumpvars(0, top);  
        clk = 0;
        forever #5 clk = ~clk;
 $monitor("Time: %0t, IO_bus: %h", $time, IO_bus);       
	// 100 MHz clock
    end
endmodule
