# Coursera Dump

- The script extracts the list of random 20 courses from the [Coursera xml-feed](https://www.coursera.org/sitemap~www~courses.xml)
- For every course extracts, language, the nearest start date, the number of weeks and the average rating
- Save this information to the output xlsx-file


# How to Install
Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.


# How to run
- Activate virtualenv
``` bash
source <path_to_virtualenv>/bin/activate
```
- Run script with virtualenv-interpreter
```bash
<path_to_virtualenv>/bin/python3.5 coursera.py course_list.xlsx
```
If everything is fine, you'll see content in your xlsx-file:

![alt-текст](https://github.com/nicko858/10_coursera/blob/master/xlsx.jpg)




# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
