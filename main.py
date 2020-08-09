from bs4 import BeautifulSoup
import requests
import json
import os
import time

# Change these values
username = "<Enter your Username>"
password = "<Enter your Password>"
current_major = "<Enter your current major>" # exact spelling from myUW profile


# Don't change anything below
payload = {"_eventId_proceed":True,'j_username': username,'j_password': password}
url = "https://my.uw.edu/profile/"


def find_major() -> None:
    with requests.Session() as session:
        responce = session.get(url)
        soup = BeautifulSoup(responce.text,"html.parser")

        login_page = "https://idp.u.washington.edu/" + soup.form["action"]
        responce2 = session.post(login_page,data=payload)
        soup = BeautifulSoup(responce2.text,"html.parser")
        login_redirect = soup.form["action"] 
        
        for x in soup.find_all("input"):
            try:
                x["name"]
            except:
                payload[x["type"]] = x["value"]
            else:
                payload[x["name"]] = x["value"]

        session.post(login_redirect,data=payload)
        reply = session.get("https://my.uw.edu/api/v1/profile/")
        info = json.loads(reply.text)
        major = info["term_majors"][0]["majors"][0]["full_name"]

    if major == current_major:
        # To test if the program works for notifying the current major, uncomment the line below
        #os.system("osascript -e \'display notification \""+str(major)+"\" with title \"REGISTER!!!\"\'")
        pass

    else:
        os.system("osascript -e \'display notification \""+str(major)+"\" with title \"REGISTER!!!\"\'")

if __name__ == "__main__":
    # please don't decrease the 600 below. 
    # That would mean sending too many requests to the UW servers.
    while True:
        find_major()
        time.sleep(600) # 600 seconds =  10 minutes 
