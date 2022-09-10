# 1.Introduction

解析路径db文件中的laneinfo，提取每条车道的经纬度信息存入xls中。

# 2.result

![image-20220910140655119](https://user-images.githubusercontent.com/40049278/189471723-b69c6774-1564-4921-a13e-6cc755dc498c.png)

提取HDMAP_LANES中的laneid和trjectory信息，并将trjectory中的经纬度坐标解析出来。

保存内容格式如下图：

![image-20220910140847431](https://user-images.githubusercontent.com/40049278/189471726-e8e6aaa9-ecad-4633-a0fc-996ee1fa2337.png)

# 3.usage 

更改文件中的db文件地址即可。

```python
conn = sqlite3.connect("D:\\***\\1_Project\\SIL_environment\\885-870-20220902.db")
```
