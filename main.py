import requests
from datetime import datetime
import dateutil.parser as dp
import re


def get_maps(is_active: bool = None) -> None | list:
    s = requests.Session()
    s.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }
    r = s.get('https://brawltime.ninja/tier-list/map#active')
    if r.status_code != 200:
        return
    else:
        maps = []
        bsmaps = r.text[r.text.find('<script type="application/ld+json">'):r.text.find('</head>')]
        for bsmap in bsmaps.split('\n'):
            for item in bsmap.split(',')[2:-2]:
                item = item.replace('"', '')
                if "name:" in item:
                    name = item.replace('name:', '')
                if "startDate:" in item:
                    startdate = item.replace('startDate:', '')
                if "endDate:" in item:
                    enddate = item.replace('endDate:', '')
                if 'url:' in item:
                    url = item.replace('url:', 'https://brawltime.ninja/').replace("maps", 'map')
                if 'image:' in item:
                    image = item.replace('image:', '').replace("map", 'maps').replace('[', '').replace(']', '')

            if datetime.utcnow().isoformat(timespec='milliseconds') > startdate:
                enddelta = (dp.parse(enddate).replace(tzinfo=None) - datetime.utcnow())
                ends_in = {'d': enddelta.days,
                           'h': enddelta.seconds // 3600,
                           'm': (enddelta.seconds % 3600) // 60,
                           's': enddelta.seconds % 60
                           }
                duration = 'Ends in: '
                for key, value in ends_in.items():
                    if value != 0:
                        duration += f'{value}{key} '
                active = True
            else:
                startdelta = (dp.parse(startdate).replace(tzinfo=None) - datetime.utcnow())
                starts_in = {'d': startdelta.days,
                             'h': startdelta.seconds // 3600,
                             'm': (startdelta.seconds % 3600) // 60,
                             's': startdelta.seconds % 60
                             }
                duration = 'Starts in: '
                for key, value in starts_in.items():
                    if value != 0:
                        duration += f'{value}{key} '
                active = False

            maps.append([name, url, image, duration, active])

    return check_active(maps, is_active)


def check_active(maps: list, is_active: bool) -> list:
    active_maps = []
    upcoming_maps = []
    if is_active is None:
        return maps
    else:
        for i in range(len(maps)):
            if maps[i][4] is True:
                active_maps.append(maps[i])
            else:
                upcoming_maps.append(maps[i])
        if is_active is True:
            return active_maps
        else:
            return upcoming_maps[:-1]


def get_picks(url: str) -> list:
    picks = []
    s = requests.Session()
    s.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }
    r = s.get(f'{url}?filter[trophyRangeGte]=9')
    indexes_s = [m.start() for m in re.finditer('class="ml-1 leading-tight">', r.text)]
    for i, index in enumerate(indexes_s):
        t = r.text[index:]
        t = t[:t.find('</figcaption>')][27:]
        picks.append(f'{i+1}. {t}')
    return picks


