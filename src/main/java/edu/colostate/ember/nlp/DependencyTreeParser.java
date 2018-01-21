package edu.colostate.ember.nlp;

import edu.colostate.ember.nlp.legacy.LazyDependencyParser;
import edu.colostate.ember.nlp.legacy.LazyPOSTagger;
import edu.colostate.ember.structure.DependencyTreeFactory;
import edu.colostate.ember.structure.DependencyTreeNode;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.TypedDependency;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class DependencyTreeParser {

    private static Logger logger = LoggerFactory.getLogger(DependencyTreeParser.class);
    private MaxentTagger tagger;
    private DependencyParser dependencyParser;

    public DependencyTreeParser() {
        logger.debug("Initializing dependency tree parser");
        tagger = LazyPOSTagger.getInstance();
        dependencyParser = LazyDependencyParser.getInstance();
        logger.debug("Finished initializing dependency tree parser");
    }

    public DependencyTreeNode parseDependencyTree(String input) {
        logger.trace("Parsing dependency tree from input: \"" + input + "\"");
        List<? extends HasWord> words = new SentenceTokenizer(input).tokenize();
        List<TaggedWord> taggedWords = tagger.tagSentence(words);
        GrammaticalStructure gs = dependencyParser.predict(taggedWords);
        Collection<TypedDependency> dependencies = gs.typedDependencies();

        DependencyTreeNode dependencyTree = DependencyTreeFactory.
                constructDependencyTree((ArrayList<TypedDependency>) dependencies);

        logger.trace("Parsing dependency tree for \"" + input + "\" finished");
        return dependencyTree;
    }

    public Collection<DependencyTreeNode> getDependencyTreeNodeByLevel(DependencyTreeNode root, int level) {
        logger.trace("Get nodes from dependency tree at level " + level);

        if (root.getLevel() != 0) {
            logger.warn("Given node is not the root node. Node level is " + root.getLevel());
        }

        Collection<DependencyTreeNode> nodes = new ArrayList<>();
        root.breadthFirstTraverse(node -> {
            if (node.getLevel() == level) {
                nodes.add(node);
            }
        });
        return nodes;
    }

    public void printDependencyTree(DependencyTreeNode root) {
        
    }
}
