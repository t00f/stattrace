# -*- coding:utf-8 -*-

import time

from stattrace.stattrace import Stattrace

from datetime import date, timedelta

trace = Stattrace()

today = date.today()
last_week = today + timedelta(days=-17)
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(days=71)

number_of_information = 60000
number_of_dates = 4


def get_time():
    """
    """
    return int(round(time.time() * 1000))


def install():
    """
    """
    for i in xrange(1, number_of_information + 1):

        user = "user%s" % i
        d = today + timedelta(days=i % number_of_dates)
        d2 = d+timedelta(days=3)

        trace.complete_objective("registered", d, user)
        trace.complete_objective("connected", d, user)

        trace.complete_objective("connected", d, user)

        trace.complete_objective("payed", d2, user)


def run():
    """
    """
    # assert len(trace.reach_objectives(["registered", "connected", "payed"])) == number_of_information  # ~730ms
    stats = trace.stats_for_objective("registered")  # ~630ms
    assert len(stats) == number_of_dates
    assert stats[str(today)] == number_of_information / number_of_dates


def flush():
    """
    """
    trace.clear()


if __name__ == '__main__':
    """
    """
    start_time = get_time()
    flush()
    flush_time = get_time()
    install()
    install_time = get_time()
    run()
    run_time = get_time()

    print "Stats for %s information" % number_of_information
    print "Flush time %sms" % (flush_time - start_time)
    print "Install time %sms" % (install_time - flush_time)
    print "Run time %sms" % (run_time - install_time)
