import requests
import random
import argparse
from bs4 import BeautifulSoup
from requests import ReadTimeout
from requests import HTTPError
from requests import ConnectionError
from openpyxl import Workbook
from openpyxl.styles import PatternFill


def get_args():
    script_usage = 'python coursera.py  <path to output file>'
    parser = argparse.ArgumentParser(
        description='How to run coursera.py:',
        usage=script_usage
    )
    parser.add_argument(
        'output_file_path',
        help='Specify the path to output file'
    )
    args = parser.parse_args()
    return args


def get_courses_list(xml_feed_url, courses_count):
    try:
        response = requests.get(xml_feed_url)
    except (ConnectionError, HTTPError, ReadTimeout):
        return None
    sitemap_index = BeautifulSoup(response.content, 'html.parser')
    urls = [element.text for element in sitemap_index.findAll('loc')]
    courses_list = random.sample(urls, courses_count)
    return courses_list


def get_course_info(course_slug):
    try:
        response = requests.get(course_slug)
    except (ConnectionError, HTTPError, ReadTimeout):
        return None
    course = BeautifulSoup(response.content, 'lxml')
    course_name = course.find(
        "h1",
        {"class": "title display-3-text"}
    ).text
    language = course.find(
        "div",
        {"class": "rc-Language"}
    ).contents[1]
    date_start = course.find(
        "div",
        {"id": "start-date-string"}
    ).text
    for character in ["Starts", "Started"]:
        if character in date_start:
            date_start = date_start.replace(character, "")
    weeks_count = len(course.find_all("div", {"class": "week"}))
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
    course_info = (
        course_name,
        language,
        date_start,
        weeks_count,
        user_score
    )
    return course_info


def make_xlsx_template():
    wb = Workbook()
    ws = wb.active
    ws.title = "Courses List"
    fill = PatternFill(fill_type='solid',
                       start_color='c1c1c1',
                       end_color='c2c2c2')
    head_row = [
        'URL',
        'COURSE_NAME',
        'LANGUAGE',
        "NEAREST_DATE",
        "WEEKS_COUNT",
        "USER_SCORE"
    ]
    ws.append(head_row)
    for cell in ['A1', 'B1', 'C1', 'D1', 'E1', 'F1']:
        ws[cell].fill = fill
    return wb, ws


def output_courses_info_to_xlsx(courses_data, wb, ws):
    for url, course_info in courses_data.items():
        try:
            (name, language, nearest_date,
             weeks_count, user_score) = course_info
            next_row = [
                url,
                name,
                language,
                nearest_date,
                weeks_count,
                user_score
            ]
        except TypeError:
            next_row = [url]
        ws.append(next_row)
    return wb


def save_output_courses_to_xlsx(wb, filepath):
    wb.save(filepath)


if __name__ == '__main__':
    args = get_args()
    output_file_path = args.output_file_path
    courses_list = get_courses_list(
        "https://www.coursera.org/sitemap~www~courses.xml", 20)
    if not courses_list:
        exit("The www.coursera.org is unavailable!")
    courses_data = {}
    for course in courses_list:
        courses_data[course] = get_course_info(course)
    workbook, worksheet = make_xlsx_template()
    xlsx_courses_info = output_courses_info_to_xlsx(
        courses_data,
        workbook,
        worksheet
    )
    try:
        save_output_courses_to_xlsx(
            xlsx_courses_info,
            filepath=output_file_path
        )
    except PermissionError:
        exit("You don't have permission to save into the"
             " '{}' directory!".format(output_file_path))
    except FileNotFoundError:
        exit(" No such file or directory {}".format(output_file_path))
