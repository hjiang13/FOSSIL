import os
from pycparser import c_parser, c_ast
import networkx as nx
from extractor.summarizer import summarize_code_with_codet5

class CodeSkeletonExtractor(c_ast.NodeVisitor):
    def __init__(self):
        self.skeleton = []
        self.snippets = []
        self.cfg = nx.DiGraph()
        self.current_function = None
        self.loop_stack = []

    def visit_FuncDef(self, node):
        func_name = node.decl.name
        func_summary = f"Function: {func_name}"
        snippet = self.extract_code(node)
        summary = summarize_code_with_codet5(snippet)
        
        self.skeleton.append(func_summary)
        self.snippets.append(snippet)
        self.cfg.add_node(func_name, type='function', label=summary)
        self.current_function = func_name
        self.generic_visit(node)
        self.current_function = None

    def visit_For(self, node):
        loop_name = f"for_loop_{len(self.snippets)}"
        snippet = self.extract_code(node)
        summary = summarize_code_with_codet5(snippet)
        
        self.skeleton.append("For Loop")
        self.snippets.append(snippet)
        self.cfg.add_node(loop_name, type='loop', label=summary)
        if self.loop_stack:
            self.cfg.add_edge(self.loop_stack[-1], loop_name)
        elif self.current_function:
            self.cfg.add_edge(self.current_function, loop_name)
        
        self.loop_stack.append(loop_name)
        self.generic_visit(node)
        self.loop_stack.pop()

    def visit_While(self, node):
        loop_name = f"while_loop_{len(self.snippets)}"
        snippet = self.extract_code(node)
        summary = summarize_code_with_codet5(snippet)
        
        self.skeleton.append("While Loop")
        self.snippets.append(snippet)
        self.cfg.add_node(loop_name, type='loop', label=summary)
        if self.loop_stack:
            self.cfg.add_edge(self.loop_stack[-1], loop_name)
        elif self.current_function:
            self.cfg.add_edge(self.current_function, loop_name)
        
        self.loop_stack.append(loop_name)
        self.generic_visit(node)
        self.loop_stack.pop()

    def visit_FuncCall(self, node):
        if self.current_function:
            callee = node.name.name if isinstance(node.name, c_ast.ID) else None
            if callee:
                if self.loop_stack:
                    self.cfg.add_edge(self.loop_stack[-1], callee, type='call')
                else:
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
