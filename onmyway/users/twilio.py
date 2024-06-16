from decouple import config 
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE_SID = config('TWILIO_VERIFY_SERVICE_SID')
print(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SERVICE_SID)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
verify = client.verify.v2.services(TWILIO_VERIFY_SERVICE_SID)

def send(phone_number):
    verify.verifications.create(to=phone_number, channel='sms')

def check(phone_number, code):
    try:
        result = verify.verification_checks.create(to=phone_number, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'