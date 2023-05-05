import numpy as np
from numpy import random
import pandas as pd
import matplotlib.pyplot as plt
# This split's scores before Finals
scores_current = {
    "xset": 112,
    "optic": 106,
    "furia": 97,
    "dark zero": 89,
    "glytch energy": 84,
    "faze": 81,
    "100 thieves": 80,
    "tsm": 78,
    "luminosity": 72,
    "meat lovers": 72,
    "wildcard": 71,
    "nrg": 71,
    "complexity": 70,
    "lanimals": 68,
    "oxygen": 60,
    "clg": 59,
    "sentinels": 57,
    "e8": 50,
    "native": 49,
    "drug free": 48
}

# Last split's scores before finals
scores_old = {
    "tsm": 113,
    "tl": 102,
    "tgrd": 95,
    "lg": 93,
    "ssg": 85,
    "100t": 84,
    "fur": 82,
    "nrg": 81,
    "hec": 81,
    "esa": 80,
    "col": 75,
    "mps": 75,
    "dz": 72,
    "szn": 67,
    "og": 65,
    "g2": 62,
    "brd": 60,
    "trp": 53,
    "clg": 49,
    "faze": 46
}

## SIMULATION PARAMETERS ##
scores = scores_current
reroll_bottom_x_wins = 5
reroll_bottom_x_second = 0
reroll_bottom_x_top5 = 0
reroll_bottom_x_top10 = 0
cutoff_place = 11
iters = 10000

points = [25,21,18,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
cutoffs = []
quals = {key: 0 for key in scores.keys()}

for i in range(iters):
    scores2 = scores.copy()
    reroll = True
    # Reroll "unlikely" outcomes based on the simulation "reroll_bottom_x" parameters set above
    while(reroll):
        reroll = False
        # Generate random Finals results
        results = random.permutation(list(scores2.keys()))
        for team in list(scores.keys())[20-reroll_bottom_x_wins:20]:
            if team == results[0]:
                reroll = True
        for team in list(scores.keys())[20-reroll_bottom_x_second:20]:
            if team == results[1]:
                reroll = True
        for team in list(scores.keys())[20-reroll_bottom_x_top5:20]:
            if team in results[0:5]:
                reroll = True
        for team in list(scores.keys())[20-reroll_bottom_x_top10:20]:
            if team in results[0:10]:
                reroll = True

    # Update scores based on results generated above
    for i in range(20):
        scores2[results[i]] += points[i]
    
    # Sort the scores dictionary for easier printing later on
    res = {key: val for key, val in sorted(scores2.items(), key = lambda ele: ele[1])}

    # Increase the total number of simulated qualifications for every qualified team
    for j in range(cutoff_place):
        quals[list(res.keys())[19-j]]+=1

    # Save the qualification cutoff score for use later
    cutoffs.append(list(res.values())[9])

# Convert qualification numbers to qualification percentage
for team in quals.keys():
    quals[team]/=(iters / 100)

# Convert dictionary to Pandas dataframe to make the formatting prettier when printed.
qualtable = pd.DataFrame(quals.items(), columns = ["Team","Chance"])
qualtable.index = qualtable.index + 1

# Print results
print(qualtable)
print("Mean cutoff: "+str(np.mean(cutoffs)))
print("Standard deviation: "+str(np.std(cutoffs)))
print("Median cutoff: "+str(np.median(cutoffs)))

# Generate histogram of qualification cutoffs
plt.hist(cutoffs, rwidth=0.75, bins=np.arange(min(cutoffs), max(cutoffs)+1, 1.0), align='left')
plt.xticks(np.arange(min(cutoffs), max(cutoffs)+1, 1.0))
plt.show()