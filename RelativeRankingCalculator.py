import os, requests, json, time

from dotenv import load_dotenv
load_dotenv()

apiKey = str(os.getenv("OSU_API_KEY"))


class RelativeRanking:
    USER_URL = "https://osu.ppy.sh/api/get_user"
    MULTI_URL = "https://osu.ppy.sh/api/get_match"
    REQUEST_DELAY = 0.7
    player_index = {}
    map_scores = {}
    sorted_map_scores = {}

    def __init__(self):
        print("Initialized")

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

    def organize_match_info(self, multi_link):
        """
        :param multi_link: link to the lobby
        :return: absolutely nothing yet
        """
        match_id = str(multi_link).strip().split("/")[-1]
        print("Processing", match_id, "...")

        match_info = self.get_match_info(match_id)

        for game in match_info['games']:
            beatmap_id = game['beatmap_id']
            if beatmap_id not in self.map_scores:
                self.map_scores[beatmap_id] = {}

            for score in game['scores']:
                # skip this user if his score is sub 150 (probably a referee)
                if int(score['score']) < 150:
                    continue

                # index player id's
                user_id = str(score['user_id'])
                if user_id not in self.player_index:
                    self.player_index[user_id] = self.id_to_username(user_id)

                user = self.player_index[user_id]
                if user_id not in self.map_scores[beatmap_id]:
                    self.map_scores[beatmap_id][user] = int(score['score'])
                else:
                    self.map_scores[beatmap_id][user] = max(self.map_scores[beatmap_id][user], int(score['score']))

        for map_score in self.map_scores:
            map_idx = {}
            scores = []
            for user, score in self.map_scores[map_score].items():
                scores.append(score)
                map_idx[score] = user

            scores = sorted(scores, reverse=True)

            self.sorted_map_scores[map_score] = {}
            for x in scores:
                self.sorted_map_scores[map_score][map_idx[x]] = x

    def get_scores(self):
        return self.sorted_map_scores

    def clear_all(self):
        self.sorted_map_scores.clear()
        self.map_scores.clear()
        self.player_index.clear()
