# -*- encoding: utf-8 -*-
"""
@Modify Time      @Author    @Version    @Email
------------      -------    --------    -----------
2022/9/8 23:44   zhangcy      2.0       zf2113106@buaa.edu.cn
"""
import sqlite3
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

    # 解析道路信息
    sql_lanes = """select laneid,trajectory FROM HDMAP_LANES"""  # 只提取laneid和trajectory道路坐标信息
    cursor.execute(sql_lanes)
    result_lanes = cursor.fetchall()  # 解析出的为一个大的列表，每一行的元素组成一个元组，其中trajectory中储存的坐标信息共同组成一个str

    lane_info = []
    # 提取trajectory中的字符串信息
    for i in range(len(result_lanes)):  # 提取每一行元素
        # 提取trajectory信息
        trajectory_list_str1 = result_lanes[i][1].split("(")  # 利用前括号分割
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
        lane_info.append(
            [int(result_lanes[i][0]), coordinate_list])  # lane_info[i][0]表示第i行的laneid，lane_info[i][1]表示第i行的traj坐标

    conn.close()

    return lane_info


def list_of_groups(list_info, per_list_len):
    '''
    :param list_info:   列表
    :param per_list_len:  每个小列表的长度
    :return:
    '''
    list_of_group = zip(*(iter(list_info),) * per_list_len)
    end_list = [list(i) for i in list_of_group]  # i is a tuple
    count = len(list_info) % per_list_len
    end_list.append(list_info[-count:]) if count != 0 else end_list
    return end_list


def HDMAP_LANE_BOUNDARYS():
    '''
    解析db文件中的路径边界部分
    :return:
    '''
    conn = sqlite3.connect("D:\\Tage\\1_Project\\SIL_environment\\885-870-20220902.db")
    cursor = conn.cursor()

    # 解析道路边界信息
    sql_lane_boundarys = """select lane_id,left_boundary,right_boundary FROM HDMAP_LANE_BOUNDARYS"""  # 只提取道路边界信息
    cursor.execute(sql_lane_boundarys)
    result_lane_boundarys = cursor.fetchall()  # 解析出的为一个大的列表，每一行的元素组成一个元组，其中trajectory中储存的坐标信息共同组成一个str

    # 解析左侧道路边界信息
    left_boundarys_info = []
    # 提取boundary中的字符串信息
    for i in range(len(result_lane_boundarys)):  # 提取每一行元素
        # 提取left_boundary信息
        left_boundary_list_str1 = result_lane_boundarys[i][1].split("(")  # 利用前括号分割
        left_boundary_list_str2 = left_boundary_list_str1[2].split(")")  # 利用后括号分割
        # 利用分号分割，得到每个路径点的信息，如：'115.991930935169,44.004314321974,872.39'
        left_boundary_list_str3 = left_boundary_list_str2[0].split(";")

        left_boundary_point_list_str = [""] * len(left_boundary_list_str3)
        left_boundary_coordinate_list_str = [["", ""]] * len(left_boundary_list_str3)
        left_boundary_coordinate_list = [[0, 0]] * len(left_boundary_list_str3)
        for j in range(len(left_boundary_list_str3)):
            left_boundary_point_list_str[j] = left_boundary_list_str3[j].split(",")  # 利用逗号分割
            left_boundary_coordinate_list_str[j][0] = left_boundary_point_list_str[j][0]
            left_boundary_coordinate_list_str[j][1] = left_boundary_point_list_str[j][1]
            left_boundary_coordinate_list[j] = list(map(float, left_boundary_coordinate_list_str[j]))

        # 存入车道线信息和trajectory信息
        # left_boundarys_info[i][0]表示第i行的laneid，lane_boundarys_info[i][1]表示第i行的traj坐标
        left_boundarys_info.append([int(result_lane_boundarys[i][0]), left_boundary_coordinate_list])

    # 解析右侧道路边界信息
    right_boundarys_info = []
    # 提取boundary中的字符串信息
    for i in range(len(result_lane_boundarys)):  # 提取每一行元素
        # 提取right_boundary信息
        right_boundary_list_str1 = result_lane_boundarys[i][2].split("(")  # 利用前括号分割
        right_boundary_list_str2 = right_boundary_list_str1[2].split(")")  # 利用后括号分割

        # 利用逗号分割，right_boundarys没有以分号分割的，因此直接用逗号分割
        # 得到单个的路径点的信息，如：'115.9953437'
        right_boundary_list_str3 = right_boundary_list_str2[0].split(",")
        # 每个元素为['115.998110366651', '44.000381835805', '876.22']
        right_boundary_point_list_str = list_of_groups(right_boundary_list_str3, 3)

        right_boundary_coordinate_list_str = [["", ""]] * len(right_boundary_list_str3)
        right_boundary_coordinate_list = [[0, 0]] * len(right_boundary_list_str3)

        for j in range(len(right_boundary_point_list_str)):
            right_boundary_coordinate_list_str[j][0] = right_boundary_point_list_str[j][0]
            right_boundary_coordinate_list_str[j][1] = right_boundary_point_list_str[j][1]
            right_boundary_coordinate_list[j] = list(map(float, right_boundary_coordinate_list_str[j]))

        # 存入车道线信息和trajectory信息
        # right_boundarys_info[i][0]表示第i行的laneid，lane_boundarys_info[i][1]表示第i行的traj坐标
        right_boundarys_info.append([int(result_lane_boundarys[i][0]), right_boundary_coordinate_list])

    conn.close()

    return left_boundarys_info, right_boundarys_info


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        print("folder exist,please remove")


def write_to_xls(lane_or_boundary_info, sheet1, lane_flag=1):
    if lane_flag:
        for i in range(len(lane_or_boundary_info)):
            sheet1.write(0, 3 * i, 'laneid')  # 添加表头laneid
            sheet1.write(1, 3 * i, lane_or_boundary_info[i][0])  # 0行3 * i列写入laneid
            for j in range(len(lane_or_boundary_info[i][1])):
                tittle_lon = 'laneid-lon-' + str(lane_or_boundary_info[i][0])
                tittle_lat = 'laneid-lat-' + str(lane_or_boundary_info[i][0])
                sheet1.write(0, 3 * i + 1, tittle_lon)  # 0行3 * i + 1列写入经度表头
                sheet1.write(0, 3 * i + 2, tittle_lat)  # 0行3 * i + 2列写入纬度表头
                sheet1.write(j + 1, 3 * i + 1, lane_or_boundary_info[i][1][j][0])  # j+1行3 * i + 1列写入经度
                sheet1.write(j + 1, 3 * i + 2, lane_or_boundary_info[i][1][j][1])  # j+1行3 * i + 2列写入纬度
    else:
        for i in range(len(lane_or_boundary_info)):
            sheet1.write(0, 3 * i, 'boundary_id')  # 添加表头boundary_id
            sheet1.write(1, 3 * i, lane_or_boundary_info[i][0])  # 0行3 * i列写入boundary_id
            for j in range(len(lane_or_boundary_info[i][1])):
                tittle_lon = 'boundaryid-lon-' + str(lane_or_boundary_info[i][0])
                tittle_lat = 'boundaryid-lat-' + str(lane_or_boundary_info[i][0])
                sheet1.write(0, 3 * i + 1, tittle_lon)  # 0行3 * i + 1列写入经度表头
                sheet1.write(0, 3 * i + 2, tittle_lat)  # 0行3 * i + 2列写入纬度表头
                sheet1.write(j + 1, 3 * i + 1, lane_or_boundary_info[i][1][j][0])  # j+1行3 * i + 1列写入经度
                sheet1.write(j + 1, 3 * i + 2, lane_or_boundary_info[i][1][j][1])  # j+1行3 * i + 2列写入纬度


def main():
    # 新建xls文件，sheet1储存纯lane_info信息
    filePath = "./lane_info"
    if not os.path.exists(filePath):
        mkdir(filePath)
    t = time.localtime()

    xls = xlwt.Workbook()
    sheet1 = xls.add_sheet('lanes', cell_overwrite_ok=True)  # 道路信息，用cell_overwrite_ok=True实现对单元格的重复写
    sheet2 = xls.add_sheet('left_boundarys', cell_overwrite_ok=True)  # 左边界信息
    sheet3 = xls.add_sheet('right_boundarys', cell_overwrite_ok=True)  # 右边界信息
    result_file_name = 'lane_info' + '-gentime-' + str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(
        t.tm_mday) + '-' + str(t.tm_hour) + '.' + str(t.tm_min) + '.xls'
    fullPath = os.path.join(filePath, result_file_name)

    # 读取db文件中的lanes信息
    lane_info = parse_db_HDMAP_LANES()

    # 读取db文件中的boundarys信息
    left_boundarys_info, right_boundarys_info = HDMAP_LANE_BOUNDARYS()

    # 写入文件
    write_to_xls(lane_info, sheet1)
    write_to_xls(left_boundarys_info, sheet2, lane_flag=0)
    write_to_xls(right_boundarys_info, sheet3, lane_flag=0)

    xls.save(fullPath)


if __name__ == '__main__':
    main()
