import pandas as pd

# Functions
class CleanData:
    def __init__(self, df):
        self.df = df
        
    def get_record(self, name: str):
        return self.df[self.df.name == name]

    def keep_record(self, records: list):
        for record in records:
            self.df.loc[record, 'keep'] = True

# Import data
df_orig = pd.read_csv("fatal-police-shootings-data.csv", index_col="id")
df = df_orig.copy()

# Add a column to determine if we want to keep the data or not
df["keep"] = True

# Begin checking for duplicates
# Remove TK TK (TK = to come, https://en.wikipedia.org/wiki/To_come_(publishing))
df_notk = df[df.name != "TK TK"].copy()

# Check for duplicate records in which name and state are the same
duplicated = list(df_notk[df_notk.duplicated(["name", "state"], keep="first")].name)

# Set all duplicate values to keep = False
df.loc[df.name.isin(duplicated), "keep"] = False

# Instantiate CleanData class
clean = CleanData(df)

# Filter the original dataset to look at the duplicated values
duplicated_df = df[df.name.isin(duplicated)].copy()

name = "Terry Hasty"
# 5572 [ref](https://www.wmbfnews.com/2020/02/25/deputy-suspect-shot-sumter-county-residence/)
clean.keep_record([5572])

name = "Daniel Hernandez"
# Keep both entries, different dates
# 614 [ref](https://www.bakersfield.com/archives/bakersfield-police-man-fatally-shot-tuesday-pointed-gun-at-officers/article_1fc51179-1fbe-5e1b-8938-a122e0080cb3.html)
# 5782 [ref](https://www.latimes.com/california/story/2020-05-07/lapd-officers-named-in-fatal-shooting-of-alleged-gunman)
clean.keep_record([614, 5782])

name = "Roderick McDaniel"
# Likely 4237 is the correct entry
# 4237 [ref](https://www.arkansasonline.com/news/2018/nov/28/prosecutor-details-magnolia-slayings-20/)
clean.keep_record([4237])

name = "Clayton Andrews"
# 5128 [ref](https://hl.nwaonline.com/news/2019/oct/30/osbi-investigating-fatal-officer-involv/)
clean.keep_record([5128])

name = "Benjamin Diaz"
# NUM [ref](https://kfoxtv.com/news/local/officer-involved-shooting-reported-near-alamogordo)
clean.keep_record([5191])

name = "Miguel Mercado Segura"
# Occured on the Jan 20, 2020
# [ref](https://www.latimes.com/socal/daily-pilot/news/story/2020-01-22/man-killed-in-officer-involved-shooting-in-fountain-valley-is-identified)
clean.keep_record([5515])

name = "Timothy Leroy Harrington"
# Threat level unclear
# 5537 [ref](https://www.wbtv.com/2020/02/15/deputy-fatally-shoots-armed-suspect-anson-co-sheriff-says/)
clean.keep_record([5537])

name = "William Patrick Floyd"
# Occured in Portland
# 5691 [ref](https://www.oregonlive.com/pacific-northwest-news/2020/03/troopers-fatally-shoot-person-on-i-5-south-of-salem.html)
clean.keep_record([5691])

# Keep only the records we want
df_mod = df[df.keep == True].copy()

# Drop the keep column
df_mod.drop(columns=["keep"], axis=0, inplace=True)

# Check dimensions
if (len(df_mod) == len(df)-7) & (len(df_orig.columns) == len(df_mod.columns)):
    # Export to csv
    print("Updated data.")
    df_mod.to_csv("fatal-police-shootings-data.csv")
else:
    print("Dimensions are incorrect. Written as backup.")
    df_mod.to_csv("fatal-police-shootings-data-mod.csv")