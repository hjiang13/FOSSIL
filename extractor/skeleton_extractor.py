import os
from pycparser import c_parser, c_ast
import networkx as nx

class CodeSkeletonExtractor(c_ast.NodeVisitor):
    def __init__(self):
        self.skeleton = []
        self.snippets = []
        self.cfg = nx.DiGraph()
        self.current_function = None

    def visit_FuncDef(self, node):
        func_summary = f"Function: {node.decl.name}"
        self.skeleton.append(func_summary)
        self.snippets.append(self.extract_code(node))
        self.current_function = node.decl.name
        self.cfg.add_node(self.current_function, type='function')
        self.generic_visit(node)
        self.current_function = None

    def visit_For(self, node):
        loop_summary = "For Loop"
        self.skeleton.append(loop_summary)
        snippet = self.extract_code(node)
        self.snippets.append(snippet)
        loop_name = f"for_loop_{len(self.snippets)}"
        self.cfg.add_node(loop_name, type='loop')
        if self.current_function:
            self.cfg.add_edge(self.current_function, loop_name)
        self.generic_visit(node)

    def visit_While(self, node):
        loop_summary = "While Loop"
        self.skeleton.append(loop_summary)
        snippet = self.extract_code(node)
        self.snippets.append(snippet)
        loop_name = f"while_loop_{len(self.snippets)}"
        self.cfg.add_node(loop_name, type='loop')
        if self.current_function:
            self.cfg.add_edge(self.current_function, loop_name)
        self.generic_visit(node)

    def visit_FuncCall(self, node):
        if self.current_function:
            callee = node.name.name if isinstance(node.name, c_ast.ID) else None
            if callee:
                self.cfg.add_edge(self.current_function, callee, type='call')

    def extract_code(self, node):
        start_line = node.coord.line
        end_line = node.coord.line
        if hasattr(node, 'block_items'):
            for item in node.block_items:
                if item.coord:
                    end_line = max(end_line, item.coord.line)
        code_lines = open(node.coord.file).read().splitlines()
        snippet = '\n'.join(code_lines[start_line - 1:end_line])
        return snippet

    def get_skeleton(self):
        return self.skeleton

    def get_snippets(self):
        return self.snippets

    def get_cfg(self):
        return self.cfg

def extract_skeleton_and_snippets(code, filename):
    parser = c_parser.CParser()
    ast = parser.parse(code, filename=filename)
    extractor = CodeSkeletonExtractor()
    extractor.visit(ast)
    return extractor.get_skeleton(), extractor.get_snippets(), extractor.get_cfg()
