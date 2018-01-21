package edu.colostate.ember.structure;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.IndexedWord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.function.Consumer;

public class DependencyTreeNode {

    private static Logger logger = LoggerFactory.getLogger(DependencyTreeNode.class);
    private DependencyTreeNode parent;
    private DependencyTreeEdge parentEdge;
    private Collection<DependencyTreeNode> children;
    private Collection<DependencyTreeEdge> edges;
    private IndexedWord word;
    private int level;
    private int wordIdx;
    private int depth;
    private boolean lastSib; // mainly for print tree purpose

    public DependencyTreeNode(IndexedWord word) {
        this.word = word;
        this.wordIdx = word.get(CoreAnnotations.IndexAnnotation.class);
        this.children = new ArrayList<>();
        this.edges = new ArrayList<>();
        this.level = 0;
    }

    public boolean isLastSib() {
        return lastSib;
    }

    public void setLastSib(boolean lastSib) {
        this.lastSib = lastSib;
    }

    public IndexedWord getWord() {
        return word;
    }

    public int getWordIndex() {
        return wordIdx;
    }

    public void incrementLevel() {
        level++;
    }

    public void decrementLevel() {
        level--;
    }

    public DependencyTreeEdge getParentEdge() {
        return parentEdge;
    }

    public void setParentEdge(DependencyTreeEdge parentEdge) {
        this.parentEdge = parentEdge;
    }

    public DependencyTreeNode getParent() {
        return parent;
    }

    public void setParent(DependencyTreeNode parent) {
        this.parent = parent;
    }

    public void addChild(DependencyTreeNode child) {
        children.add(child);
        edges.add(child.getParentEdge());
    }

    public void addChildrenEdge(DependencyTreeEdge edge) {
        this.edges.add(edge);
    }

    public Collection<DependencyTreeNode> getChildren() {
        return children;
    }

    public Collection<DependencyTreeEdge> getEdges() {
        return edges;
    }

    public int getLevel() {
        return level;
    }

    public void setLevel(int level) {
        this.level = level;
    }

    public int getDepth() {
        return depth;
    }

    public void setDepth(int depth) {
        this.depth = depth;
    }

    public void breadthFirstTraverse(Consumer<? super DependencyTreeNode> func) {
//        logger.trace("Started breadth first traverse on node \"" + this.getWord().value() + "\"");
        Queue<DependencyTreeNode> queue = new LinkedList<>();
        queue.add(this);

        while (!queue.isEmpty()) {
            DependencyTreeNode tmpNode = queue.poll();
            func.accept(tmpNode);

            if (!tmpNode.children.isEmpty()) {
                queue.addAll(tmpNode.children);
            }
        }
    }

    public void depthFirstTraverse(Consumer<? super DependencyTreeNode> func) {
//        logger.trace("Started depth first traverse on node \"" + this.getWord().value() + "\"");
        Stack<DependencyTreeNode> stack = new Stack<>();
        stack.push(this);

        while (!stack.isEmpty()) {
            DependencyTreeNode tmpNode = stack.pop();

            func.accept(tmpNode);
            if (!tmpNode.children.isEmpty()) {
                for (int i = tmpNode.children.size() - 1; i >= 0; i--) {
                    stack.add(((ArrayList<DependencyTreeNode>) tmpNode.children).get(i));
                }
            }
        }
    }

    public void simplePrintSubTree() {

    }

}
