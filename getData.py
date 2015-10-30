# -*- coding: utf-8 -*-
import re
import DB
import LG
class FreeRoom:
	def __init__(self,weeknum = '1'):
		self.aid = '353'	#区
		self.buildingid = '1688'	#楼
		self.room = '-1'
		self.whichweek = weeknum	#周
		self.week = ['1','2','3','4','5','6','7']	#星期
		LG.login()	#登陆教务在线

	#获取数据并插入数据库
	def getData(self):
		url = 'http://202.118.201.228/academic/teacher/teachresource/roomschedule_week.jsdo'
		#提交周一至周日的表单数据
		for i in self.week:
			form_data = {
				'aid' : self.aid,
				'buildingid' : self.buildingid,
				'room' : self.room,
				'whichweek' : self.whichweek,
				'week' : i	#星期1-7
			}
			html = LG.s.post(url = url,data = form_data).text	#发送Post请求
			tmp = re.finditer(r'<tr style="display:" id="tr(.*?)".*?</table>',html,re.S)	#返回迭代器，即各教室
			for j in tmp:
				id = j.group(1)
				tr = re.findall(r'<tr align="center" >(.*?)</tr>',j.group(),re.S)
				lst = re.findall(r'<td.*?</td>',tr[1],re.S)
				cnt = 0		#记录课程节数
				for k in lst[::2]:
					cnt += 1
					if k[3] == ' ':
						flag = 0
					else:
						flag = 1
					DB.insert(id,i,cnt,flag)	#将数据插入数据库
					# print id,'week = ',i,'num = ',cnt,flag

if __name__ == '__main__':
	# weeknum = raw_input('Please input weeknum:')
	weeknum = 10
	t = FreeRoom(weeknum)
	t.getData()