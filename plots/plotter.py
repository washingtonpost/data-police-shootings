import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from geopy.geocoders import Nominatim
import time
import pickle
import datetime
from scipy import ndimage
from mpl_toolkits.basemap import Basemap

def organize_data():
    df = pd.read_csv('../fatal-police-shootings-data.csv')
    df['year'] = df['date'].str.split('-').str[0]
    df['month'] = df['date'].str.split('-').str[1]
    df['day'] = df['date'].str.split('-').str[2]
    df['location'] = df['city'] + ' ' + df['state']
    df['cumulative_day'] = df.apply(make_date, axis=1)
    df['location'] = df['city'] + ' ' + df['state']
    loc_dict = pickle.load(open("location_dict.p", "rb" ))
    df['coords'] = df['location'].map(loc_dict)
    df[['x', 'y']] = df['coords'].apply(pd.Series)
    main = df[df['x'] > -140][df['x'] < -66]
    return main

def make_location_dict(df):
    location_dict = {}
    geolocator = Nominatim()
    for row in df.iterrows():
        counter = 0
        while counter < 5:qp
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

def make_plot(df, frame):
    sns.set_style("white")
    plt.figure()
    df = df[df['cumulative_day'] <= frame]
    im = plt.imread('map.png')
    implot = plt.imshow(im, origin='lower')
    df = df.groupby(['x','y']).size().reset_index()
    plt.scatter((df['x'] + 126.5) * 11.15, (df['y'] - 23.7) * 13.5, s=df[0]*20, alpha=0.4)
    plt.axis('off')
    ax = plt.gca()
    ax.text(-18 + 50, -30, '2015')
    ax.text(164 + 50, -30, '2016')
    ax.text(347 + 50, -30, '2017')

    ax.add_patch(patches.Rectangle(
        ((frame / 2) + 50, -10),   # (x,y)
        2,          # width
        10))
    plt.savefig('frames/' + str(frame), dpi=600)
    plt.close()
    return None

if __name__ == '__main__':
    main = organize_data()
    for frame in range(1, df['cumulative_day'].max()):
        make_plot(main, frame)
