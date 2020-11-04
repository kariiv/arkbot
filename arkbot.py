import re
import urllib.request
import html
import time
from datetime import datetime
from gmail import send_email


class ARKBOT:

    date_format = "%d.%m.%Y %H:%M"
    valid_cities = [
        "Haapsalu",
        "Jõhvi",
        "Kuressaare",
        "Narva",
        "Paide",
        "Pärnu",
        "Rakvere",
        "Tallinn",
        "Tartu",
        "Viljandi",
        "Võru"
    ]

    def __init__(self, kp, cities):
        if not cities:
            raise ValueError("No cities listed")
        if len([True for city in cities if city in ARKBOT.valid_cities]) != len(cities):
            raise ValueError("Unknown city listed")
        self.target_date = ARKBOT.arkdate_to_date(kp)
        self.target_cities = cities

    @staticmethod
    def get_ark_website():
        url = "https://eteenindus.mnt.ee/public/vabadSoidueksamiajad.xhtml"
        f = urllib.request.urlopen(url)
        return html.unescape(f.read().decode('utf-8'))

    @staticmethod
    def get_arkdate(city, page):
        rex = '(?<=' + city + '<\/span><\/td><td role="gridcell" class="eksam-ajad-uuendatud"><\/td><td role="gridcell" class="eksam-ajad-aeg">)[0-9. :]*'
        return re.search(rex, page).group().strip()

    @staticmethod
    def arkdate_to_date(arkdate):
        return datetime.strptime(arkdate, ARKBOT.date_format)

    @staticmethod
    def get_last_times(cities):
        page = ARKBOT.get_ark_website()
        return {city: ARKBOT.arkdate_to_date(ARKBOT.get_arkdate(city, page)) for city in cities}

    def match(self, city, date):
        self.target_date = date
        send_email(city, date)

    def run(self):
        while True:
            dates = ARKBOT.get_last_times(self.target_cities)
            [self.match(city, dates[city]) for city in dates if dates[city] < self.target_date]
            time.sleep(30)


if __name__ == "__main__":
    ARKBOT("11.01.2021 10:00", ["Rakvere"]).run()
