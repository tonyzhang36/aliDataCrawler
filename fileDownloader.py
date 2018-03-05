# -*- encoding=utf-8 -*-
import urllib
import re

def downloadFile(url,filename):
	if re.match(r'^https?:/{2}\w.+$', url):
		pass
#		print("This looks valid.")
	else:
		print("This looks invalid.")
		return False
	urllib.urlretrieve(url,filename)
	return True

#downloadFile("http://www.baidu.com","ddd.txt")