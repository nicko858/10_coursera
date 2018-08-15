import requests
from requests import ReadTimeout
from requests import HTTPError
from requests import ConnectionError
from bs4 import BeautifulSoup


def get_course_name(course):
    return course.find(
        "h1",
        {"class": "title display-3-text"}
    ).text


def get_course_language(course):
    return course.find(
        "div",
        {"class": "rc-Language"}
    ).contents[1]


def get_date_start(course):
    date_start = course.find(
        "div",
        {"id": "start-date-string"}
    ).text
    for character in ["Starts", "Started"]:
        if character in date_start:
            return date_start.replace(character, "")


def get_weeks_count(course):
    return len(course.find_all("div", {"class": "week"}))


def get_user_score(course):
    user_score = course.find(
        "div",
        {"class": "ratings-text bt3-visible-xs"})
    if hasattr(user_score, "text"):
        user_score = user_score.text.replace("stars", "")
    else:
        user_score = course.find(
            "div",
            {"class": "ratings-text headline-2-text"}
        )
        if hasattr(user_score, "text"):
            user_score = list(user_score.text.split(" "))[1]
        else:
            user_score = None
    return user_score


def get_course_info(course_slug):
    try:
        response = requests.get(course_slug)
    except (ConnectionError, HTTPError, ReadTimeout):
        return None
    course = BeautifulSoup(response.content, "lxml")
    course_name = get_course_name(course)
    language = get_course_language(course)
    date_start = get_date_start(course)
    weeks_count = get_weeks_count(course)
    user_score = get_user_score(course)
    course_info = (
        course_name,
        language,
        date_start,
        weeks_count,
        user_score
    )
    return course_info


if __name__ == "__main__":
    pass