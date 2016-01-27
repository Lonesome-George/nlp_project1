#coding:utf-8

#对于多份标注的语料，选出大家标注一致的保存至文件

import os

def proc_line(line):
    sp_list = line.split('\t')
    return sp_list[0], sp_list[1], sp_list[2]

if __name__ == '__main__':
    files_dir = './annotated'
    annotated_files = []
    for parent,dirnames,filenames in os.walk(files_dir):
        for filename in filenames:
            annotated_files.append(os.path.join(parent, filename))

    annotated_list = [] # 所有标注结果
    for filename in annotated_files:
        anno_dict = {}
        f = file(filename, 'r')
        while True:
            line = f.readline().decode("utf-8")
            if len(line) == 0: # Zero length indicates EOF
                break
            id,label,text = proc_line(line)
            anno_dict[id] = [int(label), text]
        f.close()
        annotated_list.append(anno_dict)

    for annotated in annotated_list:
        print annotated
    length = len(annotated_list)
    if length == 0:
        exit()
    id_list = []
    for id in annotated_list[0]:
        all_choose = True #是否所有人都选择了该文本
        for i in range(1, length):
            if not annotated_list[i].has_key(id):
                all_choose = False
                break
        if all_choose == True:
            id_list.append(id)
    print 'choose:', id_list
    for id in id_list:
        for i in range(1, length):
            if annotated_list[i][id][0] != annotated_list[0][id][0]:
                id_list.remove(id)
                string = id + ' '
                for j in range(length):
                    string += str(annotated_list[j][id][0]) + ' '
                print string
                break

    # 将大家都选中并且标注一致的文本输出到文件
    file_out = './annotated/output.txt'
    f = open(file_out, 'w')
    for id in id_list:
        string = id + '\t' + str(annotated_list[0][id][0]) + '\t' + annotated_list[0][id][1]
        f.write(string.encode('utf-8'))
    f.close()
