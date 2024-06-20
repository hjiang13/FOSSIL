from extractor.skeleton_extractor import extract_skeleton_and_snippets
from extractor.summarizer import summarize_code_with_huggingface
from extractor.graph_visualizer import draw_cfg

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
    summary = summarize_code_with_huggingface(snippet)
    print(f"\nSnippet:\n{snippet}\nSummary: {summary}")

print("\nControl Flow Graph:")
draw_cfg(cfg)
