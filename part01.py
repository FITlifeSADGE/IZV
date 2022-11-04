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
    x = np.linspace(-3, 3).astype("f")
    z = np.zeros_like(x)
    a = (np.multiply.outer(a, (x)**2))
    plt.plot(x, a[0], label=r'$y_{1.0}(x)$')
    plt.plot(x, a[1], label=r'$y_{2.0}(x)$')
    plt.plot(x, a[2], label=r'$y_{-2.0}(x)$')
    plt.fill_between(x, a[1], where=a[1]>z, interpolate=True, color='#ff7f0e', alpha=0.15)
    plt.fill_between(x, a[2], where=a[2]<z, interpolate=True, color='#2ca02c', alpha=0.15)
    plt.xlabel('x')
    plt.ylabel(r'$f_a(x)$')
    plt.legend(bbox_to_anchor=(0.5, 1.15), loc='upper center', ncol=3)
    plt.ylim(-20, 20)
    plt.xlim(-3, 3.9)
    plt.annotate(r'${\int}f_{2.0}(x)dx$', xy=(3.01, 18))
    plt.annotate(r'${\int}f_{1.0}(x)dx$', xy=(3.01, 9))
    plt.annotate(r'${\int}f_{-2.0}(x)dx$', xy=(3.01, -18))
    ax = plt.subplot()
    ax.spines["right"].set_position(('axes', 1.05))
    ax.spines["top"].set_bounds(-3,4.25)
    ax.spines["bottom"].set_bounds(-3,4.25)
    if show_figure:
        plt.show()
    else:
        plt.savefig(save_path, bbox_inches="tight", pad_inches=1)
    plt.close()
    pass


def generate_sinus(show_figure: bool=False, save_path: str | None=None):
    t = np.linspace(0,100,7000).astype("f")
    f1 = 0.5 * np.sin(1/50 * np.pi * t)
    f3 = np.add(0.5 * np.sin(1/50 * np.pi * t), 0.25 * np.sin(np.pi * t))
    upper = f3 > f1
    up = f3.copy()
    up[~upper] = np.nan
    down = f3.copy()
    down[upper] = np.nan
    fig = plt.figure(figsize=(8,10))
    ax = fig.add_subplot(3, 1, 1)
    ax.plot(t, 0.5 * np.sin(1/50 * np.pi * t))
    ax.set_xlim(0,100)
    ax.set_ylim(-0.8, 0.8)
    ax.set_xlabel('t')
    ax.set_ylabel(r'$f_1(x)$')
    ax = fig.add_subplot(3, 1, 2)
    ax.plot(t, 0.25 * np.sin(np.pi * t))
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.8, 0.8)
    ax.set_xlabel('t')
    ax.set_ylabel(r'$f_2(x)$')
    ax = fig.add_subplot(3, 1, 3)
    ax.plot(t, up, c="green")
    ax.plot(t, down, c="red")
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.8, 0.8)
    ax.set_xlabel('t')
    ax.set_ylabel(r'$f_3(x)$')
    if show_figure:
        fig.show()
    else:
        fig.savefig(save_path, bbox_inches="tight", pad_inches=1)
    pass


def download_data(url="https://ehw.fit.vutbr.cz/izv/temp.html"):
    pass


def get_avg_temp(data, year=None, month=None) -> float:
    pass
