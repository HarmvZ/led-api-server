from gtts import gTTS
import feedparser
import re
from pathlib import Path
from subprocess import Popen, PIPE

SOUND_FILE_PATH = "story.mp3"


class WakeUpStory:
    def __init__(self):
        # Get data
        self.news = self.get_news()
        self.weather = self.get_weather()
        self.traffic = self.get_traffic()

        # Create text story
        story = self.news + " " + self.weather + " " + self.traffic

        print(story)
        tts = gTTS(story, lang="nl")
        tts.save(SOUND_FILE_PATH)

    def play(self):
        player = Popen(
            ["omxplayer", str(Path(SOUND_FILE_PATH).absolute())],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )

    @staticmethod
    def clean_up(text):
        # Remove any html tag
        text = re.sub(r"</?[^>]*>", " ", text)

        # Remove special cases
        remove = ["&nbsp;", "(Bron: KNMI)", " LT"]
        for rm in remove:
            text = text.replace(rm, "")
        return text

    def get_news(self):
        try:
            # News
            rss_url = "http://feeds.nos.nl/nosnieuwsalgemeen"
            rss = feedparser.parse(rss_url)

            news = "En nu, de 5 belangrijkste nieuwsartikelen van NOS Algemeen. "

            # Get headlines of top 5 stories
            for story in rss["entries"][:5]:
                news += self.clean_up(story["title"]) + ". "

        except Exception:
            news = "Nieuws ophalen is niet gelukt. "

        return news

    def get_weather(self):
        try:
            # Weather
            rss_url = "http://projects.knmi.nl/RSSread/rss_KNMIverwachtingen.php"
            rss = feedparser.parse(rss_url)

            summary_dirty = rss["entries"][0]["summary"]
            summary_clean = self.clean_up(summary_dirty)
            weather = "En nu, de weersverwachtingen van het KNMI. " + summary_clean

        except Exception:
            weather = "Weer ophalen is niet gelukt. "

        return weather

    def get_traffic(self):
        try:
            # Traffic
            rss_url = "https://www.verkeerplaza.nl/rssfeed"
            rss = feedparser.parse(rss_url)

            traffic = "En nu, de actuele verkeersinformatie. "

            jams = rss["entries"]
            if jams:
                for jam in jams:
                    traffic += self.clean_up(jam) + ". "
            else:
                traffic += "Er zijn op dit moment geen files."

        except Exception:
            traffic = "Verkeer ophalen is niet gelukt."

        return traffic
