import datetime
import unittest

from parse import XMLPeopleScheduleParser, parse_person_tag


def do_anything_with_elem(elem, full_name_filter, dates_filter):
    return elem


class TestXMLPeopleScheduleParser(unittest.TestCase):
    def save_elements(self, elem, full_name_filter, dates_filter):
        """
        Function to save add found tag in self.elements. It uses custom filters to choose necessary tags
        """
        full_name, start_date, start_time, end_date, end_time = parse_person_tag(elem)

        if full_name_filter and full_name != full_name_filter:
            # if filter by full name is not equal to parsed info
            return
        if dates_filter:
            start_date_filter, end_date_filter = dates_filter
            if start_date < start_date_filter or end_date > end_date_filter:
                # if filter by date is not equal to parsed info
                return

        self.elements_list.append({
            'full_name': full_name,
            'start_date': start_date,
            'start_time': start_time,
            'end_date': end_date,
            'end_time': end_time,
        })

    def setUp(self) -> None:
        """
        Test constructor
        """
        self.parser = XMLPeopleScheduleParser('xml_files/people.xml', 'person')
        self.elements_list = []

    def testPathToFile(self):
        """
        Assert that path to file is set correctly
        """
        self.assertEqual(self.parser.path_to_file, 'xml_files/people.xml')

    def testTag(self):
        """
        Assert that tag is set correctly
        """
        self.assertEqual(self.parser.tag, 'person')

    def testNotExistingFile(self):
        """
        Assert that setting not existing file raises error
        """
        with self.assertRaises(FileNotFoundError):
            XMLPeopleScheduleParser('file_not_exists.xml', 'person')

    def testWrongFileFormatting(self):
        """
        Assert that file with wrong format returns None
        """
        self.parser.path_to_file = 'xml_files/wrong.xml'

        result = self.parser.parse_file(do_anything_with_elem, None, None)
        self.assertEqual(result, None)

    def testParseFull(self):
        """
        Assert that parsing without filter is correct
        """
        self.parser.path_to_file = 'xml_files/people.xml'
        self.parser.tag = 'person'
        self.parser.parse_file(self.save_elements, None, None)
        expect_list = [
            {
                'full_name': 'i.ivanov',
                'start_date': datetime.date(2011, 12, 21),
                'start_time': datetime.time(10, 54, 47),
                'end_date': datetime.date(2011, 12, 21),
                'end_time': datetime.time(19, 43, 2)
            },
            {
                'full_name': 'a.stepanova',
                'start_date': datetime.date(2011, 12, 21),
                'start_time': datetime.time(9, 40, 10),
                'end_date': datetime.date(2011, 12, 21),
                'end_time': datetime.time(17, 59, 15)
            },
            {
                'full_name': 'i.ivanov',
                'start_date': datetime.date(2011, 12, 25),
                'start_time': datetime.time(10, 25, 47),
                'end_date': datetime.date(2011, 12, 25),
                'end_time': datetime.time(19, 43, 2)
            }
        ]
        self.assertEqual(self.elements_list, expect_list)

    def testParseWithFullNameFilter(self):
        """
        Assert that parsing with full name filter is correct
        """
        self.parser.path_to_file = 'xml_files/people.xml'
        self.parser.tag = 'person'
        self.parser.parse_file(self.save_elements, 'i.ivanov', None)
        expect_list = [
            {
                'full_name': 'i.ivanov',
                'start_date': datetime.date(2011, 12, 21),
                'start_time': datetime.time(10, 54, 47),
                'end_date': datetime.date(2011, 12, 21),
                'end_time': datetime.time(19, 43, 2)
            },
            {
                'full_name': 'i.ivanov',
                'start_date': datetime.date(2011, 12, 25),
                'start_time': datetime.time(10, 25, 47),
                'end_date': datetime.date(2011, 12, 25),
                'end_time': datetime.time(19, 43, 2)
            }
        ]
        self.assertEqual(self.elements_list, expect_list)

    def testParseWithDateFilter(self):
        """
        Assert that parsing with date filter is correct
        """
        self.parser.path_to_file = 'xml_files/people.xml'
        self.parser.tag = 'person'
        dates_filter = (datetime.date(2011, 12, 24), datetime.date(2011, 12, 26))
        self.parser.parse_file(self.save_elements, None, dates_filter)
        expect_list = [
            {
                'full_name': 'i.ivanov',
                'start_date': datetime.date(2011, 12, 25),
                'start_time': datetime.time(10, 25, 47),
                'end_date': datetime.date(2011, 12, 25),
                'end_time': datetime.time(19, 43, 2)
            }
        ]
        self.assertEqual(self.elements_list, expect_list)

    def testParseWithFullNameAndDateFilter(self):
        """
        Assert that parsing with full name and dates filters is correct
        """
        self.parser.path_to_file = 'xml_files/people.xml'
        self.parser.tag = 'person'
        dates_filter = (datetime.date(2011, 12, 24), datetime.date(2011, 12, 26))
        self.parser.parse_file(self.save_elements, 'i.ivanov', dates_filter)
        expect_list = [
            {
                'full_name': 'i.ivanov',
                'start_date': datetime.date(2011, 12, 25),
                'start_time': datetime.time(10, 25, 47),
                'end_date': datetime.date(2011, 12, 25),
                'end_time': datetime.time(19, 43, 2)
            }
        ]
        self.assertEqual(self.elements_list, expect_list)


if __name__ == '__main__':
    unittest.main()