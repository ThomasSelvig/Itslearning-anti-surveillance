from faker import Faker
from bs4 import BeautifulSoup
import requests, progressbar, json, argparse

url = "https://afk.itslearning.com"


def getEverything(s, session, onlyStarred=False):
	stuff = []
	for course in progressbar.progressbar(getAllCourses(s, session)):
		if onlyStarred:
			if not course["starred"]:
				continue

		stuff += getAllContent(s, getCourseResourceFolder(s, course["id"], session), session)

	return stuff


def getCourseResourceFolder(s, course, session):
	r = s.get(f"{url}/ContentArea/ContentArea.aspx",
		params={"LocationID": course, "LocationType": 1},
		cookies={"ASP.NET_SessionId": session},
		headers={"User-Agent": Faker().firefox()})

	return BeautifulSoup(r.text, "html.parser").find("a", {"id": "link-resources"})["href"].split("=")[-1]

def getAllCourses(s, session):
	r = s.get(f"{url}/Course/AllCourses.aspx",
		cookies={"ASP.NET_SessionId": session},
		headers={"User-Agent": Faker().firefox()})

	items = []

	for tr in list(BeautifulSoup(r.text, "html.parser").find("table").find_all("tr"))[1:]:
		row = list(tr.find_all("td"))

		items.append({
			"title": row[2].getText(),
			"starred": row[3].find("input")["title"].lower() == "fjern stjernemerking",
			"date": row[4].getText(),
			"lastVisited": row[5].getText(),
			"id": row[2].find("a")["href"].split("=")[-1]
		})

	return items


def getFolderContents(s, folder, session):
	r = s.get(f"{url}/Folder/processfolder.aspx", 
		params={"FolderID": folder}, 
		cookies={"ASP.NET_SessionId": session},
		headers={"User-Agent": Faker().firefox()})

	folder = []

	for i in BeautifulSoup(r.text, "html.parser").find("table", {"class": "gridtable"}).find("tbody").find_all("tr"):
		row = list(i.find_all("td"))
		if len(row) == 1:
			# the folder is empty, displaying the message "Denne mappen er tom. "
			break

		try:
			folder.append({
				"title": row[1].getText(),
				"type": row[0].find("img")["alt"],
				"folder": row[0].find("img")["alt"] == "Mappe",
				"id": row[1].find("a")["href"].split("=")[-1],
				"suburl": row[1].find("a")["href"].split("?")[0],
				"param": row[1].find("a")["href"].split("?")[1].split("=")[0],
				"date": row[2].getText().split(" ")[0],
				"teacher": " ".join(row[2].getText().split(" ")[1:])
			})
		except:
			print(row)
			exit()

	return folder

def getAllContent(s, folder, session):
	stuff = []
	for item in getFolderContents(s, folder, session):
		if not item["folder"]:
			stuff.append(item)

		else:
			stuff += getAllContent(s, item["id"], session)

	return stuff


def getSoup(s, item, session):
	r = s.get(url + item["suburl"],
		params={item["param"]: item["id"]},
		cookies={"ASP.NET_SessionId": session},
		headers={"User-Agent": Faker().firefox()})

	if "SessionExpired" in r.text:
		exit("Session expired")

	return BeautifulSoup(r.text, "html.parser")


def main(session=None):
	s = requests.Session()
	assert len(session) < 16, "Provide session cookie (ASP.NET_SessionId)"

	print("Gathering IDs")
	stuff = getEverything(s, session, onlyStarred=False)

	print("\nRetrieving HTML from every item available")
	for item in progressbar.progressbar(stuff, redirect_stdout=True):
		#print(item["teacher"]+": "+item["type"]+": "+getSoup(s, item, session).find("title").getText())
		getSoup(s, item, session)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("session", help="ASP.NET_SessionId")
	main(parser.parse_args().session)
