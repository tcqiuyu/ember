package edu.colostate.ember.nlp;

import edu.colostate.ember.nlp.lazy.LazyDependencyParser;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class KeyInfoExtractor {


    private static Logger logger = LoggerFactory.getLogger(KeyInfoExtractor.class);

    private DependencyParser parser;


    public KeyInfoExtractor() {
        logger.debug("Initializing Key Information Extractor");
        logger.trace("This is trace");
        parser = LazyDependencyParser.getInstance();
        logger.warn("This is warning");
        logger.error("This is error");
    }

    public String extractInfoByLevel(String input, int level) {
        String out = "";


        return out;
    }



    public static void main(String[] args) {

        KeyInfoExtractor extractor = new KeyInfoExtractor();
//        extractor.extractInfoByLevel();
    }
}
