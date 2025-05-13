import pandas as pd
import datetime
current_time = datetime.date.today()

data1 = pd.read_csv("PlayerCounts.csv")
data2 = pd.read_csv("steamdata.csv")
#Merge Datasets
output = pd.merge(data1, data2, on='Game', how='inner')
#Drop rows that have a review count of 0, either data error or no one has reviewed Game
output.drop(output[output['Reviews Total']==0].index, inplace=True)
#Drop estimated revenue, not useful in our model
output.drop('Revenue Estimated', axis = 1, inplace = True)
#This goes through, and does the math to convert the release date to a day count numerical value
for index, row in output.iterrows():
    db_date = row['Release Date'].split('/')
    date = datetime.date(int(db_date[2]), int(db_date[0]), int(db_date[1]))
    total_age = current_time - date
    output.at[index, 'Release Date'] = total_age.days
#Changes release date to age to better show purpose of column
output.columns = output.columns.str.replace('Release Date', 'Age')
#Put the processed data into a new csv file for use in model
output.to_csv('cleaned_finaltest.csv', mode='a', index = False)
 