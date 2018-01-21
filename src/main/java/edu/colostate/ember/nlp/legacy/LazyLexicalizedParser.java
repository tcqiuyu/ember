package edu.colostate.ember.nlp.legacy;

import edu.colostate.ember.util.StaticFields;
import edu.stanford.nlp.parser.common.ParserGrammar;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import scala.util.parsing.combinator.lexical.Lexical;

public class LazyLexicalizedParser {

    private static Logger logger = LoggerFactory.getLogger(LazyLexicalizedParser.class);
    private LexicalizedParser lexicalizedParser;

    private LazyLexicalizedParser() {

        logger.debug("Initializing lexical parser w/ default model");
        lexicalizedParser = LexicalizedParser.loadModel(StaticFields.LEXPARSER_MODEL);
        logger.debug("Loaded default lex-parser");

    }

    public static LexicalizedParser getInstance() {
        return LazyLexicalizedParserHolder.INSTANCE;
    }

    private static class LazyLexicalizedParserHolder {
        static final LexicalizedParser INSTANCE = (new LazyLexicalizedParser()).lexicalizedParser;
    }

}
