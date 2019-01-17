#!/usr/bin/env python3
"""Pings a variety of servers to determine if your internet is down.

Uses the builtin ping command of your computer to check if a variety of
servers are available and records this in a .csv file.
Will ping once a minute, andonly pings until a server is reachable.
"""

import datetime
from subprocess import Popen, PIPE
from time import sleep

__author__ = "Daniel Gillo"
__copyright__ = "Copyright 2019"
__credits__ = ["Daniel Gillo"]
__license__ = "GNU GPLv3"
__version__ = "1.2"
__maintainer__ = "Daniel Gillo"
__email__ = "danigillo@gmail.com"
__status__ = "Production"


addr = ["8.8.4.4",  # Google DNS service
        "1.1.1.1",  # Cloudflare DNS service
        "4.2.2.2",  # Level3 DNS service
        "199.7.83.42",  # ICANN Toronto Root server
        "google.ca",
        "utoronto.ca",
        "192.0.43.10",  # example.com
        "lcbo.com"]  # Last resort; I need a drink

# location = "C:\\Users\\On\\Your\\Computer\\Where\\It'll\\Write\\log.csv"
location = ""

# Initialize the output line & sleep until minute begins
hour_responses = "," * ((int(datetime.datetime.now().strftime("%M")) + 1) % 60)
sleep(60.0 - float(datetime.datetime.now().strftime("%S.%f")))

# Don't forget: You're here forever
while True:
    try:
        connection_failure = True
        past = datetime.datetime.now()
        for address in addr:
            # Run OS ping command (replace "-n" with "-c" in Linux!)
            res = Popen(["ping", "-n", "1", address], stdout=PIPE, stderr=PIPE)
            stdout, stderr = res.communicate()
            # Also check if the host was unreachable
            # Note: MS ping will comtimes wrongly return a success code.
            if res.returncode == 0 and b"unreachable" not in stdout:
                # Success!
                connection_failure = False
            present = datetime.datetime.now()
            # This line takes the diff of present & past, casts to Str,
            # splits by ":", casts to Float, now we have a list of times
            # [Hr, Min, Sec]
            diff = [float(s) for s in str(present - past).split(":")]

            if diff[2] > 46.0:
                # If we've been pining for over 45 sec, abandon
                # And, yes, this will override the success above
                connection_failure = True
                break

            if diff[1] > 0.0:
                hour_responses += (",1" * int(diff[1]))
                connection_failure = True
                break

            if not connection_failure:
                break

        if connection_failure:
            # Ping couldn't connect or Ping Fucked Up, or both
            hour_responses += ",1"
            print("Fail!")
        else:
            # Success!
            hour_responses += ",0"
            print("Success!")

        if int(past.strftime("%M")) >= 59:
            # The end of the hour is nigh! Must write!
            with open((location + "log.csv"), "a") as file:
                file.write(datetime.datetime.today().strftime("%Y-%m-%d,%H") + hour_responses + "\n")
            hour_responses = ""

        # Wait for next minute
        sleep(60.0 - float(datetime.datetime.now().strftime("%S.%f")))

    except Exception as e:
        with open("e.txt", "a") as file:
            print(e)
            file.write(str(e) + "\n")
            file.write(datetime.datetime.today().strftime("%Y-%m-%d,%H") + hour_responses + "\n")
        sleep(60.0 - float(datetime.datetime.now().strftime("%S.%f")))
