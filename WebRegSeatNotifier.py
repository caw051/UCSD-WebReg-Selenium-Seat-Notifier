from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import smtplib
from selenium.webdriver.chrome.options import Options
import os

classToPick = "PHYS 2C"
startNonLectureTagNum = 1 #For DI, SE, PR, maybe labs, etc
NON_LECTURE_TAG_STR_LENGTH = 3
LECTURE_TAG_STR_LENGTH = 2
LAB_NUM_CODE = 50
seatNotifierMessage = ""

#----------------Working code----------------------

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

browser = webdriver.Chrome(options=chrome_options) #Init web driver to traverse and parse 

pageBeforeLogin = "https://students.ucsd.edu/academics/enroll/index.html" #Beginning url(as actual login site not directly accessable)

browser.get(pageBeforeLogin) #Gets url of the site

browser.find_element_by_link_text('WebReg').click() #Clicks on webreg to go into login. CHANGE INTO 

webregLoginSite = browser.current_url #Gets new url(as it is, after any redirects); should be login page

browser.get(webregLoginSite) #Gets url of site(this case is login site)

username = browser.find_element_by_id("ssousername") #Gettin//g respective ID for username(will see if correct)

time.sleep(5) #To avoid detection as robot(initially when going into webreg); seems to not be needed since even with the slow internet in China taking alot more than 5+ seconds, elements are still able to be picked

password = browser.find_element_by_id("ssopassword") #Getting respective name for username(will see if right; may need actual name of tag, etc.)

inputUsername = input("Please input your username\n")

inputPassword = input("Please input your password\n")

username.send_keys(inputUsername) #Sending username for login. May need to resort to text writing if things go wrong
password.send_keys(inputPassword) #Sending password for login; same problem as ^.

browser.find_element_by_name("_eventId_proceed").click() #Name of button is "Go" but name="continue".

time.sleep(5) #Waiting time(as it redirects); 6 seconds should be enough for it, but if completely busy traffic, you may need it here.

browser.find_element_by_link_text("Skip Two-Step Login").click()

time.sleep(5) #Waiting time(as it redirects); 6 seconds should be enough for it, but if completely busy traffic, you may need it here.

select = Select(browser.find_element_by_id('startpage-select-term')) #Automatically dragging cursor down.

select.select_by_visible_text("Fall Quarter 2019") #Selecting by visual text, e.gs are like "Summer Session" or "Spring Session"

browser.find_element_by_name("continue").click() #Clicks, and now going into webreg actual.

#<<ADD EXCEPTION CASE IF YOU ARE NOT DOING ANY DROPDOWN MENUS OR ANYTHING LIKE THAT>>



#---------------Lookup time ------------------------

#Once you actually get to the class you want to enroll. 
browser.find_element_by_id("s2id_autogen1").click()
browser.find_element_by_id("s2id_autogen1").send_keys(classToPick) #Just an example of what class to input into text box next to search button.

browser.find_element_by_id("select2-drop-mask").click() #Clicks on specific class shown in dropdown menu(the only way to make the next line work)
browser.find_element_by_xpath("//*[@id='search-div-t-b1']").click() #Clicks, and now going into webreg actual.

#---------------Class Searching time------------------------

time.sleep(5) #Waiting time(as it redirects); 5 seconds should be enough for it, but if completely busy traffic, you may need to make it longer

element2 = browser.find_element_by_id("search-div-b-tableghead_0_0").click() #The right way; this is going under the assumption that the classes are picked by selection

time.sleep(2) #Waiting time(as it redirects); 5 seconds should be enough for it, but if completely busy traffic, you may need to make it longer

print("---------------------------------------------------------Searching for starting lecture tags----------------------------------------------------------------------------")

try:
	startingLectureTag = "A00"
	startingPoint = browser.find_element_by_xpath("//tr[.//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + startingLectureTag +"' ]]") 
except:
	try:
		startingLectureTag = "001"
		startingPoint = browser.find_element_by_xpath("//tr[.//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + startingLectureTag +"' ]]") 
	except:
			print("Neither tag found. Must change algorithm.")
	else:
		#print("Hello; you just extracted 001 starting tag")
		confirmedStartTag = "001"
else:
	#print("Hey; if you are here, then you have extracted the startingLectureTag A00")
	confirmedStartTag = "A00"

#-------------------------Tag traversing(or extracting) time! Get all the tags here; below this line!-----------------------------



#------------------------Lecture tags first------------------
time.sleep(1)
#Getting all lecture tags if it is 001; might need to add the 2 zeroes; nothing seems to be done here
lectureTagArray = []
if(confirmedStartTag == "001"):
	print("---------------------------------Currently getting the 00 lecture based tags--------------------------------------------")
	tagNum = 1
	while(1):
		try:
			#Should give us 001 at at beginning and 010 when it comes
			tagNumStr = str(tagNum).zfill(NON_LECTURE_TAG_STR_LENGTH)
			print(tagNumStr)
			#The problem seems to be that if you end up 
			startingPoint = browser.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + tagNumStr +"' ]") #Exception will be caught here, before it tries to find an tag that doesn't exist
			lectureTagArray.append(startingPoint.text)
			tagNum +=1

		except:
			#Will take care of the off-by 1(forward direction) case here.
			try:
				#If 008 tag doesn't exist, but 009 does, it will mark the 009 in case. It will keep going until n-2 iterations(if a tag )
				tagNumStr = str(tagNum+1).zfill(NON_LECTURE_TAG_STR_LENGTH)
				print(tagNumStr)
				startingPoint = browser.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + tagNumStr +"' ]") #Exception will be caught here, before it tries to find an tag that doesn't exist
				lectureTagArray.append(startingPoint.text)
				tagNum +=2
			except:
				#Break out of the loop; all detectable tags for the classes found
				print("Array of tags now has: ")
				print(lectureTagArray)
				break

#Getting all lecture based tags that exist; there in case the tag found is A00 insteado of 001
if(confirmedStartTag == "A00"):
	print("---------------------------------------------------------Currently ALL LETTER based lecture based tags----------------------------------------------------------------------------")
	lectureLetter = 'A'
	while(1):
		try:
			#Appends lecture, then gets it, extracts it, places into array and so forth, going thru and getting A00, B00, ...
			tagNumStr = lectureLetter + "00"
			startingPoint = browser.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + tagNumStr +"' ]") #Exception will be caught here, before it tries to find an tag that doesn't exist
			
			lectureTagArray.append(startingPoint.text)
			lectureLetter = ord(lectureLetter)
			lectureLetter+=1
			lectureLetter = chr(lectureLetter)
		except:
			#Break out of the loop; all detectable tags for the classes found
			#print("Array of LE tags now has: ")
			#print(lectureTagArray)
			break 

#------------All possible LECTURE Tags collected; they can be used to get the info needed-------------------


#-----------Ideally, get a dropdown menu to be able to pick the lecture at this----------------------
lectureSearchedFor = "B00"

#Can hold DI/LA section Codes, and so on.
sectionTagArray = []

#(initially checking) If the A01 based tags are enrollable
if(confirmedStartTag == "A00"):
	print("------------------------------Currently getting the  DI based tags for selected lecture------------------------------")
	DILetter = lectureSearchedFor[0]
	tagNum = 1
	while(1):
		try:

			tagNumStr = str(tagNum).zfill(LECTURE_TAG_STR_LENGTH)
			tagNumStr = DILetter + tagNumStr

			#Searches for the DI based tag.
			startingPoint = browser.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + tagNumStr +"' ]") 

			#Not optimal, but for now, it gets the startingPoint's xpath(same exact, then gets prev. element, which is the section ID section; confirmed to work)
			sectionIDConfirmation = browser.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + tagNumStr +"' ]/preceding-sibling::td[@aria-describedby='search-div-b-table_SECTION_NUMBER']")
	
			#Actual str. for &nbsp: is apparently '\xa0'; everything else is fine
			if(sectionIDConfirmation.get_attribute("textContent") != '\xa0'):
				sectionTagArray.append(startingPoint.text)
				tagNum +=1				
			else:
				print("&nbsp found; not the designated tags to be used when distinguishing different sections with its respective seats")					
				break

		#When you finish dealing with all of the tags clickable
		except:
			#print("Array of DI tags now has: ")
			#print(sectionTagArray)
			break

#If the A01 based tags are unenrollable, i.e. tag is A00, and sectionTag array is 0(if it is not zero, then this must be skipped)
if(confirmedStartTag == "A00" and len(sectionTagArray) == 0):
	print("------------------------------Currently getting the A50 based tags for selected lecture------------------------------")
	DILetter = lectureSearchedFor[0]
	tagNum = LAB_NUM_CODE
	while(1):
		try:
			#Creating DI tag
			tagNumStr = str(tagNum).zfill(LECTURE_TAG_STR_LENGTH)
			tagNumStr = DILetter + tagNumStr

			#Searches for the DI based tag.
			startingPoint = browser.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + tagNumStr +"' ]") 
			
			#Capable of finding section number; if found, mission accomplished.
			sectionIDConfirmation = browser.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + tagNumStr +"' ]/preceding-sibling::td[@aria-describedby='search-div-b-table_SECTION_NUMBER']")
			
			#If section tag exists(note the get_attribute), it is enrollable and thus to be added.
			if(sectionIDConfirmation.get_attribute("textContent") != '\xa0'):
				sectionTagArray.append(startingPoint.text)
				tagNum +=1				
			else:
				break
		except:
			break

#------------All possible DI/LA Tags collected; they can be used to get the info needed; if 001 based tags picked, all of ^ that does deals w/ DI/LA will be skipped-------------------

#If 001 based tag, or if no clickable tags; rely solely on the LE(which only happens when no DI exists)
if(confirmedStartTag == "001" or len(sectionTagArray) == 0):
	
	print(lectureTagArray)

	#Getting parent tag to traverse down from
	EnrollableLectureCodeElement = browser.find_element_by_xpath("//tr[.//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + lectureSearchedFor + "' ]]")
	
	#Constructing the message directly; take out everything from "and section" up to sectionSearchedFor if no section(only LE) exists.
	seatNotifierMessage += "\n\n"
	seatNotifierMessage += "Course picked: " + classToPick + "; Lecture picked: " + lectureSearchedFor + '\n'
	seatNotifierMessage += "Seats Available: " + EnrollableLectureCodeElement.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_AVAIL_SEAT']").text + '\n' 
	seatNotifierMessage += "Seats Total " + EnrollableLectureCodeElement.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_SCTN_CPCTY_QTY']").text + '\n'
	seatNotifierMessage += "Waitlisted Total " + EnrollableLectureCodeElement.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_COUNT_ON_WAITLIST']").text + '\n'
	
	#print(seatNotifierMessage)
else:
	
	#Selected, temporarily, for our purposes. Real functionality wise, the user would have dropdown menu(based on accumulated array of sections) and would be able to pick the certain discussion at will.
	sectionSearchedFor = "B01"

	#print("section searched for is now: " + sectionSearchedFor)
	#Deals with DI/LA/ ... cases, where LE is not directly enrollable
	EnrollableSectionTagCodeElement = browser.find_element_by_xpath("//tr[.//td[@aria-describedby='search-div-b-table_SECT_CODE' and text()='" + sectionSearchedFor + "' ]]")

	#Extra line
	seatNotifierMessage += "\n\n"
	seatNotifierMessage += "Course picked: " + classToPick + "; Lecture picked: " + lectureSearchedFor + "; Section Picked " + sectionSearchedFor + '\n'
	seatNotifierMessage += "Seats Available: " + EnrollableSectionTagCodeElement.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_AVAIL_SEAT']").text + '\n' 
	seatNotifierMessage += "Seats Total " + EnrollableSectionTagCodeElement.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_SCTN_CPCTY_QTY']").text + '\n'
	seatNotifierMessage += "Waitlisted Total " + EnrollableSectionTagCodeElement.find_element_by_xpath(".//td[@aria-describedby='search-div-b-table_COUNT_ON_WAITLIST']").text + '\n'

print(seatNotifierMessage)

#Emails and notifies the student regarding seat count for a desired course.
server = smtplib.SMTP('smtp.gmail.com', 587)
server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
server.login('<The Email Used to Notify Students>', '<Password to the Email Used to Notify Students>') #Logs into the email address used to notify students about seat count.
server.sendmail('<The Email Used to Notify Students>','<Student Email to be Notified>', seatNotifierMessage) #Sends an email to a student with the seat count for a given course.

browser.close()

