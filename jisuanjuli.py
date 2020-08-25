import BesselQ
import os


SolveType = input('请输入解算类型：（键入D为正算，I为反算）\n')
while True:
    if SolveType == 'D' or SolveType == 'd':
        P1 = input('请依次输入P1点的坐标（L1，B1），方位角A1及大地线长S，中间用空格隔开：\n')
        while True:
            while True:
                try:
                    [L1, B1, A1, S] = [float(n) for n in P1.split()]
                    break
                except:
                    P1 = input('输入错误，请重新输入P1点的坐标（L1，B1），方位角A1及大地线长S，中间用空格隔开：\n')
            T = eval(input('请输入精度要求：（高于米级为1，米级为2，低于百米级为3）\n'))
            if T == 1 or 2 or 3:
                pass
            else:
                T = eval(input('输入错误，请重新输入精度要求：（高于米级为1，米级为2，低于百米级为3）\n'))
            P = BesselQ.Point()
            try:
                P.LBAS(L1, B1, A1, S, T)
                break
            except:
                P1 = input('输入错误，请重新输入P1点的坐标（L1，B1），方位角A1及大地线长S，中间用空格隔开：\n')
        L1, B1, A1, S, L2, B2, A2 = str(L1), str(B1), str(A1), str(S), str(P.L2), str(P.B2), str(P.A2)
        print('您输入P1点的坐标为：（' + L1 + '，' + B1 + '）\n方位角为：' + A1 + ',大地线长为：' + S)
        print('得到P2点的坐标为：（' + L2 + '，' + B2 + '）\n方位角为：' + A2)
        break

    elif SolveType == 'I' or SolveType == 'i':
        P1 = input('请依次输入P1点的坐标（L1，B1）及P2点的坐标（L2，B2），中间用空格隔开：\n')
        while True:
            while True:
                try:
                    [L1, B1, L2, B2] = [float(n) for n in P1.split()]
                    break
                except:
                    P1 = input('输入错误，请重新输入P1点的坐标（L1，B1）及P2点的坐标（L2，B2），中间用空格隔开：\n')
            T = eval(input('请输入精度要求：（高于米级为1，米级为2，低于百米级为3）\n'))
            if T == '1' or '2' or '3':
                pass
            else:
                T = eval(input('输入错误，请重新输入精度要求：（高于米级为1，米级为2，低于百米级为3）\n'))
            P = BesselQ.Point()
            try:
                P.LBLB(L1, B1, L2, B2, T)
                break
            except:
                P1 = input('输入错误，请重新输入P1点的坐标（L1，B1）及P2点的坐标（L2，B2），中间用空格隔开：\n')
        L1, B1, A1, S, L2, B2, A2 = str(L1), str(B1), str(P.A1), str(P.S), str(L2), str(B2), str(P.A2)
        print('您输入：\nP1点的坐标为：（' + L1 + '，' + B1 + '）\nP2点的坐标为：（' + L2 + '，' + B2 + '）')
        print('得到：\nP1点的方位角为：' + A1 + '\nP2点的方位角为：' + A2 + '\n大地线长为：' + S)
        break

    else:
        SolveType = input('输入错误，请重新输入解算类型：（键入D为正算，I为反算）\n')
os.system('pause')

