# -*- coding:utf-8 -*-

import re
import redis
import time

from datetime import date
from collections import OrderedDict


class Stattrace(object):
    """ A Stattrace enables to store objectives and 
        retrieve them later in order to compute some statistics.
    """
    REDIS_ALL = "*"
    REDIS_LINFINI = "-inf"
    REDIS_HINFINI = "+inf"

    def __init__(self, host="localhost", port="6379", db=1):
        """ 
            Initialize a tracer with the given redis parameters

            Params:
                host (string): redis hostname
                port (string): redis port
                db (int): redis database number
        """
        self._redis = redis.StrictRedis(host=host, port=port, db=db, socket_timeout=True)
        self._isword = re.compile('\w')

    # Adding / Removing information

    def complete_objective(self, objective, current_date, identifier):
        """ 
            Store a completed objective at the current_date for the given
            identifier.

            Params:
                objective (string): the objective that has been completed
                current_date (date): the date when the objective has been completed
                identifier (object): the identifier that has reached the objective

            Returns:
                Returns True if data has been stored. False something wrong happened.
        """
        if type(objective) != str or not self._isword.match(objective):
            return False

        if type(current_date) != date:
            return False

        if identifier is None:
            return False

        timestamp = self._convert_date_to_timestamp(current_date)
        self._redis.zadd(objective, timestamp, identifier)
        return True

    def clear(self, objective=None):
        """
            Clear all data related to objective.
            If objective is ommited, it will remove all data

            Params:
                objective (string): the objective to remove
        """
        if objective is None:
            objective = Stattrace.REDIS_ALL

        keys = list(self._redis.scan_iter(objective))

        if len(keys) > 0:
            self._redis.delete(*keys)

    # Statistics

    def reach_objective(self, objective, start_date=None, end_date=None):
        """ 
            Returns the number of identifiers that have reached the given
            objective between the start_date and the end_date

            Params:
                objectves (string): the name of the objective to match
                start_date (date): the start_date
                end_date (date): the end_date

            Returns:
                Returns a set containing all identifiers that have
                reacher all objectives
        """
        if objective is None:
            return set()

        start, end = self._get_timestamp_range(start_date, end_date)
        results = self._redis.zrangebyscore(objective, start, end)
        return set(results)

    def reach_objectives(self, objectives, start_date=None, end_date=None):
        """ 
            Returns the count of identifiers that reach all objectives
            between start_date and end_date

            objectives order matters.

            If start_date and end_date are ommited, it will compute the
            count on all data

            Params:
                objectves (array): list of objectves to match
                start_date (date): the start_date
                end_date (date): the end_date

            Returns:
                Returns a set containing all identifiers that have
                reacher all objectives.
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

    def stats_for_objective(self, objective, start_date=None, end_date=None):
        """
            Get count of reached objective between start_date and end_date.

            If start_date and end_date are ommited, it will returns all stats
            for the given objective.

            Params:
                objective (str): the name of the objective
                start_date (date): the date to start stats
                end_date (date): the date to end stats

            Returns:
            An OrderedDict with the following information
                dates as keys
                number of reached objective as value
        """
        stats = OrderedDict()

        if objective is None:
            return stats

        start, end = self._get_timestamp_range(start_date, end_date)
        results = self._redis.zrangebyscore(objective, start, end, withscores=True)

        for result, timestamp in results:
            current_date = str(self._convert_timestamp_to_date(timestamp))

            if current_date in stats:
                continue

            stats[current_date] = self._redis.zcount(objective, timestamp, timestamp)

        return stats

    # Utilities

    def _convert_date_to_timestamp(self, current_date):
        """ 
            Convert the given date to a timestamp

            Params:
                current_date (date): the date to convert

            Returns:
                Returns 0 if date is None or the timestamp as int.
        """
        if current_date is None:
            return 0

        return int(time.mktime(current_date.timetuple()))

    def _convert_timestamp_to_date(self, timestamp):
        """ Convert a timestamp to a date

            Params:
                timestamp (int): the timestamp to convert

            Returns:
                Returns None or the converted date
        """
        if timestamp == 0 or timestamp is None:
            return None

        return date.fromtimestamp(int(timestamp))

    def _get_timestamp_range(self, start_date, end_date):
        """ 
            Convert start_date and end_date to a timestamp

            This is used internally to call zrangebyscore

            Params:
                start_date (date): the start date
                end_date (date): the end date

            Returns:
                A tuple as (start, end) range 
        """
        start = self._convert_date_to_timestamp(start_date)
        end = self._convert_date_to_timestamp(end_date)

        if start == 0:
            start = Stattrace.REDIS_LINFINI

        if end == 0:
            end = Stattrace.REDIS_HINFINI

        return start, end
