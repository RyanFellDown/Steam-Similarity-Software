Steps:
  1. Download all files to the same folder.
  2. If desired, run ScrapingData.py to return a more recent PlayerData.csv.
  3. The previous step requires installing chromedriver.exe and changing 'path = ".../chromedriver.exe"' in ScrapingData.py to your correct path.
  4. Run preprocessing.py, altering the paths for data1 and data2 to the absolute paths for "PlayerCounts.csv" and "steamdata.csv", respectively. 
     Also, change the path of output.to_csv() to the same path where the previous two will be, along with 'cleaned_finaltest.csv' at the end.
  5. Run model.py, equally altering the path for df to the absolute path for 'cleaned_finaltest.csv'.
  6. Model.py will return a graph on Clusters vs Intertia, then allow you to choose your two most preferred features for a game, finally returning
     the top 5 games similar to your game.
