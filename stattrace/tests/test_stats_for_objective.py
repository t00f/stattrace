# -*- coding:utf-8 -*-

from unittest import TestCase
from stattrace import Stattrace
from datetime import date, timedelta


def get_dates():
    """
    """
    today = date.today()
    yesterday = today + timedelta(days=-1)
    tomorrow = today + timedelta(days=1)

    return yesterday, today, tomorrow


class TestStatsForObjective(TestCase):
    """
    """
    def setUp(self):
        """
        """
        yesterday, today, tomorrow = get_dates()

        self.trace = Stattrace()

        self.trace.complete_objective("registration", today, "user1")
        self.trace.complete_objective("registration", today, "user2")
        self.trace.complete_objective("registration", today, "user3")

        self.trace.complete_objective("registration", tomorrow, "user4")
        self.trace.complete_objective("registration", tomorrow, "user5")

        self.trace.complete_objective("order", today, "user1")
        self.trace.complete_objective("order", today, "user2")

        self.trace.complete_objective("order", tomorrow, "user3")
        self.trace.complete_objective("order", tomorrow, "user4")

    def tearDown(self):
        """
        """
        self.trace.clear()

    def test_stats_for_objective_with_dates(self):
        """
        """
        yesterday, today, tomorrow = get_dates()

        expected_results = {
            str(today): 3,
            str(tomorrow): 2
        }

        self.assertEquals(self.trace.stats_for_objective("registration", start_date=yesterday, end_date=tomorrow), expected_results)
        self.assertEquals(self.trace.stats_for_objective("registration", end_date=tomorrow), expected_results)
        self.assertEquals(self.trace.stats_for_objective("registration", start_date=today), expected_results)

    def test_stats_for_objective_with_same_dates(self):
        """
        """
        yesterday, today, tomorrow = get_dates()

        expected_results = {
            str(tomorrow): 2
        }

        self.assertEquals(self.trace.stats_for_objective("registration", start_date=tomorrow, end_date=tomorrow), expected_results)

    def test_stats_for_objective_without_dates(self):
        """
        """
        yesterday, today, tomorrow = get_dates()

        expected_results = {
            str(today): 3,
            str(tomorrow): 2
        }

        self.assertEquals(self.trace.stats_for_objective("registration"), expected_results)

    def test_stats_for_objective_with_unknown_objective(self):
        """
        """
        yesterday, today, tomorrow = get_dates()

        expected_results = {}

        self.assertEquals(self.trace.stats_for_objective("eat"), expected_results)
