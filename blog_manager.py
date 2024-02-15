#-*-coding: utf-8 -*-
import shortuuid
import pandas as pd
import os
import re

def get_permalink():
    # 读取历史uuid表
    file_name = 'url_record.xlsx'
    if not os.path.exists(file_name):
        df = pd.DataFrame(columns=['博文名称', '博文原链接', 'uuid', '博文新链接'])
        df.to_excel(file_name, index=False)
    else:
        df = pd.read_excel(file_name)
    history_uuid = set(df['uuid'])

    # 随机生成一个8位的uuid，保证该uuid不在历史uuid表中
    while True:
        new_uuid = shortuuid.ShortUUID().random(length=8)
        print(new_uuid)
        if new_uuid not in history_uuid:
            break

    # 将该uuid写入表中
    new_link = 'https://hubojing.github.io/' + new_uuid
    new_row = {'博文新链接': new_link, 'uuid': new_uuid}
    df = df.append(new_row, ignore_index=True)
    df.to_excel(file_name, index=False)
    return new_link


def get_word_cnt():
    file_path = './博客永久链接与计数.md'
    with open(file_path, 'r', encoding='utf-8') as file:
        st_flag = False
        content = ''
        for line in file.readlines():
            line = line.strip()
            line = line.replace('\n', '').replace(' ', '')
            if line == '<!--more-->':
                st_flag = True
            if st_flag:
                content += line
        pattern = r'[\u4e00-\u9fa5a-zA-Z0-9]' # 只计算中英文、数字
        result = re.findall(pattern, content)
        word_count = len(result)
    return word_count



if __name__== '__main__':
    new_link = get_permalink() # 获取uuid和记录文档
    print('永久链接：', new_link)
    word_count = get_word_cnt() # 获取文章字数
    print('文章字数：', word_count)




