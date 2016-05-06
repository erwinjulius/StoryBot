import os
import json
import requests

FB_TOKEN = os.environ.get("FB_TOKEN")
FB_URL = os.environ.get("FB_URL")

def sendBotMessage(recipient, message):
    """A script to send a facebook message to recipient
    """
    responseBody = { 
                        'recipient': { 
                            'id': recipient
                        }, 
                        'message': {
                            'text': message
                        } 
                    } 
    
    r = requests.post(FB_URL, 
                      params = { 'access_token': FB_TOKEN },
                      headers = {'content-type': 'application/json'},
                      data = json.dumps(responseBody) )

def sendBotStructuredGenericMessage(recipient, title, item_url=None, image_url=None, subtitle=None, buttons=[]):
    """ref: https://developers.facebook.com/docs/messenger-platform/send-api-reference#welcome_message_configuration
            https://developers.facebook.com/docs/messenger-platform/send-api-reference#guidelines 
    
    Regarding buttons:
        {
            "type":"web_url",
            "title":"View Website",
            "url":"https://www.petersbowlerhats.com"
        },
        {
            "type":"postback",
            "title":"Start Chatting",
            "payload":"DEVELOPER_DEFINED_PAYLOAD"
        }
    """
    
    responseBody = {
        'recipient': { 
            'id': recipient
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": title,
                            "item_url": item_url,
                            "image_url": image_url,
                            "subtitle": subtitle,
                            "buttons": buttons
                        }
                    ]
                }
            }
        }
         
    }
    
    requests.post(FB_URL, 
                  params = { 'access_token': FB_TOKEN },
                  headers = {'content-type': 'application/json'},
                  data = json.dumps(responseBody) )
    
def sendBotStructuredButtonMessage(recipient, text, buttons=[]):
    """Send a facebook structured button message
    Use this for prompts and navigation
    """

    responseBody = {
        'recipient': { 
            'id': recipient
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text":text,
                    "buttons":buttons
                }
            }
        }
         
    }
    
    r = requests.post(FB_URL, 
                  params = { 'access_token': FB_TOKEN },
                  headers = {'content-type': 'application/json'},
                  data = json.dumps(responseBody) )
    print r.json()

def sendHelpMessage( contributor ):
    """Sends a help message with the instructions on how to use the bot
    """
    sendBotMessage( contributor.social_identifier, "To read a random story just send \"\\browse\"" )
    sendBotMessage( contributor.social_identifier, "to start a story just send \"\start\"" )
    sendBotMessage( contributor.social_identifier, "to read the story you are working on just send \"\\read\"" )
    sendBotMessage( contributor.social_identifier, "to continue a story just send \"\continue\"" )
    sendBotMessage( contributor.social_identifier, "to see a history of your stories just send \"history\"" )
    

def readBackStory( contributor, story ):
    """Reads the story back and makes sure it chunks it appropriately
    """
    sendBotMessage(contributor.social_identifier, story.title)
    story_fragments = Fragment.objects.filter(story=story).order_by('position')
    for fragment in story_fragments:
        complete = "COMPLETE" if fragment.complete else "INCOMPLETE"
        sendBotMessage(contributor.social_identifier, "[" + complete + "] " + FRAGMENT_MAPPING.get(fragment.position) + " by " + fragment.alias)
        fragment_chunks = chunkString(fragment.fragment, 180)
        for chunk in fragment_chunks:
            sendBotMessage(contributor.social_identifier, chunk)