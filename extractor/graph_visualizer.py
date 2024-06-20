import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw_tree(tree, output_filename=None):
    pos = nx.spring_layout(tree)
    fig, ax = plt.subplots()

    for node in tree.nodes():
        x, y = pos[node]
        # Draw the rectangle for each node
        rect = Rectangle((x - 0.1, y - 0.05), 0.2, 0.1, fill=True, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        # Add the label inside the rectangle
        label = tree.nodes[node].get('label', node)
        plt.text(x, y, label, ha='center', va='center', fontsize=8, wrap=True)

    edge_labels = nx.get_edge_attributes(tree, 'type')
    nx.draw_networkx_edges(tree, pos, ax=ax)
    nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels, font_size=8)

    plt.axis('off')

    if output_filename:
        plt.savefig(output_filename, bbox_inches='tight')

    plt.show()
