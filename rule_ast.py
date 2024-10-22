class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value      # Value for operand nodes (e.g., number, string)
        self.left = left        # Reference to left child
        self.right = right      # Reference to right child

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, left={self.left}, right={self.right})"
