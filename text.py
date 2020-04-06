from flask import Blueprint,render_template
from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from os.path import join, dirname
import json
import os.path
import requests

text=Blueprint("text",__name__,static_folder="static",template_folder="templates")
 


@text.route("/text")
def textfile():
    authenticator = IAMAuthenticator('IXH7vQnk77jZ6HeQznP_x6VLws6DHaN1UfVeszQEHtd8')
    personality_insights = PersonalityInsightsV3(
        version='2017-10-13',
        authenticator=authenticator)

    personality_insights.set_service_url('https://gateway-lon.watsonplatform.net/personality-insights/api')

    # Add text form audio file here.

    with open(join(dirname(__file__), './test/t.txt')) as profile_json:
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
    get = requests.get('http://localhost:3001/home') # GET request
    data = get.json()

    # print(data) 

    return render_template("report_text.html",value=data)

# print(json.dumps(profile, indent=2))
