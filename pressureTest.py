import requests 
url = 'http://221.226.60.2:8082/data/b3b30a0c-0ebf-477f-9464-2fd2620c0ced' 
count = 0
# 压力测试 连续请求
for i in range(1000):
    r = requests.get(url) 
    with open("E:\Projects\PythonScript\download\demo"+str(count)+".png", "wb") as code:
        code.write(r.content)
    count += 1