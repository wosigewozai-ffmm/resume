import pdfplumber
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFTextExtractionNotAllowed

# for num in range(1, 7):
#     print(num)
#     path = str(num)+".pdf"
#     try:
#
#
#         # 用文件对象来创建一个pdf文档分析器
#         parser = PDFParser(open(path, 'rb'))
#         # 创建一个PDF文档
#         doc = PDFDocument(parser)
#         # 连接分析器 与文档对象
#         parser.set_document(doc)
#
#         # 提供初始化密码
#
#
#         # 检测文档是否提供txt转换，不提供就忽略
#         if not doc.is_extractable:
#             raise PDFTextExtractionNotAllowed
#         else:
#             # 创建PDf 资源管理器 来管理共享资源
#             rsrcmgr = PDFResourceManager()
#             # 创建一个PDF设备对象
#             laparams = LAParams()
#             device = PDFPageAggregator(rsrcmgr, laparams=laparams)
#             # 创建一个PDF解释器对象
#             interpreter = PDFPageInterpreter(rsrcmgr, device)
#
#             # 循环遍历列表，每次处理一个page的内容
#             for page in PDFPage.create_pages(doc):
#                 interpreter.process_page(page)
#                 # 接受该页面的LTPage对象
#                 layout = device.get_result()
#                 # 这里layout是一个LTPage对象，里面存放着这个 page 解析出的各种对象
#                 # 包括 LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等
#                 for x in layout:
#                     if isinstance(x, LTTextBox):
#                         print(x.get_text().strip())
#
#     except KeyError:
#         with pdfplumber.open(path) as pdf:
#             page_count = len(pdf.pages)
#             print(page_count)  # 得到页数
#             for page in pdf.pages:
#                 print('---------- 第[%d]页 ----------' % page.page_number)
#                 # 获取当前页面的全部文本信息，包括表格中的文字
#                 print(page.extract_text())

from docx import Document
import re
import jieba

allAcademy = []
jieba.load_userdict("schooldict.txt")
jieba.load_userdict("academydict.txt")
for line in open("schooldict.txt", "r", encoding='utf-8', errors='ignore'):  # 设置文件对象并读取每一行文件
    strline = str(line)
    allAcademy.append(strline[0:strline.find(" ")])

for line in open("academydict.txt", "r", encoding='utf-8', errors='ignore'):  # 设置文件对象并读取每一行文件
    strline = str(line)
    allAcademy.append(strline[0:strline.find(" ")])

doc = Document('5.docx')

# 学校列表
academyList = []
academyPos = []
wordPos = 0
educateFlag = []
educateFlagPos = []
educateNum = 0
academyDistance = 20

# 每一段的内容
for para in doc.paragraphs:
    # 正则匹配身份证号
    pattern_idNumber = re.compile('\D[0-9]{17}[0-9|x|X]\D')
    str = para.text
    seg_list = jieba.lcut(str, cut_all=False)
    # 是否存在XX大学/学院
    for seg in seg_list:
        wordPos = wordPos + 1
        if (seg in allAcademy):
            academyList.append(seg)
            academyPos.append(wordPos)
        if (seg == "专科") | (seg == "本科") | (seg == "硕士") | (seg == "博士"):
            if not (seg in educateFlag):
                educateNum = educateNum + 1
            educateFlag.append(seg)
            educateFlagPos.append(wordPos)
    str = " " + str + " "
    id_Number = pattern_idNumber.findall(str)
    if len(id_Number) > 0:
        id_Number[0] = id_Number[0][1:len(id_Number[0]) - 1]
        print("身份证号：", id_Number[0])
    # 正则匹配手机号
    pattern_phoneNumber = re.compile('\D[0-9]{11}\D')
    phone_Number = pattern_phoneNumber.findall(str)
    if len(phone_Number) > 0:
        phone_Number[0] = phone_Number[0][1:len(phone_Number[0]) - 1]
        print("手机号：", phone_Number[0])
    # 正则匹配邮箱信息
    pattern_mailAddress = re.compile('[0-9a-zA-Z.]+@[0-9a-zA-Z.]+?com')
    mail_Address = pattern_mailAddress.findall(str)
    if len(mail_Address) > 0:
        print("邮箱：", mail_Address[0])
    # 性别信息
    pattern_sex = re.compile('[^\u4E00-\u9FFF][男|女][^\u4E00-\u9FFF]')
    person_sex = pattern_sex.findall(str)
    if len(person_sex) > 0:
        person_sex[0] = person_sex[0][1:len(person_sex[0]) - 1]
        print("性别：", person_sex[0])
    # 正则匹配年龄信息
    pattern_age = re.compile('\D([0-9]{1,3})岁')
    person_age = pattern_age.findall(str)
    if len(person_age) > 0:
        print("年龄：", person_age[0])
# 匹配学历信息
for i in range(0, len(academyList) - educateNum + 1):
    for j in range(0, len(educateFlag) - educateNum + 1):
        flag = True
        duplicate = []
        for k in range(0, educateNum):
            if educateFlag[j + k] in duplicate:
                flag = False
            duplicate.append(educateFlag[j + k])
            if abs(academyPos[i + k] - educateFlagPos[j + k]) > academyDistance:
                flag = False
        if flag:
            for k in range(0, educateNum):
                print(educateFlag[j + k], ":", academyList[i + k])
