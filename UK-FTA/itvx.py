#!/usr/bin/env python3
 
import getopt
import http.client
import os
import re
import sys
import urllib
from enum import Enum
from pathlib import Path

sys.path.append(os.path.abspath('ukfta/itv_dl'))
sys.path.append(os.path.abspath('ukfta/configs'))

from ukfta.configs import config
from ukfta.itv_dl import ITVX, itv_loader


class DownloadKind(Enum):
    HELP = 0
    DOWNLOAD = 1
    LIST = 3

def Notify(message):
    APP_TOKEN = os.getenv("UKFTA_PUSHOVER_TOKEN")
    USER_KEY = os.getenv("UKFTA_PUSHOVER_KEY")
    
    if APP_TOKEN != None and USER_KEY != None:
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({"token": APP_TOKEN,
                                "user": USER_KEY,
                                "message": message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
        
def parse_range(s):
    # Pattern: either a single number or two numbers separated by a comma
    match = re.fullmatch(r"\s*(\d+)\s*(?:,\s*(\d+))?\s*", s)
    if not match:
        raise ValueError(f"Invalid input: '{s}'")
    
    first = int(match.group(1))
    second = int(match.group(2)) if match.group(2) is not None else first
    return [first, second]
    
if __name__ == "__main__":
    
    kind = None
    newest = False
    url = None
    season_number = None
    moveto = None
    whatif = False
    episode_range = [1, 999]
    season_range = [1, 999]
    itv_loader.PAGE_SIZE = 999      # Don't prompt for more pages
    itv_loader.ROW_COUNT = 999
        
    try:
        myITV= ITVX.ITV()
        kind = DownloadKind.DOWNLOAD
        
        opts, args = getopt.getopt(sys.argv[1:], 
                                   'e:S:s:l:h:n:p:w:',
                                   ['episode=','season=','show=','list=','help','newest','path=', "whatif"]
                                   )
        for opt, arg in opts:
            if opt in ('-l', '--list'):
                kind = DownloadKind.LIST
                url = arg

            elif opt in ('-h', '--help'):
                kind = DownloadKind.HELP

            elif opt in ('-e', '--episode'):                
                episode_range = parse_range(arg)
            
            elif opt in ('-s', '--season'):
                season_range = parse_range(arg)                
            
            elif opt in ('-S', '--show'):
                url = arg
            
            elif opt in ('-n', '--newest'):
                newest = True
            
            elif opt in ('-p', '--path'):
                ITVX.SAVE_PATH = Path(arg)
            
            elif opt in ('-w', '--whatif'):
                whatif = True
                

        if kind == DownloadKind.HELP:
            print("USAGE:\n\titvx [-e <url> | -s <url> | -S <url>]\n\titvx --show <url> [--season n[,n]] [--episode n[,n]] [--newest] [--help]")

        elif kind == DownloadKind.LIST:
            episodes = itv_loader.get_next_data(url)
            for i in range(0, len(episodes[0])):
                print(f"{episodes[0][i]}\t{episodes[1][i]}")
        
        elif kind == DownloadKind.DOWNLOAD:
            episodes = itv_loader.get_next_data(url)
            
            for i in range(0, len(episodes[0])): 
                episode_url = episodes[0][i]
                pattern = re.compile(r"^(\d+)\s+(\d+)\s+(.+)")
                match = pattern.match(episodes[1][i])
                if match:
                    season_number = int(match.group(1))
                    episode_number = int(match.group(2))
                    episode_title = match.group(3)

                    do_season_download = False
                    if not newest and season_number >= season_range[0] and season_number <= season_range[1]:
                        do_season_download = True

                    do_episode_download = False
                    if not newest and episode_number >= episode_range[0] and episode_number <= episode_range[1]:
                        do_episode_download = True

                    do_download_newest = newest and (episode_number == len(episodes[0]))
                    
                    if do_season_download or do_episode_download or do_download_newest:
                        print(f"{episode_title} (S{season_number:02d}E{episode_number:02d}) from {episode_url}...", end=' ' )                    
                        if not whatif:
                            filename = myITV.download(episode_url, 'No')
                            Notify(f"Downloaded {episode_title} (S{season_number:02d}E{episode_number:02d})")                             
                        print('Done.')
                        
                else:
                    print(f"Skipping episode with unexpected format: {episodes[1][i]}")
                
    except (getopt.GetoptError, ValueError) as ex:
        print(f"{str(ex)}")
        print("USAGE:\n\titvx [-e <url> | -s <url> | -S <url>]\n\titvx [--episode <url> [--season <url> | --show <url>] [-h | --help]")

    except Exception as ex:
         print(f"Failed: {str(ex)}")
         
    finally:
        pass