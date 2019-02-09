from gtts import gTTS
import feedparser
import re
from datetime import datetime
import locale
from pathlib import Path
from subprocess import Popen, PIPE


SOUND_FILE_PATH = "story.mp3"
SOUND_NAME = "Harrum"


class WakeUpStory:
    def __init__(self):
        # Get data
        greeting = self.get_greeting()
        nos_news = self.get_nos_news()
        nunl_news = self.get_nunl_news()
        weather = self.get_weather()
        traffic = self.get_traffic()

        # Create text story
        story = (
            greeting + " " + weather + " " + traffic + " " + nunl_news + " " + nos_news
        )

        tts = gTTS(story, lang="nl")
        tts.save(SOUND_FILE_PATH)

    def play(self):
        player = Popen(
            ["omxplayer", str(Path(SOUND_FILE_PATH).absolute())],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )

    def get_greeting(self):
        # Explicitly set locale to NL
        locale.setlocale(locale.LC_ALL, "nl_NL.utf-8")
        now = datetime.now()
        day_and_time = now.strftime("%A %d %B, %H:%M")

        if int(now.strftime("%H")) < 12:
            period = "morgen"
        else:
            period = "middag"
        if int(now.strftime("%H")) >= 17:
            period = "navond"

        # reads out good morning + my name
        gmt = "Goede" + period + " " + SOUND_NAME

        # reads date and time
        day = ", het is vandaag " + day_and_time + ".  "

        return gmt + day

    def get_nos_news(self):
        try:
            # News
            rss_url = "http://feeds.nos.nl/nosnieuwsalgemeen"
            rss = feedparser.parse(rss_url)

            news = "En nu, de 5 laatste artikelen van NOS Algemeen. "

            # Get headlines of top 5 stories
            for story in rss["entries"][:5]:
                news += story["title"] + ". "

        except Exception:
            news = "NOS Nieuws ophalen is niet gelukt. "

        return news

    def get_nunl_news(self):
        try:
            # News
            rss_url = "https://www.nu.nl/rss/Algemeen"
            rss = feedparser.parse(rss_url)

            news = "En nu, de 5 laatste artikelen van Nu.nl Algemeen. "

            # Get headlines of top 5 stories
            for story in rss["entries"][:5]:
                news += story["title"] + ". " + story["summary"] + ". "

        except Exception:
            news = "Nu.nl Nieuws ophalen is niet gelukt. "

        return news

    @staticmethod
    def weather_clean_up(text):
        # Remove any html tag
        text = re.sub(r"</?[^>]*>", " ", text)
        # Remove uitgifte text
        text = re.sub(r"Uitgifte: [0-9/. ]* uur LT", " ", text)

        # Remove special cases
        remove = ["&nbsp;", "(Bron: KNMI)", " LT"]
        for rm in remove:
            text = text.replace(rm, "")
        return text

    def get_weather(self):
        try:
            # Weather
            rss_url = "http://projects.knmi.nl/RSSread/rss_KNMIverwachtingen.php"
            rss = feedparser.parse(rss_url)

            summary_dirty = rss["entries"][1]["summary"]
            summary_clean = self.weather_clean_up(summary_dirty) + ". "
            weather = "En nu, de weersverwachtingen van het KNMI. " + summary_clean

        except Exception:
            weather = "Weer ophalen is niet gelukt. "

        return weather

    @staticmethod
    def traffic_clean_up(text):
        return (
            text.replace("Situatie:", "")
            .replace("Bron: Verkeerplaza.nl:", "")
            .replace(">", "naar")
        )

    def get_traffic(self):
        try:
            # Traffic
            rss_url = "https://www.verkeerplaza.nl/rssfeed"
            rss = feedparser.parse(rss_url)

            jams = rss["entries"]

            traffic = "En nu, de actuele verkeersinformatie. Er staan op dit moment {} files. ".format(
                len(jams)
            )

            if len(jams) > 5:
                traffic += "Het is druk op de weg, "
                # Filter if more than 5 traffic jams
                useful_jams = []
                for jam in jams:
                    if "A50" in jam["title"]:
                        useful_jams.append(jam)
                if len(useful_jams) > 0:
                    jams = useful_jams
                    traffic += "dit zijn de files op de A50. "
                else:
                    jams = []
                    traffic += "er staan geen files op de A50. "

            for jam in jams:
                traffic += (
                    self.traffic_clean_up(jam["summary"])
                    + " op "
                    + self.traffic_clean_up(jam["title"])
                    + ". "
                )

        except Exception:
            traffic = "Verkeer ophalen is niet gelukt."

        return traffic
