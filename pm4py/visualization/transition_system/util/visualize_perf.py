import tempfile

from graphviz import Digraph
from statistics import mean, median, stdev
from pm4py.visualization.common.utils import *


def visualize(ts, parameters=None, value=None, aggregation_measure=None):
    if parameters is None:
        parameters = {}

    image_format = parameters["format"] if "format" in parameters else "png"
    show_labels = parameters["show_labels"] if "show_labels" in parameters else True
    show_names = parameters["show_names"] if "show_names" in parameters else True
    show_value = False if aggregation_measure is None else True

    filename = tempfile.NamedTemporaryFile(suffix='.gv')
    viz = Digraph(ts.name, filename=filename.name, engine='dot')

    # states
    viz.attr('node')
    for s in ts.states:
        if show_names:
            viz.node(str(s.name))
        else:
            viz.node(str(s.name), "")
    # arcs
    for t in ts.transitions:
        if show_value:
            aggr_stat = aggregate_stats(t.data[value], aggregation_measure)
            #aggr_stat_hr = human_readable_stat(aggr_stat)
            viz.edge(str(t.from_state.name), str(t.to_state.name), label=str(aggr_stat))
        elif show_labels:
            viz.edge(str(t.from_state.name), str(t.to_state.name), label=t.name)
        else:
            viz.edge(str(t.from_state.name), str(t.to_state.name))

    viz.attr(overlap='false')
    viz.attr(fontsize='11')

    viz.format = image_format

    return viz

def aggregate_stats(statistics, aggregation_measure):
    """
    Aggregate the statistics

    Parameters
    -----------
    statistics
        Element statistics
    elem
        Current element
    aggregation_measure
        Aggregation measure (e.g. mean, min) to use

    Returns
    -----------
    aggr_stat
        Aggregated statistics
    """
    aggr_stat = 0
    if aggregation_measure == "mean" or aggregation_measure is None:
        aggr_stat = mean(statistics)
    elif aggregation_measure == "median":
        aggr_stat = median(statistics)
    elif aggregation_measure == "stdev":
        aggr_stat = stdev(statistics)
    elif aggregation_measure == "sum":
        aggr_stat = sum(statistics)
    elif aggregation_measure == "min":
        aggr_stat = min(statistics)
    elif aggregation_measure == "max":
        aggr_stat = max(statistics)

    return aggr_stat