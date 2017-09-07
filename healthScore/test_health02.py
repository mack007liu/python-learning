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


# 业务退改单维度200101
def cmpReturnWoDim(metric_values):
    # 定义初始评价得分
    dim_value = 0
    # 获取资源退单率指标结果
    return_wo_ratio = float(getMetricValue(metric_values, '100221'))
    # 获取覆盖问题退改单数指标结果，没有去掉
    if return_wo_ratio >= 0.24 and return_wo_ratio / 100 < 0.43:
        dim_value = round((0.43 - return_wo_ratio / 100) / (0.43 - 0.24) * (75 - 25)) + 25
    elif return_wo_ratio >= 0.43 and return_wo_ratio / 100 <= 1:
        dim_value = round((1 - return_wo_ratio / 100) / (1 - 0.43) * 25)
    else:
        dim_value = 0
    # 返回评价结果
    return str(dim_value)


# 地址覆盖维度200102
def cmpAddrCoverDim(metric_values):
    dim_value = 0
    addr_co_num = float(getMetricValue(metric_values, '100210'))
    error_co_num = float(getMetricValue(metric_values,'100211'))
    addr_co_ratio = float(getMetricValue(metric_values, '100212'))
    if addr_co_ratio < 0:
        addr_co_ratio = 1
    if error_co_num == 0:
        dim_value = 100
    if error_co_num > 0:
        if addr_co_num >= 145:
            dim_value = round(100 * (1 - 10 * (1 - addr_co_ratio / 100)))
        if dim_value < 0:
            dim_value = round(addr_co_ratio)
        elif addr_co_num >= 20 and addr_co_num < 145:
            dim_value = round(100 * (1 - 5 * (1 - addr_co_ratio / 100)))
        if dim_value < 0:
            dim_value = round(addr_co_ratio)
        else:
            dim_value = round(addr_co_ratio)
    return str(dim_value)


# 自动配置维度200105
def cmpAutoConfReteDim(metric_values):
    dim_value = 0
    auto_con_ratio = float(getMetricValue(metric_values, '100107'))
    one_auto_ratio = float(getMetricValue(metric_values, '100109'))
    fttx_auto_ratio = float(getMetricValue(metric_values, '100110'))
    ftth_auto_ratio = float(getMetricValue(metric_values, '100111'))
    auto_open_ratio = float(getMetricValue(metric_values, '100112'))
    ten_min_ratio = float(getMetricValue(metric_values, '100113'))
    dim_value = round(
        auto_con_ratio * 0.3 + one_auto_ratio * 0.2 + fttx_auto_ratio * 0.1 + ftth_auto_ratio * 0.1 + auto_open_ratio * 0.2 + ten_min_ratio * 0.1)
    if dim_value > 100:
        dim_value = 100
    return str(dim_value)


# 端口容量维度200107
def cmpPortCapacityDim(metric_values):
    dim_value = 0
    port_use_ratio = float(getMetricValue(metric_values, '100310'))
    port_num = float(getMetricValue(metric_values, '100309'))
    if port_num >= 64:
        if port_use_ratio > 0.72 and port_use_ratio <= 1:
            dim_value = round((1 - port_use_ratio) / (1 - 0.72) * (100 - 40)) + 40
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
            dim_value = round((1 - port_use_ratio) / (1 - 0.75) * (100 - 75)) + 75
        elif port_use_ratio >= 0 and port_use_ratio < 0.25:
            dim_value = round(port_use_ratio / 0.25 * (100 - 75)) + 75
        else:
            dim_value = 100

    if dim_value > 100:
        dim_value = 100

    return str(dim_value)


# 服务质量维度200108,暂不开发
'''def cmpServQualityDim(metric_values):
    dim_value = 0
    net_num = float(getMetricValue(metric_values,'100311'))
    rate_ratio = float(getMetricValue(metric_values,'110204'))

    dim_value = round(100 - 0.35 * 100 * net_num - 0.5 * 100 * rate_ratio)
    #OLT设备
    if spec_id == '415':
       dim_value = round(100 - 0.05 * 100 * net_num - 0.5 * 100 * rate_ratio)
    if dim_value < 0:
       dim_value = 0
    if dim_value > 100:
       dim_value = 100
    return str(dim_value) '''


# 端口准确性200103,百分比求平均值,指标还没有开发
def cmpPortAccurateDim(metric_values):
    port_consistent = float(getMetricValue(metric_values, '120301'))
    port_no_opt = float(getMetricValue(metric_values, '120302'))
    port_no_business = float(getMetricValue(metric_values, '120303'))
    dim_value = round((port_consistent + port_no_opt + port_no_business) / 3)
    return str(dim_value)


# 链路完整性200104,指标百分比,指标还没有开发
def cmpLinkCompleteDim(metric_values):
    link_complete = float(getMetricValue(metric_values, '120101'))
    dim_value = link_complete
    return str(dim_value)


# 资源一致性200106，暂不开发
'''def cmpResConsistDim(metric_values):
    dim_value = 0
    return str(dim_value) '''
# 主方法
# 调试脚本时下面4行要注释掉
for line in sys.stdin:
    try:
        line = line.strip()
        arrs = line.split()
        # def test()是调试脚本用到的方法
        # def test():
        # 调试脚本时取消下面两行注释
        # try:
        # arrs = ['2520300000045','200101','415','10','2','200108:4']
        res_id = arrs[0]
        dim_id = arrs[1]
        spec_id = arrs[2]
        area_id = arrs[3]
        sharding_id = arrs[4]
        metric_values = arrs[5]
        rtn = []
        err = []
        rtn.append(res_id)
        rtn.append(dim_id)
        rtn.append(spec_id)
        rtn.append(area_id)
        rtn.append(sharding_id)
        err.append(res_id)
        err.append(dim_id)
        err.append(spec_id)
        err.append(area_id)
        err.append(-1)
        err.append(metric_values)
        if dim_id == '200101':
            rtn.append(cmpReturnWoDim(metric_values))
        if dim_id == '200102':
            rtn.append(cmpAddrCoverDim(metric_values))
        if dim_id == '200103':
            rtn.append(cmpPortAccurateDim(metric_values))
        if dim_id == '200104':
            rtn.append(cmpLinkCompleteDim(metric_values))
        if dim_id == '200105':
            rtn.append(cmpAutoConfReteDim(metric_values))
            # if dim_id == '200106':
            # rtn.append(cmpResConsistDim(metric_values))
        if dim_id == '200107':
            rtn.append(cmpPortCapacityDim(metric_values))
            # if dim_id == '200108':
            # rtn.append(cmpServQualityDim(metric_values))
        print '\t'.join(rtn)
    except Exception, e:
        print '\t'.join(err)

# 下面两行在调试脚本时取消注释
# if __name__ == '__main__':
#  test();

