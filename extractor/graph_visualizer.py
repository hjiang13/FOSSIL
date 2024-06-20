import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw_tree(tree, output_filename=None):
    pos = nx.spring_layout(tree)
    fig, ax = plt.subplots()

    for node in tree.nodes():
        x, y = pos[node]
        label = tree.nodes[node].get('label', node)
        
        # Estimate the width and height of the rectangle based on text length
        width = max(0.2, 0.01 * len(label.split()))
        height = max(0.1, 0.01 * len(label.split()))
        
        # Draw the rectangle for each node
        rect = Rectangle((x - width / 2, y - height / 2), width, height, fill=True, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)
        
        # Add the label inside the rectangle
        plt.text(x, y, label, ha='center', va='center', fontsize=8, wrap=True, bbox=dict(facecolor='white', alpha=0.5))

    edge_labels = nx.get_edge_attributes(tree, 'type')
    nx.draw_networkx_edges(tree, pos, ax=ax)
    nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels, font_size=8)

    plt.axis('off')

    if output_filename:
        plt.savefig(output_filename, bbox_inches='tight')

    plt.show()
