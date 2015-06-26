# coding=utf-8
__author__ = 'bxm'
import sys
from utils.database import get_mongodb

reload(sys)
sys.setdefaultencoding("utf8")


#将ViewSpot中zhName写入文件
def zhName_to_file(filename):

    viewspot_conn = get_mongodb("poi", "ViewSpot", "mongo")
    cursor = viewspot_conn.find()

    f = open(filename, 'a')
    i = 0
    for val in cursor:
        i = i + 1
        if val.has_key('zhName'):
            s = str(val['zhName']) + '\n'
            f.write(s)
        if i % 1000 == 0:
            f.flush()
    f.close()

# 剔除包含英文的词，保留纯中文词
def zh_eliminate_en(filename1,filename2):
    f1=open(filename1,'r')
    f2=open(filename2,'a')
    for line in f1:
        # if check_contain_chinese(line):
        if check_all_chinese(line):
            f2.write(line)
    f2.close()
    f1.close()


# 判断字符串中是否包含中文
def check_contain_chinese(check_str):
    # check_str解码为unicode
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

# 判断字符串中是否全是中文
def check_all_chinese(check_str):
    check_str=check_str[:-1]
    for ch in check_str.decode('utf-8'):
        if not u'\u4e00' <= ch <= u'\u9fff':
            return False
    return True

# windows文本文件转为linux文件
def windows_to_linux(windows_f,linux_f):
    lines=list(open(windows_f,'r'))
    if lines[0][-1]=='\n' and lines[0][-2]=='\r':
        fl=open(linux_f,'w')
        for f in lines:
            fl.write(f[:-2]+'\n')
        fl.close()
    else:
        print '非windows文件'
        return


# 将ik词库中没有的词，加入到ik or newDic中
def add_to_ikDic(myDic, ikDic, newDic=None):
    i=0
    f2=open(ikDic,'r')
    lines=list(f2)
    f2.close()

    f1=open(myDic,'r')
    if not newDic:
        f2=open(ikDic,'a')
        for word in f1:
            if word not in lines:
                f2.write(word)
            i+=1
            if i%500==0:
                f2.flush()
                print '已合并单词数:',i
        f2.close()
    else:
        f3=open(newDic,'a')
        for word in f1:
            if word not in lines:
                f3.write(word)
            i+=1
            if i%500==0:
                f3.flush()
                print '已合并单词数:',i
        f3.close()

    f1.close()
    print '合并单词结束,共合并单词数:',i



if __name__ == '__main__':
    #
    lines=list(open("./../sgou/ik/main_chs.dic",'r'))
    print lines[-3:]
    # zh_eliminate_en("./../viewspotDic_1","./../viewspotDic_2")
    #add_to_ikDic("./../sgou/5.txt","./../sgou/sougou.txt")
    #add_to_ikDic("./../sgou//ik/professional.dic","./../sgou/ik/main_chs.dic","./../sgou/ik/pro2.dic")


    #windows_to_linux("./../sgou/ik/sougou.dic",'./../sgou/ik/sougou2.dic')

    #add_to_ikDic('./../sgou/ik/main_chs.dic','./../sgou/ik/main.dic','./../sgou/ik/sb.dic')
