import datetime
import math
import re

from django.utils.html import strip_tags


def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)
    # read_time_sec = read_time_min * 60
    read_time = str(datetime.timedelta(minutes=read_time_min))
    return read_time


def get_header_text():
    header_text = ['Believe in Billy', 'Trust my sources. I researched this shit.',
                   'I AM THE BEST. Daily affirmation...',
                   'Sometimes I\'ll start a sentence and I don\'t even know where it\'s going. I just hope I find it along the way.',
                   'Numbers don\'t lie, but then there are imaginary numbers.']
    return header_text
