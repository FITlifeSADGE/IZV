
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import zipfile

# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

# Ukol 1: nacteni dat ze ZIP souboru
def load_data(filename : str) -> pd.DataFrame:
    # tyto konstanty nemente, pomuzou vam pri nacitani
    headers = ["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
                "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27", "p28",
                "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
                "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t", "p5a"]

    # def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    regions = {
        "PHA": "00",
        "STC": "01",
        "JHC": "02",
        "PLK": "03",
        "ULK": "04",
        "HKK": "05",
        "JHM": "06",
        "MSK": "07",
        "OLK": "14",
        "ZLK": "15",
        "VYS": "16",
        "PAK": "17",
        "LBK": "18",
        "KVK": "19",
    }
    df = pd.DataFrame()
    with zipfile.ZipFile(filename) as zip:
        for z in zip.namelist():
            with zipfile.ZipFile(zip.open(z, 'r')) as archive:
                for i in archive.infolist():
                    if i.filename != 'CHODCI.csv' and i.file_size != 0:
                        with archive.open(i, 'r') as csv_file:
                            num = i.filename[0:2]
                            reg = list(regions.keys())[list(regions.values()).index(num)]
                            data = pd.read_csv(csv_file, encoding='cp1250', low_memory=False, sep=';', names=headers, decimal=',')
                            data["region"] = reg
                            df = pd.concat([df, data]) 
    return df

        
# Ukol 2: zpracovani dat
def parse_data(df : pd.DataFrame, verbose : bool = False) -> pd.DataFrame:
    new_df = df.copy()
    if verbose:
        original = (new_df.memory_usage(index=False, deep=True).sum())/(1000*1000)
        original = round(original, 1)
        print("orig_size = {} MB".format(original))
    my_list = list(new_df)
    removed = ['region', 'a', 'b', 'd', 'e', 'f', 'g']
    for i in removed:
        my_list.remove(i)
    to_float = list(['d', 'e', 'f', 'g', 'a', 'b'])
    new_df["date"] = pd.to_datetime(new_df["p2a"])
    new_df[my_list] = new_df[my_list].astype('category')
    new_df[to_float] = new_df[to_float].apply(pd.to_numeric, errors='coerce', downcast='float')
    new_df.drop_duplicates(subset=["p1"], inplace=True)
    if verbose:
        new = (new_df.memory_usage(index=False, deep=True).sum())/(1000*1000)
        new = round(new, 1)
        print("new_size = {} MB".format(new))
    return new_df
    pass

# Ukol 3: počty nehod v jednotlivých regionech podle viditelnosti
def plot_visibility(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    regions = ['PHA', 'STC', 'JHM', 'PLK']
    #df = df[df["region"].isin(regions)]
    df = df.loc[df["region"].isin(regions)]
    types = {
        1: "den: viditelnost nezhoršená vlivem povětrnostních podmínek",
        2: "den: zhoršená viditelnost (svítání, soumrak)",
        3: "den: zhoršená viditelnost vlivem povětrnostních podmínek (mlha, sněžení, déšť apod.)",
        4: "noc: s veřejným osvětlením, viditelnost nezhoršená vlivem povětrnostních podmínek",
        5: "noc: s veřejným osvětlením, zhoršená viditelnost vlivem povětrnostních podmínek (mlha, déšť, sněžení apod.)",
        6: "noc: bez veřejného osvětlení, viditelnost nezhoršená vlivem povětrnostních podmínek",
        7: "noc: bez veřejného osvětlení, viditelnost zhoršená vlivem povětrnostních podmínek (mlha, déšť, sněžení apod.)",
    }
    df["visibility"] = df["p19"].map(types)
    visibility_accident = df.groupby(["region", "visibility"]).size()
    print(visibility_accident[0])
    
    pass

# Ukol4: druh srážky jedoucích vozidel
def plot_direction(df: pd.DataFrame, fig_location: str = None,
                   show_figure: bool = False):
    pass

# Ukol 5: Následky v čase
def plot_consequences(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    pass

if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni 
    # funkce.
    df = load_data("data/data.zip")
    df2 = parse_data(df, True)
    
    plot_visibility(df2, "01_visibility.png")
    plot_direction(df2, "02_direction.png", True)
    plot_consequences(df2, "03_consequences.png")


# Poznamka:
# pro to, abyste se vyhnuli castemu nacitani muzete vyuzit napr
# VS Code a oznaceni jako bunky (radek #%%% )
# Pak muzete data jednou nacist a dale ladit jednotlive funkce
# Pripadne si muzete vysledny dataframe ulozit nekam na disk (pro ladici
# ucely) a nacitat jej naparsovany z disku
