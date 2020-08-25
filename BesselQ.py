import math as m


class Earth():
    # 建立椭球类，采用SGCS2000中国大地坐标系数据
    def __init__(self):  # 给定椭球数据
        # 长半轴
        self.a = 6378137.0
        # 短半轴
        self.b = 6356752.31414
        # 扁率
        self.f = 1/298.257222101
        # 第一偏心率的平方
        self.e1s = m.pow(0.0818191910428, 2)
        # 第二偏心率的平方
        self.e2s = self.e1s / (1 - self.e1s)

    def W(self, B):  # 计算第一辅助函数
        self.w = m.sqrt(1 - self.e1s * m.sin(B) * m.sin(B))
        return self.w

    def V(self, B):  # 计算第二辅助函数
        self.v = m.sqrt(1 + self.e2s * m.cos(B) * m.cos(B))
        return self.v


class Bessel():
    # 建立贝塞尔解算类
    def __init__(self):  # 导入椭球数据
        self.E = Earth()

    def Direct(self, L1, B1, A1, S, T):  # 正算
        # 标记精度：高于米级为1，米级为2，低于百米级为3
        self.Type = {1: (1, 1), 2: (0, 1), 3: (0, 0)}
        self.t1 = self.Type[T][0]
        self.t2 = self.Type[T][1]

        # 将角度转化为弧度
        self.L1, self.B1, self.A1 = m.radians(L1), m.radians(B1), m.radians(A1)

        # Ⅰ将椭球面元素投影到球面上
        # 由B1求u1
        self.u1 = m.atan(m.sqrt(1 - self.E.e1s) * m.tan(self.B1))
        # 计算辅助函数值
        self.M = m.atan(m.tan(self.u1) / m.cos(self.A1))
        if self.M < 0:
            self.M += m.pi
        self.m = m.asin(m.cos(self.u1) * m.sin(self.A1))
        if self.m < 0:
            self.m += 2 * m.pi

        # 将S化为σ
        self.k2 = self.E.e2s * m.cos(self.m) * m.cos(self.m)
        self.k4 = self.k2 * self.k2
        self.k6 = self.k4 * self.k2 * self.t1
        self.ρ = 180 / m.pi * 3600
        self.α1 = m.sqrt(1 + self.E.e2s) / self.E.a * (1 - self.k2 / 4 + 7 / 64 * self.k4 - 15 / 256 * self.k6)
        self.β1 = self.k2 / 4 - self.k4 / 8 + 37 / 512 * self.k6
        self.γ1 = (self.k4 - self.k6) / 128 * self.t2
        self.σ1 = self.α1 * S
        while True:
            self.σ2 = self.α1 * S + self.β1 * m.sin(self.σ1) * m.cos(2 * self.M + self.σ1) + \
                self.γ1 * m.sin(2 * self.σ1) * m.cos(4 * self.M + 2 * self.σ1)
            if abs(self.σ1 - self.σ2) < 0.1 / self.ρ / 3600:
                break
            self.σ1 = self.σ2
        self.σ = self.σ2

        # Ⅱ在球面上解算
        # 求A2
        self.A2 = m.atan(m.tan(self.m) / m.cos(self.M + self.σ))
        if self.A2 < 0:
            self.A2 += m.pi
        if self.A1 < m.pi:
            self.A2 += m.pi
        # 求u2
        self.u2 = m.atan(-m.cos(self.A2) * m.tan(self.M + self.σ))
        # 求λ
        self.λ1 = m.atan(m.sin(self.u1) * m.tan(self.A1))
        if self.λ1 < 0:
            self.λ1 += m.pi
        if self.m > m.pi:
            self.λ1 += m.pi
        self.λ2 = m.atan(m.sin(self.u2) * m.tan(self.A2))
        if self.λ2 < 0:
            self.λ2 += m.pi
        if self.m < m.pi:
            if self.M + self.σ > m.pi:
                self.λ2 += m.pi
        else:
            if self.M + self.σ < m.pi:
                self.λ2 += m.pi
        self.λ = self.λ2 - self.λ1

        # Ⅲ将球面元素换算到椭球面上
        # 由u2求B2
        self.B2 = m.atan(m.sqrt(1 + self.E.e2s) * m.tan(self.u2))
        # 求L2
        self.α2 = (0.5 + self.E.e1s / 8 - self.E.e1s * self.E.e1s / 16) * self.E.e1s - \
            self.t1 * (self.E.e1s / 16 * (1 + self.E.e1s) * self.k2 - 3 / 128 * self.E.e1s * self.k4)
        self.β2 = self.t2 * (self.E.e1s / 16 * (1 + self.t1 * self.E.e1s) * self.k2 -
                             self.t1 * self.E.e1s / 32 * self.k4)
        self.γ2 = self.t2 * self.E.e1s / 256 * self.k4
        self.L2 = self.L1 + self.λ - m.sin(self.m) * (self.α2 * self.σ + self.β2 * m.sin(self.σ)
                                                      * m.cos(2 * self.M + self.σ) + self.γ2
                                                      * m.sin(2 * self.σ) * m.cos(4 * self.M + 2 * self.σ))

        self.result = [self.L2 * 180 / m.pi, self.B2 * 180 / m.pi, self.A2 * 180 / m.pi]
        return(self.result)

    def Inverse(self, L1, B1, L2, B2, T):  # 反算
        # 标记精度：高于米级为1，米级为2，低于百米级为3
        self.Type = {1: (1, 1), 2: (0, 1), 3: (0, 0)}
        self.t1 = self.Type[T][0]
        self.t2 = self.Type[T][1]

        # 将角度转化为弧度
        self.L1, self.B1, self.L2, self.B2 = m.radians(L1), m.radians(B1), m.radians(L2), m.radians(B2)

        # Ⅰ将椭球面元素投影到球面上
        # 由B求u
        self.u1 = m.atan(m.sqrt(1 - self.E.e1s) * m.tan(self.B1))
        self.u2 = m.atan(m.sqrt(1 - self.E.e1s) * m.tan(self.B2))
        # 由l求λ
        self.l = self.L2 - self.L1
        # 利用初值λ0=l计算λ1
        self.σ0 = m.acos(m.sin(self.u1) * m.sin(self.u2) + m.cos(self.u1) * m.cos(self.u2) * m.cos(self.l))

        self.m0 = m.asin(m.cos(self.u1) * m.cos(self.u2) * m.sin(self.l) / m.sin(self.σ0))
        self.k2 = self.E.e2s * m.cos(self.m0) * m.cos(self.m0)
        self.k4 = self.k2 * self.k2
        self.α2 = (1 / 2 + self.E.e1s / 8 - self.E.e1s * self.E.e1s / 16) * self.E.e1s - \
            self.E.e1s / 16 * (1 + self.E.e1s) * self.k2 + 3 / 128 * self.E.e1s * self.k4
        self.Δλ = self.α2 * self.σ0 * m.sin(self.m0)
        self.λ0 = self.l + self.Δλ
        self.Δσ = m.sin(self.m0) * self.Δλ
        self.σ1 = self.σ0 + self.Δσ
        self.m1 = m.asin(m.cos(self.u1) * m.cos(self.u2) * m.sin(self.λ0) / m.sin(self.σ1))
        self.A10 = m.atan(m.sin(self.λ0) / (m.cos(self.u1) * m.tan(self.u2) - m.sin(self.u1) * m.cos(self.λ0)))
        if self.A10 < 0:
            self.A10 += m.pi
        if self.m1 < 0:
            self.A10 += m.pi
        self.M1 = m.atan(m.sin(self.u1) * m.tan(self.A10) / m.sin(self.m1))
        if self.M1 < 0:
            self.M1 += m.pi

        self.k2 = self.E.e2s * m.cos(self.m1) * m.cos(self.m1)
        self.k4 = self.k2 * self.k2
        self.α2 = (1 / 2 + self.E.e1s / 8 - self.E.e1s * self.E.e1s / 16) * self.E.e1s - \
            self.E.e1s / 16 * (1 + self.E.e1s) * self.k2 + 3 / 128 * self.E.e1s * self.k4
        self.β2 = self.E.e1s / 16 * (1 + self.E.e1s) * self.k2 - self.E.e1s / 32 * self.k4
        self.λ = self.l + m.sin(self.m1) * (self.α2 * self.σ1 + self.β2 * m.sin(self.σ1) * m.cos(2 * self.M1 + self.σ1))

        # Ⅱ解算球面三角形
        # 求σ
        self.σ = m.acos(m.sin(self.u1) * m.sin(self.u2) + m.cos(self.u1) * m.cos(self.u2) * m.cos(self.λ))
        # 求self.A1、self.A2
        self.A1 = m.atan(m.sin(self.λ) / (m.cos(self.u1) * m.tan(self.u2) - m.sin(self.u1) * m.cos(self.λ)))
        self.m = m.asin(m.cos(self.u1) * m.sin(self.A1))
        if self.A1 < 0:
            self.A1 += m.pi
        if self.m > 0:
            self.A1 += m.pi
        self.M = m.atan(m.sin(self.u1) * m.tan(self.A10) / m.sin(self.m1))
        if self.M < 0:
            self.M += m.pi
        self.A2 = m.atan(m.sin(self.λ) / (m.sin(self.u2) * m.cos(self.λ) - m.tan(self.u1) * m.cos(self.u2)))
        if self.A2 < 0:
            self.A2 += m.pi
        if self.m < 0:
            self.A2 += m.pi

        # Ⅲ将椭球面元素换算到球面上
        self.k2 = self.E.e2s * m.cos(self.m) * m.cos(self.m)
        self.k4 = self.k2 * self.k2
        self.k6 = self.k4 * self.k2 * self.t1
        self.α1 = m.sqrt(1 + self.E.e2s) / self.E.a * (1 - self.k2 / 4 + 7 / 64 * self.k4 - 15 / 256 * self.k6)
        self.β1 = self.k2 / 4 - self.k4 / 8 + 37 / 512 * self.k6
        self.γ1 = (self.k4 - self.k6) / 128 * self.t2
        self.S = 1 / self.α1 * (self.σ - self.β1 * m.sin(self.σ) * m.cos(2 * self.M + self.σ) -
                                self.γ1 * m.sin(2 * self.σ) * m.cos(4 * self.M + 2 * self.σ))

        self.Result = [self.A1 * 180 / m.pi, self.A2 * 180 / m.pi, self.S]
        return self.Result


class Point():
    # 建立点类
    def LBAS(self, L1, B1, A1, S, T):  # 建立正算点类
        self.L1, self.B1, self.A1, self.S, self.T = L1, B1, A1, S, T
        self.P = Bessel()
        self.Result = self.P.Direct(self.L1, self.B1, self.A1, self.S, self.T)
        self.L2, self.B2, self.A2 = self.Result[0], self.Result[1], self.Result[2]

    def LBLB(self, L1, B1, L2, B2, T):  # 建立反算点类
        self.L1, self.B1, self.L2, self.B2, self.T = L1, B1, L2, B2, T
        self.P = Bessel()
        self.Result = self.P.Inverse(self.L1, self.B1, self.L2, self.B2, self.T)
        self.A1, self.A2, self.S = self.Result[0], self.Result[1], self.Result[2]

if __name__ == '__main__':
    P = Point()
    P.LBLB(120.692896455016, 36.3780045662363,120.692896455016 ,36.3707979442078 ,1 ) # 精度设置为米以下
    print(float(P.S))