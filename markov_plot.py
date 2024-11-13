import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = 'random_stock.xlsx'
data = pd.read_excel(file_path)

def classify_state(change):
    if change > 1:
        return 'Bullish'
    elif change < -1:
        return 'Bearish'
    else:
        return 'Stagnant'

data['State'] = data['Change(%)'].apply(classify_state)

transition_counts = {
    'Bullish': {'Bullish': 0.53, 'Bearish': 0.29, 'Stagnant': 0.18},
    'Bearish': {'Bullish': 0.31, 'Bearish': 0.54, 'Stagnant': 0.15},
    'Stagnant': {'Bullish': 0.12, 'Bearish': 0.75, 'Stagnant': 0.13}
}

weeks = len(data)
probabilities = {'Bullish': [], 'Bearish': [], 'Stagnant': []}

# setting Bullish to 1 and others to 0 at Week 0
initial_probs = {'Bullish': 1.0, 'Bearish': 0.0, 'Stagnant': 0.0}
current_probs = initial_probs.copy()

for week in range(weeks):
    probabilities['Bullish'].append(current_probs['Bullish'])
    probabilities['Bearish'].append(current_probs['Bearish'])
    probabilities['Stagnant'].append(current_probs['Stagnant'])

    new_probs = {
        state: sum(current_probs[prev_state] * transition_counts[prev_state][state]
                   for prev_state in transition_counts)
        for state in transition_counts
    }
    current_probs = new_probs

# Plotting the results
plt.figure(figsize=(8, 6))
plt.plot(range(weeks), probabilities['Bullish'], label='Bullish', color='blue')
plt.plot(range(weeks), probabilities['Bearish'], label='Bearish', color='red')
plt.plot(range(weeks), probabilities['Stagnant'], label='Stagnant', color='black')

# Burn-in line at Week 15
burn_in_week = 15
plt.axvline(x=burn_in_week, color='green', linestyle='--', label='Burn In')

plt.xlim(0, weeks - 1)
plt.ylim(0, 1)
plt.xlabel("Week")
plt.ylabel("p(Market State)")
plt.legend()
plt.tight_layout()
plt.show()
