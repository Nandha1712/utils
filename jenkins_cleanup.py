import logging
import logging.handlers
import os
import shutil
from datetime import datetime

JENKINS_WORKSPACE_PATH = "/var/lib/jenkins/jobs"


"""
Usage:
Need to run with sudo permissions.

sudo nohup python3 <this_filename>.py

sudo tail -f nohup.out

"""

def create_and_get_logging_location():
    # logging_location = "D:" + '/logs/'
    logging_location = os.environ['HOME'] + '/logs/'

    if not os.path.exists(logging_location):
        try:
            os.makedirs(logging_location)
        except Exception as e:
            print(e)

    return logging_location


def create_logger(app_name):
    logging_location = create_and_get_logging_location()
    logging_level = logging.INFO
    log_file_name = str(datetime.now()).replace('-', '').replace(':', '').replace(' ', '').split('.')[0] + '.log'

    logger = logging.getLogger(app_name)
    logger.setLevel(logging_level)
    _logfile = logging_location + '_' + log_file_name

    fh = logging.FileHandler(_logfile)
    fh.setLevel(logging_level)

    ch = logging.StreamHandler()
    ch.setLevel(logging_level)

    formatter = logging.Formatter(
        "%(asctime)s - [%(filename)s - %(funcName)10s():%(lineno)s ] - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


# These number of recent builds will not be deleted
BUILDS_TO_LEAVE = 10


def get_contents_of_build_directory(build_path):
    req_build_ids = []
    builds = os.listdir(build_path)
    for curr_build in builds:
        if not str(curr_build).isdigit():
            continue

        req_path = str(build_path) + "/" + str(curr_build)
        if not os.path.isdir(req_path):
            continue

        req_build_ids.append(int(curr_build))

    return req_build_ids


def delete_builds(parent_path, req_build_ids):
    for curr_build in req_build_ids:
        to_be_deleted = parent_path + "/" + str(curr_build)
        try:
            shutil.rmtree(to_be_deleted)
        except Exception as exp:
            print(f"Exception {exp} while deleting {to_be_deleted}")


def start_cleaning_up():
    contents = os.listdir(JENKINS_WORKSPACE_PATH)
    for curr_job in contents:
        req_job = str(JENKINS_WORKSPACE_PATH) + "/" + str(curr_job)
        if not os.path.isdir(req_job):
            continue

        builds_path = req_job + "/builds"
        if not os.path.exists(builds_path):
            continue

        print(f"builds_path: ${builds_path}")
        build_ids = get_contents_of_build_directory(builds_path)
        build_ids.sort()

        # Leave last 10 builds, delete rest of them

        print(f"All build ids: {build_ids}")
        not_deleted = build_ids[-BUILDS_TO_LEAVE:]
        print(f"Not deleted {not_deleted}")

        builds_to_delete = build_ids[: len(build_ids) - BUILDS_TO_LEAVE]
        print(f"To be deleted {builds_to_delete}")
        if len(builds_to_delete) == 0:
            continue

        delete_builds(builds_path, builds_to_delete)


if __name__ == '__main__':
    start_cleaning_up()
