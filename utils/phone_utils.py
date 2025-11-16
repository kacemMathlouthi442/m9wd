import phonenumbers
from phonenumbers import NumberParseException



def is_valid_phone_number(number: str, region: str = None) -> bool:
    try:
        parsed_number = phonenumbers.parse(number, region)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False
    
