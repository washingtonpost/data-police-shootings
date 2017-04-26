import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
import time
import pickle
import datetime
from scipy import ndimage
from mpl_toolkits.basemap import Basemap

df = pd.read_csv('../fatal-police-shootings-data.csv')
df['year'] = df['date'].str.split('-').str[0]
df['month'] = df['date'].str.split('-').str[1]
df['day'] = df['date'].str.split('-').str[2]
df['location'] = df['city'] + ' ' + df['state']
df['cumulative_day'] = df.apply(make_date, axis=1)
df['location'] = df['city'] + ' ' + df['state']

df.groupby(['city', 'state']).size().sort_values()

def make_location_dict(df):
    location_dict = {}
    geolocator = Nominatim()
    for row in df.iterrows():
        counter = 0
        while counter < 5:
            location = row[1]['city'] + ' ' + row[1]['state']
            try:
                if location not in location_dict:
                    struct = {'city': row[1]['city'], 'state': row[1]['state']}
                    coords = geolocator.geocode(struct)
                    y = coords.latitude
                    x = coords.longitude
                    location_dict[location] = [x, y]
                    print location, x, y
                break
            except:
                print '**************', location
                counter += 1
                time.sleep(10)
    pickle.dump(location_dict, open("location_dict.p", "wb" ))


    
def make_date(row):      
    return (datetime.datetime(int(row['year']), int(row['month']), int(row['day'])) - datetime.datetime(2015, 1, 1)).days


loc_dict = pickle.load(open("location_dict.p", "rb" ))

df['coords'] = df['location'].map(loc_dict)
df[['x', 'y']] = df['coords'].apply(pd.Series)

plt.scatter(main['x'], main['y'], alpha = 0.03)
plt.show()

main = df[df['x'] > -140][df['x'] < -60]

im = plt.imread('map2.tif')
im = ndimage.rotate(im, 9)
implot = plt.imshow(im, origin='lower')
plt.scatter((main['x'] + 132) * 15, (main['y'] - 23) * 21, alpha = 0.5)
plt.show()

