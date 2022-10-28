#!/usr/bin/env python3
"""
IZV cast1 projektu
Autor: 

Detailni zadani projektu je v samostatnem projektu e-learningu.
Nezapomente na to, ze python soubory maji dane formatovani.

Muzete pouzit libovolnou vestavenou knihovnu a knihovny predstavene na prednasce
"""


from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt
from typing import List


def integrate(x: np.array, y: np.array) -> float:
    return (np.sum(np.multiply(np.subtract(x[1:], x[0:-1]), np.add(y[0:-1], y[1:])/2)))
    pass


def generate_graph(a: List[float], show_figure: bool = False, save_path: str | None=None):
    # x = np.arange(-3, 3.1, 0.1).astype("f")
    # z = np.zeros_like(x)
    # a = (np.multiply.outer(a, (x)**2))
    # plt.plot(x, a[0])
    # plt.plot(x, a[1])
    # plt.plot(x, a[2])
    # plt.fill_between(x, a[1], where=a[1]>z, interpolate=True, color='#ff7f0e', alpha=0.15)
    # plt.fill_between(x, a[2], where=a[2]<z, interpolate=True, color='#2ca02c', alpha=0.15)
    x = np.linspace(-3, 3).astype("f")
    a = (np.multiply.outer(a, (x)**2))
    plt.plot(x, a[0])
    plt.plot(x, a[1])
    plt.plot(x, a[2])
    plt.savefig("mygraph.png")
    pass


def generate_sinus(show_figure: bool=False, save_path: str | None=None):
    pass


def download_data(url="https://ehw.fit.vutbr.cz/izv/temp.html"):
    pass


def get_avg_temp(data, year=None, month=None) -> float:
    pass
