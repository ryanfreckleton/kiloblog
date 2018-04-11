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
- Templates [gzipped/minified] 1 kilobyte

Total: 2 kilobytes

Quick Start
-----------
~~~
$ pip install -r requirements.txt
$ . scripts/activate
$ metrics
Python 1018
HTML 1020
$ flask run
* Serving Flask app "kiloblog"
* Forcing debug mode on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 000-000-000
~~~

Modify setup.cfg as appropriate before deploying, **take special mind to change the password and secret key.**

Developing
----------
Development requirements are in `requirements-dev.txt` and tests are run with `py.test`

Statistics:
-----------
- Python — 1018/1024 [99%]
- HTML — 1020/1024 [**100%**]

Author
------
- Ryan E. Freckleton

License
-------
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details
