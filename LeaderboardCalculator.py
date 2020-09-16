import csv

class ModLeaderboardCalculator:

    results = {}
    sorted_mod_lb = {}
    player_count = []
    mod_lb = {"NM": {}, "HD": {}, "HR": {}, "DT": {}, "FM": {}, "TB": {}}
    total_lb = {}

    def __init__(self, results):
        self.results = results

    def calc_mod_lb(self):
        self.sorted_mod_lb.clear()
        self.player_count.clear()

        print(self.results)

        for map_name in self.results:
            for player, score in self.results[map_name].items():
                if str(map_name).startswith("NM"):
                    if player not in self.mod_lb["NM"]:
                        self.mod_lb["NM"][player] = score
                    else:
                        self.mod_lb["NM"][player] += score
                if str(map_name).startswith("HD"):
                    if player not in self.mod_lb["HD"]:
                        self.mod_lb["HD"][player] = score
                    else:
                        self.mod_lb["HD"][player] += score
                if str(map_name).startswith("HR"):
                    if player not in self.mod_lb["HR"]:
                        self.mod_lb["HR"][player] = score
                    else:
                        self.mod_lb["HR"][player] += score
                if str(map_name).startswith("DT"):
                    if player not in self.mod_lb["DT"]:
                        self.mod_lb["DT"][player] = score
                    else:
                        self.mod_lb["DT"][player] += score
                if str(map_name).startswith("FM"):
                    if player not in self.mod_lb["FM"]:
                        self.mod_lb["FM"][player] = score
                    else:
                        self.mod_lb["FM"][player] += score
                if str(map_name).startswith("TB"):
                    if player not in self.mod_lb["TB"]:
                        self.mod_lb["TB"][player] = score
                    else:
                        self.mod_lb["TB"][player] += score

        for map_score in self.mod_lb:
            self.player_count.append(len(self.mod_lb[map_score]))
            map_idx = {}
            scores = []
            for user, score in self.mod_lb[map_score].items():
                scores.append(score)
                map_idx[score] = user

            scores = sorted(scores, reverse=True)

            self.sorted_mod_lb[map_score] = {}
            for x in scores:
                self.sorted_mod_lb[map_score][map_idx[x]] = x

        for map_name in self.results:
            for player, score in self.results[map_name].items():
                if str(map_name).startswith("NM"):
                    if player not in self.total_lb:
                        self.total_lb[player] = score
                    else:
                        self.total_lb[player] += score
                if str(map_name).startswith("HD"):
                    if player not in self.total_lb:
                        self.total_lb[player] = score
                    else:
                        self.total_lb[player] += score
                if str(map_name).startswith("HR"):
                    if player not in self.total_lb:
                        self.total_lb[player] = score
                    else:
                        self.total_lb[player] += score
                if str(map_name).startswith("DT"):
                    if player not in self.total_lb:
                        self.total_lb[player] = score
                    else:
                        self.total_lb[player] += score
                if str(map_name).startswith("FM"):
                    if player not in self.total_lb:
                        self.total_lb[player] = score
                    else:
                        self.total_lb[player] += score
                if str(map_name).startswith("TB"):
                    if player not in self.total_lb:
                        self.total_lb[player] = score
                    else:
                        self.total_lb[player] += score

        print(self.total_lb)
        sort_lb = sorted(self.total_lb.items(), key = lambda x : x[1], reverse=True)
        self.total_lb = dict(sort_lb)



    def extract_to_csv(self):
        with open('mod_lb.csv', 'w') as f:
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(cnt for cnt in self.player_count)

            for map_name in self.sorted_mod_lb:
                f.write('"{}"'.format(map_name) + "\n")
                for row in self.sorted_mod_lb[map_name].items():
                    writer.writerow(row)
                writer.writerow(" ")
            f.close()

        with open('final_lb.csv', 'w') as f:
            f.truncate()
            writer = csv.writer(f)
            for row in self.total_lb.items():
                writer.writerow(row)
            f.close()


