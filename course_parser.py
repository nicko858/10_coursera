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
    for word in ["Starts", "Started"]:
        if word in date_start:
            return date_start.replace(word, "")


def get_weeks_count(course):
    return len(course.find_all("div", {"class": "week"}))


def get_user_score(course):
    user_score = course.find(
        "div",
        {"class": "ratings-text bt3-visible-xs"})
    if user_score:
        user_score = user_score.text.replace("stars", "")
    else:
        user_score = course.find(
            "div",
            {"class": "ratings-text headline-2-text"}
        )
        if user_score:
            user_score = list(user_score.text.split(" "))[1]
    return user_score


if __name__ == "__main__":
    pass