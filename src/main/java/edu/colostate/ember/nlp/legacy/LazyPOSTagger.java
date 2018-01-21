package edu.colostate.ember.nlp.lazy;

import edu.colostate.ember.util.StaticFields;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LazyPOSTagger {

    private static Logger logger = LoggerFactory.getLogger(LazyLexicalizedParser.class);
    private MaxentTagger tagger;

    private LazyPOSTagger() {

        logger.info("Initializing POS tagger");
        tagger = new MaxentTagger(StaticFields.POS_TAGGER_MODEL);
        logger.info("Loaded POS tagger");

    }

    public static MaxentTagger getInstance() {
        return LazyPOSTaggerHolder.INSTANCE;
    }

    private static class LazyPOSTaggerHolder {
        static final MaxentTagger INSTANCE = (new LazyPOSTagger()).tagger;
    }

}
