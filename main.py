# -*- encoding: utf-8 -*-
"""
@Modify Time      @Author    @Version    @Email
------------      -------    --------    -----------
2022/9/8 23:44   zhangcy      1.0       zf2113106@buaa.edu.cn
"""
import sqlite3
import sys
import os
import time
import xlwt

def parse_db_HDMAP_LANES():
    '''
    解析db文件中的路径部分
    :return:lane_info包含laneid和coordinate的列表
    '''
    conn = sqlite3.connect("D:\\Tage\\1_Project\\SIL_environment\\885-870-20220902.db")
    cursor = conn.cursor()
    sql = """select laneid,trajectory FROM HDMAP_LANES"""  # 只提取laneid和trajectory道路坐标信息
    cursor.execute(sql)
    result = cursor.fetchall()  # 解析出的为一个大的列表，每一行的元素组成一个元组，其中trajectory中储存的坐标信息共同组成一个str

    lane_info = []
    # 提取trajectory中的字符串信息
    for i in range(len(result)):  # 提取每一行元素
        # 提取trajectory信息
        trajectory_list_str1 = result[i][1].split("(")  # 利用前括号分割
        trajectory_list_str2 = trajectory_list_str1[2].split(")")  # 利用后括号分割

        # 利用分号分割，得到每个路径点的信息，如：'115.9953437,44.0042902,877.24,132.69,5.55,0,0,877.24'
        trajectory_list_str3 = trajectory_list_str2[0].split(";")
        lane_point_list_str = [""] * len(trajectory_list_str3)
        coordinate_list_str = [["", ""]] * len(trajectory_list_str3)
        coordinate_list = [[0, 0]] * len(trajectory_list_str3)

        for j in range(len(trajectory_list_str3)):
            lane_point_list_str[j] = trajectory_list_str3[j].split(",")  # 利用逗号分割
            coordinate_list_str[j][0] = lane_point_list_str[j][0]
            coordinate_list_str[j][1] = lane_point_list_str[j][1]
            coordinate_list[j] = list(map(float, coordinate_list_str[j]))

        # 存入车道线信息和trajectory信息
        lane_info.append([int(result[i][0]),coordinate_list]) # lane_info[i][0]表示第i行的laneid，lane_info[i][1]表示第i行的traj坐标

    conn.close()

    return lane_info


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        print("folder exist,please remove")


def write_to_xls(lane_info, sheet1):
    for i in range(len(lane_info)):
        sheet1.write(0, 3 * i, 'laneid') #添加表头laneid
        sheet1.write(1, 3 * i, lane_info[i][0])  # 0行3 * i列写入laneid
        for j in range(len(lane_info[i][1])):
            tittle_lon = 'laneid-lon-' + str(lane_info[i][0])
            tittle_lat = 'laneid-lat-' + str(lane_info[i][0])
            sheet1.write(0, 3 * i + 1, tittle_lon)  # 0行3 * i + 1列写入经度表头
            sheet1.write(0, 3 * i + 2, tittle_lat)  # 0行3 * i + 2列写入纬度表头
            sheet1.write(j+1, 3 * i + 1, lane_info[i][1][j][0]) #j+1行3 * i + 1列写入经度
            sheet1.write(j+1, 3 * i + 2, lane_info[i][1][j][1]) #j+1行3 * i + 2列写入纬度


def main():


    # 新建xls文件，sheet1储存纯lane_info信息
    filePath = "./lane_info"
    if not os.path.exists(filePath):
        mkdir(filePath)
    t = time.localtime()

    xls = xlwt.Workbook()
    sheet1 = xls.add_sheet('sheet1', cell_overwrite_ok=True)  # 用cell_overwrite_ok=True实现对单元格的重复写
    result_file_name = 'lane_info' + '-gentime-' + str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(
        t.tm_mday) + '-' + str(t.tm_hour) + '.' + str(t.tm_min) + '.xls'
    fullPath = os.path.join(filePath, result_file_name)

    # 读取db文件信息
    lane_info = parse_db_HDMAP_LANES()

    # 写入文件
    write_to_xls(lane_info, sheet1)

    xls.save(fullPath)


if __name__ == '__main__':
    main()
