# -*- coding:utf-8 -*-

import re
import time

from datetime import date


class Stattrace(object):
    """
    """
    REDIS_ALL = "*"
    REDIS_LINFINI = "-inf"
    REDIS_HINFINI = "+inf"

    def __init__(self, redis):
        """
        """
        self._redis = redis
        self._isword = re.compile('\w')

    def timestamp(self, current_date):
        """
        """
        if current_date is None:
            return 0

        return int(time.mktime(current_date.timetuple()))

    def clear(self, objective=None):
        """
        """
        if objective is None:
            objective = Stattrace.REDIS_ALL

        keys = list(self._redis.scan_iter(objective))

        if len(keys) > 0:
            self._redis.delete(*keys)

    def complete_objective(self, objective, current_date, identifier):
        """
        """
        if type(objective) != str or not self._isword.match(objective):
            return False

        if type(current_date) != date:
            return False

        if identifier is None:
            return False

        timestamp = self.timestamp(current_date)
        self._redis.zadd(objective, timestamp, identifier)
        return True

    def reach_objective(self, objective, start_date=None, end_date=None):
        """
        """
        if objective is None:
            return set()

        start = self.timestamp(start_date)
        end = self.timestamp(end_date)

        if start == 0:
            start = Stattrace.REDIS_LINFINI
        
        if end == 0:
            end = Stattrace.REDIS_HINFINI

        results = self._redis.zrangebyscore(objective, start, end)
        return set(results)

    def reach_objectives(self, objectives, start_date=None, end_date=None):
        """
        """
        identifiers = set()

        for objective in objectives:
            unified_identifiers = self.reach_objective(objective, start_date, end_date)

            if len(identifiers) == 0:

                if len(unified_identifiers) == 0:
                    return identifiers

                identifiers = unified_identifiers
            else:
                identifiers.intersection_update(unified_identifiers)

        return identifiers
