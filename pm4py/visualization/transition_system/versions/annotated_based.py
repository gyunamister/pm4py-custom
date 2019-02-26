import pm4py


def apply(tsys, parameters=None, value=None, aggregation_measure=None):
    """
    Get visualization of a Transition System

    Parameters
    -----------
    tsys
        Transition system
    parameters
        Optional parameters of the algorithm

    Returns
    ----------
    gviz
        Graph visualization
    """

    gviz = pm4py.visualization.transition_system.util.visualize_perf.visualize(tsys, parameters=parameters, value=value, aggregation_measure=aggregation_measure)
    return gviz
