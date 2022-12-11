
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
    removed = ['region', 'h', 'i', 'p2a']
    cat = ['k', 'l', 'o', 'p', 'q']
    for i in removed:
        my_list.remove(i)
    new_df["date"] = pd.to_datetime(new_df["p2a"])
    new_df[my_list] = new_df[my_list].apply(pd.to_numeric, errors='coerce')
    new_df[cat] = new_df[cat].astype('category')
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
    df = df.loc[df["region"].isin(regions)]
    types = {
        1: "den: viditelnost nezhoršená",
        2: "den: viditelnost zhoršená",
        3: "den: viditelnost zhoršená",
        4: "noc: viditelnost nezhoršená",
        5: "noc: viditelnost zhoršená",
        6: "noc: viditelnost nezhoršená",
        7: "noc: viditelnost zhoršená",
    }
    df["p19"] = df["p19"].replace(types)
    titles = ["den: viditelnost nezhoršená", "den: viditelnost zhoršená", "noc: viditelnost nezhoršená", "noc: viditelnost zhoršená"]

    visibility_accident = (df.groupby(["region", "p19"]).agg({"p1": "count"}).reset_index())
    
    sns.set_style("darkgrid")
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8.27, 8.27))
    axes = axes.flatten()
    for i in range(4):
        sns.barplot(ax=axes[i], data=visibility_accident[i::4], x='region', y='p1', saturation=1)
        axes[i].set_title(titles[i], fontweight="bold")
        axes[i].set(ylabel='', xlabel='')
        axes[i].spines['bottom'].set_color('#404040')
        axes[i].set(ylabel='Počet nehod', xlabel='Kraj')
    axes[0].set(xlabel='')
    axes[1].set(xlabel='')
    axes[1].set(ylabel='')
    axes[3].set(ylabel='')
    plt.tight_layout()

    # save or show
    if fig_location:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()

    
    pass

# Ukol4: druh srážky jedoucích vozidel
def plot_direction(df: pd.DataFrame, fig_location: str = None,
                   show_figure: bool = False):   
    regions = ['PHA', 'STC', 'JHM', 'PLK']
    df = df.loc[df["region"].isin(regions)]
    types = {
        1: "čelní",
        2: "boční",
        3: "boční",
        4: "zezadu",
    }
    df["p7"] = df["p7"].replace(types)
    titles = ["Kraj: JHM", "Kraj: PLK", "Kraj: PHA", "Kraj: STC"]
    
    month_accident = (df.groupby(["region", df.date.dt.month, "p7"]).agg({"p1": "count"}).reset_index())
    month_accident = month_accident[month_accident.p7 != 0]
    
    graph = sns.catplot(data=month_accident, x="date", y='p1', col="region", col_wrap=2, hue='p7', legend=True, kind="bar", saturation=0.5, sharey=False)
    
    graph.set_axis_labels("Měsíc", "Počet nehod")
    graph.legend.set_title('Druh srážky')
    graph.set_titles('Kraj: {col_name}')
    if fig_location:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()
    
    pass

# Ukol 5: Následky v čase
def plot_consequences(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    pass

if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni 
    # funkce.
    
    file_name ="parsed_data.csv"
    new_load = False
    if new_load:
        df = load_data("data/data.zip")
        df2 = parse_data(df, True)
        df2.to_pickle(file_name)
    else:
        df2 = pd.read_pickle(file_name)
    
    plot_visibility(df2, "01_visibility.png")
    plot_direction(df2, "02_direction.png", True)
    plot_consequences(df2, "03_consequences.png")


# Poznamka:
# pro to, abyste se vyhnuli castemu nacitani muzete vyuzit napr
# VS Code a oznaceni jako bunky (radek #%%% )
# Pak muzete data jednou nacist a dale ladit jednotlive funkce
# Pripadne si muzete vysledny dataframe ulozit nekam na disk (pro ladici
# ucely) a nacitat jej naparsovany z disku

# %%
