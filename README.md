## 基于规则的专家系统 -- 图形检测
### 前言
此项目是**人工智能**的课程项目。具体要求为实现一个*基于规则的专家系统*， 用来进行简单直线型几何图形的形状检测。  
项目实现的重点在于**规则的表示**， **推理机的构建**， **知识库的构建**， **图形的预处理** 和 **用户界面**。  
项目实现语言为Python，图形预处理用到了OpenCV， 用户界面用到了wxPython。  
专家系统的设计参考了[《人工智能 - 智能系统指南》(原书第3版)](https://book.douban.com/subject/11606478/) 第2章。    
如有任何对项目的改进建议，欢迎评论。 :~) 

### 目录
1. [概述](#general)
2. [图形检测专家系统的结构](#structure)
3. [规则的构建和表示](#rule)
4. [知识库的表示](#knowledge)
5. [图形的预处理](#pic_handle)
6. [数据库的表示](#fact)
7. [推理引擎的构建 : 后向链接推理技术](#back)
8. [用户界面](#GUI)
9. [测试用例](#test)
10. [总结](#conclusion)

### <a name='general'></a>概述
图形检测专家系统的运作流程为：  

* 通过图形预处理得到一组基本事实（即图形中各线段端点坐标）
* 处理这一组基本事实，产生专家系统的数据库
* 推理引擎读取外部的规则文档，产生知识库
* 推理引擎读入数据库
* 采用后向链接推理技术进行推理
* 推理过程中记录触发的规则和符合规则的事实
* 绘制出用户所要检测的图形的位置
* 在用户界面中显示出来  

图形检测专家系统还提供另外的功能，包括：

* 提供规则编辑器，用于增添新的规则
* 展示目前的规则库
* 展示当前检测图片的事实库 

图形检测专家系统目前支持检测的图形包括：

* 三角形
    * 锐角三角形
    * 直角三角形
    * 钝角三角形
    * 等腰三角形
        * 直角等腰三角形
        * 锐角等腰三角形
        * 钝角等腰三角形
    * 等边三角形
* 四边形
    * 平行四边形
        * 矩形
            * 正方形
        * 菱形
    * 梯形
        * 等腰梯形
        * 直角梯形      
* 五边形
    * 正五边形
* 六边形
    * 正六边形

图形检测专家系统支持不同位置，各种形态，各种大小的图形检测，且支持一张图片多个图形的检测。

### <a name='structure'></a>图形检测专家系统的结构
图形检测专家系统的结构尽可能模仿了书中展示的**基于规则的专家系统的基本结构**。
具体结构如下：  
![structure](https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/readme_picture/structure.png)  
图形检测专家系统也由5部分组成：[知识库Knowledge base](https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/rules/rules.txt), [数据库Database](https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/facts/facts.txt), [推理引擎Inference engine](https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/engine/inference_engine.py), [解释设备Explanation facilities, 用户界面User interface](https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/GUI/main_frame.py).  
对应的项目文件夹分别为rules, facts, engine, GUI。  
另外，由于图形的特殊性，项目文件中还包含[图形预处理器](https://github.com/Sorosliu1029/Rule-based_Expert_System/blob/master/Picture_handler/cv_handler2.py).

### <a name='rule'></a>规则的构建和表示
因为专家系统需要支持动态的加载知识库，所以检测规则不能硬编码在程序中，而是需要长期存储在外部文件中，并在推理引擎中加载。  
基于以上原因，首先构建了一个Rule类用来表示某条规则

### <a name='knowledge'></a>知识库的表示

### <a name='pic_handle'></a>图形的预处理

### <a name='fact'></a>数据库的表示

### <a name='back'></a>推理引擎的构建 : 后向链接推理技术

### <a name='GUI'></a>用户界面

### <a name='test'></a>测试用例

### <a name='conclusion'></a>总结

