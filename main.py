from extractor.skeleton_extractor import extract_skeleton_and_snippets
from extractor.summarizer import summarize_code_with_codet5
from extractor.graph_visualizer import draw_cfg
import networkx as nx

example_code = """
void foo() {
    for (int i = 0; i < 10; i++) {
        printf("%d\\n", i);
    }
    while (1) {
        break;
    }
}

void bar() {
    printf("Hello, World!\\n");
}

void baz() {
    foo();
    bar();
}
"""

filename = 'example.c'
with open(filename, 'w') as f:
    f.write(example_code)

skeleton, snippets, cfg = extract_skeleton_and_snippets(example_code, filename)

print("Skeleton:")
print(skeleton)

print("\nSnippets and Summaries:")
for snippet in snippets:
    summary = summarize_code_with_codet5(snippet)
    print(f"\nSnippet:\n{snippet}\nSummary: {summary}")

# Save the CFG to a file
cfg_filename = 'control_flow_graph.graphml'
nx.write_graphml(cfg, cfg_filename)
print(f"Control Flow Graph saved to {cfg_filename}")

# Draw and save the CFG visualization as JPEG
jpeg_filename = 'control_flow_graph.jpg'
draw_cfg(cfg, output_filename=jpeg_filename)
print(f"Control Flow Graph visualization saved to {jpeg_filename}")
