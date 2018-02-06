from nltk.tree import ParentedTree
from nltk.tree import Tree
from itertools import combinations


class Node(ParentedTree):
    """
    The node object which constructs a syntactic tree

    Attributes:

    """

    # delta = 1
    # theta = 1
    # size = 0
    # depth = 0
    # index = 0
    # children_list = []
    # is_terminal = None

    def __init__(self, node, children=None):
        self.delta = 1
        self.theta = 1
        self.size = 0
        self.depth = 0
        self.index = 0
        self.children_list = []
        self.is_terminal = None
        self.production = ()
        super().__init__(node, children)

    def _get_node(self):
        pass

    def _set_node(self, value):
        pass

    def _update_delta(self):
        """
        delta = 1.2 where node i's POS tag is VB/NN
        delta = 1.1 where node i's POS tag is VP/NP
        delta = 1 otherwise
        :return: delta
        """
        label = self.label()
        if label.startswith("VB") or label.startswith("NN"):
            self.delta = 1.2
        elif label.startswith("VP") or label.startswith("NP"):
            self.delta = 1.1
        else:
            self.delta = 1

    def _update_size(self):
        """
        The size of a node is the number of all its descendants
        :return:
        """

        # TODO: here might have additional loops, may improve performance by integrate it with dfs traverse
        self.subtrees()
        for _ in self.subtrees():
            self.size += 1
        # Because the subtrees returns the node itself, so need to subtract 1
        # self.size -= 1

    def _update_theta(self):
        """
        theta is the production of all delta's for a tree fragment
        :return:
        """

        # TODO: here might have additional loops, may improve performance by integrate it with dfs traverse
        self.subtrees()
        for subtree in self.subtrees():
            self.theta *= subtree.delta

    def _update_depth(self):
        """
        the level of the tree fragment root in the entire syntactic parsing tree, with D_root=1
        :return:
        """
        for pos in self.treepositions():
            node = self[pos]
            if type(node) == Node:
                node.depth = len(pos) + 1

    def _update_index(self):
        idx = 0
        for tr in self.subtrees():
            tr.index = idx
            idx += 1

    def _update_children(self):
        if self.is_terminal:
            # Ignore the word itself in order to compute similarity matrix
            # self.children_list.append(self[0])
            return
        for tr in self.subtrees(lambda t: t.depth == self.depth + 1):
            self.children_list.append(tr)

    def _update_production(self):
        children_labels = []
        for i in self.children_list:
            if self.is_terminal:
                children_labels.append(i)
            else:
                children_labels.append(i.label())
        self.production = (self.label(), children_labels)

    def update(self):
        child = self[0]
        self.is_terminal = isinstance(child, str)
        self._update_delta()
        self._update_size()

    def update_tree(self):
        self.depth_first_traverse(lambda n: n.update())
        self._update_index()
        self._update_depth()
        self.depth_first_traverse(lambda n: (n._update_theta(), n._update_children(), n._update_production()))

    def depth_first_traverse(self, func):
        if type(self) == Node:
            func(self)
            for subtree in self:
                if type(subtree) == Node:
                    subtree.depth_first_traverse(func)

    @classmethod
    def fromstring(cls, s, brackets='()', read_node=None, read_leaf=None, node_pattern=None, leaf_pattern=None,
                   remove_empty_top_bracketing=True):
        out = super().fromstring(s, brackets, read_node, read_leaf, node_pattern, leaf_pattern,
                                 remove_empty_top_bracketing)
        out.update_tree()
        return out

    def is_matching(self, another_node):
        return self.label() == another_node.label() and self.production == another_node.production

    def get_tree_fragments_at_root(self):
        frags = [self]

        if self.is_terminal:
            return frags

        leaves = []

        for i in range(len(self.leaves())):
            leaves.append(self.leaf_treeposition(i))

        leaves_combination = []
        for i in range(1, len(leaves) + 1):
            iter = combinations(leaves, i)
            leaves_combination.append(list(iter))

        for temp in leaves_combination:
            for leaves_to_delete in temp:
                frag = self.copy(deep=True)
                for leaves in leaves_to_delete:
                    del frag[leaves]
                frags.append(frag)
        return frags

    def get_tree_fragments(self):
        frags = []
        for node in self.subtrees():
            frags.extend(node.get_tree_fragments_at_root())
        return frags


if __name__ == '__main__':
    # tree = Node.fromstring('(ROOT (S (NP (PRP It)) (VP (VBZ is) (ADJP (RB so) (JJ nice))) (. .)))')
    tree = Node.fromstring("(ROOT (S (NP (NNP Amrozi)) (VP (VBD accused) (NP (NP (NP (PRP$ his) (NN brother)) (, ,) (SBAR (WHNP (WP whom)) (S (NP (PRP he)) (VP (VBD called) (S (`` ``) (NP (DT the) (NN witness)) ('' ''))))) (, ,)) (PP (IN of) (S (VP (ADVP (RB deliberately)) (VBG distorting) (NP (PRP$ his) (NN evidence))))))) (. .)))")
    # tree.depth_first_traverse(lambda n: n.get_delta())
    # tree.update_tree()
    fra = tree.get_tree_fragments()
    print("Finished")
    tree.draw()
