#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Author: Shieber
#    Date: 2019.01.12
#
#                             APACHE LICENSE
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
#                            Function Description
#    统计年度消费数据 
#
#    Copyright 2019 
#    All Rights Reserved!

import json
import sys,re
import datetime

def add_new_month_cost(argv):
    '''添加新一个月的消费数据'''
    if len(argv) > 5:
        print("Error, 4 arguments need, %d given."%(len(argv)-1))
        return None

    year  = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    with open(argv[1]) as fobj:
        expen_dic = json.load(fobj)
        year_keys = expen_dic.keys()
        if year not in year_keys:
            expen_dic[year] = {}
            expen_dic[year]["All"] = {"Alipay": 0, "JDpay": 0, "Wechat": 0, "Ztotal": 0}

        year_data  = expen_dic[year]
        month_keys = year_data.keys()
        if month not in month_keys:
            year_data[month] = {"Alipay": 0, "JDpay": 0, "Wechat": 0, "Ztotal": 0}

        item = ["Alipay","JDpay","Wechat"]
        expen_list = argv[2:]
        for i in range(len(expen_list)):
            year_data[month][item[i]] = float(expen_list[i])

    with open(argv[1],'w') as fobj:
        json.dump(expen_dic,fobj, indent=4, sort_keys=True)

def sum_year_months(argv):
    '''统计各年内各月份的消费数据'''
    with open(argv[1]) as fobj:
        expen_dic = json.load(fobj)
        year_keys = expen_dic.keys()
        del year_keys[year_keys.index("All")]

    for year_key in year_keys:
        year_data  = expen_dic[year_key]
        month_keys = year_data.keys()
        for month_key in month_keys:
            month_data = year_data[month_key]
            total_cost = month_data["JDpay"] + month_data["Alipay" ] + month_data["Wechat"]
            month_data["Ztotal"] = round(total_cost,2)

    with open(argv[1],'w') as fobj:
        json.dump(expen_dic,fobj, indent=4, sort_keys=True)

def sum_year_all(argv):
    '''统计一年的总消费数据'''
    with open(argv[1]) as fobj:
        expen_dic = json.load(fobj)
        year_keys = expen_dic.keys()
        del year_keys[year_keys.index("All")]

    items = ["JDpay","Alipay","Wechat", "Ztotal"]
    for year_key in year_keys:
        year_data  = expen_dic[year_key]
        month_keys = year_data.keys()
        del month_keys[month_keys.index("All")]

        for item in items:
            item_cost = 0
            for month_key in month_keys:
                month_data = year_data[month_key]
                item_cost += month_data[item] 
            year_data["All"][item] = round(item_cost,2)

    with open(argv[1],'w') as fobj:
        json.dump(expen_dic,fobj, indent=4, sort_keys=True)

def sum_years_all(argv):
    '''统计各项的总消费数据'''
    with open(argv[1]) as fobj:
        expen_dic = json.load(fobj)
        year_keys = expen_dic.keys()
        del year_keys[year_keys.index("All")]

    items = expen_dic["All"].keys()
    for item in items: 
        cost = 0
        for year_key in year_keys:
            year_data = expen_dic[year_key]
            cost += year_data["All"][item]

        expen_dic["All"][item] = round(cost,2)

    with open(argv[1],'w') as fobj:
        json.dump(expen_dic,fobj, indent=4, sort_keys=True)

def sums(argv):
    '''统计所有消费数据'''
    add_new_month_cost(argv) #Add the expenditure of current month
    sum_year_months(argv)    #统计各年各月的数据
    sum_year_all(argv)       #统计各年各月的总数据
    sum_years_all(argv)      #统计所以年份的总数据

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) <2:
        print("Usage: python %s expen.json [300 400 500]"%argv[0])
        sys.exit(-1)
    sums(argv)
