from kavenegar import *


def send_otp_code(phone_number,code):
  

    # try:
    #     api = KavenegarAPI('2F5A71335043456F5A6B6D775379686B68434979643754516A5438782B796154376D316D596B354C6E36493D')
    #     params = {
    #         'sender': '',#optional
    #         'receptor': phone_number,#multiple mobile number, split by comma
    #         'message': f'{code}کد تایید شما',
    #     } 
    #     response = api.sms_send(params)
    #     print(response)
    # except APIException as e: 
    #     print(e)
    # except HTTPException as e: 
    #     print(e)

    try:
        api = KavenegarAPI('2F5A71335043456F5A6B6D775379686B68434979643754516A5438782B796154376D316D596B354C6E36493D')
        params = {
            'receptor': phone_number,
            'template': 'verify',
            'token': str(code),
            'token2': str(code),
            'token3': str(code),
            'type': 'sms',#sms vs call
        }   
        response = api.verify_lookup(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)