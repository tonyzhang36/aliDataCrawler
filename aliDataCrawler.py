# -*- encoding=utf-8 -*-
import xlwt
import dataCrawler
import time

'''
urlLists = ['https://detail.1688.com/offer/561115721722.html?spm=a360q.7751291.0.0.BkuyHl',\
'https://detail.1688.com/offer/42201709111.html?spm=a360q.7751291.0.0.ldp7Cj',\
'https://detail.1688.com/offer/525600411538.html?spm=a2615.2177701.0.0.24462deaC4zEUu'\
]
'''

urlListFile = open('./destUrl.txt')
tempList = urlListFile.readlines()
urlListFile.close()
#print tempList
urlLists = []
for url in tempList:
	src = url.replace('\n','')
	if src in urlLists:
		continue
	else:
		urlLists.append(src)

print urlLists

print '---------------start process---------------'
#写入excel文件
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('My Worksheet')

alignment = xlwt.Alignment() # Create Alignment
alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
alignment.vert = xlwt.Alignment.VERT_CENTER | xlwt.Alignment.WRAP_AT_RIGHT # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
xfStyle = xlwt.easyxf('align: wrap on') # Create Style
xfStyle.alignment = alignment # Add Alignment to Style

worksheet.write(0, 0, label = '序号')
worksheet.write(0, 1, label = '名称')
worksheet.write(0, 2, label = '图片')
worksheet.write(0, 3, label = '链接')
worksheet.write(0, 4, label = '供货商名称')
worksheet.write(0, 5, label = '简称')
worksheet.write(0, 6, label = '代号')
worksheet.write(0, 7, label = '尺码')
worksheet.write(0, 8, label = '颜色种类')
worksheet.write(0, 9, label = '颜色;尺码;订货数量（件）')
worksheet.write(0, 10, label = '订货总数量（件）')
worksheet.write(0, 11, label = '进货价格（元/件）')
worksheet.write(0, 12, label = '运费（元/单）')
worksheet.write(0, 13, label = '订单总价（元）')
worksheet.write(0, 14, label = '每件成本（元/件）')
worksheet.write(0, 15, label = '引流款定价(定价=成本价+运费(7元)+附加价值)')
worksheet.write(0, 16, label = '利润款定价(定价=成本价+运费+售后费用+附加价值费用+推广费用10%)')
worksheet.write(0, 17, label = '是否提供数据包')
worksheet.write(0, 18, label = '支持一件代发')
worksheet.write(0, 19, label = '价格是否优惠')
worksheet.write(0, 20, label = '供货商链接')
worksheet.write(0, 21, label = '客服响应速度与态度')
worksheet.write(0, 22, label = '支付方式')
worksheet.write(0, 23, label = '备注')
worksheet.write(0, 24, label = '到货时间')
worksheet.write(0, 25, label = '验货')
	
itemCount=1
for baobeiUrl in urlLists:
	#print baobeiUrl
	isSuc = dataCrawler.crawlData(baobeiUrl,itemCount,worksheet,xfStyle)
	if isSuc:
		itemCount += 1

fileSavePath='./'
resultFileName='%s%s%s.xls'%(fileSavePath,"result",time.strftime("%Y%m%d%H%M%S", time.localtime()) )
workbook.save(resultFileName)

print '---------------finish process---------------'