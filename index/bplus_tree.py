import math

class Node:
   
    def __init__(self, order):
        self.order = order
        self.keys = []

    def is_full(self):
        return len(self.keys) == self.order


class LeafNode(Node):
    
    def __init__(self, order):
        super().__init__(order)
        self.values = []
        self.next_leaf = None

    def insert(self, key, value):
     
        pos = 0
        while pos < len(self.keys) and self.keys[pos] < key:
            pos += 1

        if pos < len(self.keys) and self.keys[pos] == key:
        
            self.values[pos] = value
        else:
            self.keys.insert(pos, key)
            self.values.insert(pos, value)

    def split(self):
       
        mid = int(math.ceil(self.order / 2))
        
        new_leaf = LeafNode(self.order)
        new_leaf.keys = self.keys[mid:]
        new_leaf.values = self.values[mid:]
        
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        
        # Maintain linked list
        new_leaf.next_leaf = self.next_leaf
        self.next_leaf = new_leaf
        
        return new_leaf.keys[0], new_leaf


class InternalNode(Node):
    
    def __init__(self, order):
        super().__init__(order)
        self.children = []

    def insert(self, key, child):
   
        pos = 0
        while pos < len(self.keys) and self.keys[pos] < key:
            pos += 1
            
        self.keys.insert(pos, key)
        self.children.insert(pos + 1, child)

    def split(self):
        
        mid = int(math.ceil(self.order / 2))
        
        new_internal = InternalNode(self.order)
        new_internal.keys = self.keys[mid + 1:]
        new_internal.children = self.children[mid + 1:]
        
       
        split_key = self.keys[mid]
        
        self.keys = self.keys[:mid]
        self.children = self.children[:mid + 1]
        
        return split_key, new_internal


class BPlusTree:
   
    def __init__(self, order=4):
        self.order = order
        self.root = LeafNode(order)

    def insert(self, key, value):

        leaf, path = self._find_leaf(key)
        
        leaf.insert(key, value)
        
        if leaf.is_full():
            
            split_key, new_leaf = leaf.split()
            self._insert_into_parent(leaf, split_key, new_leaf, path)

    def find(self, key):
        
        leaf, _ = self._find_leaf(key)
        
        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf.values[i]
        return None

    def _find_leaf(self, key):
        
        node = self.root
        path = []
        
        while isinstance(node, InternalNode):
            path.append(node)
            pos = 0
            while pos < len(node.keys) and key >= node.keys[pos]:
                pos += 1
            node = node.children[pos]
            
        return node, path

    def _insert_into_parent(self, left_node, key, right_node, path):
       
        if not path:
        
            new_root = InternalNode(self.order)
            new_root.keys.append(key)
            new_root.children.append(left_node)
            new_root.children.append(right_node)
            self.root = new_root
            return

        
        parent = path.pop()
        parent.insert(key, right_node)
        
        if parent.is_full():
            
            split_key, new_internal = parent.split()
            self._insert_into_parent(parent, split_key, new_internal, path)

    def print_tree(self):
       
        print("--- B+ Tree ---")
        if not self.root:
            print("Empty")
            return
            
        queue = [(self.root, 0)]
        current_level = 0
        while queue:
            node, level = queue.pop(0)
            if level != current_level:
                print()
                current_level = level
                
            print(f"{node.keys}", end=" | ")
            
            if isinstance(node, InternalNode):
                for child in node.children:
                    queue.append((child, level + 1))
        print("\n---------------")
