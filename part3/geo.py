#!/usr/bin/python3.10
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily
import sklearn.cluster
import numpy as np
# muzete pridat vlastni knihovny


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""
    df = df.dropna(subset=['d', 'e'])
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df['d'], df['e']), crs="EPSG:5514")
    return gdf

def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s nehodami s alkoholem pro roky 2018-2021 """
    regions = ['JHM']
    gdf = gdf[gdf['region'].isin(regions)]
    gdf = gdf[gdf['p11'] >= 3]
    
    titles = ['JHM kraj (2018)', 'JHM kraj (2019)', 'JHM kraj (2020)', 'JHM kraj (2021)']
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    axes = axes.flatten()
    for i in range(4):
        gdf[gdf['p2a'].str[0:4] == str(2018 + i)].plot(ax=axes[i], markersize=1, color='red')
        axes[i].set_title(titles[i])
        axes[i].axis('off')
        contextily.add_basemap(axes[i], crs=gdf.crs.to_string(), source=contextily.providers.Stamen.TonerLite, zoom=10, alpha=0.9)
    
    if fig_location:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()
    pass

def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """
    regions = ['JHM']
    gdf = gdf[gdf['region'].isin(regions)]
    gdf = gdf[gdf['p36'].isin([1, 2, 3])]
    
    #make 2d array from gdf.geometry.x and gdf.geometry.y
    array = np.array([gdf.geometry.x, gdf.geometry.y]).T
    
    #AgglomerativeClustering je nejlepší používat v případě: Many clusters, possibly connectivity constraints, non Euclidean, distances, transductive
    #Nejlépe odpovídá našemu případu
    #Vyzkoušena metoda DBSCAN, ale výsledky nebyly tak dobré
    gdf['Cluster'] = sklearn.cluster.AgglomerativeClustering(n_clusters=20).fit(X=array).labels_
    
    gdf= gdf.dissolve(by='Cluster', aggfunc={"p1": "count"})
    
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    gdf.plot(ax=axes, markersize=1, column = 'p1', legend=True)
    axes.axis('off')
    contextily.add_basemap(axes, crs=gdf.crs.to_string(), source=contextily.providers.Stamen.TonerLite, zoom=10, alpha=0.9, reset_extent=True)
    axes.set_title('Nehody v JHM kraji na silnicích 1., 2. a 3. třídy')
    
    plt.tight_layout()
    if fig_location:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()
    pass
if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    
    file_name = "parsed_data.csv"
    new_load = False
    if new_load:
        gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
        gdf.to_pickle(file_name)
    else:
        gdf = pd.read_pickle(file_name)
    
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)
