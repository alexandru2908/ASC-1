from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import os
from logging.handlers import RotatingFileHandler
# from app.routes import logger1



if os.path.exists("webserver.log"):
    with open("webserver.log", "w") as f:
        f.write("")


webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.tasks_runner.start()


if not os.path.exists("results"):
    os.mkdir("results")


webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

from app import routes
