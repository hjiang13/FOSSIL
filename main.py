from extractor.skeleton_extractor import extract_skeleton_and_snippets
from extractor.summarizer import summarize_code_with_codet5
from extractor.graph_visualizer import draw_tree
import networkx as nx

example_code = """

void process_data(int data) {
    printf("Processing data: %d\\n", data);
}

void handle_request(int request) {
    for (int i = 0; i < request; i++) {
        printf("Handling request %d\\n", i);
        for (int j = 0; j < i; j++) {
            process_data(j);
        }
    }
}

void server_loop() {
    for (int k = 0; k < 5; k++) {
        printf("Server loop iteration %d\\n", k);
        handle_request(k);
    }
}

int main() {
    printf("Starting server\\n");
    server_loop();
    printf("Server stopped\\n");
    return 0;
}
"""

filename = 'example.c'
with open(filename, 'w') as f:
    f.write(example_code)

skeleton, snippets, tree = extract_skeleton_and_snippets(example_code, filename)

print("Skeleton:")
print(skeleton)

print("\nSnippets and Summaries:")
for snippet in snippets:
    summary = summarize_code_with_codet5(snippet)
    print(f"\nSnippet:\n{snippet}\nSummary: {summary}")

# Save the hierarchical tree to a file
tree_filename = 'code_hierarchy.graphml'
nx.write_graphml(tree, tree_filename)
print(f"Code hierarchy saved to {tree_filename}")

# Draw and save the hierarchical tree visualization as JPEG
jpeg_filename = 'code_hierarchy.jpg'
draw_tree(tree, output_filename=jpeg_filename)
print(f"Code hierarchy visualization saved to {jpeg_filename}")
