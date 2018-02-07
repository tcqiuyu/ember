from nltk.tree import ParentedTree
from nltk.tree import Tree
from itertools import combinations
import re


def get_delta(label):
    if label.startswith("VB") or label.startswith("NN"):
        return 1.2
    elif label.startswith("VP") or label.startswith("NP") or label.startswith("RB") or label.startswith("JJ"):
        return 1.1
    else:
        return 1


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

    def __init__(self, node, children=None, **kwargs):
        self.delta = kwargs['delta'] if 'delta' in kwargs else 1
        self.theta = kwargs['theta'] if 'theta' in kwargs else 1
        self.size = kwargs['size'] if 'size' in kwargs else 0
        self.depth = kwargs['depth'] if 'depth' in kwargs else 0
        self.height = kwargs['height'] if 'height' in kwargs else 0
        self.index = kwargs['index'] if 'index' in kwargs else 0
        self.children_list = kwargs['children_list'] if 'children_list' in kwargs else []
        self.is_terminal = kwargs['is_terminal'] if 'is_terminal' in kwargs else False
        self.production = kwargs['production'] if 'production' in kwargs else ()

        super().__init__(node, children)

    def _get_node(self):
        pass

    def _set_node(self, value):
        pass

    def _update_production(self):
        children_labels = []
        for i in self.children_list:
            if self.is_terminal:
                children_labels.append(i)
            else:
                children_labels.append(i.label())
        self.production = (self.label(), children_labels)

    @classmethod
    def fromstring(cls, s, brackets='()', read_node=None, read_leaf=None, node_pattern=None, leaf_pattern=None,
                   remove_empty_top_bracketing=True):
        if not isinstance(brackets, str) or len(brackets) != 2:
            raise TypeError('brackets must be a length-2 string')
        if re.search('\s', brackets):
            raise TypeError('whitespace brackets not allowed')
        # Construct a regexp that will tokenize the string.
        open_b, close_b = brackets
        open_pattern, close_pattern = (re.escape(open_b), re.escape(close_b))
        if node_pattern is None:
            node_pattern = '[^\s%s%s]+' % (open_pattern, close_pattern)
        if leaf_pattern is None:
            leaf_pattern = '[^\s%s%s]+' % (open_pattern, close_pattern)
        token_re = re.compile('%s\s*(%s)?|%s|(%s)' % (
            open_pattern, node_pattern, close_pattern, leaf_pattern))
        # Walk through each token, updating a stack of trees.
        stack = [(None, [])]  # list of (node, children) tuples

        depth = 0
        index = 0
        for match in token_re.finditer(s):
            token = match.group()
            # Beginning of a tree/subtree
            if token[0] == open_b:
                # theta = 1
                depth += 1
                if len(stack) == 1 and len(stack[0][1]) > 0:
                    cls._parse_error(s, match, 'end-of-string')
                label = token[1:].lstrip()
                if read_node is not None: label = read_node(label)
                stack.append((label, []))
            # End of a tree/subtree
            elif token == close_b:
                if len(stack) == 1:
                    if len(stack[0][1]) == 0:
                        cls._parse_error(s, match, open_b)
                    else:
                        cls._parse_error(s, match, 'end-of-string')
                index += 1
                label, children = stack.pop()
                delta = get_delta(label)
                is_terminal = False
                theta = 1
                size = 1
                children_labels = []
                height = 1
                for child in children:

                    if isinstance(child, str):
                        is_terminal = True
                    else:
                        child_delta = child.delta
                        child_theta = child.theta
                        child_size = child.size
                        child_height = child.height
                        theta *= child_delta * child_theta
                        height = max(height, child_height + 1)
                        size += child_size
                        children_labels.append(child.label())
                production = (label, children_labels)
                stack[-1][1].append(
                    cls(label, children, theta=theta, delta=delta, index=index, depth=depth, is_terminal=is_terminal,
                        size=size, children_list=children, production=production, height=height))
                depth -= 1
            # Leaf node
            else:
                if len(stack) == 1:
                    cls._parse_error(s, match, open_b)
                if read_leaf is not None: token = read_leaf(token)
                stack[-1][1].append(token)

        # check that we got exactly one complete tree.
        if len(stack) > 1:
            cls._parse_error(s, 'end-of-string', close_b)
        elif len(stack[0][1]) == 0:
            cls._parse_error(s, 'end-of-string', open_b)
        else:
            assert stack[0][0] is None
            assert len(stack[0][1]) == 1
        tree = stack[0][1][0]

        # If the tree has an extra level with node='', then get rid of
        # it.  E.g.: "((S (NP ...) (VP ...)))"
        if remove_empty_top_bracketing and tree._label == '' and len(tree) == 1:
            tree = tree[0]
        return tree

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
    tree = Node.fromstring('(ROOT (S (NP (PRP It)) (VP (VBZ is) (ADJP (RB so) (JJ nice))) (. .)))')
    # tree = Node.fromstring("(ROOT (S (NP (NNP Amrozi)) (VP (VBD accused) (NP (NP (NP (PRP$ his) (NN brother)) (, ,) (SBAR (WHNP (WP whom)) (S (NP (PRP he)) (VP (VBD called) (S (`` ``) (NP (DT the) (NN witness)) ('' ''))))) (, ,)) (PP (IN of) (S (VP (ADVP (RB deliberately)) (VBG distorting) (NP (PRP$ his) (NN evidence))))))) (. .)))")
    # tree.depth_first_traverse(lambda n: n.get_delta())
    # tree.update_tree()
    fra = tree.get_tree_fragments()
    print("Finished")
    tree.draw()
