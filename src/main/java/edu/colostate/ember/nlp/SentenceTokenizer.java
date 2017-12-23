package edu.colostate.ember.nlp;

import edu.stanford.nlp.ling.Word;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.process.WordTokenFactory;

import java.io.FileNotFoundException;
import java.io.StringReader;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

public class SentenceTokenizer implements Tokenizer<Word> {

    private DocumentPreprocessor dp;
    private List<Word> tokens;
    private int index = 0;
    private Iterator<Word> iter;


//    private String ptb3Escaping = "false";
//    private String[] puncWord = new String[]{".", "?", "!"};

//    public SentenceTokenizer(Reader input) {

//        dp = new DocumentPreprocessor(input);
//        String[] puncWord = new String[]{".", "*NL*"};
//        dp.setSentenceFinalPuncWords(puncWord);
//        dp.setTokenizerFactory(PTBTokenizer.coreLabelFactory("tokenizeNLs=true,ptb3Escaping=" + ptb3Escaping));
//        String rrb = ptb3Escaping.equals("true") ? "-RRB-" : ")";
//
//        sentences = new ArrayList<>();
//        String refNumber = "";
//        for (List<HasWord> sentence : dp) {
//
//            if (sentence.get(1).toString().equals(rrb)) {
//                refNumber = sentence.get(2).toString();
//            }
//
//            if (sentence.toString().contains("?")) {
//                sentence.add(new Word(refNumber));
//                sentences.add(sentence);
////                System.out.println(sentence);
//            }
//        }
//
//
//        iter = sentences.iterator();
//    }

    public SentenceTokenizer(String input) {
        this(input, "");
    }

    public SentenceTokenizer(String input, String option) {
        PTBTokenizer<Word> tokenizer = new PTBTokenizer<>(new StringReader(input), new WordTokenFactory(), option);
        this.tokens = tokenizer.tokenize();
        this.iter = tokens.iterator();
    }

    @Override
    public Word next() {
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
    public Word peek() {
        return tokens.get(index);
    }

    @Override
    public List<Word> tokenize() {
        return tokens;
    }

    public static void main(String[] args) throws FileNotFoundException {
//        SentenceTokenizer qt = new SentenceTokenizer(new FileReader(StaticFields.INPUT_PATH));
        SentenceTokenizer qt = new SentenceTokenizer("If Asian or Pacific Islander");
        System.out.println(Arrays.toString(qt.tokenize().toArray()));
//        while (true) {
//            System.out.println(qt.next());
//        }
    }

}
