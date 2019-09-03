# LED Sunrise Alarm Clock
This is a hobby project that consists of a Django based website that runs on a Raspberry Pi 3 connected to a strip of 300 RGB LEDS. The aim of the project is to create a sunrise alarm clock that will announce the weather, traffic and some news.  

## Features
* Alarm clock
  * Set, update and delete alarms that are connected with crontab entries
  * Emulate sunrise with LED strip
  * Uses Google Text-to-Speech engine to tell a "wake up story" containing:
    * Weather forecast
    * Traffic info
    * Latest news
* RGB LED strip
  * Set color
  * Transition to color
  * Show digital clock


## Libraries used (among others)
* Django, Bootstrap, jQuery, Iconic
* https://github.com/jgarff/rpi_ws281x
* https://github.com/pndurette/gTTS
* https://github.com/weareoutman/clockpicker
* https://github.com/kurtmckee/feedparser
* https://gitlab.com/doctormo/python-crontab/
* https://github.com/Salamek/cron-descriptor