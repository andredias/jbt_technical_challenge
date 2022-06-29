JBT TechnicalChallenge
======================

The specification is described in the file `specification.rst`.


Installation
============

You must have `poetry <https://python-poetry.org/>`_ installed to run the project.

Execute:

.. code:: console

    $ poetry install
    $ poetry shell


Run
===

Execute:

.. code:: console

    $ make run

Then, visit the URL ``http://localhost:5000/docs`` to test the project.

.. important::

    The location of the store is (lat: 0.0, long: 0.0). There is no way to change that currently.

.. tip::

    1. You can load a ``csv`` file containing the coordinates for the destinations.
       For example:

       .. code:: csv

            time,lat,long
            2022-06-29 10:15:40.576367,0.04,0.02
            2022-06-29 10:15:41.576367,0.01,0.02
            2022-06-29 10:15:42.576367,0.02,0.02

    2. The ``username`` and ``password`` are fixed in ``config.py``.
       Their currently values are ``drone`` and ``1234`` respectively.
    3. The endpoint ``/drone/next_destination`` requires authentication, but not the others.
    4. Also, ``/drone/next_destination`` simulates the expected drone behavior, i.e.,
       the drone moves to the next destination and the destination is removed from the list.
       If there is no more destinations available or the drone's remaining range is insuficient for the next delivery, it returns to the store (0.0, 0.0).
    5. The drone's remaining range is fixed in ``5`` in file ``jbt_drone/drone.py`` and cannot be changed in runtime in the current version.


Testing
=======

Execute:

.. code:: console

    $ make test
