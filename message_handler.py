import os
import datetime

import conf
import parse

logger = conf.logger


def result_response(elem, full_name_filter=None, date_filter=None):
    """
    Function describes what to do with the found element in xml
    :param elem: person tag found
    :param full_name_filter: full name of person for filtering
    :param date_filter: work date for filtering
    """
    # parsed_info
    full_name, start_date, start_time, end_date, end_time = parse.parse_person_tag(elem)

    if full_name_filter and full_name != full_name_filter:
        # if filter by full name is not equal to parsed info
        return
    if date_filter:
        start_date_filter, end_date_filter = date_filter
        if start_date < start_date_filter or end_date > end_date_filter:
            # if filter by date name is not equal to parsed info
            return
    timedelta = end_time - start_time
    # give info to user
    logger.info(f'full_name: {full_name}')
    logger.info(f'date: {str(start_date)}')
    logger.info(f'time at work: {str(timedelta)}')


def error_message(err: str):
    logger.error('Something went wrong! {}'.format(err))


def date_is_valid(date_text) -> bool:
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y')
        return True
    except ValueError:
        return False


def ask_to_filter_by(val: str):
    """
    Function asks user if he wants to filter data by exact value
    :param val:
    :return:
    """
    logger.info(f"Do you want to filter data by {val}")

    logger.info("1: Yes")
    logger.info("*ANY KEY*: No")

    return input().strip()


class MessageHandler:
    """
    Class for handling messages came from user.
    """
    def __init__(self):
        """
        Class is using state of dialogue with user to send correct messages to him
        """
        # parser object
        self.parser = None
        # state of dialogue with user
        self.state = conf.START
        # full name of person to filter
        self.full_name_filter = None
        # start date and end date to filter work date of person
        self.date_filter = None
        # start dialogue with user
        self.generate_message()

    def generate_message(self):
        """
        Function to manage Message Handler depending on dialogue state with user
        :return:
        """
        if self.state == conf.START:
            self.hello_message()

        elif self.state == conf.SEND_FILE:
            self.filter_name_message()

        elif self.state == conf.FILTERED_BY_NAME:
            self.filter_date_message()

        elif self.state == conf.FILTERED_BY_DATE:
            self.show_info_message()

        elif self.state == conf.EXIT:
            self.exit_message()

    def hello_message(self):
        """
        Function says hello and returns input of user
        :return: input file path of user
        """
        logger.info("Hello, it's a simple script to parse and analyze XML files.")
        logger.info("Please write path to an XML file")

        # take path to xml file
        path_to_file = input().strip()
        if os.path.exists(path_to_file):
            # if file exists, create parser with path
            self.parser = parse.XMLPeopleScheduleParser(path_to_file, 'person')
            self.state = conf.SEND_FILE
        else:
            # file does not exist, report it to user
            error_message('File does not exist. Try again?')
            logger.info("1: Try again")
            logger.info("*ANY KEY*: Exit")

            answer = input().strip()
            if answer == '1':
                self.state = conf.START
            else:
                # user wants to exit
                self.state = conf.EXIT
        self.generate_message()

    def filter_name_message(self):
        """
        Function asks user if he wants to filter xml information by name
        """
        answer = ask_to_filter_by('name')
        if answer == '1':
            # user wants to filter by full name
            logger.info('Write the full name of person to filter')
            self.full_name_filter = input().strip()
        # at this moment we accept the state as FILTERED_BY_NAME, no matter what the user chose
        self.state = conf.FILTERED_BY_NAME
        self.generate_message()

    def filter_date_message(self):
        """
        Function asks user if he wants to filter xml information by date
        """
        answer = ask_to_filter_by('date')
        if answer == '1':
            # user wants to filter by date
            logger.info('Write the start work date of person to filter in format DD-MM-YYYY')
            start_date_filter = input().strip()

            logger.info('Write the end work date of person to filter in format DD-MM-YYYY')
            end_date_filter = input().strip()
            if not date_is_valid(start_date_filter) or not not date_is_valid(end_date_filter):
                # not valid date, try to ask about filtering date again
                error_message("Incorrect format of date")
                self.state = conf.FILTERED_BY_NAME
            else:
                # date is valid
                self.date_filter = (datetime.datetime.strptime(start_date_filter, "%d-%m-%y"),
                                    datetime.datetime.strptime(end_date_filter, "%d-%m-%y"))
                self.state = conf.FILTERED_BY_DATE
        else:
            # at this moment we accept the state as FILTERED_BY_DATE,
            # user will get info with all dates without filtering
            self.state = conf.FILTERED_BY_DATE
        self.generate_message()

    def show_info_message(self):
        """
        Function shows result of user response xml
        """
        self.parser.parse_file(result_response, full_name_filter=self.full_name_filter,
                               date_filter=self.date_filter)

        logger.info('Do you want to exit or load another file?')
        logger.info('1: Load another file')
        logger.info("*ANY KEY*: Exit")

        answer = input().strip()
        if answer == '1':
            self.state = conf.START
        else:
            self.state = conf.EXIT
        self.generate_message()

    def exit_message(self):
        """
        Function says goodbye to the user
        """
        logger.info('Good bye')
        return
