package edu.colostate.ember.util;

import edu.colostate.ember.nlp.QuestionLexParser;
import edu.colostate.ember.nlp.Sentenizer;
import edu.stanford.nlp.trees.Tree;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class AddHealthUtil {

    private static String parsingBrackets(String input, QuestionLexParser qp) {
        List<String> brackets = TextUtil.extractPatterns(input, StaticFields.BRACKETORPAREN_PATTERN);
        List<String> subs = new ArrayList<>();

        for (String bracket : brackets) {
            Tree parse = qp.parseToken(bracket);

            bracket = bracket.substring(1, bracket.length() - 1).trim();

            if (bracket.contains("/")) {
                subs.add(bracket.split("\\/")[0].trim());
            } else if (bracket.matches("[A-Z]*")) {
                subs.add("John");
            } else if (parse.firstChild().label().toString().equals("NP")) {
                subs.add(bracket);
            } else {
                subs.add("");
            }
        }

        for (String sub : subs) {
//            System.out.println(StaticFields.ANSI_RED + sub + StaticFields.ANSI_RESET);
            input = input.replaceFirst(StaticFields.BRACKETORPAREN_PATTERN, sub);
//            LogUtil.printErr(input);
        }
        return input;
    }


    private static void phase1() throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new FileReader(StaticFields.ADDHEALTH_INPUT_PATH));

        String line = "";
        String ref = "";
        String main_text = "";


        QuestionLexParser qp = new QuestionLexParser();

//        qp.loadShiftReduceModel();
        File out = new File(StaticFields.ADDHEALTH_INTERMEDIATE_PATH);
        if (out.exists()) {
            System.out.println(StaticFields.ADDHEALTH_INTERMEDIATE_PATH + " exists, deleted");
            out.delete();
        }

        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(StaticFields.ADDHEALTH_INTERMEDIATE_PATH, true));

        while ((line = bufferedReader.readLine()) != null) {
            boolean hasQuestion = false;
            List<String> supplement = new ArrayList<>();

            ref = line.split("\\|")[0];
            line = TextUtil.removePuncWordInBracket(line.split("\\|")[1]);

            List<String> sentences = new Sentenizer(new StringReader(line)).parseSentences().tokenize();

            if (sentences.size() == 1) {
                hasQuestion = true;
                main_text = sentences.get(0);
                if (main_text.matches(StaticFields.BRACKET_PATTERN)) {
                    main_text = parsingBrackets(main_text, qp);
                }
            } else {
                for (String sentence : sentences) {
                    if (sentence.matches(StaticFields.BRACKET_PATTERN)) {
                        sentence = parsingBrackets(sentence, qp);
//                        System.out.println(sentence);
                    }
                    sentence = sentence.trim();
                    Tree parseTree = qp.parseToken(sentence);
                    String firstLabel = parseTree.firstChild().label().value();

                    if (hasQuestion) {
                        supplement.add(sentence);
                    } else if (sentence.contains("?")) {
                        hasQuestion = true;
                        main_text = sentence;
                    } else if (firstLabel.matches("SBARQ|SINV|SQ")) {
                        hasQuestion = true;
                        main_text = sentence;
                    } else {
//                        main_text = "";
                        supplement.add(sentence);
                    }
                }
            }
            main_text = hasQuestion ? main_text : "";
            bufferedWriter.write(ref + "|" + main_text + "|" + TextUtil.listToString(supplement) + "\n");
        }

        bufferedReader.close();
        bufferedWriter.flush();
        bufferedWriter.close();
    }


    public static void main(String[] args) throws IOException {
        phase1();
    }


}
