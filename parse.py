import datetime
import os

from lxml import etree

import conf

logger = conf.logger


def parse_date_time(date_time_str: str):
    """
    Function parses date and time from string
    :param date_time_str: string with date and time
    :return: parsed date and time
    """
    date_str = date_time_str.split(' ')[0]
    time_str = date_time_str.split(' ')[1]
    return datetime.datetime.strptime(date_str, "%d-%m-%Y").date(), \
           datetime.datetime.strptime(time_str, '%H:%M:%S').time()


def parse_person_tag(elem) -> tuple:
    """
    Function parses person tag
    :param elem: person tag found
    :return: tuple with parsed full_name, start_date, start_time, end_date and end_time
    """
    full_name = elem.attrib['full_name']
    for date_tag in elem:
        if date_tag.tag == 'start':
            start_date_time = date_tag.text
        elif date_tag.tag == 'end':
            end_date_time = date_tag.text
    start_date, start_time = parse_date_time(start_date_time)
    end_date, end_time = parse_date_time(end_date_time)
    return full_name, start_date, start_time, end_date, end_time


class XMLPeopleScheduleParser:
    """
    Class for parsing xml file with
    """

    def __init__(self, path_to_file, tag):
        """
        :param path_to_file: path to xml file
        :param tag: name of tag user is searching for
        """
        if os.path.exists(path_to_file):
            self.path_to_file = path_to_file
        else:
            raise FileNotFoundError('File does not exists')

        self.tag = tag

    def fast_iter(self, context, func, full_name_filter, dates_filter):
        """
        Function iterator goes through xml file and finds tags that user needs
        :param dates_filter: filter people by work dates
        :param full_name_filter: filter people by full_name
        :param context: variable from lxml library, contains filename and tag
        :param func: function to do something with tag element found in xml
        """
        for event, elem in context:
            func(elem, full_name_filter, dates_filter)
            # cleaning up unnecessary links to nodes
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context

    def parse_file(self, func, full_name_filter, dates_filter):
        """
        Function takes function to to pass this information to the iterator
        :param dates_filter: filter people by work dates
        :param full_name_filter: filter people by full_name
        :param func: function to do something with tag element found in xml
        """
        try:
            context = etree.iterparse(self.path_to_file, events=('end',), tag=self.tag)
            self.fast_iter(context, func, full_name_filter, dates_filter)
        except ValueError:
            logger.error("Invalid file formatting")
            return None
