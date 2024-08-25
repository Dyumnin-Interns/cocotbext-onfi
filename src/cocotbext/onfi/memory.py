'''def map_alternate_names(sigdict):
    new_sigdict = {}

    for main_name, aliases in sigdict.items():
        # If there are multiple aliases, assume the first one is the main name
        primary_name = aliases[0]
        for name in aliases:
            new_sigdict[name] = primary_name

    return new_sigdict'''

sigdict = {
    "RE_x_n": {"Primary name": "RE_x_n", "Secondary name": "RE_x_t"},
    "RE_x_c": {"Primary name": "RE_x_c", "Secondary name": None},
    "WR_x_n": {"Primary name": "WR_x_n", "Secondary name": None},
    "CE_x_n": {"Primary name": "CE_x_n", "Secondary name": None},
    "Vcc": {"Primary name": "Vcc", "Secondary name": None},
    "VccQ": {"Primary name": "VccQ", "Secondary name": None},
    "Vss": {"Primary name": "Vss", "Secondary name": None},
    "VssQ": {"Primary name": "VssQ", "Secondary name": None},
    "VREFQ_x": {"Primary name": "VREFQ_x", "Secondary name": None},
    "Vpp": {"Primary name": "Vpp", "Secondary name": None},
    "CLE_x": {"Primary name": "CLE_x", "Secondary name": None},
    "ALE_x": {"Primary name": "ALE_x", "Secondary name": None},
    "WE_x_n": {"Primary name": "WE_x_n", "Secondary name": None},
    "CLK_x": {"Primary name": "CLK_x", "Secondary name": None},
    "WP_x_n": {"Primary name": "WP_x_n", "Secondary name": None},
    "IO0_0": {"Primary name": "IO0_0", "Secondary name": "DQ0_0"},
    "IO1_0": {"Primary name": "IO1_0", "Secondary name": "DQ1_0"},
    "IO2_0": {"Primary name": "IO2_0", "Secondary name": "DQ2_0"},
    "IO3_0": {"Primary name": "IO3_0", "Secondary name": "DQ3_0"},
    "IO4_0": {"Primary name": "IO4_0", "Secondary name": "DQ4_0"},
    "IO5_0": {"Primary name": "IO5_0", "Secondary name": "DQ5_0"},
    "IO6_0": {"Primary name": "IO6_0", "Secondary name": "DQ6_0"},
    "IO7_0": {"Primary name": "IO7_0", "Secondary name": "DQ7_0"},
    "IO8": {"Primary name": "IO8", "Secondary name": None},
    "IO9": {"Primary name": "IO9", "Secondary name": None},
    "IO10": {"Primary name": "IO10", "Secondary name": None},
    "IO11": {"Primary name": "IO11", "Secondary name": None},
    "IO12": {"Primary name": "IO12", "Secondary name": None},
    "IO13": {"Primary name": "IO13", "Secondary name": None},
    "IO14": {"Primary name": "IO14", "Secondary name": None},
    "IO15": {"Primary name": "IO15", "Secondary name": None},
    "IO0_1": {"Primary name": "IO0_1", "Secondary name": "DQ0_1"},
    "IO1_1": {"Primary name": "IO1_1", "Secondary name": "DQ1_1"},
    "IO2_1": {"Primary name": "IO2_1", "Secondary name": "DQ2_1"},
    "IO3_1": {"Primary name": "IO3_1", "Secondary name": "DQ3_1"},
    "IO4_1": {"Primary name": "IO4_1", "Secondary name": "DQ4_1"},
    "IO5_1": {"Primary name": "IO5_1", "Secondary name": "DQ5_1"},
    "IO6_1": {"Primary name": "IO6_1", "Secondary name": "DQ6_1"},
    "IO7_1": {"Primary name": "IO7_1", "Secondary name": "DQ7_1"},
    "DQS_x_t": {"Primary name": "DQS_x_t", "Secondary name": "DQS"},
    "DQS_x_c": {"Primary name": "DQS_x_c", "Secondary name": None},
    "DBI_x": {"Primary name": "DBI_x", "Secondary name": None},
    "ENo": {"Primary name": "ENo", "Secondary name": None},
    "ENi": {"Primary name": "ENi", "Secondary name": None},
    "VSP_x": {"Primary name": "VSP_x", "Secondary name": None},
    "R": {"Primary name": "R", "Secondary name": None},
    "RFT": {"Primary name": "RFT", "Secondary name": None},
    "NU": {"Primary name": "NU", "Secondary name": None},
    "NC": {"Primary name": "NC", "Secondary name": None},
    "ZQ_x": {"Primary name": "ZQ_x", "Secondary name": None}
}



'''
# Applying the function
mapped_sigdict = map_alternate_names(sigdict)

# Result
print(mapped_sigdict)
'''
