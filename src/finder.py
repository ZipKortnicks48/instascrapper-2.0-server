#класс для работы с API
import json
import codecs
import datetime
import os.path
import logging
import argparse
import time
import sys  # sys нужен для передачи argv в QApplication
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError,MediaTypes,ClientCookieExpiredError, ClientLoginRequiredError,__version__ as client_version
from instagram_web_api import Client as WebClient

def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))

class Finder(object):
    def __init__(self,id):
        self.__getMyWebAPI()#в конструкторе сразу получим доступ к апи и доступ к айд отслеживаемого пользователя
        self.webClient=WebClient(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
        time.sleep(0.2)
        self.userId=id
    def __getMyWebAPI(self):
        logging.basicConfig()
        logger = logging.getLogger('instagram_private_api')
        logger.setLevel(logging.WARNING)
        password='Djljrfyfk48'
        login='vodok2020'
        fil='loginset.json'
        print('Client version: {0!s}'.format(client_version))

        device_id = None
        try:

            settings_file = fil
            if not os.path.isfile(settings_file):
                # settings file does not exist
                print('Unable to find file: {0!s}'.format(settings_file))

                # login new
                self.myWebAPI = Client(
                login, password,
                on_login=lambda x: onlogin_callback(x, fil))
            else:
                with open(settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook=from_json)
                print('Reusing settings: {0!s}'.format(settings_file))

                device_id = cached_settings.get('device_id')
                # reuse auth settings
                self.myWebAPI = Client(
                login, password,
                settings=cached_settings)

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
            self.myWebAPI = Client(
                login, password,
                device_id=device_id,
                on_login=lambda x: onlogin_callback(x, fil))

        except ClientLoginError as e:
            print('ClientLoginError {0!s}'.format(e))
            exit(9)
        except ClientError as e:
            print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
            exit(9)
        except Exception as e:
            print('Unexpected Exception: {0!s}'.format(e))
            exit(99)

         # Show when login expires
        cookie_expiry = self.myWebAPI.cookie_jar.auth_expires
        print('Cookie Expiry: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))
        ############
    def findFeed(self,next):
        if next!=-1 and next!=-2: 
            feed = self.myWebAPI.user_feed(self.userId,max_id=next)
            time.sleep(0.2)
        else:
            feed = self.myWebAPI.user_feed(self.userId)
            time.sleep(0.2)
        return feed['items'],feed.get('next_max_id',-2)
    def findComments(self,media_id,next):
        if next!=-1 and next!=-2: 
            comments = self.myWebAPI.media_comments(media_id,max_id=next)
            time.sleep(0.2)
        else:
            comments = self.myWebAPI.media_comments(media_id)
            time.sleep(0.2)
        return comments['comments'],comments.get('next_max_id',-2)
    def takeCommentsWithoutCircle(self,media_id,comment_count):
        comments = self.myWebAPI.media_n_comments(media_id,n=comment_count,reverse=True)
        time.sleep(0.2)
        return comments
    def findNewFeed(self):
        feed = self.myWebAPI.user_feed(self.userId)
        time.sleep(0.2)
        return feed['items']
    def findIGTV(self):
        igtv=self.webClient.user_info2('igor_artamonov48')
        time.sleep(0.2)
        return igtv['edge_felix_video_timeline']['edges']
