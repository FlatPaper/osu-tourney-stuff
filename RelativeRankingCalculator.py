import os, requests, json, time, discord

from dotenv import load_dotenv
load_dotenv()

apiKey = str(os.getenv("OSU_API_KEY"))


class RelativeRanking:
    USER_URL = "https://osu.ppy.sh/api/get_user"
    MULTI_URL = "https://osu.ppy.sh/api/get_match"
    MAP_URL = "https://osu.ppy.sh/api/get_beatmaps"
    REQUEST_DELAY = 0.7
    player_index = {}
    map_scores = {}
    sorted_map_scores = {}
    modIdx = {}
    result = {}
    map_count = 0

    def __init__(self, message):
        self.message = message
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

    def get_beatmap_info(self, map_id):
        map_id = str(map_id).strip()
        param = {'k': apiKey, 'b': map_id}
        r = self.request(self.MAP_URL, param)
        data = r.json()
        data = json.dumps(data)
        data = json.loads(data)
        return data[0]

    def organize_match_info(self, multi_link):
        """
        Finds out the sorted map scores in self.sorted_map_scores
        :param multi_link: link to the lobby
        :return: nothing
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

    def organize_map_info(self):
        message = self.message.content.strip().split()

        nomod_count = int(message[1])
        hidden_count = int(message[2])
        hard_rock_count = int(message[3])
        double_time_count = int(message[4])
        free_mod_count = int(message[5])
        tiebreaker_count = int(message[6])

        self.map_count = nomod_count + hidden_count + hard_rock_count + double_time_count + free_mod_count + tiebreaker_count

        for i in range(nomod_count):
            self.modIdx["NM" + str(i+1)] = message[i+7]
        for i in range(hidden_count):
            self.modIdx["HD" + str(i+1)] = message[i+7+nomod_count]
        for i in range(hard_rock_count):
            self.modIdx["HR" + str(i + 1)] = message[i + 7 + nomod_count + hidden_count]
        for i in range(double_time_count):
            self.modIdx["DT" + str(i + 1)] = message[i + 7 + nomod_count + hidden_count + hard_rock_count]
        for i in range(free_mod_count):
            self.modIdx["FM" + str(i + 1)] = message[i + 7 + nomod_count + hidden_count + hard_rock_count +
                                                  double_time_count]
        for i in range(tiebreaker_count):
            self.modIdx["TB" + str(i + 1)] = message[i + 7 + nomod_count + hidden_count + hard_rock_count +
                                                  double_time_count + free_mod_count]

    def get_scores(self):
        return self.sorted_map_scores

    def clear_all(self):
        self.sorted_map_scores.clear()
        self.map_scores.clear()
        self.player_index.clear()
        self.modIdx.clear()
        self.result.clear()

    async def run(self):
        self.organize_map_info()
        message = self.message.content.strip().split()
        for i in range(self.map_count+7, len(message)):
            match_id = message[i]
            await self.message.channel.send("Processing {}...".format(match_id))
            self.organize_match_info(match_id)

        for mod, map_id in self.modIdx.items():
            map_info = self.get_beatmap_info(map_id)
            name = str(mod) + ": " + map_info["artist"] +  " - " + map_info["title"] + " [" + map_info["version"] + "]"
            if str(map_id) not in self.sorted_map_scores:
                self.result[name] = "Map was not played."
            else:
                self.result[name] = self.sorted_map_scores[str(map_id)]

        print(json.dumps(self.result, indent=4))

        self.clear_all()
