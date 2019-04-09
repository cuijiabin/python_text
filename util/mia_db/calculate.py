import util as bm


def get_precent(a, b):
    if b == 0 or b is None:
        return ""
    else:
        return round(a / b * 100, 2)


def get_warehouse_id(supper_id):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "SELECT id FROM stock_warehouse WHERE supplier_id = " + str(supper_id)
    cur.execute(sql)
    result_data = cur.fetchall()
    return result_data[0][0]


def get_business_id_ng(supper_id):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "SELECT business_id_ng FROM customer_supplier WHERE id = " + str(supper_id)
    cur.execute(sql)
    result_data = cur.fetchall()
    return result_data[0][0]


def get_trac_rate(supper_id):
    warehouse_id = get_warehouse_id(supper_id)

    cur = bm.get_mia_cursor("mia_mirror")
    sql1 = "select COUNT(ntii.id) from new_trac_issue_info ntii INNER JOIN orders o ON o.order_code = ntii.order_code " \
           "WHERE ntii.create_time >= '2018-11-07 00:00:00' " \
           "AND ntii.status = 30 " \
           "AND o.warehouse_id = " + str(warehouse_id)

    cur.execute(sql1)
    result_data = cur.fetchall()
    r1 = result_data[0][0]

    sql2 = "select COUNT(ntii.id) from new_trac_issue_info ntii INNER JOIN orders o ON o.order_code = ntii.order_code " \
           "WHERE ntii.create_time >= '2018-11-07 00:00:00' AND o.warehouse_id = " + str(warehouse_id)

    cur.execute(sql2)
    result_data = cur.fetchall()
    r2 = result_data[0][0]

    return (r1, r2)


def get_category_rate(supper_id):
    warehouse_id = get_warehouse_id(supper_id)
    business_id_ng = get_business_id_ng(supper_id)
    cur = bm.get_mia_cursor("mia_mirror")

    sql = "SELECT sum(o.pay_price) as price FROM mia_mirror.orders o WHERE o.warehouse_id = " + str(
        warehouse_id) + " AND o.order_time >= '2018-11-07' AND o.order_time < '2018-12-07'"
    cur.execute(sql)
    result_data = cur.fetchall()
    r0 = result_data[0][0]

    sql = "SELECT sum(oi.pay_price) as price " \
          "FROM mia_mirror.orders o  " \
          "LEFT JOIN order_item oi  ON o.id = oi.order_id " \
          "LEFT JOIN stock_item si ON si.id = oi.stock_item_id  " \
          "LEFT JOIN item i ON i.id = si.item_id " \
          "WHERE o.warehouse_id = " + str(warehouse_id) \
          + " AND o.order_time >= '2018-11-07' " \
            "AND o.order_time < '2018-12-07' " \
            "AND i.category_id_ng = " + str(business_id_ng)

    cur.execute(sql)
    result_data = cur.fetchall()
    r1 = result_data[0][0]

    sql = "SELECT sum(o.pay_price) as price FROM mia_mirror.orders o WHERE o.warehouse_id = " + str(
        warehouse_id) + " AND o.order_time >= '2018-12-07'"
    cur.execute(sql)
    result_data = cur.fetchall()
    r2 = result_data[0][0]

    sql = "SELECT sum(oi.pay_price) as price " \
          "FROM mia_mirror.orders o  " \
          "LEFT JOIN order_item oi  ON o.id = oi.order_id " \
          "LEFT JOIN stock_item si ON si.id = oi.stock_item_id  " \
          "LEFT JOIN item i ON i.id = si.item_id " \
          "WHERE o.warehouse_id = " + str(warehouse_id) \
          + " AND o.order_time >= '2018-12-07' " \
            "AND i.category_id_ng =" + str(business_id_ng)

    cur.execute(sql)
    result_data = cur.fetchall()
    r3 = result_data[0][0]

    return (r0, r1, r2, r3, business_id_ng)


if __name__ == "__main__":
    supplier_ids = [4, 6, 7, 10, 11, 17, 22, 29, 35, 36, 62, 78, 79, 103, 113, 140, 173, 200, 207, 226, 228, 230, 232,
                    251, 253, 254, 257, 260, 262, 264, 265, 271, 277, 281, 282, 291, 311, 336, 357, 351, 353, 367, 377,
                    373, 389, 436, 434, 431, 459, 458, 463, 479, 462, 476, 481, 497, 490, 516, 503, 510, 515, 517, 527,
                    542, 544, 550, 557, 583, 569, 570, 579, 624, 671, 605, 593, 598, 595, 596, 663, 629, 642, 630, 640,
                    634, 636, 637, 660, 682, 659, 658, 675, 720, 701, 738, 756, 788, 755, 764, 834, 839, 783, 786, 813,
                    814, 849, 833, 851, 889, 930, 1976, 896, 895, 897, 892, 912, 910, 962, 932, 940, 972, 952, 1003,
                    957, 1009, 1027, 1071, 1081, 1067, 1085, 1106, 1103, 1104, 1110, 1121, 1131, 1133, 1168, 1174, 1179,
                    1258, 1189, 1217, 1247, 1229, 1248, 1230, 1281, 1300, 1301, 1329, 1383, 1363, 1393, 1346, 1412,
                    1362, 1347, 1443, 1413, 1392, 1461, 2051, 1649, 6271, 1484, 1485, 1459, 1487, 1483, 1644, 1473,
                    1600, 1646, 1608, 1504, 1523, 1533, 1606, 1582, 1645, 1597, 1584, 1605, 1610, 1667, 1545, 1652,
                    1583, 1622, 1722, 1613, 1615, 1686, 1689, 1726, 1702, 1692, 1691, 1706, 2085, 1637, 1714, 1750,
                    1671, 1783, 1740, 1713, 1721, 1709, 1805, 1679, 1759, 1774, 1723, 1828, 1733, 2226, 1838, 1739,
                    1738, 1776, 1757, 1795, 1763, 1794, 1766, 1756, 1785, 1844, 1792, 1847, 1809, 1818, 1907, 1945,
                    1871, 1883, 1824, 1920, 1842, 1840, 1820, 1841, 1888, 1891, 1863, 1872, 1831, 1856, 2082, 1851,
                    1898, 2045, 1887, 1886, 2059, 1931, 1893, 1896, 2233, 1922, 1921, 1925, 2049, 1980, 2148, 1959,
                    1962, 1966, 1979, 1961, 2033, 1991, 2042, 2035, 2147, 2034, 2203, 1975, 2073, 1977, 1985, 1967,
                    1978, 4490, 1974, 2040, 2252, 2024, 2257, 2312, 2125, 2185, 2023, 2074, 2081, 2031, 2052, 2124,
                    2060, 2120, 2197, 2079, 2273, 2215, 2222, 2399, 2123, 2221, 2375, 2408, 2207, 2112, 2426, 2097,
                    2461, 2190, 2218, 2623, 2208, 2174, 2262, 2229, 2153, 2193, 2225, 2253, 2296, 2219, 2298, 2189,
                    2328, 2266, 2502, 2259, 2310, 2318, 2241, 2291, 2367, 2474, 2311, 2362, 2400, 2552, 2356, 2377,
                    2803, 2345, 2519, 2487, 2655, 2667, 2492, 2539, 2483, 2378, 2468, 2544, 2486, 2432, 2448, 2470,
                    2441, 3158, 2521, 2554, 2644, 2497, 2657, 2570, 2546, 2491, 2559, 2569, 2573, 2626, 2680, 2610,
                    2640, 2694, 2690, 2647, 2634, 2631, 5211, 3875, 2882, 2721, 2741, 2829, 2912, 2742, 2845, 2822,
                    2729, 2798, 2854, 3650, 2877, 2795, 2870, 2838, 2922, 2891, 2936, 2892, 2970, 2851, 2895, 2873,
                    2940, 2927, 2872, 3984, 2926, 3006, 2942, 3098, 2990, 2943, 2984, 2959, 2976, 3177, 3672, 3030,
                    3007, 2995, 3009, 3024, 3079, 3011, 3049, 3248, 3045, 3065, 3188, 3050, 3056, 3160, 3047, 3083,
                    3059, 3086, 3073, 3082, 3084, 3107, 3134, 3194, 3537, 3240, 3141, 3167, 3149, 3238, 3164, 3193,
                    3249, 3166, 3191, 3189, 3236, 3228, 3202, 3409, 3224, 3220, 3308, 3260, 3798, 3261, 3255, 3330,
                    3360, 3327, 3402, 3314, 3286, 3304, 3279, 3351, 3317, 3338, 3302, 4060, 3319, 3329, 3349, 3355,
                    3374, 3689, 3661, 3446, 3426, 3411, 3492, 3417, 3721, 3506, 3419, 3674, 3515, 3456, 5027, 3493,
                    3474, 3496, 3484, 3520, 3579, 3554, 3590, 3572, 3545, 3636, 3539, 3635, 3723, 3551, 3639, 3571,
                    3632, 3555, 3642, 3690, 3718, 3666, 3651, 3622, 3698, 3677, 3641, 3631, 6686, 3649, 3781, 6336,
                    3670, 3767, 3673, 3669, 3894, 3675, 3719, 3682, 3692, 3726, 3700, 3688, 5539, 3730, 3728, 3874,
                    3750, 3746, 3773, 3763, 3764, 3749, 3895, 3760, 3786, 3846, 3775, 3785, 3870, 3852, 3809, 3850,
                    3832, 3848, 3868, 3988, 3866, 3919, 3937, 3934, 3942, 3936, 3995, 4659, 3940, 3927, 3970, 3924,
                    3964, 3952, 3978, 4486, 3975, 3974, 3977, 3980, 3994, 4092, 4015, 4002, 4028, 3991, 3986, 4035,
                    4014, 4011, 4018, 4038, 4041, 4044, 4039, 5963, 4054, 4083, 4201, 4053, 4050, 4089, 4073, 4431,
                    4097, 4131, 4078, 4076, 4071, 4075, 4072, 4085, 4142, 4080, 4104, 4122, 4099, 4101, 6275, 4232,
                    4279, 4149, 4182, 4124, 4167, 4123, 4125, 4130, 4129, 4132, 4184, 4140, 4138, 4139, 4148, 4137,
                    4150, 4169, 4146, 4143, 4164, 4158, 4154, 4321, 4209, 4163, 4242, 4170, 4173, 4172, 4178, 4174,
                    4205, 4193, 4216, 4224, 4253, 4199, 4233, 4188, 4379, 4215, 4221, 4196, 4599, 4453, 4204, 4547,
                    4222, 4394, 4410, 4212, 4228, 4218, 4227, 4211, 4426, 4254, 4259, 4412, 4269, 4255, 4260, 4247,
                    4238, 4267, 4244, 4277, 4299, 4256, 4548, 4271, 4282, 4293, 4270, 4265, 4313, 4266, 4328, 4298,
                    4300, 4273, 4308, 4341, 4376, 4305, 4414, 4291, 4304, 4324, 4312, 4399, 4315, 4311, 4297, 4411,
                    4330, 4335, 4310, 4358, 4318, 4307, 4381, 4317, 4325, 4366, 4319, 4320, 4413, 4361, 4339, 4337,
                    4348, 4365, 4355, 4346, 4362, 4390, 4372, 4367, 4368, 4392, 4359, 5239, 4461, 4360, 4369, 4472,
                    4382, 4506, 4383, 4417, 4377, 4385, 4404, 4416, 4400, 4484, 4430, 4428, 4457, 4425, 4406, 4435,
                    4531, 4465, 4444, 4409, 4427, 4408, 4423, 4447, 4467, 4433, 4504, 4462, 4523, 4436, 4569, 4469,
                    4473, 4450, 4459, 4466, 4526, 4463, 4481, 4464, 4544, 4509, 4507, 4973, 5041, 4483, 4491, 4549,
                    4527, 4521, 4593, 4671, 4515, 4501, 4503, 4529, 4568, 4545, 4546, 4524, 4554, 4627, 4536, 4540,
                    4532, 4579, 4538, 4542, 4964, 4560, 4567, 4539, 4558, 4654, 4605, 4556, 4587, 4566, 4557, 4551,
                    4602, 4592, 4564, 4652, 4572, 4611, 4600, 4580, 4573, 4585, 4653, 4744, 5349, 4662, 4578, 4661,
                    4581, 4591, 4597, 4660, 4610, 4617, 4609, 4657, 4606, 4613, 4618, 4628, 4939, 4624, 4621, 4672,
                    4770, 4663, 4623, 4616, 4632, 4664, 4620, 4625, 4635, 4637, 4633, 4693, 4639, 4680, 4695, 4643,
                    4766, 4642, 4648, 4721, 4670, 4852, 4677, 4720, 4669, 4735, 4685, 4678, 4741, 4742, 4739, 4682,
                    4681, 4689, 4696, 4694, 5039, 4705, 4691, 5269, 4722, 4710, 4709, 4692, 4703, 4724, 4690, 4698,
                    4751, 4687, 4701, 4716, 4719, 4750, 4697, 4718, 4713, 4717, 4731, 4728, 4738, 4882, 4823, 4819,
                    4803, 4804, 4752, 4730, 4758, 4822, 4817, 4753, 4767, 4782, 4779, 4815, 4783, 4854, 4863, 4842,
                    4772, 4824, 4864, 4818, 4850, 4775, 4960, 4813, 4797, 4837, 4773, 4812, 4928, 4774, 4800, 4839,
                    4832, 4806, 4811, 4814, 4846, 4838, 4848, 4912, 4858, 4859, 4867, 4895, 4894, 4945, 4862, 4918,
                    4874, 4868, 4872, 4890, 4881, 4941, 4975, 4916, 4889, 4929, 4911, 4888, 4902, 4932, 4897, 4898,
                    5382, 4922, 4910, 4931, 4908, 4913, 4994, 4923, 4957, 4979, 4989, 4925, 5035, 4947, 4921, 4984,
                    4965, 4969, 4935, 4943, 5528, 5072, 5031, 4956, 4955, 5077, 4954, 5515, 4996, 4958, 4966, 4972,
                    5102, 4968, 5005, 5011, 4976, 5235, 4988, 5108, 4993, 5012, 5026, 4998, 5013, 5015, 4997, 5044,
                    5029, 5020, 5018, 5034, 5017, 5040, 5024, 5021, 5022, 5032, 5025, 5030, 5071, 5056, 5088, 5069,
                    5055, 5073, 5042, 5037, 5063, 5104, 5060, 5066, 5090, 5070, 5082, 5080, 5113, 5183, 5134, 5089,
                    5076, 5085, 5100, 5097, 5101, 5115, 5237, 5238, 5096, 5145, 5117, 5122, 5119, 5116, 5114, 5118,
                    5123, 5147, 5110, 5125, 5128, 5138, 5127, 5124, 5130, 5148, 5149, 5257, 5152, 5142, 5212, 5160,
                    5158, 5233, 5204, 5151, 5157, 5223, 5209, 5227, 5205, 5264, 5208, 5385, 5325, 5361, 5179, 5168,
                    5200, 5324, 5210, 5177, 5170, 5298, 5175, 5165, 5184, 5201, 5174, 5247, 5190, 5192, 5197, 5191,
                    5189, 5213, 5202, 5203, 5214, 5218, 5317, 5216, 5219, 5215, 5358, 5265, 5226, 5229, 5270, 5268,
                    5251, 5231, 5228, 5232, 5274, 5250, 5243, 5253, 5245, 5273, 5267, 5297, 5272, 5279, 5283, 5276,
                    5263, 5249, 7058, 5252, 5329, 5259, 5271, 5281, 5290, 5310, 5296, 5307, 5291, 5341, 5292, 5302,
                    5331, 5344, 5280, 5335, 5309, 5368, 5305, 5372, 5343, 5334, 5333, 5312, 5347, 5314, 5318, 5332,
                    5321, 5354, 5351, 5348, 5322, 5390, 5330, 5750, 5414, 6241, 5386, 5345, 5338, 5373, 5355, 5493,
                    5350, 5592, 5365, 5353, 5468, 5352, 5366, 5455, 5432, 5425, 5374, 5456, 5383, 5437, 5376, 5379,
                    5369, 5371, 5429, 5421, 5424, 5419, 5389, 5394, 5395, 5378, 5402, 5377, 5391, 5384, 5393, 5407,
                    5462, 6721, 5431, 5411, 5492, 5420, 5436, 5417, 5413, 5487, 5426, 5410, 5404, 5655, 5460, 5403,
                    5422, 5409, 5510, 5440, 5408, 5484, 5427, 5423, 5451, 5430, 5519, 5498, 5428, 5452, 5446, 5496,
                    5438, 5714, 5466, 5459, 5458, 5649, 5453, 5442, 5509, 5471, 5449, 5445, 5500, 5507, 5495, 5469,
                    5481, 5491, 5494, 5557, 5480, 6794, 5502, 5488, 5478, 5522, 5504, 5505, 5474, 5542, 5526, 5520,
                    5540, 5523, 5524, 5477, 5499, 5586, 5514, 5623, 5594, 5512, 5527, 5556, 5563, 5578, 5717, 7379,
                    5521, 5718, 5534, 5531, 5543, 5564, 5652, 5532, 5720, 5536, 5548, 5607, 5533, 5530, 5869, 5719,
                    5584, 5588, 5590, 5979, 6263, 5568, 5790, 5589, 5537, 5632, 5624, 5618, 5559, 5561, 5541, 5571,
                    5582, 5545, 5546, 5692, 5587, 5577, 5567, 5550, 5691, 5558, 5583, 5575, 5631, 5658, 5573, 5562,
                    5595, 5591, 5641, 5574, 5758, 5683, 5617, 5633, 5601, 5630, 5651, 5585, 5616, 5640, 5600, 5712,
                    5647, 5619, 5581, 5895, 5566, 5782, 5596, 5910, 5735, 5610, 5772, 5667, 5741, 5650, 5636, 5687,
                    5635, 5637, 5754, 5659, 5708, 5621, 5629, 5973, 5627, 5736, 5783, 5703, 5690, 5602, 5722, 5620,
                    5728, 5638, 5643, 5948, 5639, 5645, 5660, 5613, 5661, 5673, 5628, 5898, 5757, 5646, 5668, 5679,
                    5672, 5700, 5704, 5656, 5653, 5663, 5686, 5662, 5699, 5648, 5654, 5842, 5674, 5676, 5678, 5675,
                    5681, 5928, 5883, 5684, 5707, 5706, 5694, 5731, 5775, 5864, 5737, 5755, 5851, 5713, 5746, 5695,
                    6371, 5726, 5809, 5724, 5810, 6461, 5751, 5815, 5814, 5701, 5711, 5702, 5734, 5841, 5733, 5771,
                    5923, 5773, 5723, 5738, 5732, 5749, 5768, 5767, 5747, 5808, 6521, 5727, 5745, 5778, 5811, 5763,
                    5756, 5933, 6184, 5863, 5776, 5812, 6247, 6194, 5760, 5819, 5830, 5761, 5818, 5804, 5766, 5759,
                    5850, 5862, 5962, 5780, 5947, 5937, 5827, 5885, 5792, 5786, 5793, 5834, 5925, 5801, 5932, 5789,
                    5781, 5788, 5777, 5972, 5799, 6382, 5840, 5787, 5899, 5785, 6560, 5911, 5817, 5927, 5796, 5832,
                    5865, 5824, 5873, 5983, 5874, 5944, 5821, 6616, 6023, 5822, 5901, 6579, 5931, 5974, 6244, 5845,
                    5820, 5857, 5880, 5922, 6031, 5909, 5976, 5966, 5902, 6192, 5900, 5875, 5847, 5929, 6596, 5924,
                    5892, 6523, 5896, 5852, 6274, 5975, 5867, 6643, 5907, 5856, 5915, 5921, 5860, 5891, 5877, 5930,
                    5949, 5904, 5882, 5859, 5905, 5876, 5866, 5890, 5888, 5950, 5887, 6195, 6550, 6026, 5897, 6029,
                    6032, 5914, 5988, 5886, 6259, 6243, 5919, 5918, 5980, 6316, 5961, 5912, 5970, 6264, 6795, 5913,
                    5964, 5936, 5884, 6330, 5965, 6193, 5960, 5959, 5990, 5971, 5941, 5953, 6237, 6276, 5939, 5934,
                    6230, 5958, 6682, 5951, 6273, 5978, 6698, 6650, 6022, 5954, 6256, 6028, 6245, 6232, 6984, 6321,
                    5986, 5985, 6337, 6261, 6187, 6239, 6191, 6198, 6190, 6188, 6027, 6319, 6418, 6236, 6360, 6262,
                    6272, 6324, 6258, 6197, 6242, 6345, 6695, 6449, 6340, 6254, 6326, 6284, 6339, 6338, 6417, 6279,
                    6512, 6249, 6327, 6416, 6320, 6291, 6290, 6323, 6289, 6288, 6383, 6285, 6636, 6969, 6318, 6403,
                    6315, 6361, 6310, 6311, 6415, 6313, 6567, 6332, 6309, 6377, 6349, 6344, 6414, 6413, 6331, 6420,
                    6474, 6370, 6475, 6369, 6576, 6407, 6443, 6447, 6368, 6440, 6496, 6549, 6467, 7500, 6385, 6425,
                    6423, 6424, 6509, 6756, 6619, 6446, 6580, 6419, 6459, 6448, 6482, 6464, 6463, 6481, 6480, 6479,
                    6813, 6485, 6473, 6491, 6478, 6484, 6476, 6499, 6515, 6506, 6505, 6559, 6511, 6502, 6507, 6862,
                    6519, 6524, 6581, 6627, 6544, 6518, 6528, 6517, 6629, 6533, 6670, 6546, 6525, 6865, 6527, 6534,
                    6551, 6659, 6568, 6578, 6970, 6555, 6622, 6594, 6599, 6585, 6607, 6620, 6572, 6574, 6644, 6575,
                    6601, 6595, 6612, 6664, 6593, 6582, 6592, 6625, 6630, 6632, 6663, 6588, 6587, 6606, 6609, 6604,
                    6611, 6626, 6694, 6608, 6615, 6660, 6904, 6672, 6747, 6633, 6631, 6666, 6641, 7296, 6638, 6648,
                    6651, 6652, 6649, 6645, 6684, 6657, 6655, 6656, 6673, 6678, 6807, 6746, 6702, 6724, 6667, 6707,
                    6811, 6730, 6800, 6710, 6703, 6683, 6838, 6753, 6685, 6687, 6749, 6741, 6737, 6720, 6711, 6692,
                    6723, 6752, 6725, 6700, 6762, 6734, 6750, 6784, 6722, 6718, 6735, 6716, 6736, 6902, 6738, 6866,
                    6745, 6805, 6890, 6759, 6742, 6842, 6775, 6848, 6758, 6765, 6755, 6818, 6769, 6770, 6754, 6806,
                    6785, 6781, 6793, 6810, 6801, 6918, 6835, 6897, 6799, 6831, 6792, 6791, 6828, 6849, 6798, 6841,
                    6797, 6796, 6864, 6966, 6814, 6809, 6847, 6837, 6824, 6830, 6833, 6987, 7021, 6912, 6889, 6851,
                    6859, 6863, 6892, 6850, 6914, 7007, 6853, 6941, 6860, 6894, 6869, 6953, 7298, 6968, 6992, 6868,
                    6867, 7380, 6978, 6874, 6888, 6927, 7024, 6903, 7026, 6885, 6928, 6886, 6944, 6884, 6883, 6882,
                    6891, 6881, 6911, 6915, 6901, 7151, 6950, 7157, 6906, 6917, 6947, 6979, 6955, 6951, 7029, 6908,
                    6960, 6937, 6949, 6954, 6948, 6939, 6926, 6943, 6990, 7097, 6972, 6977, 6963, 6964, 6942, 6956,
                    7369, 6957, 7072, 7032, 7538, 7069, 7027, 7057, 7003, 7013, 7082, 6967, 7055, 7046, 6995, 6975,
                    7076, 7015, 7019, 7002, 7189, 6980, 7054, 6996, 6989, 7040, 6997, 7018, 7147, 7133, 7042, 7044,
                    6999, 7016, 7014, 6998, 7012, 7078, 7158, 7037, 7041, 7017, 7050, 7067, 7030, 7036, 7073, 7068,
                    7043, 7113, 7039, 7047, 7031, 7023, 7071, 7049, 7052, 7048, 7045, 7051, 7077, 7161, 7080, 7096,
                    7070, 7100, 7066, 7254, 7152, 7063, 7064, 7062, 7106, 7172, 7093, 7148, 7086, 7134, 7089, 7091,
                    7103, 7105, 7193, 7143, 7101, 7140, 7112, 7197, 7130, 7111, 7118, 7169, 7117, 7115, 7424, 7132,
                    7129, 7116, 7154, 7179, 7126, 7136, 7138, 7139, 7144, 7430, 7149, 7188, 7215, 7205, 7173, 7159,
                    7153, 7168, 7268, 7223, 7174, 7227, 7160, 7282, 7180, 7198, 7187, 7192, 7195, 7191, 7185, 7245,
                    7252, 7186, 7284, 7225, 7540, 7218, 7234, 7399, 7230, 7203, 7210, 7386, 7209, 7236, 7211, 7224,
                    7259, 7261, 7229, 7216, 7267, 7243, 7251, 7248, 7244, 7426, 7406, 7300, 7319, 7372, 7277, 7253,
                    7308, 7255, 7258, 7318, 7979, 7269, 7317, 7341, 7327, 7280, 7315, 7272, 7281, 7682, 7321, 7279,
                    7291, 7283, 7328, 7292, 7303, 7408, 7301, 7297, 7302, 7335, 7384, 7314, 7788, 7307, 7395, 7312,
                    7360, 7333, 7414, 7390, 7356, 7342, 7346, 7345, 7339, 7334, 7350, 7355, 7385, 7375, 7771, 7371,
                    7348, 7347, 7361, 7387, 7383, 7442, 7507, 7370, 7396, 7377, 7374, 7376, 7513, 7388, 7394, 7382,
                    7439, 7381, 7403, 7391, 7392, 7398, 7418, 7402, 7412, 7450, 7411, 7504, 7419, 7420, 7421, 7422,
                    7429, 7425, 7427, 7517, 7413, 7423, 7435, 7465, 7468, 7457, 7454, 7428, 7458, 7466, 7446, 7453,
                    7476, 7499, 7544, 7512, 7488, 7479, 7485, 7474, 7475, 7518, 7482, 7508, 7473, 7463, 7483, 7467,
                    7480, 7464, 7471, 7497, 7491, 7484, 7487, 7528, 7481, 7520, 7498, 7553, 7511, 7501, 7495, 7492,
                    7496, 7519, 7505, 7539, 7502, 7503, 7716, 7533, 7516, 7514, 7530, 7542, 7535, 7597, 7532, 7543,
                    7551, 7531, 7558, 7548, 7559, 7579, 7537, 7541, 7536, 7547, 7557, 7546, 7571, 7555, 7582, 7552,
                    7576, 7556, 7581, 7625, 7569, 7575, 7562, 7574, 7584, 7561, 7572, 7567, 7585, 7568, 7570, 7573,
                    7580, 7603, 7587, 7620, 7609, 7606, 7616, 7604, 7633, 7627, 7615, 7614, 7608, 7623, 7672, 7637,
                    7619, 7634, 7617, 7629, 7636, 7643, 7662, 7720, 7676, 7630, 7635, 7659, 7656, 7641, 7640, 7644,
                    7652, 7647, 7661, 7653, 7658, 7665, 7657, 7691, 7660, 7678, 7670, 7727, 7668, 7781, 7671, 7673,
                    7677, 7765, 7679, 7687, 7680, 7684, 7685, 7686, 7696, 7692, 7688, 7711, 7690, 7706, 7694, 7689,
                    7709, 7705, 7699, 7708, 7693, 7695, 7704, 7702, 7743, 7715, 7710, 7748, 7718, 7719, 7725, 7713,
                    7712, 7721, 7732, 7728, 7730, 7734, 7726, 7729, 7756, 7724, 7722, 7723, 7776, 7739, 7735, 7731,
                    7775, 7762, 7744, 7749, 7757, 7747, 7750, 7769, 7754, 7766, 7751, 7770, 7753, 7760, 7763, 7899,
                    7768, 7764, 7810, 7822, 7780, 7783, 7823, 7774, 7773, 7772, 7786, 7789, 7782, 7784, 7811, 7779,
                    7787, 7777, 7791, 7785, 7796, 7793, 7908, 7850, 7813, 7792, 7808, 7804, 7797, 7816, 7801, 7800,
                    7814, 7802, 7799, 7840, 7805, 7859, 7803, 7806, 7807, 7809, 7863, 7817, 7812, 7818, 7820, 7827,
                    7819, 7867, 7834, 7845, 7842, 7826, 7839, 7825, 7824, 7858, 7831, 7832, 7837, 7838, 7854, 7846,
                    7897, 7843, 7844, 7860, 7865, 7881, 7861, 7862, 7880, 7877, 7874, 7869, 7868, 7879, 7872, 7873,
                    7875, 7888, 7870, 7878, 7876, 7892, 7884, 7883, 7885, 7882, 7891, 7913, 7909, 7900, 7889, 7905,
                    7886, 7893, 7894, 7896, 7906, 7904, 7929, 7920, 7903, 7950, 7907, 7914, 7911, 7916, 7910, 7912,
                    7918, 7942, 7915, 7937, 7930, 7925, 7917, 7919, 7922, 7923, 7932, 7921, 7934, 7935, 7924, 7928,
                    7926, 7927, 7939, 7954, 7947, 7941, 7938, 7944, 7960, 7940, 7943, 7946, 7968, 7945, 7961, 7948,
                    7949, 7965, 7957, 7953, 7977, 7956, 7958, 7964, 7962, 7963, 7969, 7975, 7992, 7981, 7989, 7971,
                    7972, 7985, 7999, 7997, 7983, 7978, 7987, 7982, 8005, 8004, 8000, 8006]
    for supplier_id in supplier_ids:
        data1 = get_trac_rate(supplier_id)
        data2 = get_category_rate(supplier_id)
        # print(supplier_id, get_precent(data[1], data[0]))
        print(supplier_id, data1, data2)
