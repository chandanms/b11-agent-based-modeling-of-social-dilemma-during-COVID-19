import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def plot_graph_aspiration_no_government_facet():
    """Plot graph for number of agents going out and staying in for
    range of aspiration when there is no involvement of government

    Returns:
        Displays a facet grids of graphs of agents staying in and
        going out for varying aspiration
    """
    column_names = ["steps", "stayin", "goout"]

    steps_list = []
    stayin_list = []
    goout_list = []
    aspiration_list = []
    file_names = ["simulation/dilemma_aspiration_0.1_stringent_0.csv",
                  "simulation/dilemma_aspiration_0.5_stringent_0.csv",
                  "simulation/dilemma_aspiration_0.9_stringent_0.csv"]

    for i, file in enumerate(file_names):
        df = pd.read_csv(file, names=column_names)

        steps_to_graph = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        df = df[df['steps'].isin(steps_to_graph)]

        steps_list.extend(df['steps'].values.tolist())
        stayin_list.extend(df['stayin'].values.tolist())
        goout_list.extend(df['goout'].values.tolist())

        if i == 0:
            aspiration_list.extend([0.1] * len(df["steps"].values.tolist()))
        elif i == 1:
            aspiration_list.extend([0.5] * len(df["steps"].values.tolist()))
        else:
            aspiration_list.extend([0.9] * len(df["steps"].values.tolist()))

    df_to_graph = pd.DataFrame(list(zip(steps_list,
                                        stayin_list,
                                        goout_list,
                                        aspiration_list)),
                               columns=["steps",
                                        "stayin",
                                        "goout",
                                        "aspiration"])

    grid = sns.FacetGrid(
        df_to_graph,
        col="aspiration",
        hue="aspiration",
        palette="tab20c",
        col_wrap=3,
        height=3,
        legend_out=True)

    grid.map(
        plt.plot,
        "steps",
        "stayin",
        marker="o",
        color="green",
        label="stayin")
    grid.map(
        plt.plot,
        "steps",
        "goout",
        marker="+",
        color="red",
        label="goout")

    grid.set(xlabel="steps", ylabel="")

    plt.subplots_adjust(top=0.8)
    grid.fig.suptitle('No government strictness')

    plt.show()


def plot_graph_aspiration_government_1_facet():
    """Plot graph for number of agents going out and staying in for
    range of aspiration when there government strictness of 0.1

    Returns:
        Displays a facet grids of graphs of agents staying in and
        going out for varying aspiration
    """

    column_names = ["steps", "stayin", "goout"]

    steps_list = []
    stayin_list = []
    goout_list = []
    aspiration_list = []
    file_names = ["simulation/dilemma_aspiration_0.1_stringent_0.1.csv",
                  "simulation/dilemma_aspiration_0.5_stringent_0.1.csv",
                  "simulation/dilemma_aspiration_0.9_stringent_0.1.csv"]

    for i, file in enumerate(file_names):
        df = pd.read_csv(file, names=column_names)

        steps_to_graph = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        df = df[df['steps'].isin(steps_to_graph)]

        steps_list.extend(df['steps'].values.tolist())
        stayin_list.extend(df['stayin'].values.tolist())
        goout_list.extend(df['goout'].values.tolist())

        if i == 0:
            aspiration_list.extend([0.1] * len(df["steps"].values.tolist()))
        elif i == 1:
            aspiration_list.extend([0.5] * len(df["steps"].values.tolist()))
        else:
            aspiration_list.extend([0.9] * len(df["steps"].values.tolist()))

    df_to_graph = pd.DataFrame(list(zip(steps_list,
                                        stayin_list,
                                        goout_list,
                                        aspiration_list)),
                               columns=["steps",
                                        "stayin",
                                        "goout",
                                        "aspiration"])

    grid = sns.FacetGrid(
        df_to_graph,
        col="aspiration",
        hue="aspiration",
        palette="tab20c",
        col_wrap=3,
        height=3,
        legend_out=True)

    grid.map(
        plt.plot,
        "steps",
        "stayin",
        marker="o",
        color="green",
        label="stayin")
    grid.map(
        plt.plot,
        "steps",
        "goout",
        marker="+",
        color="red",
        label="goout")

    grid.set(xlabel="steps", ylabel="")

    plt.subplots_adjust(top=0.8)
    grid.fig.suptitle('Government Strictness = 0.1')

    plt.show()


def plot_graph_aspiration_government_5_facet():
    """Plot graph for number of agents going out and staying in for
    range of aspiration when there government strictness of 0.5

    Returns:
        Displays a facet grids of graphs of agents staying in and
        going out for varying aspiration
    """

    column_names = ["steps", "stayin", "goout"]

    steps_list = []
    stayin_list = []
    goout_list = []
    aspiration_list = []
    file_names = ["simulation/dilemma_aspiration_0.1_stringent_0.5.csv",
                  "simulation/dilemma_aspiration_0.5_stringent_0.5.csv",
                  "simulation/dilemma_aspiration_0.9_stringent_0.5.csv"]

    for i, file in enumerate(file_names):
        df = pd.read_csv(file, names=column_names)

        steps_to_graph = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        df = df[df['steps'].isin(steps_to_graph)]

        steps_list.extend(df['steps'].values.tolist())
        stayin_list.extend(df['stayin'].values.tolist())
        goout_list.extend(df['goout'].values.tolist())

        if i == 0:
            aspiration_list.extend([0.1] * len(df["steps"].values.tolist()))
        elif i == 1:
            aspiration_list.extend([0.5] * len(df["steps"].values.tolist()))
        else:
            aspiration_list.extend([0.9] * len(df["steps"].values.tolist()))

    df_to_graph = pd.DataFrame(list(zip(steps_list,
                                        stayin_list,
                                        goout_list,
                                        aspiration_list)),
                               columns=["steps",
                                        "stayin",
                                        "goout",
                                        "aspiration"])

    grid = sns.FacetGrid(
        df_to_graph,
        col="aspiration",
        hue="aspiration",
        palette="tab20c",
        col_wrap=3,
        height=3,
        legend_out=True)

    grid.map(
        plt.plot,
        "steps",
        "stayin",
        marker="o",
        color="green",
        label="stayin")
    grid.map(
        plt.plot,
        "steps",
        "goout",
        marker="+",
        color="red",
        label="goout")

    grid.set(xlabel="steps", ylabel="")

    plt.subplots_adjust(top=0.8)
    grid.fig.suptitle('Government Strictness = 0.5')

    plt.show()


def plot_graph_aspiration_government_9_facet():
    """Plot graph for number of agents going out and staying in for
    range of aspiration when there government strictness of 0.9

    Returns:
        Displays a facet grids of graphs of agents staying in and
        going out for varying aspiration
    """

    column_names = ["steps", "stayin", "goout"]

    steps_list = []
    stayin_list = []
    goout_list = []
    aspiration_list = []
    file_names = ["simulation/dilemma_aspiration_0.1_stringent_0.9.csv",
                  "simulation/dilemma_aspiration_0.5_stringent_0.9.csv",
                  "simulation/dilemma_aspiration_0.9_stringent_0.9.csv"]

    for i, file in enumerate(file_names):
        df = pd.read_csv(file, names=column_names)

        steps_to_graph = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        df = df[df['steps'].isin(steps_to_graph)]

        steps_list.extend(df['steps'].values.tolist())
        stayin_list.extend(df['stayin'].values.tolist())
        goout_list.extend(df['goout'].values.tolist())

        if i == 0:
            aspiration_list.extend([0.1] * len(df["steps"].values.tolist()))
        elif i == 1:
            aspiration_list.extend([0.5] * len(df["steps"].values.tolist()))
        else:
            aspiration_list.extend([0.9] * len(df["steps"].values.tolist()))

    df_to_graph = pd.DataFrame(list(zip(steps_list,
                                        stayin_list,
                                        goout_list,
                                        aspiration_list)),
                               columns=["steps",
                                        "stayin",
                                        "goout",
                                        "aspiration"])

    grid = sns.FacetGrid(
        df_to_graph,
        col="aspiration",
        hue="aspiration",
        palette="tab20c",
        col_wrap=3,
        height=3,
        legend_out=True)

    grid.map(
        plt.plot,
        "steps",
        "stayin",
        marker="o",
        color="green",
        label="stayin")
    grid.map(
        plt.plot,
        "steps",
        "goout",
        marker="+",
        color="red",
        label="goout")

    grid.set(xlabel="steps", ylabel="")

    plt.subplots_adjust(top=0.8)
    grid.fig.suptitle('Government Strictness = 0.9')

    plt.show()


def plot_heatmap():
    """Plot the graph of heatmap of infection with respect to steps and government strictness

    Returns:
        The graph of heatmap, xaxis as steps and yaxis as government strictness
    """
    column_names = ["steps", "infection"]

    file_names = ["simulation/infection_number_stringent_0.9.csv", "simulation/infection_number_stringent_0.8.csv",
                  "simulation/infection_number_stringent_0.7.csv", "simulation/infection_number_stringent_0.6.csv",
                  "simulation/infection_number_stringent_0.5.csv", "simulation/infection_number_stringent_0.4.csv",
                  "simulation/infection_number_stringent_0.3.csv", "simulation/infection_number_stringent_0.2.csv",
                  "simulation/infection_number_stringent_0.1.csv", "simulation/infection_number_stringent_0.csv"]

    strictness_list = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    column_names_graph = [
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17"]
    df_to_graph = pd.DataFrame(columns=column_names_graph)

    for i, file in enumerate(file_names):
        infection_list = []

        df = pd.read_csv(file, names=column_names)
        infection_list.extend(df['infection'].values.tolist())

        df_to_graph.loc[i] = infection_list[0:13]

    midpoint = (df_to_graph.values.max() - df_to_graph.values.min()) / 2

    heat_map = sns.heatmap(df_to_graph, cmap="Reds", vmin=0.0, vmax=1.0, annot=True,
                           linewidth=0.3, cbar_kws={"shrink": .8}, yticklabels=strictness_list)

    heat_map.set(xlabel="steps", ylabel="government stringency")

    plt.show()


"""Plot the graph functions"""

plot_graph_aspiration_no_government_facet()
plot_graph_aspiration_government_1_facet()
plot_graph_aspiration_government_5_facet()
plot_graph_aspiration_government_9_facet()
plot_heatmap()
