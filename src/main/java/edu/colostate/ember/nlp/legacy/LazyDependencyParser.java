package edu.colostate.ember.nlp.legacy;

import edu.colostate.ember.util.StaticFields;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LazyDependencyParser{


    private static Logger logger = LoggerFactory.getLogger(LazyDependencyParser.class);
    private DependencyParser parser;

    private LazyDependencyParser() {

        logger.debug("Initializing dependency parser");
        parser = DependencyParser.loadFromModelFile(StaticFields.DEPENDENCY_PARSER_MODEL);
        logger.debug("Loaded dependency parser");

    }

    private static class LazyDependencyParserHolder{
        static final DependencyParser INSTANCE = (new LazyDependencyParser()).parser;
    }

    public static DependencyParser getInstance() {
        return LazyDependencyParserHolder.INSTANCE;
    }


}
