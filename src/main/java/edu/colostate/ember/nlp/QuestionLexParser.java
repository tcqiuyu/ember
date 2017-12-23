package edu.colostate.ember.nlp;

import edu.colostate.ember.util.StaticFields;
import edu.stanford.nlp.ling.SentenceUtils;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.ling.Word;
import edu.stanford.nlp.parser.common.ParserGrammar;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.parser.shiftreduce.ShiftReduceParser;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.Tree;

import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.List;

public class QuestionLexParser {
    //    private LexicalizedParser lp;
    private ParserGrammar pg;
    //    private ShiftReduceParser sp;
    private MaxentTagger tagger;
    private String model = "lexical";

    public QuestionLexParser() {
        pg = LexicalizedParser.loadModel(StaticFields.LEXPARSER_MODEL);
//        sp = ShiftReduceParser.loadModel(StaticFields.SHIFTPARSER_MODEL);
//        tagger = new MaxentTagger(StaticFields.POS_TAGGER_MODEL);
    }

    public QuestionLexParser loadLexicalModel() {
        pg = LexicalizedParser.loadModel(StaticFields.LEXPARSER_MODEL);
        model = "lexical";
        return this;
    }

    public QuestionLexParser loadShiftReduceModel() {
        pg = ShiftReduceParser.loadModel(StaticFields.SHIFTPARSER_MODEL);
        tagger = new MaxentTagger(StaticFields.POS_TAGGER_MODEL);
        model = "shiftreduce";
        return this;
    }

    public Tree parseToken(List<Word> tokens) {

        Tree parse;

        switch (model) {
            case "lexical":
                parse = pg.apply(tokens);
                return parse;
            case "shiftreduce":
                List<TaggedWord> taggedWords = tagger.tagSentence(tokens);
                parse = pg.apply(taggedWords);
                return parse;
            default:
                return null;
        }
//        parse.pennPrint();
//        System.out.println(parse.firstChild().label());
    }

    public Tree parseToken(String sentence) {
        List<String> array = Arrays.asList(sentence.split("\\s+"));
        List<Word> rawWords = SentenceUtils.toUntaggedList(array);

        return parseToken(rawWords);
    }


    public static void main(String[] args) throws FileNotFoundException {
////        SentenceTokenizer qt = new SentenceTokenizer(new FileReader(StaticFields.INPUT_PATH));
        SentenceTokenizer qt = new SentenceTokenizer("( this school )");
        QuestionLexParser lexParser = new QuestionLexParser();
        List<Word> sentences = qt.tokenize();
        Tree tree = lexParser.parseToken(sentences);
        System.out.println("HE");

//

//        lexParser.parseToken("If Asian or Pacific Islander").pennPrint();
//
//
//        for (List<HasWord> sentence : sentences) {
//
////            List<CoreLabel> rawWords = SentenceUtils.toCoreLabelList(sentence.subList(0, sentence.size() - 1));
//            String rawSentence = SentenceUtils.listToString(sentence.subList(0, sentence.size() - 1));
//            String refNumber = SentenceUtils.listToString(sentence.subList(sentence.size() - 1, sentence.size()));
////            String.join(" ", rawWords);
////            System.out.println(refNumber);
////            qp.parseToken(rawWords);
//
//        }


    }
}
