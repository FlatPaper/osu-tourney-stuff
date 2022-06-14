import json
import os

from Osu import Osu

# Code calculates qualifier results for hkttycup2 (finds best OVERALL team score, not best individual performance)
class Teams:
    username_to_team = {}
    id_to_username = {}

    def __init__(self, teams_file: str):
        self.teams_file = teams_file

    def import_info(self):
        with open(self.teams_file, encoding='utf-8') as f:
            for line in f:
                team_info = line.strip().split('\t')
                player_id = team_info[0]
                player_username = team_info[1]
                player_team = team_info[2]

                self.id_to_username[player_id] = player_username
                self.username_to_team[player_username] = player_team
        f.close()

        with open("players.json", "w", encoding='utf-8') as f:
            f.write(json.dumps(self.id_to_username, indent=4))
        f.close()

        with open("teams.json", "w", encoding='utf-8') as f:
            f.write(json.dumps(self.username_to_team, indent=4))
        f.close()


class LobbyParser:

    maps = {
        "759316": "NM1",
        "2219575": "NM2",
        "3011729": "HD1",
        "2944309": "HD2",
        "2981393": "HR1",
        "122042": "HR2",
        "3631489": "DT1",
        "2042814": "DT2"
    }

    team_map_scores = {
        "NM1": {},
        "NM2": {},
        "HD1": {},
        "HD2": {},
        "HR1": {},
        "HR2": {},
        "DT1": {},
        "DT2": {}
    }

    user_map_scores = {
        "NM1": {},
        "NM2": {},
        "HD1": {},
        "HD2": {},
        "HR1": {},
        "HR2": {},
        "DT1": {},
        "DT2": {}
    }

    def __init__(self):
        print("Starting...")

    def parse_singe_lobby(self, multi_id, teams: Teams):
        multi_info = Osu.get_match_info(multi_id)

        for game in multi_info['games']:
            beatmap_id = game['beatmap_id']

            # edge case if the beatmap played is not from the pool
            if beatmap_id not in self.maps.keys():
                continue

            map_mod = self.maps[beatmap_id]

            team_temp_scores = {}
            user_temp_scores = {}

            for score in game['scores']:
                user_id = score["user_id"]
                user_score = int(score["score"])

                username = teams.id_to_username[user_id]
                team = teams.username_to_team[username]

                print(f'{user_id} {user_score} {username} {team}')

                if team not in team_temp_scores:
                    team_temp_scores[team] = user_score
                else:
                    team_temp_scores[team] += user_score

                user_temp_scores[username] = user_score

            for team, score in team_temp_scores.items():
                if team not in self.team_map_scores[map_mod]:
                    self.team_map_scores[map_mod][team] = score
                elif score > self.team_map_scores[map_mod][team]:
                    self.team_map_scores[map_mod][team] = score
                    overwrite = True

        self.team_map_scores["NM1"] = {k: v for k, v in sorted(self.team_map_scores["NM1"].items(), key=lambda item: item[1], reverse=True)}
        self.team_map_scores["NM2"] = {k: v for k, v in sorted(self.team_map_scores["NM2"].items(), key=lambda item: item[1], reverse=True)}
        self.team_map_scores["HD1"] = {k: v for k, v in sorted(self.team_map_scores["HD1"].items(), key=lambda item: item[1], reverse=True)}
        self.team_map_scores["HD2"] = {k: v for k, v in sorted(self.team_map_scores["HD2"].items(), key=lambda item: item[1], reverse=True)}
        self.team_map_scores["HR1"] = {k: v for k, v in sorted(self.team_map_scores["HR1"].items(), key=lambda item: item[1], reverse=True)}
        self.team_map_scores["HR2"] = {k: v for k, v in sorted(self.team_map_scores["HR2"].items(), key=lambda item: item[1], reverse=True)}
        self.team_map_scores["DT1"] = {k: v for k, v in sorted(self.team_map_scores["DT1"].items(), key=lambda item: item[1], reverse=True)}
        self.team_map_scores["DT2"] = {k: v for k, v in sorted(self.team_map_scores["DT2"].items(), key=lambda item: item[1], reverse=True)}

        with open("scores.json", "w", encoding='utf-8') as f:
            f.write(json.dumps(self.team_map_scores, indent=4))
        f.close()


x = Teams("teams.txt")
x.import_info()

with open('lobbies.txt', 'r') as f:
    data = f.readlines()
    data = [x.strip().split("/")[-1] for x in data]
    y = LobbyParser()
    for multi_id in data:
        y.parse_singe_lobby(multi_id, x)

    with open('scores.json', 'r', encoding='utf-8') as json_file:
        scores = json.load(json_file)
        team_order_file = open('score_calc_teams.txt', 'r')
        team_order = team_order_file.readlines()

        with open('sheets_output.txt', 'w', encoding='utf-8') as output:
            for team in team_order:
                team = team.strip()
                if team not in scores["NM1"]:
                    print(team)
                    output.write('\n')
                    continue
                nm1_score = scores["NM1"][team]
                nm2_score = scores["NM2"][team]
                hd1_score = scores["HD1"][team]
                hd2_score = scores["HD2"][team]
                hr1_score = scores["HR1"][team]
                hr2_score = scores["HR2"][team]
                dt1_score = scores["DT1"][team]
                dt2_score = scores["DT2"][team]
                final = f"{nm1_score}\t{nm2_score}\t{hd1_score}\t{hd2_score}\t{hr1_score}\t{hr2_score}\t{dt1_score}\t{dt2_score}\n"
                output.write(final)
        output.close()
    json_file.close()
f.close()
