from flask import Blueprint, render_template
from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from os.path import join, dirname
import json
import os.path
import requests
import zipfile
import textract
import re
import glob
# text=Blueprint("text",__name__,static_folder="static",template_folder="templates")
# @text.route("/text")


def textfile():
    authenticator = IAMAuthenticator(
        'IXH7vQnk77jZ6HeQznP_x6VLws6DHaN1UfVeszQEHtd8')
    personality_insights = PersonalityInsightsV3(
        version='2017-10-13',
        authenticator=authenticator)

    personality_insights.set_service_url(
        'https://gateway-lon.watsonplatform.net/personality-insights/api')

    for filename in glob.glob("./uploads/*.docx"):
        cv_file = filename

    MY_TEXT = textract.process(cv_file)
    MY_TEXT = MY_TEXT.decode("utf-8")
    MY_TEXT = re.sub("(\n+\t+)|(\n+)|(\t+)", ". ", (MY_TEXT))
    print(MY_TEXT)

    with open("./uploads/cv.txt", "w") as text_file:
        print(str(MY_TEXT), file=text_file)

    with open(join(dirname(__file__), './uploads/cv.txt')) as profile_json:
        profile = personality_insights.profile(
            profile_json.read(),
            'application/json',
            content_type='text/plain',
            consumption_preferences=True,
            raw_scores=False
        ).get_result()

# # save_path = 'D:\react\back'
# # where you save node js file -put that directory down
    completeName = os.path.join('../node-master/node-master/result2.json')
    with open(completeName, 'w') as fp:
        json.dump(profile, fp)
    get = requests.get('http://localhost:3001/cv')  # GET request
    data1 = get.json()

    with open(join(dirname(__file__), './uploads/audio_text.txt')) as profile_json:
        profile = personality_insights.profile(
            profile_json.read(),
            'application/json',
            content_type='text/plain',
            consumption_preferences=True,
            raw_scores=False
        ).get_result()
    completeName = os.path.join('../node-master/node-master/result3.json')
    with open(completeName, 'w') as fp:
        json.dump(profile, fp)
    get = requests.get('http://localhost:3001/ans')  # GET request
    data2 = get.json()
    print(data1)
    print(data2)
    return data1, data2

# print(json.dumps(profile, indent=2))

# d1,d2=textfile()
# print(d1)

# print(d2)
