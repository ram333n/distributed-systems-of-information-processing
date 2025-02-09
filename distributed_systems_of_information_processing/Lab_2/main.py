from itertools import chain


class TreeNode:
    def __init__(self, id):
        self.id = id
        self.children = []

    def get_id(self):
        return self.id

    def get_children(self):
        return self.children

    def set_children(self, children):
        self.children = children

    def get_grandchildren(self):
        result = []

        for child in self.get_children():
            result.extend(child.get_children())

        return result

    def print_tree(self):
        self.__print_tree(self, 0)

    def __print_tree(self, root, level=0):
        if root is None:
            return

        print(" " * (level * 4) + f"└── {root.id}")
        for child in root.children:
            self.__print_tree(child, level + 1)


def find_mis(node):
    # sum(I[w]), where w=child of 'node'
    from_children = [find_mis(child) for child in node.get_children()]
    from_children = list(chain.from_iterable(from_children))

    # sum(I[w]) + 1, where w=grandchild of 'node', + 1 - adding 'node' to list
    from_grandchildren = [mis_node for mis_node in (find_mis(grandchildren) for grandchildren in node.get_grandchildren())]
    from_grandchildren = list(chain.from_iterable(from_grandchildren))
    from_grandchildren.append(node)

    return max(from_children, from_grandchildren, key=len)
"""
Tree example 1: 
└── 1
    └── 2
        └── 5
        └── 6
    └── 3
        └── 7
    └── 4
"""
def build_example_tree_1():
    root = TreeNode(1)

    child_1 = TreeNode(2)
    child_2 = TreeNode(3)
    child_3 = TreeNode(4)

    grandchild_1 = TreeNode(5)
    grandchild_2 = TreeNode(6)
    grandchild_3 = TreeNode(7)

    root.set_children([child_1, child_2, child_3])
    child_1.set_children([grandchild_1, grandchild_2])
    child_2.set_children([grandchild_3])

    return root


"""
Tree example 2: 
└── 1
    └── 2
        └── 3
            └── 6
        └── 4
            └── 7
            └── 8
        └── 5
"""
def build_example_tree_2():
    root = TreeNode(1)
    child_1_1 = TreeNode(2)

    child_2_1 = TreeNode(3)
    child_2_2 = TreeNode(4)
    child_2_3 = TreeNode(5)

    child_3_1 = TreeNode(6)
    child_3_2 = TreeNode(7)
    child_3_3 = TreeNode(8)

    root.set_children([child_1_1])

    child_1_1.set_children([child_2_1, child_2_2, child_2_3])

    child_2_1.set_children([child_3_1])
    child_2_2.set_children([child_3_2, child_3_3])

    return root

if __name__ == '__main__':
    root = build_example_tree_1()
    print(f'==========================Example tree 1==========================')
    print(root.print_tree())
    mis = [node.get_id() for node in find_mis(root)]
    print(f'Found MIS: {mis}, size: {len(mis)}')

    root = build_example_tree_2()
    print(f'==========================Example tree 2==========================')
    print(root.print_tree())
    mis = [node.get_id() for node in find_mis(root)]
    print(f'Found MIS: {mis}, size: {len(mis)}')

