from pycparser import c_parser, c_ast
from graphviz import Digraph

class SemanticAnalyzer(c_ast.NodeVisitor):
    def __init__(self):
        self.functions = {}
        self.current_function = None
        self.variables = set()
        self.control_flow_edges = []
        self.data_flow_edges = []
        self.callee_caller_edges = []
        self.previous_node = None
        self.node_counter = 0

    def generate_node_id(self):
        self.node_counter += 1
        return f'node_{self.node_counter}'

    def visit_FuncDef(self, node):
        func_name = node.decl.name
        func_node_id = self.generate_node_id()
        self.functions[func_name] = {
            'node_id': func_node_id,
            'variables': set(),
            'calls': set(),
            'control_flow': [],
            'children': []
        }
        self.current_function = func_name
        self.previous_node = func_node_id
        self.generic_visit(node)
        self.current_function = None
        self.previous_node = None

    def visit_Decl(self, node):
        if isinstance(node.type, c_ast.TypeDecl):
            var_name = node.name
            self.variables.add(var_name)
            if self.current_function:
                self.functions[self.current_function]['variables'].add(var_name)
                var_node_id = self.generate_node_id()
                self.data_flow_edges.append((self.previous_node, var_node_id))
                self.functions[self.current_function]['children'].append((var_name, var_node_id))
        self.generic_visit(node)

    def visit_If(self, node):
        if_node_id = self.generate_node_id()
        if_node_label = f"If (line {node.coord.line})"
        self.functions[self.current_function]['control_flow'].append(if_node_label)
        self.control_flow_edges.append((self.previous_node, if_node_id))
        self.functions[self.current_function]['children'].append((if_node_label, if_node_id))
        self.previous_node = if_node_id
        self.generic_visit(node)
        self.previous_node = if_node_id

    def visit_For(self, node):
        for_node_id = self.generate_node_id()
        for_node_label = f"For (line {node.coord.line})"
        self.functions[self.current_function]['control_flow'].append(for_node_label)
        self.control_flow_edges.append((self.previous_node, for_node_id))
        self.functions[self.current_function]['children'].append((for_node_label, for_node_id))
        self.previous_node = for_node_id
        self.generic_visit(node)
        self.previous_node = for_node_id

    def visit_While(self, node):
        while_node_id = self.generate_node_id()
        while_node_label = f"While (line {node.coord.line})"
        self.functions[self.current_function]['control_flow'].append(while_node_label)
        self.control_flow_edges.append((self.previous_node, while_node_id))
        self.functions[self.current_function]['children'].append((while_node_label, while_node_id))
        self.previous_node = while_node_id
        self.generic_visit(node)
        self.previous_node = while_node_id

    def visit_FuncCall(self, node):
        if self.current_function:
            func_name = node.name.name
            call_node_id = self.generate_node_id()
            call_node_label = f"Call to {func_name} (line {node.coord.line})"
            self.functions[self.current_function]['calls'].add(func_name)
            self.callee_caller_edges.append((self.previous_node, call_node_id))
            self.control_flow_edges.append((self.previous_node, call_node_id))
            self.functions[self.current_function]['children'].append((call_node_label, call_node_id))
            self.previous_node = call_node_id
        self.generic_visit(node)

def parse_c_code(code):
    parser = c_parser.CParser()
    return parser.parse(code)

def visualize_skeleton(semantic_info):
    dot = Digraph(comment='Foldable Semantic Skeleton')
    
    for func, details in semantic_info['functions'].items():
        with dot.subgraph(name=f'cluster_{func}') as sub:
            sub.node(details['node_id'], func, shape='box')
            for label, node_id in details['children']:
                shape = 'ellipse' if 'declares' in label else 'diamond' if 'If' in label else 'hexagon'
                sub.node(node_id, label, shape=shape)
                sub.edge(details['node_id'], node_id, label='contains')

    for start, end in semantic_info['control_flow_edges']:
        dot.edge(start, end, label='flows to')

    for caller, callee in semantic_info['callee_caller_edges']:
        dot.edge(caller, callee, label='calls')

    return dot

def main():
    code = """
    #include <stdio.h>

    void foo() {
        printf("Hello from foo\\n");
    }

    int main() {
        int x = 10;
        if (x > 0) {
            printf("%d\\n", x);
        } else {
            printf("%d\\n", -x);
        }
        for (int i = 0; i < x; i++) {
            foo();
        }
        return 0;
    }
    """

    ast = parse_c_code(code)
    analyzer = SemanticAnalyzer()
    analyzer.visit(ast)

    semantic_info = {
        'functions': analyzer.functions,
        'variables': list(analyzer.variables),
        'control_flow_edges': analyzer.control_flow_edges,
        'data_flow_edges': analyzer.data_flow_edges,
        'callee_caller_edges': analyzer.callee_caller_edges
    }

    dot = visualize_skeleton(semantic_info)
    dot.save('foldable_semantic_skeleton.dot')

if __name__ == "__main__":
    main()
