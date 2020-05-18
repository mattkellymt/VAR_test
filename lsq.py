from scipy.linalg import lstsq
import numpy as np
import random
import matplotlib.pyplot as plt 
import math 
import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import minmax_scale

length = 100
# Number of coefficients I will artifically introduce into both the "pm" and "emotion" series
coef_len = 10 

# Noise is just a starting point for the first lags equal to the number of coefficients
noise = np.array([random.gauss(0, 0.1) for i in range(length)])

# X-axis
x_list = np.linspace(0, length - 1, length)

pm = noise.copy()
pm_pm_coef = np.array([math.sin(i / 10) - 1 for i in range(coef_len)])

# Apply lags for PM
for i in range(coef_len, len(pm)):
    last_pm = pm[i - coef_len: i]

    next_pm = sum(last_pm * pm_pm_coef) + random.gauss(0, 1)
    pm[i] = next_pm

emotion = noise.copy()
e_pm_coeff = np.array([-i / 10 for i in range(coef_len)])
e_e_coeff = np.array([i / 10 for i in range(coef_len)])

# Apply lags for the emotion series
for i in range(coef_len, len(emotion)):
    last_pm = pm[i - coef_len: i]
    last_e = emotion[i - coef_len: i]

    next_e = sum(last_pm * e_pm_coeff + last_e * e_e_coeff) + random.gauss(0, 1)

# Remove the starting values which came from the noise series
pm = pm[coef_len:]
emotion = emotion[coef_len:]
x_list = x_list[coef_len:]

# This function finds coefficients, makes a prediction for the next day, feeds that prediction back into the series, and repeats moving 1 day forward now using the prediction as the last element. 
def test(x_list, pm, emotion, title=""):
    # "Model_lag_len" is the number of lags for each independent variable.
    model_lag_len = 3

    # The number of unknowns is (the number of independent variables) * (the number of lags) + (1 for the dependent variable).
    num_unknowns = model_lag_len * 2 + 1

    # Increasing "train_len" will transition from overfit to underfit as the linear regression fits more of the non-linear data.
    train_len = 14
    train_len = max(train_len, num_unknowns + 1)
    test_len = 14

    # Predict
    emotion_copy = emotion.copy()
    pm_copy = pm.copy()
    for i in range(test_len):
        test_e = []
        test_pm = []

        for lag in range(1, model_lag_len + 1):
            start = -train_len - test_len - lag + i
            end = start + train_len

            lagged_e = emotion_copy[start: end]
            lagged_pm = pm_copy[start:end]

            test_e.append(lagged_e)
            test_pm.append(lagged_pm)

        # Train
        constant = [np.ones(train_len)]
        columns = constant + test_e + test_pm

        train_x = np.column_stack(columns)
        train_y = emotion_copy[-train_len - test_len + i: -test_len + i]

        model = sm.OLS(train_y, train_x)
        result = model.fit()

        # Test and feed the prediction back into the series for the next iteration
        constant = [np.ones(train_len)]
        columns = constant + test_e + test_pm
        test_x = np.column_stack(columns)

        test_y = emotion_copy[-train_len - test_len + i + 1: -test_len + i + 1]
        prediction = result.predict(test_x)

        emotion_copy[-test_len + i + 1] = prediction[-1]

    # Plotting
    fig, ax1 = plt.subplots()
    ax1.plot(x_list[-test_len * 2:], pm[-test_len * 2:], label="PM", color="red")
    ax1.set_ylabel("PM", color="red")
    ax1.tick_params(axis="y", color="red")

    ax2 = ax1.twinx()
    ax2.plot(x_list[-test_len * 2:], emotion[-test_len * 2:], label="Actual", color="blue")
    ax2.set_ylabel("Sentiment")
    ax2.tick_params(axis="y", color="red")

    ax2.plot(x_list[-test_len * 2:], emotion_copy[-test_len * 2:], label="Predicted", color="black")
    ax2.legend()
    plt.title(title)
    plt.show()

def normalize(values, min_value=1, max_value=100):
    feature_range = min_value, max_value
    normalized = minmax_scale(values, feature_range=feature_range, copy=True)
    return normalized

def difference(values):
    differenced = pd.DataFrame(values).diff()[0].values
    return differenced

emotion = normalize(emotion)
pm = normalize(pm)
test(x_list, pm, emotion, "Normalized")

emotion = difference(emotion)
pm = difference(pm)
test(x_list, pm, emotion, "Differenced")
