#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import traceback
import logging


# 解析字符串，得到指标值
def getMetricValue(metric_values, metricId):
    # 有逗号分隔
    if metric_values.find(',') > 0:
        arrs = metric_values.split(',')
        for arr in arrs:
            metric_id = arr.split(':')[0]
            metric_value = arr.split(':')[1]
            if metric_id == metricId:
                return metric_value
    # 没有逗号分隔
    if metric_values.find(',') == -1:
        metric_id = metric_values.split(':')[0]
        metric_value = metric_values.split(':')[1]
        if metric_id == metricId:
            return metric_value
    return '-1'


# 计算业务退改单维度200101
def cmpReturnWoDim(metric_values):
    dim_value = 0
    return_wo_ratio = float(getMetricValue(metric_values, '100221'))
    return_wo_num = float(getMetricValue(metric_values, '100209'))
    if return_wo_num <= 3:
        if return_wo_ratio >= 0 and return_wo_ratio < 0.24:
            dim_value = round((0.24 - return_wo_ratio) / 0.24 * (100 - 75)) + 75
        elif return_wo_ratio >= 0.24 and return_wo_ratio < 0.43:
            dim_value = round((0.43 - return_wo_ratio) / (0.43 - 0.24) * (75 - 50)) + 50
        elif return_wo_ratio >= 0.43 and return_wo_ratio <= 1:
            dim_value = round((1 - return_wo_ratio) / (1 - 0.43) * 15 + 35)
    elif return_wo_num > 3 and return_wo_num < 10:
        dim_value = round((1 - return_wo_ratio) * 50)
    else:
        dim_value = 0
    return str(dim_value)


# 地址覆盖维度200102
def cmpAddrCoverDim(metric_values):
    dim_value = 0
    addr_co_num = float(getMetricValue(metric_values, '100210'))
    error_co_num = float(getMetricValue(metric_values, '100211'))
    addr_co_ratio = float(getMetricValue(metric_values, '100212'))
    if addr_co_ratio < 0:
        addr_co_ratio = 1
    if error_co_num == 0:
        dim_value = 100
    if error_co_num > 0:
        if addr_co_num >= 145:
            dim_value = round(100 * (1 - 10 * (1 - addr_co_ratio)))
        if dim_value < 0:
            dim_value = round(100 * addr_co_ratio)
        elif addr_co_num >= 20 and addr_co_num < 145:
            dim_value = round(100 * (1 - 5 * (1 - addr_co_ratio)))
        if dim_value < 0:
            dim_value = round(100 * addr_co_ratio)
        else:
            dim_value = round(100 * addr_co_ratio)
    return str(dim_value)


# 自动配置维度1004
def cmpAutoConfReteDim(metric_values):
    dim_value = 0
    auto_con_ratio = float(getMetricValue(metric_values, '100107'))
    one_auto_ratio = float(getMetricValue(metric_values, '100109'))
    not_auto_num = float(getMetricValue(metric_values, '100103'))
    if not_auto_num > 5:
        dim_value = 0
    else:
        dim_value = round(auto_con_ratio * 50 + one_auto_ratio * 50)
    if dim_value > 100 or dim_value < 0:
        dim_value = 100
    return str(dim_value)


# 端口容量维度1005
def cmpPortCapacityDim(metric_values):
    dim_value = 0
    port_use_ratio = float(getMetricValue(metric_values, '100311'))
    port_num = float(getMetricValue(metric_values, '100309'))
    if port_num >= 64:
        if port_use_ratio > 0.72 and port_use_ratio <= 1:
            dim_value = round((1 - port_use_ratio) / (1 - 0.72) * (100 - 40)) + 30
        elif port_use_ratio >= 0 and port_use_ratio < 0.25:
            dim_value = round(port_use_ratio / 0.25 * (100 - 30)) + 30
        else:
            dim_value = 100
    if port_num > 8 and port_num < 64:
        if port_use_ratio > 0.75 and port_use_ratio <= 1:
            dim_value = round((1 - port_use_ratio) / (1 - 0.75) * (100 - 50)) + 50
        elif port_use_ratio >= 0 and port_use_ratio < 0.25:
            dim_value = round(port_use_ratio / 0.25 * (100 - 50)) + 50
        else:
            dim_value = 100

    if port_num <= 8:
        if port_use_ratio > 0.75 and port_use_ratio <= 1:
            dim_value = round((1 - port_use_ratio) / (1 - 0.75) * (100 - 50)) + 75
        elif port_use_ratio >= 0 and port_use_ratio < 0.25:
            dim_value = round(port_use_ratio / 0.25 * (100 - 50)) + 75
        else:
            dim_value = 100

    if dim_value > 100:
        dim_value = 100

    return str(dim_value)


# 服务质量维度1006
def cmpServQualityDim(metric_values, spec_id):
    dim_value = 0
    net_num = float(getMetricValue(metric_values, '110201'))
    rate_ratio = float(getMetricValue(metric_values, '110204'))

    dim_value = round(100 - 0.35 * 100 * net_num - 0.5 * 100 * rate_ratio)
    # OLT设备
    if spec_id == '415':
        dim_value = round(100 - 0.05 * 100 * net_num - 0.5 * 100 * rate_ratio)
    if dim_value < 0:
        dim_value = 0
    if dim_value > 100:
        dim_value = 100
    return str(dim_value)


# 地位2000
def cmpPositionDim(metric_values, spec_id):
    dim_value, level_score, client_score, user_tran, user_score = [0, 0, 0, 0, 0]
    level_score = float(getMetricValue(metric_values, '130101'))
    acce_user = float(getMetricValue(metric_values, '130103'))
    brd_user = float(getMetricValue(metric_values, '130104'))

    # OLT
    if spec_id == '415':
        dim_value = 85
    # C类ONU/光交
    elif spec_id == 421 or spec_id == 703:
        # 客户等级数评分
        if level_score == 0:
            client_score = 0
        elif level_score >= 800:
            client_score = 100
        elif level_score == 1:
            client_score = 6
        else:
            client_score = round(100 * logging.log(10, level_score) / logging.log(10, 800))

        # 用户数评分
        if user_tran == 0:
            user_score = 0
        elif user_tran > 800:
            user_score = 100
        elif user_tran == 1:
            user_score = 6
        else:
            user_score = round(100 * logging.log(10, user_tran) / logging.log(10, 800))

        # 地位评分
        dim_value = round(0.5 * client_score + 0.5 * user_score)

    # 光分
    elif spec_id == '704':
        # 客户数评分
        if level_score == 0:
            client_score = 0
        elif level_score >= 400:
            client_score = 100
        elif level_score == 1:
            client_score = 6
        else:
            client_score = round(100 * logging.log(10, level_score) / logging.log(10, 400))

        # 用户数评分
        if user_tran == 0:
            user_score = 0
        elif user_tran > 800:
            user_score = 100
        elif user_tran == 1:
            user_score = 6
        else:
            user_score = round(100 * logging.log(10, user_tran) / logging.log(10, 800))

        # 地位评分
        dim_value = round(0.5 * client_score + 0.5 * user_score)
    # 其他(按B-ONU)
    else:
        # 客户数评分
        if level_score >= 100:
            client_score = 100
        else:
            client_score = level_score

            # 用户数评分
        if user_tran == 0:
            user_score = 0
        elif user_tran > 100:
            user_score = 100
        elif user_tran == 1:
            user_score = 6
        else:
            user_score = round(100 * logging.log(10, user_tran) / logging.log(10, 100))

            # 地位评分
        dim_value = round(0.5 * client_score + 0.5 * user_score)

    if dim_value > 100:
        dim_value = 100

    return str(dim_value)


# 配置总数维度3001
def cmpConfNumDim(metric_values):
    dim_value = 0
    config_num = float(getMetricValue(metric_values, '100101'))
    if config_num > 20:
        dim_value = 100
    else:
        dim_value = 5 * config_num
    if dim_value < 0:
        dim_value = 0
    return str(dim_value)


# 近30天用户增长量维度3002
def cmpAddUserDim(metric_values):
    dim_value = 0
    add_user = float(getMetricValue(metric_values, '130106'))
    if add_user < -10 or add_user > 10:
        dim_value = 100
    else:
        dim_value = abs(add_user) * 10
    return str(dim_value)


# 端口利用率维度3003
def cmpPortUseRateDim(metric_values):
    dim_value = 0
    port_use = float(getMetricValue(metric_values, '100311'))
    if port_use > 1:
        port_use = 1
    dim_value = round(100 * port_use)
    if dim_value < 0:
        dim_value = 0
    return str(dim_value)


# 资源检查维度5001
def cmpResCheckDim(metric_values):
    dim_value, dim_value1, dim_value2 = [0, 0, 0]
    address_num = float(getMetricValue(metric_values, '100209'))
    port_que_num = float(getMetricValue(metric_values, '100215'))
    if address_num > 10:
        dim_value1 = 0
    else:
        dim_value1 = 100 - address_num * 10

    if port_que_num > 10:
        dim_value2 = 0
    else:
        dim_value2 = 100 - port_que_num * 10

    dim_value = round(dim_value1 * 0.5 + dim_value2 * 0.5)

    if dim_value < 0:
        dim_value = 0

    if dim_value > 100:
        dim_value = 100
    return str(dim_value)


# 人工配置数4000
def cmpHumanConfigDim(metric_values):
    dim_value = 0
    config_num = float(getMetricValue(metric_values, '100103'))
    dim_value = 100 - 5 * config_num
    if dim_value < 0:
        dim_value = 0
    if dim_value > 100:
        dim_value = 100
    return str(dim_value)


# 主方法
for line in sys.stdin:
    try:
        line = line.strip()
        arrs = line.split()
        def test():
            arrs = ['2520300000045','3001','415','10','NULL','100101:23']
        res_id = arrs[0]
        dim_id = arrs[1]
        spec_id = arrs[2]
        area_id = arrs[3]
        grid_id = arrs[4]
        metric_values = arrs[5]
        rtn = []
        err = []
        rtn.append(res_id)
        rtn.append(dim_id)
        rtn.append(spec_id)
        rtn.append(area_id)
        rtn.append(grid_id)
        err.append(res_id)
        err.append(dim_id)
        err.append(spec_id)
        err.append(area_id)
        err.append(-1)
        err.append(metric_values)
        if dim_id == '1001':
            rtn.append(cmpReturnWoDim(metric_values))
        if dim_id == '1002':
            rtn.append(cmpAddrCoverDim(metric_values))
        if dim_id == '1004':
            rtn.append(cmpAutoConfReteDim(metric_values))
        if dim_id == '1005':
            rtn.append(cmpPortCapacityDim(metric_values))
        if dim_id == '1006':
            rtn.append(cmpServQualityDim(metric_values, spec_id))
        if dim_id == '2000':
            rtn.append(cmpPositionDim(metric_values, spec_id))
        if dim_id == '3001':
            rtn.append(cmpConfNumDim(metric_values))
        if dim_id == '3002':
            rtn.append(cmpConfNumDim(metric_values))
        if dim_id == '3003':
            rtn.append(cmpPortUseRateDim(metric_values))
        if dim_id == '5001':
            rtn.append(cmpResCheckDim(metric_values))
        if dim_id == '4000':
            rtn.append(cmpHumanConfigDim(metric_values))
        print
        '\t'.join(rtn)
    except Exception, e:
        print
        '\t'.join(err)

if __name__ == '__main__':
        test();

