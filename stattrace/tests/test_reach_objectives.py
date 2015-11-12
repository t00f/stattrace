# -*- coding:utf-8 -*-

import redis

from unittest import TestCase
from stattrace import Stattrace
from datetime import date, timedelta


class TestreacherObjectives(TestCase):
    """
    """
    def setUp(self):
        """
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)

        self.trace = Stattrace(redis=redis.StrictRedis(host="127.0.0.1", port="6379", db=7))
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

    def test_reach_objectives_for_same_day(self):
        """
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)

        self.assertEqual(self.trace.reach_objectives(objectives=["registration", "order"], start_date=today, end_date=today), {"user1", "user2"})
        self.assertEqual(self.trace.reach_objectives(objectives=["registration", "order"], start_date=today), {"user1", "user2", "user3", "user4"})
        self.assertEqual(self.trace.reach_objectives(objectives=["registration", "order"], start_date=tomorrow), {"user4"})

    def test_reach_objectives_without_date(self):
        """
        """
        self.assertEqual(self.trace.reach_objectives(objectives=["registration", "order"]), {"user1", "user2", "user3", "user4"})

    def test_reach_objectives_without_objectives(self):
        """
        """
        self.assertEqual(self.trace.reach_objectives(objectives=[]), set())

    def test_reach_objectives_with_unknown_objectives(self):
        """
        """
        self.assertEqual(self.trace.reach_objectives(objectives=["died", "order"]), set())