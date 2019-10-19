from graphify.backbone.networkx import NetworkxImplementation
from graphify.build.initialization import initialize_backbone


def initialize_graph(name='ROOT'):
    """
    Initializes a raw graph, subject to the chosen underlying graph library
    # TODO: check some global flag indicating which backbone to use
    """
    return initialize_backbone(NetworkxImplementation(root=name))
