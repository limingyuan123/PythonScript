#coding=utf-8
def reconstructBUS():
    lines=[]
    f=open(r"E:\Projects\SWMM_LISFLOOD_Solution\Core\mainCopy.cpp",'r', encoding='UTF-8') #your path!
    for line in f:
        lines.append(line)
    f.close()
    lineCount = {}

    # 刷新标识的位置
    def updateLineCount(key, num):
        index1 = 0
        index2 = 0
        for item in lineCount:
            index1 += 1
            if item == key:
                break
        for item in lineCount:
            index2 += 1
            if index1 < index2:
                lineCount[item] += num

    count = 0
    for line in lines:
        count += 1
        if line.startswith('//[MAIN]'):
            lineCount['MAIN'] = count
        if line.startswith('//[CONFIG]'):
            lineCount['CONFIG'] = count
        if line.startswith('//[LOAD_CONFIG]'):
            lineCount['LOAD_CONFIG'] = count
        if line.startswith('//[INIT_MODEL]'):
            lineCount['INIT_MODEL'] = count
        if line.startswith('//[INIT_PARAMETER]'):
            lineCount['INIT_PARAMETER'] = count
        if line.startswith('//[GET_PARAMETER]'):
            lineCount['GET_PARAMETER'] = count
        if line.startswith('//[CUSTOM_PARAMETER]'):
            lineCount['CUSTOM_PARAMETER'] = count
        if line.startswith('//[SPACE_THORW_COUNT]'):
            lineCount['SPACE_THORW_COUNT'] = count
        if line.startswith('//[TIME_MATCH]'):
            lineCount['TIME_MATCH'] = count
        if line.startswith('//[TIME_MATCH_WHILE]'):
            lineCount['TIME_MATCH_WHILE'] = count
        if line.startswith('//[CYCLE_RELATE]'):
            lineCount['CYCLE_RELATE'] = count
        if line.startswith('//[INTERACTIVE]'):
            lineCount['INTERACTIVE'] = count
        if line.startswith('//[SPACE_MATCH]'):
            lineCount['SPACE_MATCH'] = count
        if line.startswith('//[LOGICAL_INTERACTION]'):
            lineCount['LOGICAL_INTERACTION'] = count
        if line.startswith('//[END_SIMULATION]'):
            lineCount['END_SIMULATION'] = count

    for line in lines:
        if line.startswith('//[MAIN]'):
            lines.insert(lineCount['MAIN'], "sss\n")
            # 根据配置插入内容
            num = 1
            updateLineCount('MAIN', num)
        elif line.startswith('//[CONFIG]'):
            lines.insert(lineCount['CONFIG'], "sss\n")
            num = 1
            updateLineCount('CONFIG', num)
            
        elif line.startswith('//[LOAD_CONFIG]'):
            lines.insert(lineCount['LOAD_CONFIG'], "sss\n")
            num = 1
            updateLineCount('LOAD_CONFIG', num)
            
        elif line.startswith('//[INIT_MODEL]'):
            lines.insert(lineCount['INIT_MODEL'], "sss\n")
            num = 1
            updateLineCount('INIT_MODEL', num)
            
        elif line.startswith('//[INIT_PARAMETER]'):
            lines.insert(lineCount['INIT_PARAMETER'], "sss\n")
            num = 1
            updateLineCount('INIT_PARAMETER', num)
            
        elif line.startswith('//[GET_PARAMETER]'):
            lines.insert(lineCount['GET_PARAMETER'], "sss\n")
            num = 1
            updateLineCount('GET_PARAMETER', num)
            
        elif line.startswith('//[CUSTOM_PARAMETER]'):
            lines.insert(lineCount['CUSTOM_PARAMETER'], "sss\n")
            num = 1
            updateLineCount('CUSTOM_PARAMETER', num)
            
        elif line.startswith('//[SPACE_THORW_COUNT]'):
            lines.insert(lineCount['SPACE_THORW_COUNT'], "sss\n")
            num = 1
            updateLineCount('SPACE_THORW_COUNT', num)
            
        elif line.startswith('//[TIME_MATCH]'):
            lines.insert(lineCount['TIME_MATCH'], "sss\n")
            num = 1
            updateLineCount('TIME_MATCH', num)
            
        elif line.startswith('//[TIME_MATCH_WHILE]'):
            lines.insert(lineCount['TIME_MATCH_WHILE'], "sss\n")
            num = 1
            updateLineCount('TIME_MATCH_WHILE', num)
            
        elif line.startswith('//[CYCLE_RELATE]'):
            lines.insert(lineCount['CYCLE_RELATE'], "sss\n")
            num = 1
            updateLineCount('CYCLE_RELATE', num)
            
        elif line.startswith('//[INTERACTIVE]'):
            lines.insert(lineCount['INTERACTIVE'], "sss\n")
            num = 1
            updateLineCount('INTERACTIVE', num)
            
        elif line.startswith('//[SPACE_MATCH]'):
            lines.insert(lineCount['SPACE_MATCH'], "sss\n")
            num = 1
            updateLineCount('SPACE_MATCH', num)
            
        elif line.startswith('//[LOGICAL_INTERACTION]'):
            lines.insert(lineCount['LOGICAL_INTERACTION'], "sss\n")
            num = 1
            updateLineCount('LOGICAL_INTERACTION', num)  

        elif line.startswith('//[END_SIMULATION]'):
            lines.insert(lineCount['END_SIMULATION'], "sss\n")
            num = 1
            updateLineCount('END_SIMULATION', num)

    s=''.join(lines)
    f=open(r"E:\Projects\SWMM_LISFLOOD_Solution\Core\mainCopy.cpp",'w+', encoding='UTF-8') #重新写入文件
    f.write(s)
    f.close()
    del lines[:] #清空列表
    print (lines)

if __name__ == '__main__':
    reconstructBUS()