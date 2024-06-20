import networkx as nx
import matplotlib.pyplot as plt

def draw_cfg(cfg):
    pos = nx.spring_layout(cfg)
    labels = nx.get_node_attributes(cfg, 'type')
    nx.draw(cfg, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(cfg, 'type')
    nx.draw_networkx_edge_labels(cfg, pos, edge_labels=edge_labels)
    plt.show()
