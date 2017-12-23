package edu.colostate.ember.structure;

import edu.stanford.nlp.trees.GrammaticalRelation;
import edu.stanford.nlp.trees.TypedDependency;

public class DependencyTreeEdge {

    private DependencyTreeNode gov;
    private DependencyTreeNode dep;
    private GrammaticalRelation reln;

    public DependencyTreeEdge(DependencyTreeNode gov, DependencyTreeNode dep, GrammaticalRelation reln) {
        this.gov = gov;
        this.dep = dep;
        this.reln = reln;
        gov.addChild(dep);
        gov.addChildrenEdge(this);

        dep.setParent(gov);
        dep.setParentEdge(this);

        dep.setLevel(gov.getLevel() + 1);
    }

    public DependencyTreeEdge(TypedDependency dependency) {
        this(new DependencyTreeNode(dependency.gov()), new DependencyTreeNode(dependency.dep()), dependency.reln());
    }

    public DependencyTreeNode getGov() {
        return gov;
    }

    public DependencyTreeNode getDep() {
        return dep;
    }

    public GrammaticalRelation getReln() {
        return reln;
    }

}
