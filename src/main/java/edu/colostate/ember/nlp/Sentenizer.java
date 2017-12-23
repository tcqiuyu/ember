package edu.colostate.ember.nlp;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.SentenceUtils;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.Tokenizer;

import java.io.Reader;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

public class Sentenizer implements Tokenizer<String> {

    private String[] puncWord = new String[]{".", "?", "!", "\n"};
    private DocumentPreprocessor dp;
    private String ptb3Escaping = "false";
    private List<String> sentences;
    private Iterator<String> iter;
    private int index = 0;
    private Reader input;

    public Sentenizer(Reader input) {
        this.input = input;
    }

    public Sentenizer setPuncWord(String[] puncWordList) {
        this.puncWord = puncWordList;
        return this;
    }

    public Sentenizer parseSentences() {
        dp = new DocumentPreprocessor(input);
        dp.setSentenceFinalPuncWords(puncWord);
        dp.setTokenizerFactory(PTBTokenizer.coreLabelFactory("ptb3Escaping=" + ptb3Escaping));

        sentences = new ArrayList<>();
        for (List<HasWord> sentenceTokenList : dp) {
            String sentence = SentenceUtils.listToString(sentenceTokenList);
            sentences.add(sentence);
        }


        iter = sentences.iterator();
        return this;
    }


    @Override
    public String next() {
        index++;
        return iter.next();
    }

    @Override
    public boolean hasNext() {
        return iter.hasNext();
    }

    @Override
    public void remove() {

    }

    @Override
    public String peek() {
        return sentences.get(index);
    }

    @Override
    public List<String> tokenize() {
        return sentences;
    }

    public static void main(String[] args) {
        Sentenizer sentenizer = new Sentenizer(new StringReader(" ( current survey round) == 11|   UNIVERSE: R's bio/adoptive dad alive; has been in contact with R since R1|   COMMENT: this is round 11")).parseSentences();
        List<String> a = sentenizer.tokenize();
        System.out.println(Arrays.asList(sentenizer.tokenize()));
    }
}
