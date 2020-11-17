from flask import Flask, request, Response
from decouple import config
import base64
import hashlib
import hmac 
import json
import re
import api_config #local
import catfacts #local

app = Flask(__name__)
api= api_config.create_api()

CONSUMER_KEY=config('consumer_key')
CONSUMER_SECRET=config('consumer_secret')
ACCESS_TOKEN=config('access_token')
ACCESS_TOKEN_SECRET=config('access_token_secret')

@app.route('/webhook/twitter', methods=['GET'])
def webhook_challenge():
    consumer_secret_bytes = bytes(CONSUMER_SECRET,'utf-8')
    message = bytes(request.args.get('crc_token'),'utf-8')

    sha256_hash_digest = hmac.new(consumer_secret_bytes, message , digestmod=hashlib.sha256).digest()
    response={
        'response_token':'sha256='+base64.b64encode(sha256_hash_digest).decode('utf-8')
    }

    return json.dumps(response)

@app.route('/webhook/twitter',methods=['POST'])
def respond_with_facts():
    req=json.load(request.get_json())
    
    msg_txt=''
    cat_regex=re.compile(r'[Ss][Ee][Nn][Dd] [Mm][Ee] [Cc][Aa][Tt] [Ff][Aa][Cc][Tt][Ss]')

    if req['direct_message_events']:
        msg_txt = req['direct_message_events'][0]['message_create']['message_data']['text']
        user_id = str(req['direct_message_events'][0]['message_create']['sender_id'])
    
    send_cats = cat_regex.search(msg_txt)
    if send_cats:
        api.send_direct_message(user_id,catfacts.retrieveCatfact()+" Ny a~")
        

    return {'status_code':200}

@app.route('/')
def index():
    return f"<h3>Welcome to Cat Facts!</h3>"


if __name__=='__main__':
    app.run(port=5000)


# {
# 'for_user_id': '359498984', 
# 'direct_message_events': [{
#     'type': 'message_create',
#     'id': '1328502450765131783', 
#     'created_timestamp': '1605574641301', 
#     'message_create': {
#         'target': {
#             'recipient_id': '359498984'
#             }, 
#         'sender_id': '1215422201966538754', 
#         'message_data': {
#             'text': 'Hello!', 
#             'entities': {
#                 'hashtags': [], 
#                 'symbols': [], 
#                 'user_mentions': [], 
#                 'urls': []
#             }
#         }
#     }
# }], 
# 'users': {
#     '1215422201966538754': {
#         'id': '1215422201966538754', 
#         'created_timestamp': '1578614224727', 
#         'name': 'Snarky', 
#         'screen_name': 'snarky_raven', 
#         'description': 'Software Engineer student,  aspiring game dev. HUGE FUCKING NERD.', 
#         'protected': False, 'verified': False, 'followers_count': 5, 'friends_count': 60, 
#         'statuses_count': 1, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1215423381819940864/KLk30fg-_normal.jpg', 
#         'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1215423381819940864/KLk30fg-_normal.jpg'}, 
#     '359498984': {
#             'id': '359498984', 
#             'created_timestamp': '1313949571000', 
#             'name': 'quantum_Raven', 
#             'screen_name': '_quantumRaven', 
#             'description': 'Software engineer. \nAspiring Game Developer. \nHuge fucking nerd.\nIRL Multiclassed Wizard/Artificer.\n\nDM me and say "send me cat facts"', 
#             'protected': False, 'verified': False, 'followers_count': 58, 'friends_count': 318, 
#             'statuses_count': 1921, 
#             'profile_image_url': 'http://pbs.twimg.com/profile_images/1274411129935200256/UUUDKxRl_normal.jpg',
#             'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1274411129935200256/UUUDKxRl_normal.jpg'}}}