import requests
import random
import argparse
from argparse import ArgumentTypeError
from bs4 import BeautifulSoup
from requests import ReadTimeout
from requests import HTTPError
from requests import ConnectionError
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from os import access
from os import W_OK
from os import path
from course_parser import get_course_info


def check_file_extension(extensions, file_path):
    file_name, file_extension = path.splitext(file_path)
    return file_extension in extensions


def check_file_path(file_path):
    if not access(path.dirname(file_path), W_OK):
        raise ArgumentTypeError(
            "You don't have permissions to '{}' , "
            "or directory doesn't exist!".format(file_path)
        )
    elif path.isdir(file_path):
        raise ArgumentTypeError(
            "The '{}' is not a file!".format(file_path)
        )
    elif not check_file_extension(".xlsx", file_path):
        raise ArgumentTypeError("Invalid file extension!\n"
                                "The valid extension is {}".format(
                                 ".xlsx"
                                 ))
    else:
        return file_path


def get_args():
    script_usage = "python coursera.py  <path to output file>"
    parser = argparse.ArgumentParser(
        description="How to run coursera.py:",
        usage=script_usage
    )
    parser.add_argument(
        "output_file_path",
        type=check_file_path,
        help="Specify the path to output file"
    )
    args = parser.parse_args()
    return args


def get_courses_list(xml_feed_url, courses_count):
    try:
        response = requests.get(xml_feed_url)
    except (ConnectionError, HTTPError, ReadTimeout):
        return None
    sitemap_index = BeautifulSoup(response.content, "html.parser")
    urls = [element.text for element in sitemap_index.findAll("loc")]
    courses_list = random.sample(urls, courses_count)
    return courses_list


def make_xlsx_template():
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Courses List"
    fill = PatternFill(
        fill_type="solid",
        start_color="c1c1c1",
        end_color="c2c2c2"
    )
    head_row = [
        "URL",
        "COURSE_NAME",
        "LANGUAGE",
        "NEAREST_DATE",
        "WEEKS_COUNT",
        "USER_SCORE"
    ]
    worksheet.append(head_row)
    for cell in ["A1", "B1", "C1", "D1", "E1", "F1"]:
        worksheet[cell].fill = fill
    return workbook, worksheet


def output_courses_info_to_xlsx(courses_data, workbook, worksheet):
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
        worksheet.append(next_row)
    return workbook


def save_output_courses_to_xlsx(wb, filepath):
    wb.save(filepath)


if __name__ == "__main__":
    args = get_args()
    output_file_path = args.output_file_path
    courses_list = get_courses_list(
        "https://www.coursera.org/sitemap~www~courses.xml",
        courses_count=20
    )
    if not courses_list:
        exit("The www.coursera.org is unavailable!")
    courses_info = {}
    for course in courses_list:
        courses_info[course] = get_course_info(course)
    workbook, worksheet = make_xlsx_template()
    xlsx_courses_info = output_courses_info_to_xlsx(
        courses_info,
        workbook,
        worksheet
    )
    save_output_courses_to_xlsx(
        xlsx_courses_info,
        filepath=output_file_path
    )
    print("Saved successfully to the {}.".format(output_file_path))
