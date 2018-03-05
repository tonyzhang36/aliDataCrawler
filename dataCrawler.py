# -*- encoding=utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import re
import fileDownloader
import dirMaker
import xlwt

def crawlData(baobeiUrl,itemCount,worksheet,xfStyle):
	sizeList=[]
	colorList=[]
	firstMainImg=''
	firstMainImgPath=''
	#无颜色图片的链接
#	baobeiUrl='https://detail.1688.com/offer/42201709111.html?spm=a360q.7751291.0.0.ldp7Cj'
	print '------------------------------>'
	print u'数据抓取开始，序号：%d，宝贝链接为：%s' % (itemCount,baobeiUrl)
	#请求页面内容
	try:
		response=urllib2.urlopen(baobeiUrl)
	except BaseException as e:
		print 'urlopen failed'
		return False
	finally:
		pass
	htmlDoc = response.read()


	#初始化网页解析器对象
	soup = BeautifulSoup(htmlDoc,'html.parser',from_encoding = 'utf-8')
	#print htmlDoc

	#print soup.body.attrs


	#找到宝贝的标题
	itemName = soup.find('h1', class_ = 'd-title')
	#print type(itemName)
	#print itemName
	if not itemName == None:
		name = itemName.get_text()
	else:
		print 'can\'t find itemName! stop'
		print u'数据抓取失败，序号：%d，可能原因：宝贝已下架'
		print '------------------------------<'
		return False
	fileSavePath = './%s/' %name
	dirMaker.mkdir(fileSavePath)
	
	#找到公司名称
	#<div class="company-name" title="汕头市潮阳区贵屿玉珊瑚针织厂">汕头市潮阳区贵屿玉珊瑚针织厂</div>
	companyName = soup.find('div', class_='company-name').get_text()
	print 'company:',companyName
	
	#保存原始网页内容
	htmlFile = open("%soriginal.html"%fileSavePath,'w+')
	htmlFile.write(htmlDoc)
	htmlFile.close()

	outFile = open("%sout.html"%fileSavePath,'w+')
	outFile.write("<!DOCTYPE html>")
	outFile.write("\r\n")
	outFile.write("<br>")
	outFile.write("<html>")
	outFile.write("\r\n")
	outFile.write("<br>")

	title = (r"<a href=%s>%s</a>") % (baobeiUrl,name.encode("utf-8"))
	outFile.write(title)
	outFile.write("\r\n")
	outFile.write("<br>")

	#查找主图链接（主图链接的alt属性和宝贝名称一致，利用此特点进行筛选）
	mainPicUrls = soup.find_all('img', alt=name)
	count = 1
	for url in mainPicUrls:
	#	print url.get('alt')
		alt = url.get('alt')
		src = url.get('src')
		data_lazy_src = url.get(r'data-lazy-src')
		if data_lazy_src == None:
			pass
		else:
			src = data_lazy_src
		sizeStr = re.search(r'([\w]+)x\1\.',src)
		if sizeStr:
			size = sizeStr.group()
			src = src.replace(size,'')
		else:
			pass
		httpsStr = re.search(r'https:',src)
		if httpsStr == None:
			src = 'https:%s' % src
		#print src
		filename = (src.split(r'/'))[-1]	
		filename = r'%s/%03d-%s-%s' % (fileSavePath,count,u'主图',filename)
		print filename
		print src
		fileDownloader.downloadFile(src,filename)
		if count == 1:
			firstMainImg = src
			firstMainImgPath = filename
		count+=1
		imgTag = "<img src=\"%s\">" % src
		outFile.write(imgTag)
		outFile.write("\r\n")
		outFile.write("<br>")

	'''
	有图：
	<div class="unit-detail-spec-operator active" data-unit-config="{&quot;name&quot;:&quot;黑色&quot;}" data-imgs="{&quot;preview&quot;:&quot;https://cbu01.alicdn.com/img/ibank/2018/671/910/8571019176_321387875.400x400.jpg&quot;,&quot;original&quot;:&quot;https://cbu01.alicdn.com/img/ibank/2018/671/910/8571019176_321387875.jpg&quot;}">
			<a rel="nofollow" hidefocus="true" class="image selected" title="黑色" href="#">
			<span class="vertical-img">
				<span class="box-img">
					<img src="https://cbu01.alicdn.com/img/ibank/2018/671/910/8571019176_321387875.32x32.jpg" alt="黑色">
				</span>
			</span>
			<div class="cor"></div>
		</a>
		</div>
	无图：
	<div class="unit-detail-spec-operator active" data-unit-config="{&quot;name&quot;:&quot;白色&quot;}">
			<a rel="nofollow" hidefocus="true" class="no-image selected" title="白色" href="#">
			<span class="text text-single-line">白色</span>
			<div class="cor"></div>
		</a>
		</div>
	'''
		
	#查找宝贝颜色图种类信息以及图片链接
	mainPicUrls = soup.find_all('div', class_ = re.compile("unit-detail-spec-operator?"))
	for url in mainPicUrls:
	#	print url
	#	color = re.split(r':',url['data-unit-config'])[1]
		color = re.sub(r'{|}|"|:|name','',url['data-unit-config'])
		colorList.append(color.encode('utf-8'))
		#检查颜色图片，若存在，则搜索图片地址并下载，若不存在，则跳过。
		dataImgsStr = re.search(r'data-imgs',url['data-unit-config'])
		if dataImgsStr == None:
			pass
		else:
			src = re.search(r'"original":"https:.+\.jpg"',url['data-imgs']).group()
			src = re.sub(r'"original":','',src)
			src = re.sub(r'"','',src)
			filename = (src.split(r'/'))[-1]
			filename = (r'%s/%03d-%s-%s')%(fileSavePath,count,color,filename)
		#	print filename
		#	print src
			fileDownloader.downloadFile(src,filename)
			count+=1
			imgTag = "<img src=\"%s\">" % src
			outFile.write(imgTag)
			outFile.write("\r\n")
			outFile.write("<br>")

	#输出颜色列表
	outFile.write('<a>')
	outFile.write('\r\n'.join(colorList))
	outFile.write('</a>\r\n<br>')

	print ('color:%s' % '，'.join(colorList)).decode('utf-8')

	#查找宝贝尺码种类
	#有的宝贝没有尺码属性（只有颜色属性），如：https://detail.1688.com/offer/545038862232.html?spm=b26110380.sw1688.mof001.1.bOJt0w&tracelog=p4p
	'''
	情况一：
	颜色一行，div的class是obj-leading；尺码一行，div的class是obj-sku
	情况二：
	颜色有多行，div的class是obj-sku，每行一个SKU；没有尺码行
	'''
	sizeNameList = soup.find_all('div', class_ = re.compile("obj-sku?"))
	for size in sizeNameList:
		for sizeName in size.find_all('td',class_='name'):
			sizeStr = sizeName.find('span').get_text()
			sizeList.append(sizeStr.encode('utf-8'))
		print ('size:%s' % '，'.join(sizeList)).decode('utf-8')
		pass
	outFile.write('<a>')
	outFile.write('\r\n'.join(sizeList))
	outFile.write('</a>\r\n<br>')

	#查找宝贝详情图链接（宝贝详情页是二次请求得到动态的变量之后，再次请求图片才进行展示的）
	
	'''
	情况一：
	<div id="mod-detail-description" class="mod-detail-description mod-info mod" data-mod-config='{"showOn":["mod-detail-description"],"title":"详细信息","tabConfig":{"trace":"tabdetail","showKey":"mod-detail-description"} ,"catalog":[{&quot;contentUrl&quot;:&quot;https://img.alicdn.com/tfscom/TB1lOqZSFXXXXXFXpXXXXXXXXXX&quot;,&quot;id&quot;:&quot;0&quot;,&quot;title&quot;:&quot;图文详情&quot;}] }' data-spm="descBanner">
	
			

	    <div class="de-description-detail fd-editor " id="de-description-detail" >
	    	    	    								<div id="desc-lazyload-container" class="desc-lazyload-container" data-url="https://laputa.1688.com/offer/ajax/OfferDesc.do" data-tfs-url="https://img.alicdn.com/tfscom/TB1bfmaSFXXXXbCapXXXXXXXXXX" data-enable="true">加载中...</div>
	
	情况二：
	<div id="mod-detail-description" class="mod-detail-description mod-info mod" data-mod-config='{"showOn":["mod-detail-description"],"title":"详细信息","tabConfig":{"trace":"tabdetail","showKey":"mod-detail-description"} }' data-spm="descBanner">
	
			
					

	    <div class="de-description-detail fd-editor nocatalog " id="de-description-detail" >
	    	    	    								<div id="desc-lazyload-container" class="desc-lazyload-container" data-url="https://laputa.1688.com/offer/ajax/OfferDesc.do" data-tfs-url="https://desc.alicdn.com/i4/530/180/536183983951/TB1uM6napmWBuNjSspd8qvugXla.desc%7Cvar%5Edesc%3Blang%5Egbk%3Bsign%5Eac4546617e98f15d70e88f354a5ff5c8%3Bt%5E1520052005" data-enable="true">加载中...</div>
														
	观察发现，情况二是通用的，以情况二作为提取标准
	'''
	mainPicUrl = soup.find('div',class_='desc-lazyload-container')
	url = mainPicUrl['data-tfs-url']
	content = urllib2.urlopen(url)
	#构造详情页面的BS对象
	contentSoup = BeautifulSoup(content.read(),'html.parser',from_encoding = 'utf-8')

	#找到详情页面的所有图片链接
	#某些img标签没有src属性，运行报错
	'''
	<img height="1" width="265" style="visibility: visible;"></td><td>
	<img height="1" width="130" style="visibility: visible;"></td><td>
	<img height="1" width="132" style="visibility: visible;"></td><td>	
	'''
	imgUrls = contentSoup.find_all('img', src = re.compile(r'https://|//'))
	for imgUrl in imgUrls:
	#	print imgUrl
		url = imgUrl['src'].replace(r'\"','')
		filename = (url.split(r'/'))[-1]	
		filename = (r'%s/%03d-%s-%s')%(fileSavePath,count,u'详情',filename)
		count+=1
	#	print url
		fileDownloader.downloadFile(url,filename)
		imgTag = "<img src=\"%s\">" % url
		outFile.write(imgTag)
		outFile.write("\r\n")
		outFile.write("<br>")
		
	outFile.write("</html>")
	outFile.close()


	worksheet.write(itemCount, 0, label = itemCount,style=xfStyle)
	worksheet.write(itemCount, 1 , label = name,style=xfStyle)
	worksheet.write(itemCount, 2 , label = xlwt.Formula('HYPERLINK("%s")'%(firstMainImg)),style=xfStyle)
	worksheet.write(itemCount, 3 , label = baobeiUrl,style=xfStyle)
	worksheet.write(itemCount, 4 , label = companyName,style=xfStyle)
	worksheet.write(itemCount, 5 , label = '',style=xfStyle)
	worksheet.write(itemCount, 6 , label = '',style=xfStyle)
	worksheet.write(itemCount, 7 , label = '\r\n'.join(sizeList),style=xfStyle)
	worksheet.write(itemCount, 8 , label = '\r\n'.join(colorList),style=xfStyle)


	#
	print u'数据抓取完毕，序号：%d，抓取宝贝为：%s' % (itemCount,name)
	
	print '------------------------------<'
	return True