import json, csv
from Osu import Osu

class RelativeRanking:
    player_index = {}
    map_scores = {}
    sorted_map_scores = {}
    modIdx = {}
    result = {}
    player_count = []
    map_count = 0
    player_list = []

    def __init__(self, message):
        self.message = message
        print("Initialized")

    @staticmethod
    def username_to_id(username):
        user_info = Osu.get_user_info(username=username)
        return user_info['user_id']

    @staticmethod
    def id_to_username(user_id):
        user_info = Osu.get_user_info(user_id=user_id)
        return user_info['username']

    def organize_match_info(self, multi_link):
        """
        Finds out the sorted map scores in self.sorted_map_scores
        :param multi_link: link to the lobby
        :return: nothing
        """
        match_id = str(multi_link).strip().split("/")[-1]
        print("Processing", match_id, "...")

        match_info = Osu.get_match_info(match_id)

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
                    self.player_index[user_id] = RelativeRanking.id_to_username(user_id)

                # skip this user if we don't want to track him, if we are tracking people
                user = self.player_index[user_id]
                if user not in self.player_list and len(self.player_list) != 0:
                    continue

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

    def track_user(self):
        with open('track_users.txt', 'r') as f:
            for line in f:
                self.player_list.append(line.strip())
        print(self.player_list)

    def get_scores(self):
        return self.sorted_map_scores

    def clear_all(self):
        self.sorted_map_scores.clear()
        self.map_scores.clear()
        self.player_index.clear()
        self.modIdx.clear()
        self.result.clear()
        self.player_list.clear()

    def extract_to_csv(self):
        with open('maps.csv', 'w') as f:
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(cnt for cnt in self.player_count)

            for map_name in self.result:
                f.write('"{}"'.format(map_name) + "\n")
                if self.result[map_name] == "Map was not played.":
                    writer.writerow(" ")
                else:
                    for row in self.result[map_name].items():
                        writer.writerow(row)
                    writer.writerow(" ")
            f.close()

    async def run(self):
        self.organize_map_info()
        self.track_user()
        message = self.message.content.strip().split()
        for i in range(self.map_count+7, len(message)):
            match_id = message[i]
            await self.message.channel.send("Processing {}...".format(match_id))
            self.organize_match_info(match_id)

        for mod, map_id in self.modIdx.items():
            map_info = Osu.get_beatmap_info(map_id)
            name = str(mod) + ": " + map_info["artist"] +  " - " + map_info["title"] + " [" + map_info["version"] + "]"
            if str(map_id) not in self.sorted_map_scores:
                self.player_count.append(0)
                self.result[name] = "Map was not played."
            else:
                self.result[name] = self.sorted_map_scores[str(map_id)]
                self.player_count.append(len(self.result[name]))

        self.extract_to_csv()

        print("Completed!")
        await self.message.channel.send("Completed!")

        self.clear_all()
