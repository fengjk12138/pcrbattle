from cvxpy import *
# Create two scalar optimization variables.
# 在CVXPY中变量有标量(只有数值大小)，向量，矩阵。
# 在CVXPY中有常量(见下文的Parameter)
x = Variable() # 定义变量x,定义变量y。两个都是标量
y = Variable()
# Create two constraints.
# 定义两个约束式
constraints = [x + y == 1,
              x - y >= 1]
# 优化的目标函数
obj = Minimize(square(x - y))
# 把目标函数与约束传进Problem函数中
prob = Problem(obj, constraints)
prob.solve()  # Returns the optimal value.
print("status:", prob.status)
print("optimal value", prob.value) # 最优值
print("optimal var", x.value, y.value) # x与y的解