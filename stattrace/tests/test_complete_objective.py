# -*- coding:utf-8 -*-

from unittest import TestCase
from stattrace import Stattrace
from datetime import date


class TestCompleteObjective(TestCase):
    """
    """
    def setUp(self):
        """
        """
        self.trace = Stattrace()

    def tearDown(self):
        """
        """
        self.trace.clear()

    def test_complete_objective_with_all_information(self):
        """
        """
        today = date.today()
        self.assertTrue(self.trace.complete_objective("registration", today, "user1"))

    def test_complete_objective_without_objective(self):
        """
        """
        today = date.today()
        self.assertFalse(self.trace.complete_objective(None, today, "user1"))

    def test_complete_objective_without_current_date(self):
        """
        """
        self.assertFalse(self.trace.complete_objective("registration", None, "user1"))

    def test_complete_objective_without_identifier(self):
        """
        """
        today = date.today()
        self.assertFalse(self.trace.complete_objective("registration", today, None))
