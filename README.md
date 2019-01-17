# ping_script
Pings a variety of servers to determine if your internet is down.

Uses the builtin ping command of your computer to check if a variety of
servers are available and records this in a .csv file.
Will ping once a minute, andonly pings until a server is reachable.

*Only been tested on Windows. For Linux, replace "-n" with "-c" on Line 44.*