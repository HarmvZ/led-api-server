from gtts import gTTS
import feedparser
import re
from datetime import datetime
import locale
from pathlib import Path
from subprocess import Popen, PIPE


SOUND_FILE_PATH = "story.mp3"
SOUND_NAME = "Harm"


class WakeUpStory:
    def __init__(self):
        # Get data
        greeting = self.get_greeting()
        news = self.get_news()
        weather = self.get_weather()
        traffic = self.get_traffic()

        # Create text story
        story = greeting + " " + news + " " + weather + " " + traffic

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

    def get_news(self):
        try:
            # News
            rss_url = "http://feeds.nos.nl/nosnieuwsalgemeen"
            rss = feedparser.parse(rss_url)

            news = "En nu, de 5 laatste artikelen van NOS Algemeen. "

            # Get headlines of top 5 stories
            for story in rss["entries"][:5]:
                news += story["title"] + ". "

        except Exception:
            news = "Nieuws ophalen is niet gelukt. "

        return news

    @staticmethod
    def weather_clean_up(text):
        # Remove any html tag
        text = re.sub(r"</?[^>]*>", " ", text)

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

            summary_dirty = rss["entries"][0]["summary"]
            summary_clean = self.weather_clean_up(summary_dirty)
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

            traffic = "En nu, de actuele verkeersinformatie. "

            jams = rss["entries"]
            if jams:
                for jam in jams:
                    traffic += (
                        self.traffic_clean_up(jam["summary"])
                        + " op "
                        + self.traffic_clean_up(jam["title"])
                        + ". "
                    )
            else:
                traffic += "Er zijn op dit moment geen files."

        except Exception:
            traffic = "Verkeer ophalen is niet gelukt."

        return traffic
