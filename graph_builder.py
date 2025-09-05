import networkx as nx
import matplotlib.pyplot as plt

def build_and_visualize_graph(data):
    """Builds a graph from the AI data and returns a plot."""
    G = nx.DiGraph()

    equipment = data.get("equipment", [])
    lines = data.get("lines", [])

    # Add nodes
    for item in equipment:
        if 'tag' in item:
            G.add_node(item['tag'], label=f"{item['tag']}\n({item['type']})")

    # Add edges 
    for line in lines:
        if 'source_tag' in line and 'destination_tag' in line:
            if G.has_node(line['source_tag']) and G.has_node(line['destination_tag']):
                G.add_edge(line['source_tag'], line['destination_tag'], label=line.get('line_number_tag', ''))

    if not G.nodes():
        return None 

    # Create plot
    plt.figure(figsize=(16, 10))
    pos = nx.spring_layout(G, k=0.9, iterations=50) 
    node_labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, with_labels=False, node_size=3000, node_color='skyblue', font_size=10, width=1.5, edge_color='gray')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=7)

    plt.title("P&ID Process Flow Diagram")

    # Saveplot
    plot_path = "temp_plot.png"
    plt.savefig(plot_path)
    plt.close()

    return plot_path