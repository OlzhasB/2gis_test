import datetime

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
    return datetime.datetime.strptime(date_str, "%d-%m-%y"), datetime.datetime.strptime(time_str, '%H:%M:%S')


def parse_person_tag(elem) -> tuple:
    """
    Function parses person tag
    :param elem: person tag found
    :return: tuple with parsed full_name, start_date, start_time, end_date and end_time
    """
    full_name = elem.attrib['full_name']
    start_date_time = elem[0].text.decode('utf-8')
    end_date_time = elem[1].text.decode('utf-8')
    return full_name, parse_date_time(start_date_time), parse_date_time(end_date_time)


class XMLPeopleScheduleParser:
    """
    Class for parsing xml file with
    """
    def __init__(self, path_to_file, tag):
        """
        :param path_to_file: path to xml file
        :param tag: name of tage user is searching for
        """
        self.path_to_file = path_to_file
        self.tag = tag

    def fast_iter(self, context, func, **kwargs):
        """
        Function iterator goes through xml file and finds tags that user needs
        :param context: variable from lxml library, contains filename and tag
        :param func: function to do something with tag element found in xml
        """
        for event, elem in context:
            func(elem, kwargs)
            # cleaning up unnecessary links to nodes
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context

    def parse_file(self, func, **kwargs):
        """
        Function takes function to to pass this information to the iterator
        :param func: function to do something with tag element found in xml
        """
        context = etree.iterparse(self.path_to_file, events=('end',), tag=self.tag)
        self.fast_iter(context, func, **kwargs)
