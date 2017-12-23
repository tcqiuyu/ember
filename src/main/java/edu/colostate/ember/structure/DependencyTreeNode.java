
package edu.colostate.ember.structure;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.IndexedWord;

import java.util.ArrayList;
import java.util.Collection;

public class DependencyTreeNode {

    private DependencyTreeNode parent;
    private DependencyTreeEdge parentEdge;
    private Collection<DependencyTreeNode> children;
    private Collection<DependencyTreeEdge> edges;
    private IndexedWord word;
    private int level;
    private int wordIdx;
    private int depth;

    public DependencyTreeNode(IndexedWord word) {
        this.word = word;
        this.wordIdx = word.get(CoreAnnotations.IndexAnnotation.class);
        this.children = new ArrayList<>();
        this.edges = new ArrayList<>();
        this.level = 0;
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
}
