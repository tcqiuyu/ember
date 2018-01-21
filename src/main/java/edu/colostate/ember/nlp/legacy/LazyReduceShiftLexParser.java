package edu.colostate.ember.nlp.legacy;

import edu.colostate.ember.util.StaticFields;
import edu.stanford.nlp.parser.common.ParserGrammar;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LazyReduceShiftLexParser {

    private static Logger logger = LoggerFactory.getLogger(LazyReduceShiftLexParser.class);
    private ParserGrammar pg;

    private LazyReduceShiftLexParser() {

        logger.debug("Initializing lexical parser w/ reduce shift model");
        pg = LexicalizedParser.loadModel(StaticFields.SHIFTPARSER_MODEL);
        logger.debug("Loaded shift lex-parser");

    }

    public static ParserGrammar getInstance() {
        return LazyReduceShiftLexParserHolder.INSTANCE;
    }

    private static class LazyReduceShiftLexParserHolder {
        static final ParserGrammar INSTANCE = (new LazyReduceShiftLexParser()).pg;
    }

}
