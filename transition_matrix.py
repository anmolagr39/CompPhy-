import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Read the existing random stock data from Excel
file_path = 'random_stock.xlsx'
df = pd.read_excel(file_path)

bullish_threshold = 1.0  
bearish_threshold = -1.0  
df['State'] = df['Change(%)'].apply(lambda x: 'Bullish' 
    if x > bullish_threshold 
    else ('Bearish' if x < bearish_threshold else 'Stagnant'))

states_list = ['Bullish', 'Bearish', 'Stagnant']
transition_matrix = {state: {s: 0 for s in states_list} for state in states_list}

for i in range(1, len(df)):
    prev_state = df.iloc[i-1]['State']
    current_state = df.iloc[i]['State']
    transition_matrix[prev_state][current_state] += 1

print("Transition Matrix (Counts):")
for state in transition_matrix:
    print(f"{state}: {transition_matrix[state]}")

for state in transition_matrix:
    total_transitions = sum(transition_matrix[state].values())
    if total_transitions > 0:
        for next_state in transition_matrix[state]:
            transition_matrix[state][next_state] /= total_transitions

print("\nTransition Matrix (Probabilities):")
for state in transition_matrix:
    print(f"{state}: {transition_matrix[state]}")

