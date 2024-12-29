import re


PHONE_NUMBER_PATTERN = '(^(09)\d{9}$)'
        
def validate_phone_number(phone_number):
    if re.fullmatch(PHONE_NUMBER_PATTERN, phone_number):
        return True
    else:
        return False