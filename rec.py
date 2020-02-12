import os
from flask import Flask, request, Response
from app import detect_intent_texts, send_message, channel_info, list_channels
app = Flask(__name__)

SLACK_WEBHOOK_SECRET = 'hOQE3Otv4rQUFPbgfZif3MKD'
project_id = 'tcc-chatbot-kyhwfw'
DIALOGFLOW_PROJECT_ID = 'tcc-chatbot-kyhwfw'
OMDB_API_KEY = 'http://www.omdbapi.com/?i=tt3896198&apikey=c7626fa'
GOOGLE_APPLICATION_CREDENTIALS = 'tcc-chatbot-kyhwfw-3eaebfc2d29f.json'


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + " says: " + text
        print(inbound_message)
    return Response(), 200


@app.route('/slack/send_msg', methods=['POST', 'GET'])
def send_msg():
    channel_data = channel_info('CT559GGSD')
    if channel_data['latest']['user'] == 'UTFA0P464':
        channels = list_channels()
        if channels:
            # print("Channels: ")
            for channel in channels:
                # print(channel['name'] + " (" + channel['id'] + ")")
                # detailed_info = channel_info(channel['id'])
                detailed_info = channel_info(channel['id'])
                if channel['name'] == 'general':
                    detailed_info = channel_info(channel['id'])
                    # print('Latest text from ' + channel['name'] + ":")
                    # print(detailed_info['latest']['text'])
                    user_intent = detect_intent_texts('tcc-chatbot-kyhwfw', "unique", detailed_info['latest']['text'],
                                                      'en')
                    send_message(channel['id'], user_intent)
                    break

                if detailed_info['latest']['text'] == 'exit':
                    send_message(channel['id'], 'break')
                    break
                    # if user_intent == "dance" and channel['name'] == 'general':
                    # if detailed_info['latest']['text'] == 'dance':
                    #     send_message(channel['id'], "It worked!")
                    # if detailed_info['latest']['text'] == 'ok':
                    #     send_message(channel['id'], "no")

        else:
            print("Unable to authenticate.")


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    app.run(debug=True)
