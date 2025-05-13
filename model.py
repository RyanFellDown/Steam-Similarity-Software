import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

df = pd.read_csv('cleaned_finaltest.csv')
df_no_string = df.drop(columns=['Game', 'Tags'])

scalar = StandardScaler()
scaled_df = scalar.fit_transform(df_no_string.select_dtypes(include=['number']))

inertia_list = []

#   Test intertia values for clusters with n = 2 -> 30
for i in range (2,30):
    kmean = KMeans(n_clusters=i)
    kmean.fit(scaled_df)
    inertia_list.append(kmean.inertia_)
elbow = pd.DataFrame({'Cluster':range(2,30), 'Error':inertia_list})
plt.figure(figsize=(12,6))
plt.plot(elbow['Cluster'], elbow['Error'], marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia') 
plt.show()

#   After printing out and plotting the table we see that the best size for n clusters is between 7-13, were going to use 9
clusterSize = 9
kmean = KMeans(n_clusters=clusterSize)
kmean.fit(scaled_df)

#   We know have our clusters with our data, we can s
pred = kmean.predict(scaled_df)
frame = pd.DataFrame(scaled_df)
frame['cluster'] = pred
print(frame)
frame.head()

#    Ask user what features they think are important (2 Features)
#   Printing out features user can choose from, if they choose two features from the list, do work, otherwise prompt them again.
userFeature1 = ""
userFeature2 = ""

while userFeature1 not in list(df_no_string.columns) or userFeature2 not in list(df_no_string.columns):
    print("Please select two features from the following list: ", list(df_no_string.columns))
    userFeature1 = input("Enter your first preferred feature: ")
    userFeature2 = input("Enter your second preferred feature: ")
    if userFeature1 not in list(df_no_string.columns) or userFeature2 not in list(df_no_string.columns):
        print("One of the features you choose isn't in the list, please try again...")

#   Look at frame, find cluster whith highest avg of both features
#   I'm sorting the clusters into their own individual datasets, and THEN taking the average of the features.
#   FIRST, however, I can remove the features that AREN'T important in the dataset.
clusters = []
for x in range(0, clusterSize):
    clusters.append(df.loc[frame['cluster'] == x])

#   Here, I'm averaging out the features the user choose within each cluster.
average1Values = []
average2Values = []
for x in range(0, clusterSize):
    average1Values.append(clusters[x][userFeature1].mean())
    average2Values.append(clusters[x][userFeature2].mean())
            
#    Now, what needs to be done is returning the cluster with the bests averages in each category. HOWEVER, we're assuming certain things,
#   like the user wanting a LOW age value or a LOW price count. So first, we're going to normalize the values to give each feature
#   the same amount of weight.
normFeature1 = []
normFeature2 = []
for element in average1Values:
    normFeature1.append(element/max(average1Values))
for element in average2Values:
    normFeature2.append(element/max(average2Values))

#   Here, we need the inverse of any values that originate from Age or Price; that way, the lower the value, the more weight it's given.
normalizedInverse1 = []
normalizedInverse2 = []
if userFeature1 == "Age" or userFeature1 == "Launch Price":
    for x in normFeature1:
        normalizedInverse1.append(float(1)-x)
else:
    normalizedInverse1 = normFeature1
if userFeature2 == "Age" or userFeature2 == "Launch Price":
    for x in normFeature2:
        normalizedInverse2.append(float(1)-x)
else:
    normalizedInverse2 = normFeature2

print("The normalized averages for clusters 1-9 of user feature ", userFeature1, " are: ", normalizedInverse1)
print("The normalized averages for clusters 1-9 of user feature ", userFeature2, " are: ", normalizedInverse2)

#   We're taking the means of the user feature from each cluster and getting their average. Then, if that's the biggest so far,
#   we replace greatestMean with whatever cluster that mean was from. At the end, we get the best cluster for the user features.
greatestMean = 0
for x in range(0, clusterSize):
    if ((normalizedInverse1[x]+normalizedInverse2[x])/2) > greatestMean:
        greatestMean = x
print("The best cluster for your features is: ", greatestMean)

#   From the best cluster (aka the greatestMean), we use the games in the cluster to finally recommend games to the user.
names = clusters[greatestMean]['Game'].values.tolist()

#   bestCluster will be the cluster with the greatest average of both features, removing duplicates which may occur due to DLC's of games.
bestCluster = clusters[greatestMean][[userFeature1, userFeature2, 'Game']]
bestCluster = bestCluster.drop_duplicates(subset=['Game'])

#   Normalizing the values and inversing Age or Launch Price as needed...
if userFeature1 == "Age" or userFeature1 == "Launch Price":
    bestCluster[userFeature1] = 1-(bestCluster[userFeature1]/bestCluster[userFeature1].abs().max())
else:
    bestCluster[userFeature1] = bestCluster[userFeature1]/bestCluster[userFeature1].abs().max()
if userFeature2 == "Age" or userFeature2 == "Launch Price":
    bestCluster[userFeature2] = 1-(bestCluster[userFeature2]/bestCluster[userFeature2].abs().max())
else:
    bestCluster[userFeature2] = bestCluster[userFeature2]/bestCluster[userFeature2].abs().max()

#   Take the mean of the user features of all the games, sorted by the top ones, and return those games.
bestCluster['mean'] = bestCluster[[userFeature1, userFeature2]].mean(axis=1)
print(bestCluster.sort_values(by=['mean'], ascending=False))

#   And FINALLY, return the top games based on the user preferences.
bestChoicesCleaned = bestCluster['Game'].values.tolist()
print("These are the top games for your preferences from the given cluster are: ", bestChoicesCleaned[:10])