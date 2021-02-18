"""

This file is intended for running gunicorn in config motion.
$ gunicorn -c config.py app:app
repo: https://github.com/charfole/SCNU-CS-2018-DatabaseProject

"""

import  os
import multiprocessing
debug = False
bind = "0.0.0.0:5000"
accesslog="./log/gunicorn_access.log"
errorlog = "./log/gunicorn_error.log"
workers = multiprocessing.cpu_count()*2 + 1
daemon=True