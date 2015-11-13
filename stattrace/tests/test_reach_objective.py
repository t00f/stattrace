# -*- coding:utf-8 -*-

from unittest import TestCase
from stattrace import Stattrace
from datetime import date, timedelta


class TestReachObjective(TestCase):
    """
    """
    def setUp(self):
        """
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)

        self.trace = Stattrace()
        self.trace.complete_objective("registration", today, "user1")
        self.trace.complete_objective("registration", today, "user2")
        self.trace.complete_objective("registration", today, "user3")

        self.trace.complete_objective("registration", tomorrow, "user4")
        self.trace.complete_objective("registration", tomorrow, "user5")

    def tearDown(self):
        """
        """
        self.trace.clear()

    def test_reach_objective_with_all_information(self):
        """
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)

        self.assertEqual(self.trace.reach_objective(objective="registration", start_date=today), {"user1", "user2", "user3", "user4", "user5"})
        self.assertEqual(self.trace.reach_objective(objective="registration", start_date=tomorrow), {"user4", "user5"})

    def test_reach_objective_without_date(self):
        """
        """
        self.assertEqual(self.trace.reach_objective("registration"), {"user1", "user2", "user3", "user4", "user5"})

    def test_reach_objective_without_objective(self):
        """
        """
        today = date.today()
        self.assertEqual(self.trace.reach_objective(objective=None, start_date=today), set())

    def test_reach_objective_without_all_information(self):
        """
        """
        self.assertEqual(self.trace.reach_objective(objective=None, start_date=None), set())


