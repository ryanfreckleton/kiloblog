KiloBlog
========
A simple blog engine written in 1024 bytes of minified, gzipped python code.

- https://github.com/ryanfreckleton/kiloblog

Designed primarily as a starting point for others to expand on and teaching tool.
Non-python code also needs to be 1024 bytes when minified.
Libraries through CDN or installable from PyPI don't count towards the limit.

Tests, configuration, build files, etc. don't count towards this limit.

So this means:

- Python [gzipped/minified] 1 kilobyte
- HTML [gzipped/minified] 1 kilobyte
- CSS [gzipped/minified] 1 kilobyte
- Javascript [gzipped/minified] 1 kilobyte

Total: 4 kilobytes

Quick Start
-----------
To get started, set environment variables `SUPERUSER` and `SUPERUSER_PASSWORD` and run kiloblog.py with

    $ ./kiloblog.py

It should run at `localhost:5000` at which point you should be able to login.

Deployment
----------
- Heroku
- Waitress, etc.

Build Status
------------
TBD

Statistics:
-----------
- Python -- 972/1024 [95%]
- HTML -- 684/1024 [67%]
- CSS -- 0/1024 [0%]
- Javascript -- 0/1024 [0%]

TODO
----
 - I can successfully visit URLs that don't yet exist and it doesn't give a
   proper 404 yet...

Author
------
- Ryan Freckleton

License
-------
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
