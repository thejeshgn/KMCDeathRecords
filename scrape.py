import os
import requests
import time
import datetime
import json
from datetime import date, timedelta

url = "https://www.kmcgov.in/KMCPortal/KMCDeathRegistrationAction.do"
START_DATE = date(2010, 1, 1)
END_DATE = date(2021, 6, 11)
RESTRT_DELAY = 60
REQUEST_DELAY = 2
name_patern = "%%%"
raw_data_folder = "./raw"
raw_data_file_name = "./raw/{current_running_date_file_name_str}.json"

cookies = {
    "JSESSIONID": "ac10a13530d8348beacc48f24ac48dcdb41a7a672079.e34Ta3iQchiMay0Rb30NbxeTbhr0n6jAmljGr5XDqQLvpAe.1",
}

headers = {
    "Accept": "*/*",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.kmcgov.in",
    "Referer": "https://www.kmcgov.in/KMCPortal/jsp/KMCDeathRecordSearch.jsp",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
}

params = (("var", "getVal"),)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_latest_scrape_date():
    l = os.listdir(raw_data_folder)
    last_scraped_file = max(l)
    if len(l) == 0 or last_scraped_file is None:
        return None
    last_scraped_file = last_scraped_file.replace(".json", "")
    d = datetime.datetime.strptime(last_scraped_file, "%Y-%m-%d")
    return d.date()


def scrape_now(start_date, end_date):
    for current_running_date in daterange(start_date, end_date):
        current_running_date_str = current_running_date.strftime("%d/%m/%Y")
        current_running_date_file_name_str = current_running_date.strftime("%Y-%m-%d")
        print(
            "Running for {current_running_date_str}".format(
                current_running_date_str=current_running_date_str
            )
        )

        data = {}
        data["deceasedName"] = "%%%"
        data["dateOfDeath"] = current_running_date_str

        response = requests.post(
            "https://www.kmcgov.in/KMCPortal/KMCDeathRegistrationAction.do",
            headers=headers,
            params=params,
            cookies=cookies,
            data=data,
        )

        if response and response.status_code == 200:
            file_name = raw_data_file_name.format(
                current_running_date_file_name_str=current_running_date_file_name_str
            )
            file_obj = open(file_name, "wb")
            file_obj.write(response.content)
            file_obj.close()
        else:
            break

        time.sleep(REQUEST_DELAY)


def main():
    latest_scrape_date = get_latest_scrape_date()
    if latest_scrape_date == None:
        start_date = START_DATE
    else:
        start_date = latest_scrape_date + timedelta(days=1)

    end_date = END_DATE
    print("start_date {} and end_date {}".format(start_date, end_date))
    scrape_now(start_date, end_date)


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("** RESTARTING **")
            time.sleep(60)
        else:
            break
    print("** COMPLETE **")
        
