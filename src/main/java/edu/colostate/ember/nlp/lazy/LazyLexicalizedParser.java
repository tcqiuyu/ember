package edu.colostate.ember.nlp.lazy;

import edu.colostate.ember.util.StaticFields;
import edu.stanford.nlp.parser.common.ParserGrammar;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LazyLexicalizedParser {

    private static Logger logger = LoggerFactory.getLogger(LazyLexicalizedParser.class);
    private ParserGrammar pg;

    private LazyLexicalizedParser() {

        logger.info("Initializing lexical parser w/ default model");
        pg = LexicalizedParser.loadModel(StaticFields.LEXPARSER_MODEL);
        logger.info("Loaded default lex-parser");

    }

    public static ParserGrammar getInstance() {
        return LazyLexicalizedParserHolder.INSTANCE;
    }

    private static class LazyLexicalizedParserHolder {
        static final ParserGrammar INSTANCE = (new LazyLexicalizedParser()).pg;
    }

}
