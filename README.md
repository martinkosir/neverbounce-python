# neverbounce-python

Python library for the [NeverBounce API v3](https://neverbounce.com/) — a real-time email verification service. 

## Usage

[Sign up](https://app.neverbounce.com/register) to get an [API username and key](https://app.neverbounce.com/settings/api) and 1000 free monthly verifications.

```python
from neverbounce import NeverBounce

neverbounce = NeverBounce('my_api_username', 'my_api_key')
verified_email = neverbounce.verify_single('some.email@example.com')

verified_email.result
# 'valid'

verified_email.is_valid
# True

verified_email.result_code
# 0

str(verified_email)
# 'some.email@example.com: valid'
```
    
## Documentation
 * [Official docs for the NeverBounce RESTful API](https://docs.neverbounce.com/)
