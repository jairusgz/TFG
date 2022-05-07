import pandas as pd
import numpy as np
import os


class LeaderboardManager:
    def __init__(self):
        self._leaderboard_path = '../Data/high_scores.csv'
        self._high_scores = self.read_high_scores()
        self.read_high_scores()

    def write_high_scores(self, player_name, player_score):
        self._high_scores = self._high_scores.append({'Player_name': player_name, 'Score': player_score},
                                                     ignore_index=True)
        top_10 = self._high_scores.sort_values(by=['Score'], ascending=False)[:3]
        top_10.to_csv(self._leaderboard_path, index=False)

    def read_high_scores(self):
        return pd.read_csv(self._leaderboard_path)
