package edu.colostate.ember.nlp;

import edu.colostate.ember.structure.DependencyTreeNode;
import edu.stanford.nlp.trees.TreePrint;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collection;

public class KeyInfoExtractor {


    private static Logger logger = LoggerFactory.getLogger(KeyInfoExtractor.class);
    private DependencyTreeParser dependencyTreeParser;

    public KeyInfoExtractor() {
        logger.debug("Initializing key-information-extractor");
        dependencyTreeParser = new DependencyTreeParser();
        logger.debug("Finished initializing key-information-extractor");
    }

    public String extractInfoByLevel(String input, int level) {
        logger.trace("Extracting information at level " + level + " from \"" + input + "\"");
        DependencyTreeNode root = dependencyTreeParser.parseDependencyTree(input);
        Collection<DependencyTreeNode> nodes = dependencyTreeParser.getDependencyTreeNodeByLevel(root, level);
        StringBuilder sb = new StringBuilder();
        nodes.forEach(node -> sb.append(node.getWord().value()).append(" "));
        return sb.toString().trim();
    }


    public static void main(String[] args) {

        KeyInfoExtractor extractor = new KeyInfoExtractor();
//        extractor.extractInfoByLevel();
        String input = "In the past 12 months , how often have you felt really sick ?";
        String out = extractor.extractInfoByLevel(input, 2);
        logger.error(out);

    }
}
