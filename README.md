Stattrace
=========

Enables to quickly create and query statistics stored in `redis` database with `python`


How to use it ?
---------------

1) Store information when an objective is completed

>>> trace = Stattrace(redis=REDIS_DATABASE)
>>> trace..complete_objective(objective="registered", current_date=today, identifier=user.id)

2) Search for reached objectives

>>> trace.reach_objective("registered")
>>> trace.reach_objective("registered", start_date=today)
>>> trace.reach_objective("registered", start_date=today, end_date=end_of_the_year)

Example
-------

Need an example ? Take a look at `sample.py`

Performance
-----------

With 60000 information stored, the following query takes around 800ms

>>> trace.reach_objectives(["registered", "connected", "payed"])
