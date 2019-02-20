import jieba
import pandas as pd
import spacy
import sys
import time
import os
import re
from os import path
from spacy.tokenizer import Tokenizer

save_path = '../..'


def loadDataset(path1, path2):
    # 中文语料分词
    jieba.enable_parallel(16)  # 16个线程跑
    dirname = os.path.join(save_path, path1)  # 要读的目录
    cn_cut = os.path.join(save_path, 'cn_cut')  # 要写的目录

    with open(dirname) as  fr, open(cn_cut, 'w') as cn:
        for line in fr:
            if line.strip():
                cn.write(' '.join(jieba.cut(line)))

    # 英文语料分词
    nlp = spacy.load('en_core_web_sm', disable=['tagger', 'ner', 'parser'])
    dirnames = os.path.join(save_path, path2)  # 要读的目录
    en_cut = os.path.join(save_path, 'en_cut')  # 要写的目录

    with open(dirnames) as  fr, open(en_cut, 'w') as en:
        for line in fr:
            if line.strip():
                doc = nlp(line)
                tokens = [w.text for w in doc]
                en.write(' '.join(tokens))
    return cn_cut, en_cut


def testDataset(path1, path2):
    save_path = '../../corpus'
    out_path = '../../fast_align/build'
    # out_path = '../../corpus'
    dirname = os.path.join(save_path, path1)  # 要读的目录
    dirnames = os.path.join(save_path, path2)  # 要读的目录
    train_cn_en = os.path.join(out_path, 'train.cn-en')  # 要写的目录

    with open(dirname) as fr, open(dirnames) as dr, open(train_cn_en, 'w') as tr:
        for line in fr:
            tr.write(line.strip())
            tr.write(' ||| ')
            # tr.write('\n')
            tr.write(dr.readline())


def commaDataset(path1, path2, path3):
    cn = os.path.join(save_path, path1)  # 要读的cn corpus
    en = os.path.join(save_path, path2)  # 要读的en cropus
    align = os.path.join(save_path, path3)  # 要读的align corpus
    analysis = os.path.join(save_path, 'analysis')  # 要写的目录 分析

    comma_dict = {}
    with open(align) as fr, open(cn) as cr, open(en) as er, open(analysis, 'w') as wr:
        comma_1 = ','
        comma_2 = '，'
        comma_alnum = 0  # 逗号-字母数字
        comma_cma = 0  # 逗号-逗号
        comma_period = 0  # 逗号-句号
        comma_semicolon = 0  # 逗号-分号
        other = 0  # 逗号-其他情况，数据保留

        for line in fr:
            cn_line = cr.readline()
            en_line = er.readline()

            cn = []
            for count, item in enumerate(cn_line.split()):
                if item == comma_2:
                    cn.append(count)  # 确定cn corpus中逗号的位置，并存入列表cn

            cn = sorted(list(cn))  # 去重，排序

            align_dict = {}  # 将fast-liagn元素存储为一个字典，cn为key,映射为en
            part = "([0-9]+)\-([0-9]+)"
            for item in line.split():
                match = re.match(part, item)
                key = match.group(1)
                value = int(key)
                if (key not in align_dict) and (value in cn):
                    align_dict[key] = []
                    align_dict[key].append(match.group(2))  # 只保存中文中","对应的列表

            en = []
            en = [en.extend(w) for w in align_dict.values()]  # 将对应的英文标号合并到一个列表中
            en = sorted(list(set(en)))  # 去重，排序

            for count, item in enumerate(en_line.split()):  # 判断各种情况
                if count in en:
                    if item == comma_1:
                        comma_cma += 1
                    elif item.isalnum():
                        comma_alnum += 1
                    elif item == '.':
                        comma_period += 1
                    elif item == ',':
                        comma_semicolon += 1
                    else:
                        other += 1
                        wr.write(item)

            #将结果转化成字典，进一步转化成Dataframe，便于分析
        align={'comma_cma': , 'comma_alnum': , 'comma_period': ,'comma_semicolon': ,'other': }
        df = pd.DataFrame(data=align)
        print(align)



if __name__ == "__main__":
    # cn_cut,en_cut=loadDataset('abst_cn', 'abst_en')   #分词任务,返回文件路径

    # testDataset('cn_cut','en_cut')#用fast_align测试

    commaDataset('cn_test', 'en_test', 'traindata_test')  # 检索到逗号，存储为字典格式，结构为：
    # dict{‘cn’:{'comma_num':number,'comma_isalpha':[number,frequency],
    # 'comma_isdigital':[number,frequency],'comma_iscomma':[number,frequency]},
    # 'en':{...},
    # 'fast-align':{...},
    # }




