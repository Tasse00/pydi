import unittest

from di.utils import get_cls_name, get_cls_from_name
from tests.app import Staff


class TestUtils(unittest.TestCase):

    def test_get_cls_name(self):
        self.assertEqual(get_cls_name(Staff), 'tests.app.staff.Staff')

    def test_get_cls_from_name(self):
        self.assertEqual(get_cls_from_name("tests.app.staff.Staff"), Staff)
