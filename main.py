import numpy as np
import pandas as pd
import time

from BankPlan import BankPlan
from check_solution import *
from Brotherhood import Brotherhood


def path_to_solution(path):
    # Remove first entry (0), reverse the path and decrease index by 1.
    return np.array(path[1:][::-1], dtype=np.int64) - 1


if __name__ == "__main__":
    time_to_run = 3*60

    start_time = time.time()
    df = pd.read_csv("bank_data.csv")

    bank_plan = BankPlan(df.copy())

    robbers = Brotherhood(
        graph=bank_plan.get_graph(),
        budget=24,
        treasures=bank_plan.get_treasures(),
        number_robbers=10,
        evaporation_rate=0.05,
        alpha=0.5,
        randomness_rate=0.1,
        gamma_parameters={"shape": 2.0, "scale": 2.0}
    )

    i = 0
    while time.time() - start_time < time_to_run:
        i += 1
        robbers.generation()
        score = check_solution(path_to_solution(robbers.hall_of_fame[1]), df, verbose=0)
        print(f"Generation #{i}: {score} after {int(time.time() - start_time)}s")

    print("\nFinal Result")
    print(check_solution(path_to_solution(robbers.hall_of_fame[1]), df))
