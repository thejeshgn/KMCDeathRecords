# KMDC Death Records

Source: https://www.kmcgov.in/KMCPortal/KMCDeathRegistrationAction.do

# Setup
Install dependencies in `requirements.txt`

```pip3 install -R requirements.txt```

# Scrape

1. Edit scrape.py and update the END_DATE
```END_DATE = date(2021, 5, 15)```
2. Run 
```python scrape.py```
3. It will download only the missing days
4. It will add the raw data to `raw` folder

# Process
1. Delete the current sqlite file inside `data` folder
2. Run
```python process.py```
3. It will generate the sqlite file with a single table called `death_records`
4. You can explore it using any clients. My [preference is sqlitebrowser](https://sqlitebrowser.org/)

# Data
Currently I have the processed data for 
```
START_DATE = date(2010, 1, 1)
END_DATE = date(2021, 5, 15)
```
inside `data` folder. It also has zipped csv for convience.

