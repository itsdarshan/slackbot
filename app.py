import os
from slackclient import SlackClient
from flask import Flask, request, jsonify, render_template
import dialogflow
import requests
import json

credential_path = "tcc-chatbot-kyhwfw-3eaebfc2d29f.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
project_id = 'tcc-chatbot-kyhwfw'
DIALOGFLOW_PROJECT_ID = 'tcc-chatbot-kyhwfw'
OMDB_API_KEY = 'http://www.omdbapi.com/?i=tt3896198&apikey=c7626fa'
GOOGLE_APPLICATION_CREDENTIALS = 'tcc-chatbot-kyhwfw-3eaebfc2d29f.json'
SLACK_TOKEN = 'xoxp-920553244658-933340786208-923185483633-b359dffa1333b9d2d19f9c62fa5dda9f'

slack_client = SlackClient(SLACK_TOKEN)


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None


def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None


def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        #as_user, attachments, blocks, mrkdwn
        username='pythonbot',
        icon_emoji=':robot_face:'
    )


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text


# if __name__ == '__main__':
#     app.run()
    # channels = list_channels()
    # if channels:
    #     # print("Channels: ")
    #     for channel in channels:
    #         # print(channel['name'] + " (" + channel['id'] + ")")
    #         # detailed_info = channel_info(channel['id'])
    #         if channel['name'] == 'general':
    #             detailed_info = channel_info(channel['id'])
    #             # print('Latest text from ' + channel['name'] + ":")
    #             # print(detailed_info['latest']['text'])
    #             user_intent = detect_intent_texts('test-slackbot-bvhvpc', "unique", detailed_info['latest']['text'], 'en')
    #             send_message(channel['id'], user_intent)
    #
    #             if detailed_info['latest']['text'] == 'exit':
    #                 send_message(channel['id'], 'break')
    #                 break
    #                 # if user_intent == "dance" and channel['name'] == 'general':
    #                 # if detailed_info['latest']['text'] == 'dance':
    #                 #     send_message(channel['id'], "It worked!")
    #                 # if detailed_info['latest']['text'] == 'ok':
    #                 #     send_message(channel['id'], "no")
    #
    # else:
    #     print("Unable to authenticate.")
