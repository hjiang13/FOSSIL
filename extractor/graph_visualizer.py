import networkx as nx
import matplotlib.pyplot as plt

def draw_tree(tree, output_filename=None):
    pos = nx.spring_layout(tree)
    labels = nx.get_node_attributes(tree, 'label')
    nx.draw(tree, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(tree, 'type')
    nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels)
    
    if output_filename:
        plt.savefig(output_filename)
    
    plt.show()
