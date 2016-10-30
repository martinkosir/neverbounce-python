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
    >>> verified_email = neverbounce.verify('some.email@example.com')

    >>> verified_email.result_text
    'valid'

    >>> verified_email.result_code
    0

    >>> verified_email.is_valid
    True

    >>> str(verified_email)
    'some.email@example.com: valid'

Bulk verification
~~~~~~~~~~~~~~~~~

To use this features you need to `configure a payment method`_ in
NeverBounce account settings.

.. code::

    >>> from neverbounce import NeverBounce
    >>> neverbounce = NeverBounce('my_api_username', 'my_api_key')

Create the job and get it's id:

.. code::

    >>> emails = ['some.email@example.com', 'john.doe@gmail.com']
    >>> job_id = neverbounce.create_job(emails).job_id

Periodically poll for the verification job result:

.. code::

    >>> job_status = neverbounce.check_job(job_id)

Retrieve the result when the job is completed:

.. code::

    >>> if job_status.is_completed:
    >>>     verified_emails = neverbounce.retrieve_job(job_id)
    >>>     for email in verified_emails:
    >>>         print(str(email))
    'some.email@example.com: valid'
    'john.doe@gmail.com: invalid'

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
