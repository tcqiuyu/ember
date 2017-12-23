package edu.colostate.ember.structure;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.trees.TypedDependency;

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedList;
import java.util.Queue;
import java.util.function.Consumer;

public class DependencyTreeFactory {


    public static DependencyTreeNode constructDependencyTree(ArrayList<TypedDependency> typedDependencies) {
        DependencyTreeNode[] node = new DependencyTreeNode[typedDependencies.size() + 1];
        for (TypedDependency dependency : typedDependencies) {
            int idx = dependency.dep().get(CoreAnnotations.IndexAnnotation.class);
            boolean start = true;
            DependencyTreeNode lastGov = null;

            while (node[idx] == null) {
                DependencyTreeNode dep = null, gov = null;

                if (start) {// If it is the start of a new path, then construct new node
                    dep = new DependencyTreeNode(dependency.dep());
                } else {// otherwise, use the one stored in previous loop
                    dep = lastGov;
                }
                gov = new DependencyTreeNode(dependency.gov());

                node[idx] = dep;
                idx = gov.getWordIndex();


                if (node[idx] != null) {// If the next node has been traversed
                    new DependencyTreeEdge(node[idx], dep, dependency.reln());
                } else if (idx == 0) {// If the next node is ROOT
                    node[idx] = gov;
                    new DependencyTreeEdge(gov, dep, dependency.reln());
                } else {// If there are more to traverse
                    start = false;
                    new DependencyTreeEdge(gov, dep, dependency.reln());
                    lastGov = gov;
                    dependency = typedDependencies.get(idx - 1);
                }

            }
        }
        resetDependencyTreeLevel(node[0]);
//        getDependencyTreeNodeByLevel(node[0], 4).forEach(nod -> System.out.println(nod.getWord()));
        return node[0];
    }

    private static void resetDependencyTreeLevel(DependencyTreeNode root) {//using bfs traverse
        Queue<DependencyTreeNode> queue = new LinkedList<>();
        root.setLevel(0);
        queue.add(root);
        int maxDepth = 0;
        while (!queue.isEmpty()) {
            DependencyTreeNode tmpNode = queue.poll();

            if (!tmpNode.getChildren().isEmpty()) {
                tmpNode.getChildren().forEach(node -> node.setLevel(tmpNode.getLevel() + 1));

                if (tmpNode.getLevel() > maxDepth) {
                    maxDepth = tmpNode.getLevel();
                }

                queue.addAll(tmpNode.getChildren());

            }
        }
        int finalMaxDepth = maxDepth;
        bfsDependencyTree(root, n -> {
            n.setDepth(finalMaxDepth - n.getLevel());
        });
    }

    public static void bfsDependencyTree(DependencyTreeNode root, Consumer<? super DependencyTreeNode> func) {
        Queue<DependencyTreeNode> queue = new LinkedList<>();
        queue.add(root);

        while (!queue.isEmpty()) {
            DependencyTreeNode tmpNode = queue.poll();
            func.accept(tmpNode);

            if (!tmpNode.getChildren().isEmpty()) {
                queue.addAll(tmpNode.getChildren());
            }
        }
    }

    public static Collection<DependencyTreeNode> getDependencyTreeNodeByLevel(DependencyTreeNode root, int level) {
        Collection<DependencyTreeNode> nodes = new ArrayList<>();
        bfsDependencyTree(root, node -> {
            if (node.getLevel() == level) {
                nodes.add(node);
            }
        });
        return nodes;
    }

    public static void main(String[] args) {
//        DependencyTreeNode[] node = new DependencyTreeNode[13 + 1];
    }
}
