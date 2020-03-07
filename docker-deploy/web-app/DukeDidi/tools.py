import re
import datetime
from django.utils import timezone
# from datetime import datetime, timedelta
import os

def check_email(email):
    valid_email = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if re.match(valid_email, email):
        return True
    return

def check_license_plate_number(string):
    valid_number = r'^[A-Z]{3}[0-9]{4}$'
    if re.match(valid_number,string):
        return True
    return False

def parse_date_time(string):
    return datetime.datetime(*[int(v) for v in string.replace('T', '-').replace(':', '-').split('-')])


def sharable(string):
    if string == "yes":
        return True
    elif string == "no":
        return False
    return None


def not_all_none(arr):
    for i in arr:
        if i is None:
            return False
    return True

def judge_legal_search_sharable(destination, start_time, end_time, passenger_party_size):
    return not_all_none([destination, start_time, end_time, passenger_party_size]) and end_time - start_time > datetime.timedelta(minutes=1)

def parse_sharer_partysize_pair(string):
    pair_list = string.split(';')[0:-1]
    return pair_list

def remaining_sharers_list(pair_list,curr_email):
    ans = []
    for pair in pair_list:
        if not pair.startswith(curr_email):
            ans.append(pair[0:-2])
    return ans

def remaining_pair_list(pair_list,curr_email):
    ans = ''
    for pair in pair_list:
        if not pair.startswith(curr_email):
            ans = ans + str(pair) + ';'
    return ans

def get_canceled_sharer_size(pair_list,curr_email):
    for pair in pair_list:
        if pair.startswith(curr_email):
            return int(pair[-1])
    return None

# def ride_filter(arr):
#     ret = []
#     for i in arr:
#         if(ride=models.Ride.objects.get(i) and not ride.iscompleted and ride.isconfirmed):
#             ret += [ride.pk]
#

pw = '1234'
salt = os.urandom(40)
add = pw+str(salt)
print(add)