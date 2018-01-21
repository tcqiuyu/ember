package edu.colostate.ember.nlp.legacy;

import edu.colostate.ember.util.StaticFields;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LazyPOSTagger {

    private static Logger logger = LoggerFactory.getLogger(LazyPOSTagger.class);
    private MaxentTagger tagger;

    private LazyPOSTagger() {

        logger.debug("Initializing POS tagger");
        tagger = new MaxentTagger(StaticFields.POS_TAGGER_MODEL);
        logger.debug("Loaded POS tagger");

    }

    public static MaxentTagger getInstance() {
        return LazyPOSTaggerHolder.INSTANCE;
    }

    private static class LazyPOSTaggerHolder {
        static final MaxentTagger INSTANCE = (new LazyPOSTagger()).tagger;
    }

}
