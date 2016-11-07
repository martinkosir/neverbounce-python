NeverBounce
===========

Python API wrapper library for the `NeverBounce`_ email
verification service.

Installation
------------

.. code::

    $ pip install neverbounce

The only dependency is the `requests`_ library.

Usage
-----

`Sign up`_ to get an `API username and key`_ and 1000 free monthly
verifications. The **free account** supports only **single verifications**.

Single verification
~~~~~~~~~~~~~~~~~~~

.. code::

    >>> from neverbounce import NeverBounce

    >>> neverbounce = NeverBounce('my_api_username', 'my_api_key')
    >>> verified = neverbounce.verify('martin@martinkosir.net')

    >>> print(str(verified))
    martin@martinkosir.net: valid

    >>> print(verified.email, verified.result_text, verified.result_code, verified.is_valid)
    martin@martinkosir.net valid 0 True

Bulk verification
~~~~~~~~~~~~~~~~~

To use this features you need to `configure a payment method`_ in
NeverBounce account settings.

.. code::

    >>> from neverbounce import NeverBounce
    >>> neverbounce = NeverBounce('my_api_username', 'my_api_key')

Create the job and get it's id:

.. code::

    >>> emails = ['some.email@example.com', 'john.smith@gmail.com']
    >>> job_id = neverbounce.create_job(emails).job_id

Periodically check the status of verification job:

.. code::

    >>> job_status = neverbounce.check_job(job_id)

Use the `results` generator to iterate over verified emails if the job has been completed:

.. code::

    >>> if job_status.is_completed:
    ...     for verified in neverbounce.results(job_id):
    ...         print(verified.email, verified.result_text, verified.result_code, verified.is_valid)
    some.email@example.com invalid 1 False
    john.smith@gmail.com invalid 1 False

Account information
~~~~~~~~~~~~~~~~~~~

Get the information about your API account:

.. code::

    >>> from neverbounce import NeverBounce
    >>> neverbounce = NeverBounce('my_api_username', 'my_api_key')
    >>> account = neverbounce.account()

    >>> print(str(account))
    Credits: 999, Jobs Completed: 22, Jobs Processing: 0

    >>> print(account.credits, account.jobs_completed, account.jobs_processing)
    999 22 0

Documentation
-------------

-  `Official docs for the NeverBounce RESTful API`_


.. _NeverBounce: https://neverbounce.com/
.. _requests: http://docs.python-requests.org/
.. _Sign up: https://app.neverbounce.com/register
.. _API username and key: https://app.neverbounce.com/settings/api
.. _configure a payment method: https://app.neverbounce.com/settings/billing
.. _Official docs for the NeverBounce RESTful API: https://docs.neverbounce.com/

Build status
------------

.. image:: https://travis-ci.org/martinkosir/neverbounce-python.svg?branch=master
    :target: https://travis-ci.org/martinkosir/neverbounce-python
