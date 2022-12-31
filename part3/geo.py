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
    regions = ['JHM']
    df_regs = df[df['region'].isin(regions)].copy()
    df_regs = df_regs.dropna(subset=['d', 'e'])
    gdf = geopandas.GeoDataFrame(df_regs, geometry=geopandas.points_from_xy(df_regs['d'], df_regs['e']), crs="EPSG:5514")
    return gdf
    pass

def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s nehodami s alkoholem pro roky 2018-2021 """
    gdf_new = gdf[gdf['p11'] >= 3]
    gdf_new = gdf_new.to_crs("epsg:3857")
    
    titles = ["JHM kraj (2018)", "JHM kraj (2019)", "JHM kraj (2020)", "JHM kraj (2021)"]

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 7))
    axes = axes.flatten()
    for i in range(4):
        gdf_new[gdf_new['p2a'].str[0:4].astype(int) == i + 2018].plot(ax=axes[i], markersize=1)
        axes[i].set_title(titles[i])
        axes[i].axis("off")
        contextily.add_basemap(axes[i], crs=gdf_new.crs.to_string(), source=contextily.providers.Stamen.TonerLite, alpha=0.9)
    plt.tight_layout()

    if fig_location:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()
    pass

def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """
    new_gdf = gdf[gdf['p36'] >= 1]
    new_gdf = new_gdf[new_gdf['p36'] <= 3].to_crs("epsg:3857")
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    # collect points in a 2d array
    points = np.reshape(list(zip(new_gdf.geometry.x, new_gdf.geometry.y)), (-1, 2))
    
    # cluster into frequency groups
    # Agglomerative clustering was chosen because of many clusters and connectivity constraints
    # The results after agglomerative clustering also resemble the given example map the most
    # and this clustering method produces similar results in each run unlike e.g. MiniBatch KMeans
    new_gdf["frequency_group"] = sklearn.cluster.AgglomerativeClustering(n_clusters=20).fit(X=points).labels_

    # magic at this point.. for each group of points assign the cluster size
    # this value will represent the color in the resulting map
    new_gdf = new_gdf.dissolve(by="frequency_group", aggfunc={"p1": "count"})

    new_gdf.plot(ax=ax, markersize=1, column="p1", legend=True)
    ax.set_axis_off()
    contextily.add_basemap(ax, crs=new_gdf.crs.to_string(), alpha=0.9, attribution_size=6,
                    reset_extent=False, source=contextily.providers.Stamen.TonerLite)
    ax.set_title('Nehody v JHM kraji na silnicích 1., 2. a 3. třídy', fontsize="medium")
    plt.tight_layout()
    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()
    pass

if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    #plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)
