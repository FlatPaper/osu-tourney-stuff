import os, requests, json, time

from dotenv import load_dotenv
load_dotenv()

apiKey = str(os.getenv("OSU_API_KEY"))


class RelativeRanking:
    USER_URL = "https://osu.ppy.sh/api/get_user"
    MULTI_URL = "https://osu.ppy.sh/api/get_match"
    REQUEST_DELAY = 0.7

    def __init__(self, links):
        self.links = links

    def request(self, url, args):
        """
        :param url: the API base link in a string
        :param args: a dictionary to handle parameters for the url
        :return: an API object - see https://requests.readthedocs.io/en/master/
        """
        ret = requests.get(url, args)
        time.sleep(self.REQUEST_DELAY)
        return ret

    def username_to_id(self, username):
        """
        :param username: a string input that is a valid osu! username
        :return: a string - the accompanying user id
        """
        username = str(username).strip()
        param = {'k': apiKey, 'u': username, 'm': 0, 'type': 'string'}
        r = self.request(self.USER_URL, param)
        data = r.json()
        data = json.dumps(data)
        data = json.loads(data)
        return data[0]['user_id']

    def id_to_username(self, user_id):
        """
        :param user_id: a string input that is a valid osu! ID
        :return: a string - the accompanying username
        """
        user_id = str(user_id).strip()
        param = {'k': apiKey, 'u': user_id, 'm': 0, 'type': 'id'}
        r = self.request(self.USER_URL, param)
        data = r.json()
        data = json.dumps(data)
        data = json.loads(data)
        return data[0]['username']

    def get_match_info(self, match_id):
        """
        :param match_id: a string input that is a valid multi link
        :return: a dictionary containing match information
        """
        match_id = str(match_id).strip()
        param = {'k': apiKey, 'mp': match_id}
        r = self.request(self.MULTI_URL, param)
        data = r.json()
        data = json.dumps(data)
        data = json.loads(data)
        return data
