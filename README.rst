neverbounce-python
==================

Python library for the `NeverBounce API v3`_ — a real-time email
verification service.

Usage
-----

`Sign up`_ to get an `API username and key`_ and 1000 free monthly
verifications.

A single email verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from neverbounce import NeverBounce

    neverbounce = NeverBounce('my_api_username', 'my_api_key')
    verified_email = neverbounce.verify('some.email@example.com')

    verified_email.result_text
    # 'valid'

    verified_email.result_code
    # 0

    verified_email.is_valid
    # True

    str(verified_email)
    # 'some.email@example.com: valid'

Bulk verification
~~~~~~~~~~~~~~~~~

.. code:: python

    from neverbounce import NeverBounce

    neverbounce = NeverBounce('my_api_username', 'my_api_key')
    emails = ['some.email@example.com', 'john.doe@gmail.com']
    job_id = neverbounce.create_job(emails).job_id

    # Periodically poll for the verification results
    job_status = neverbounce.check_status(job_id)

    # Retrieve the results
    if job_status.is_completed:
        verified_emails = neverbounce.retrieve_results(job_id)
        for email in verified_emails:
            print(str(email))

Documentation
-------------

-  `Official docs for the NeverBounce RESTful API`_

.. _NeverBounce API v3: https://neverbounce.com/
.. _Sign up: https://app.neverbounce.com/register
.. _API username and key: https://app.neverbounce.com/settings/api
.. _Official docs for the NeverBounce RESTful API: https://docs.neverbounce.com/