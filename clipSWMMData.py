import os

# 将fenhu.asc外面的数据裁掉
bdypath = r'E:\research\model\modelCoupling\lisflood\30_res_timeSim_9_11_1.bdy'
bcipath = r'E:\research\model\modelCoupling\lisflood\node_corrd.bci'
wbdyPath = r'E:\research\model\modelCoupling\lisflood\30_res_timeSim_9_11_1_clip.bdy'
wbciPath = r'E:\research\model\modelCoupling\lisflood\node_corrd_clip.bci'

fileBdy = open(bdypath)
fileBci = open(bcipath)

#边界数据
tleft = [13451951.3544, 3616138.04956]
tright = [13452595.1145, 3616138.04956]
bleft = [13451951.3544, 3614948.84919]
bright = [13452595.1145, 3614948.84919]
count1 = 0
for bci in fileBci:
    bciarr = bci.split()
    if float(bciarr[1]) < 13451951.3544 or float(bciarr[1]) > 13452595.1145 or float(bciarr[2]) < 3614948.84919 or float(bciarr[2]) > 3616138.04956:
        count1 += 1
        continue
    else:
        with open(wbciPath, 'a+') as f1:
            # bdy写入
            f1.write(bci)
            # bci写入
            begin = count1 * 27
            end = (count1+1)*27
            count2 = 0
            # 关闭bdy的open，重新打开文件读取
            fileBdy.close()
            fileBdy = open(bdypath)
            for bdy in fileBdy:
                if count2 < begin:
                    count2+=1
                    continue
                elif count2>=begin and count2<end:
                    with open(wbdyPath, 'a+') as f2:
                        # bci写入
                        f2.write(bdy)
                else:
                    break
                count2+=1
    count1 += 1