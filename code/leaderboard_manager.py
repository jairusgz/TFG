import pandas as pd


class LeaderboardManager:
    _leaderboard_path = 'tfg/Data/high_scores.csv'

    @classmethod
    def write_high_scores(cls, player_name, player_score):
        scores = LeaderboardManager.read_high_scores()
        scores = scores.append({'Player_name': player_name, 'Score': player_score}, ignore_index=True)
        top = scores.sort_values(by=['Score'], ascending=False)[:3]
        top.to_csv(LeaderboardManager._leaderboard_path, index=False)

    @classmethod
    def read_high_scores(cls):
        return pd.read_csv(LeaderboardManager._leaderboard_path)
