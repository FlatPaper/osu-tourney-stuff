import os, requests, time, json
from dotenv import load_dotenv

load_dotenv()
api_key = str(os.getenv("OSU_API_KEY"))


class Osu:
    USER_URL = "https://osu.ppy.sh/api/get_user"
    MULTI_URL = "https://osu.ppy.sh/api/get_match"
    MAP_URL = "https://osu.ppy.sh/api/get_beatmaps"
    REQUEST_DELAY = 0.7

    @staticmethod
    def request(url, args):
        ret = requests.get(url, args)
        time.sleep(Osu.REQUEST_DELAY)
        return ret

    @staticmethod
    def get_user_info(username="", user_id=0):
        if len(username)==0 and user_id==0:
            return "Error"
        if user_id == 0:
            username = str(username).strip()
            param = {'k': api_key, 'u': username, 'm': 0, 'type': 'string'}
            r = Osu.request(Osu.USER_URL, param)
            data = r.json()
            data = json.dumps(data)
            data = json.loads(data)
            return data[0]
        if len(username) == 0:
            user_id = str(user_id).strip()
            param = {'k': api_key, 'u': user_id, 'm': 0, 'type': 'id'}
            r = Osu.request(Osu.USER_URL, param)
            data = r.json()
            data = json.dumps(data)
            data = json.loads(data)
            return data[0]

    @staticmethod
    def get_match_info(match_id):
        match_id = str(match_id).strip()
        param = {'k': api_key, 'mp': match_id}
        r = Osu.request(Osu.MULTI_URL, param)
        data = r.json()
        data = json.dumps(data)
        data = json.loads(data)
        return data

    @staticmethod
    def get_beatmap_info(map_id):
        map_id = str(map_id).strip()
        param = {'k': api_key, 'b': map_id}
        r = Osu.request(Osu.MAP_URL, param)
        data = r.json()
        data = json.dumps(data)
        data = json.loads(data)
        return data[0]

