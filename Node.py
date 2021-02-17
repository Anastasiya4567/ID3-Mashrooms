class Node:
    def __init__(self, column_name, result):
        self.column = column_name
        self.nodes = dict()
        self.result = result

    def add_child(self, child_key, child_node):
        self.nodes[child_key] = child_node
