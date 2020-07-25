# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:36:12 2020

@author: Administrator
"""
import json
from pyecharts import options as opts
from pyecharts.charts import Graph, Page
import numpy as np
# 打开作者属性文件
authorsdict_filename = "../get_vector/authorsdict/new_article_authorlist.json"
authorsdict_out = open(authorsdict_filename, 'r', encoding='utf-8')
authorsdict = json.load(authorsdict_out)
# 调整参数
addr_word = {}
cnt1 = 1
while 1:
    print("请输入您要查找合作网络的地理信息关键词（可输入多个,输quit结束输入）:", end='')
    ADDR = input() # 地理关键词
    if ADDR == 'quit':
        break
    addr_word[ADDR] = cnt1
    cnt1 += 1
data_len = 2000 # 数据量
# data_len = int(input()) # 数据量
# 合作者网络
node_to_authors = ['None'] # 点序号：作者
authors_to_node = {} # 作者:点序号
authors_degree = {} # 作者节点度
links = [] # 存储边数
nodes = [] # 存放点
cnt = 1 # 节点计数
flag = 0 # 反馈计数
name_to_addr = {} # 作者:地理关键词
# 构建网络
for line in authorsdict:
    # 反馈输出
    if flag%100==0:
        print(flag)
    flag += 1
    # 结束设置
    if flag >= data_len:
        break
    # 取出地理信息，并作筛选
    f = 0
    addr_string = authorsdict[line]["addr"]
    for ad in addr_word:
        if ad in addr_string:
            name_to_addr[line] = ad
            f = 1
            break
    if f == 0:
        continue
    # 当前行的合作者字典
    Coners_string = authorsdict[line]["Coners"]
    # 记录作者，将姓名与节点编号联系
    if line in node_to_authors:
        start = authors_to_node[line]
    else :
        node_to_authors.append(line)
        authors_to_node[line] = cnt
        authors_degree[line] = 0
        cnt += 1
    # 遍历作者的合作者
    for coner in Coners_string:
        if line == coner:
            continue
        # 记录合作者，将姓名与节点编号联系
        if coner in node_to_authors:
            end = authors_to_node[coner]
            authors_degree[coner] += Coners_string[coner]
            authors_degree[line] += Coners_string[coner]
        else:
            node_to_authors.append(coner)
            authors_to_node[coner] = cnt
            authors_degree[coner] = Coners_string[coner]
            authors_degree[line] += Coners_string[coner]
            cnt += 1
        # 建立边
        links.append({"source": line, "target": coner, "value": Coners_string[coner]})
        links.append({"source": coner, "target": line, "value": Coners_string[coner]})
# 构造地理分组表单
categories=[{'name': '无地理信息'}]
for ad in addr_word:
    categories.append({'name': ad})
# 添加节点及其属性信息
for i in range(1,len(node_to_authors)):
    name = node_to_authors[i]
    if name not in name_to_addr:
        nodes.append({"name": name, "symbolSize": authors_degree[name] / 10, "category": 0})
    else:
        addr = name_to_addr[name]
        nodes.append({"name": name, "symbolSize": authors_degree[name]/10,"category":addr_word[addr]})
# 绘图
c = (
        Graph(init_opts=opts.InitOpts(width="1600px", height="600px"))
        .add("", nodes, links, categories=categories,repulsion=8000,
            layout="circular",
            is_rotate_label=True,
            linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
            label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="DBLP合作网络"),)
)
# 输出网页
c.render(path="../show/coners.html")
