import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
import taipy.gui.builder as tgb
from taipy.gui import Gui

class Analysis:
    def __init__(self, data_path, eps, min_sample):
        self.eps = eps 
        self.data_path = data_path
        self.min_sample = min_sample
        df = pd.read_csv(self.data_path)
        X = df[['xlat', 'xlon', 'activity_index_total']].values
        X_scaled = StandardScaler().fit_transform(X)
        # Perform clustering
        #epsilon: maximum distance between two samples for one to be considered as in the neighborhood of the other (degrees)
        #min_samples: This parameter specifies the minimum number of points required to form a cluster
        dbscan = DBSCAN(eps=self.eps, min_samples=self.min_sample)
        df['cluster'] = dbscan.fit_predict(X_scaled)
        self.cluster_ranks = df.groupby('cluster').agg({
        'activity_index_total': 'sum',
        'xlat': 'mean',
        'xlon': 'mean'
        }).sort_values('activity_index_total', ascending=False)
        

    def place_stations(self, n_stations, min_distance=0.01):
        stations = []
        for _, cluster in self.cluster_ranks.iterrows():
            if len(stations) == n_stations:
                break
            station_coords = np.array([[station['lat'], station['lon']] for station in stations])
            if len(stations) == 0 or np.min(cdist([cluster[['xlat', 'xlon']].values], station_coords)) > min_distance:
                stations.append({
                    'name': f"Rank {len(stations) + 1}",
                    'lat': cluster['xlat'],
                    'lon': cluster['xlon'],
                    'activity_index_total': cluster['activity_index_total']
                })
        
        return(stations)
    
    def runcalc(self, n_stations):
        stations = self.place_stations(n_stations)

        places = [{
            'name': station['name'],
            'lat': station['lat'],
            'lon': station['lon'],
            'activity_index_total': station['activity_index_total']
        } for station in stations]
        #places = [{'name': 'Rank 1', 'lat': 47.61851000261457, 'lon': -122.29117929150571, 'activity_index_total': 41526.377905}, {'name': 'Rank 2', 'lat': 47.58996, 'lon': -122.28729277777776, 'activity_index_total': 21.081911}, {'name': 'Rank 3', 'lat': 47.61675066666667, 'lon': -122.19319133333333, 'activity_index_total': 19.145928}, {'name': 'Rank 4', 'lat': 47.575303636363635, 'lon': -122.31959454545455, 'activity_index_total': 14.968326000000001}, {'name': 'Rank 5', 'lat': 47.667972999999996, 'lon': -122.375883, 'activity_index_total': 11.682293}, {'name': 'Rank 6', 'lat': 47.67191111111111, 'lon': -122.18864444444444, 'activity_index_total': 7.233445}, {'name': 'Rank 7', 'lat': 47.64605400000001, 'lon': -122.30543399999999, 'activity_index_total': 5.422448}]
        
        return places