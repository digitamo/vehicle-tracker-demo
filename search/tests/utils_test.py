from datetime import datetime
from unittest import TestCase

from search.utils import dump_datetime


class Utils(TestCase):

    def test_dump_datetime(self):
        date = datetime.fromisoformat('2019-07-24T04:51:06.562952')
        date_dump = dump_datetime(date)
        self.assertEqual(date_dump, '2019-07-24T04:51:06.562952')
