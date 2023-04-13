from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
account_sid= os.getenv('account_sid')
auth_token =os.getenv('auth_token')
my_number=os.getenv('my_number')
twilio_number=os.getenv('twilio_number')
verify_sid=os.getenv('verify_sid')


def solicitar_otp():
    client= Client(account_sid, auth_token)
    client.verify.services(verify_sid).verifications.create(
    to=my_number, channel="call"
    ) 
      

def verifica_otp(otp_code):
        client= Client(account_sid, auth_token)

        otp_verification_check=client.verify.services(verify_sid).verification_checks.create(
            to=my_number, code=otp_code
        )
        # Verificar se a verificação foi aprovada
        if otp_verification_check.status == 'approved':
            return True
        else:
            return False
        
        

#print(otp_vcheck)