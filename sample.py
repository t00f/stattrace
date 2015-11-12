# -*- coding:utf-8 -*-

import redis
import time

from stattrace.stattrace import Stattrace

from datetime import date, timedelta

db = redis.StrictRedis(host="127.0.0.1", port="6379", db=1)
trace = Stattrace(redis=db)

today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days=5)

number_of_information = 60000


def get_time():
    """
    """
    return int(round(time.time() * 1000))


def install():
    """
    """
    for i in xrange(1, number_of_information + 1):

        user = "user%s" % i
        d = today + timedelta(days=i % 20)
        d2 = d+timedelta(days=3)

        trace.complete_objective("registered", d, user)
        trace.complete_objective("connected", d, user)

        trace.complete_objective("connected", d, user)

        trace.complete_objective("payed", d2, user)


def run():
    # assert len(trace.reach_objective("registered")) == number_of_information
    assert len(trace.reach_objectives(["registered", "connected", "payed"])) == number_of_information


def flush():
    trace.clear()


if __name__ == '__main__':
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
