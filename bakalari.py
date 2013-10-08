# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
from htmldom import htmldom


class Bakalari():
	def __init__(self, user, passsword, baseUrl):
		self.baseUrl = baseUrl
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		self.opener.addheaders.append(('User-agent', "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko)Chrome/6.0.472.62 Safari/534.3"))
		self.login(user, passsword)

	def login(self, user, password):
		html = urllib.urlopen(self.baseUrl).read()
		dom = htmldom.HtmlDom().createDom(html)
		vs = dom.find("input#__VIEWSTATE").attr("value")

		postData = dict()
		postData["__LASTFOCUS"] = ""
		postData["__EVENTTARGET"] = ""
		postData["__EVENTARGUMENT"] = ""
		postData["__VIEWSTATE"] = vs
		postData["ctl00$cphmain$TextBoxjmeno"] = user
		postData["ctl00$cphmain$TextBoxheslo"] = password
		postData["ctl00$cphmain$ButtonPrihlas"] = ""

		self.opener.open(self.baseUrl + 'login.aspx', urllib.urlencode(postData))


	def getGrades(self):
		html = self.opener.open(self.baseUrl + 'prehled.aspx?s=2').read()

		dom = htmldom.HtmlDom().createDom(html)
		vs = dom.find("input#__VIEWSTATE").attr("value")
		ev = dom.find("input#__EVENTVALIDATION").attr("value")

		postData = dict()
		postData["__EVENTTARGET"] = "ctl00$cphmain$Checkdetail"
		postData["__EVENTARGUMENT"] = ""
		postData["__LASTFOCUS"] = ""
		postData["__VIEWSTATE"] = vs
		postData["__EVENTVALIDATION"] = ev
		postData["ctl00$cphmain$Flyout2$Checktypy"] = "on"
		postData["ctl00$cphmain$Flyout2$Checkdatumy"] = "on"


		html = self.opener.open(self.baseUrl + 'prehled.aspx?s=2', urllib.urlencode(postData)).read()

		dom = htmldom.HtmlDom().createDom(html)

		gradesDom = dom.find("table.radekznamky")
		#print gradesDom.html()

		subjects = gradesDom.children().toList()

		subjectsArr = list()
		subInd = 0
		for sub in subjects:
			subName = sub.firstChild().firstChild().firstChild().firstChild().text
			subjectsArr.append({'name': subName, "grades": []})

			subDom = htmldom.HtmlDom().createDom(sub.html())
			gradesDom = subDom.find("tr.detznamka")
			gradeInd = 0
			for grade in gradesDom.find("td").toList():
				gradeTitle = grade.attr("title").strip()
				gradeText = grade.getText().strip()
				gradeDate = subDom.find("tr.datum").find("td").toList()[gradeInd].getText().strip()
				gradeWeight = subDom.find("tr.typ").find("td").toList()[gradeInd].getText().strip()
				subjectsArr[subInd]["grades"].append({"title": gradeTitle, "grade": gradeText, "date": gradeDate, "weight": gradeWeight})
				gradeInd += 1

			subInd += 1
		return subjectsArr

	def getTimetable(self):
		html = self.opener.open(self.baseUrl + 'prehled.aspx?s=6').read()

		dom = htmldom.HtmlDom().createDom(html)

		gradesDom = dom.find("table.rozbunka")
		print gradesDom.html()



