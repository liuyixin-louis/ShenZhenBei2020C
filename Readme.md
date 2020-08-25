# **2020年“深圳杯”数学建模挑战赛C题-无线可充电传感器网络充电路线规划**

## 题目梳理

> http://www.m2ct.org/view-page.jsp?editId=12&uri=0D00233&gobackUrl=modular-list.jsp&pageType=smxly&menuType=flowUp

![image-20200821221840421](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200821221840421.png)

- 网络中三类节点：数据中心DC（Data Center）、传感器（Sensors）、移动充电器MC（Mobile Charger）

- Sensors：
  - 能量来源：环境能量、MC
  - 传感器都有特定的能量消耗速率，以及**固定的电池容量**
  - 当**一个**传感器的电量低于一个阈值时便无法进行正常的信息采集工作
- MC：
  - 能量消耗：
    - 一是**为传感器节点充电**所导致的正常的能量消耗；
    - 另外一方面则是**移动充电器在去为传感器充电的路上的能量消耗**
  - 移动规则：
    - 移动充电器从**数据中心**出发，以**固定的速度**依次经过每个传感器，在每个传感器处**停留一段时间**并以**固定的充电速率**为传感器充电，**直到为所有传感器充电完成之后返回数据中心**。



### 任务：

1. 若给出每个节点的经纬度（见附件1），请考虑当只派出一个移动充电器时，如何规划移动充电器的充电路线才能最小化移动充电器在路上的能量消耗。
2. 若给出每个节点的经纬度、每个节点的能量消耗速率（见附件2），并假设传感器的电量只有在高于f(mA)时才能正常工作，移动充电器的移动速度为v(m/s)、移动充电器的充电速率为r（mA/s），在只派出一个移动充电器的情况下，若采用问题1）规划出来的充电路线，每个传感器的电池的容量应至少是多大才能保证整个系统一直正常运行（即系统中每个传感器的电量都不会低于f（mA））？
3. 若给出每个节点的经纬度、每个节点的能量消耗速率（同见附件2），并假设传感器的电量只有在高于f(mA)时才能正常工作，移动充电器的移动速度为v(m/s)、移动充电器的充电速率为r（mA/s），但为了提高充电效率，同时派出4个移动充电器进行充电，在这种情况下应该如何规划移动充电器的充电路线以最小化所有移动充电器在路上的总的能量消耗？每个传感器的电池的容量应至少是多大才能保证整个系统一直正常运行？