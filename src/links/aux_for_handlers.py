from typing import Dict
from random import choice
from string import ascii_letters
from datetime import datetime, timedelta

def gen_short_code(l=6):
    generated_code = ''.join(choice(ascii_letters) for _ in range(l))
    return generated_code

def fill_fields_initially(new_link : Dict):
    current_time = datetime.now()  # datetime.now(pytz.UTC)
    new_link['created_time'] = current_time
    new_link['last_usage_time'] = current_time
    new_link['expired_time'] = current_time + timedelta(weeks=2)
    new_link['usage_cnt'] = 0
    return new_link