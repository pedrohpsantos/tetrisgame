import json


class RankingManager:
    def __init__(self, file_path="ranking.json"):
        self.file_path = file_path
        self.rankings = self.load_rankings()

    def load_rankings(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_rankings(self):
        with open(self.file_path, "w") as file:
            json.dump(self.rankings, file, indent=4)

    def add_score(self, name, score):
        self.rankings.append({"name": name, "score": score})
        self.rankings.sort(key=lambda x: x["score"], reverse=True)
        self.rankings = self.rankings[:10]
        self.save_rankings()

    def display_rankings(self):
        print("\n--- Rankings ---")
        for idx, entry in enumerate(self.rankings, start=1):
            print(f"{idx}. {entry['name']}: {entry['score']}")
        print("----------------\n")
