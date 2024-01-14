import os
import subprocess
import traceback

try:
    # for TYPE in ['butu-nuoma', 'butai']:
    #     # When using shell=True, pass the command as a single string
    #     subprocess.run(f"python BOT_crawler.py -t {TYPE} -c 'vilniuje'", shell=True)

    for TYPE in ['butai']:
        # When shell=False (default), pass command and arguments as a list
        subprocess.run(["python", "BOT_scraper.py", "-t", TYPE, "-co", "n"])
        print("Done. Scraping failed pages once again.")
        subprocess.run(["python", "BOT_scraper.py", "-t", TYPE, "-co", "Y"])
        print(f"Done scraping {TYPE}")
except Exception as e:
    print(traceback.format_exc())
