# 凸优化课程作业代码说明文档

作者：刘程华 王晨瑜 李子岳 顾欣然

各文件与报告中求解过程的对应关系如下：

* 调用Google ortools API求解垃圾清理顺序: ```tsp.py```
* 使用scipy.optimize求解凸优化问题: ```cvx_program.py ```
* 加入线性约束和网格搜索:```add_constraints.py```
* 计算机器人转角及采样点个数:```calculate_angles.py```

```visualize.py```包含了常用的绘图函数，包括绘制问题的场景，绘制中心路径和覆盖区域等；```utils.py```包含了常用的工具函数，比如将凸多边形表达成线性不等式，检查两个凸集是否有交集等。





