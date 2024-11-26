import random
import time
import requests
from plugins.FlowerCore.configs import *


def link(problem):
    try:
        return "https://codeforces.com/problemset/problem/" + str(problem['contestId']) + '/' + str(
            problem['index'])
    except KeyError:
        return str(problem)


def get_recent_submission(CF_id):
    try:
        json = requests.get('https://codeforces.com/api/user.status?handle={:s}&from=1&count=1'.format(CF_id)).json()
        print(json)
        if json['status'] == 'FAILED':
            return None
        try:
            return json['result'][0]
        except IndexError:
            return None
    except requests.exceptions.JSONDecodeError:
        return None


def problem_name(problem, rating=False):
    try:
        if rating:
            return str(problem['contestId']) + str(problem['index']) + '(*{:d})'.format(problem['rating'])
        return str(problem['contestId']) + str(problem['index'])
    except KeyError:
        return str(problem)


problems = []
problems_update_time = ""
contests = []
contests_update_time = ""
contests_start_time = {}

def fetch_problems() -> bool:
    global problems, problems_update_time
    nowtime = time.strftime("%Y%m%d", time.localtime(time.time()))
    if problems_update_time == nowtime:
        return True
    problems_update_time = nowtime
    print(problems_update_time)
    for cnt in range(3):
        try:
            problems = (requests.get('https://codeforces.com/api/problemset.problems').json())['result']['problems']
            return True
        except BaseException:
            pass
    return False

def fetch_contests() -> bool:
    global contests, contests_update_time
    nowtime = time.strftime("%Y%m%d", time.localtime(time.time()))
    if contests_update_time == nowtime:
        return True
    contests_update_time = nowtime
    print(contests_update_time)
    for cnt in range(3):
        try:
            contests = (requests.get('https://codeforces.com/api/contest.list').json())['result']
            for item in contests:
                contest = item['id']
                if 'startTimeSeconds' in item:
                    contests_start_time[contest] = item['startTimeSeconds']
                else:
                    contests_start_time[contest] = 0
            return True
        except BaseException:
            pass
    return False

def daily_problem(*args):
    fetch_problems()
    fetch_contests()

    print(args)
    if len(args) == 0:
        t = time.localtime(time.time())
    else:
        t = time.strptime(args[0], "%Y%m%d")
    res_easy = []
    res_hard = []
    for x in problems:
        try:
            if x['contestId'] >= 300 and not ('*special' in x['tags']) and contests_start_time[x['contestId']] < time.mktime(t):
                if x['rating'] <= DAILY_EASY_UPPER_BOUND:
                    res_easy.append(x)
                else:
                    res_hard.append(x)
        except KeyError:
            pass
    seed = (t.tm_year * 19260817 + t.tm_mon * 114514 * t.tm_mday)
    return [res_easy[seed % len(res_easy)], res_hard[seed % len(res_hard)]]


def problem_record(user):
    try:
        try:
            d = requests.get('https://codeforces.com/api/user.status?handle=' + user, timeout=5)
        except TimeoutError:
            return set()
        JSON = d.json()
        if JSON['status'] != 'OK':
            return []
        res = {problem_name(x["problem"]) for x in JSON['result']}
        return res
    except:
        return set()


def request_problem(tags, excluded_problems=None):
    fetch_problems()
    if excluded_problems is None:
        excluded_problems = set()
    assert (type(tags[0]) == int)
    rating = tags[0]
    tags = tags[1:]
    result = []
    for x in problems:
        if (not 'tags' in x) or (not 'rating' in x) or (not 'contestId' in x):
            continue
        if excluded_problems is not None:
            if problem_name(x) in excluded_problems:
                continue
        flag = 1
        for y in tags:
            if y == 'not-seen':
                continue
            if y[0] != '!':
                if y == 'new':
                    if 'contestId' in x and x['contestId'] < NEW_THRESHOLD:
                        flag = 0
                    continue
                if not y in x['tags']:
                    flag = 0
            else:
                if y == '!new':
                    if 'contestId' in x and x['contestId'] >= NEW_THRESHOLD:
                        flag = 0
                    continue
                if y[1:] in x['tags']:
                    flag = 0
        if not flag:
            continue
        if rating == 0 or x['rating'] == rating:
            result.append(x)
    if not result:
        return None
    return random.choice(result)
