path1 = r'E:\research\model\modelCoupling\文件型耦合实验\flooding_res.bdy'
path2 = r'E:\research\model\modelCoupling\文件型耦合实验\corr.txt'
resPath = r'E:\research\model\modelCoupling\文件型耦合实验\corr_res.txt'

fileBdy = open(path1)
fileCorr = open(path2)

corrs = {}
count = 0

for corr in fileCorr:
    arr = corr.split()
    
    corrs[arr[0]] = {
        'x':arr[1],
        'y':arr[2],
    }

for bdy in fileBdy:
    if count%5 == 0:
        # 获取到node值
        node = bdy.strip()
        if corrs.get(node, 0) != 0:
            arrRes = [node, corrs[node]['x'], corrs[node]['y']]
            with open(resPath, 'a+') as f:
                    f.write((' ').join(map(str, arrRes)))
                    f.write('\n')
    count += 1
