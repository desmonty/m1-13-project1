import numpy as np
import pandas as pd


class BankPlan(object):
    """docstring for BankPlanGenerator"""

    def __init__(self, df: pd.DataFrame, speed: float = 30.0):
        """
        speed is in km/h
        Unit for '{x,y}_coordinate' in df is kilometer
        Unit for time in 'time (hr)' in df is hour
        """
        super(BankPlan, self).__init__()

        assert np.abs(speed) > 1e-8, "'speed' too close to zero"

        # We add a row at the beginning of the dataframe.
        # It will be used as our starting point for the search.
        # This point is situated in (0, 0) and its reward is
        # freedom.
        helipad = pd.DataFrame({
            "id": 0,
            "x_coordinate": 0,
            "y_coordinate": 0,
            "money": 0,
            "time (hr)": 0
        }, index=[0])
        self.df = pd.concat([helipad, df]).reset_index(drop=True)
        self.df["id"] = self.df.index

        self.speed = speed
        self.graph = self.construct_graph()

    def construct_graph(self):
        """
        This function construct a graph based on the provided
        dataframe. [i, j] is the time taken to go from i to j
        at {speed}km/h AND robbing bank[j] which is described
        in cell df[j, "time (hr)"].
        """
        x_mat = self.repeated_matrix(self.df['x_coordinate'])
        y_mat = self.repeated_matrix(self.df['y_coordinate'])

        dist_mat = np.sqrt(
            np.power((x_mat - x_mat.T), 2.0) + np.power((y_mat - y_mat.T), 2.0)
        )
        dist_time_mat = dist_mat / self.speed

        # Take transpose so that [i, j] include robbery time of j
        robbery_time_mat = self.repeated_matrix(self.df['time (hr)']).T
        # [i, i] is zero for all i
        robbery_time_mat -= np.diag(self.df['time (hr)'])

        return dist_time_mat + robbery_time_mat

    def repeated_matrix(self, column):
        """
        Take a DataFrame column and return a square matrix
        with the column repeated.
        E.G.
        column = [1, 2, 3]
        return:
        np.array(
            [[1, 1, 1]
             [2, 2, 2]
             [3, 3, 3]]
        )
        """
        return np.reshape(
            np.repeat(np.array(column), len(self.df)),
            (len(self.df), len(self.df))
        )

    def get_treasures(self):
        return self.df["money"] / max(self.df["money"])

    def get_graph(self):
        return self.graph
