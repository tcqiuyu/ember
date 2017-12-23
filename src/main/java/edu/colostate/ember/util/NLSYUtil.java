package edu.colostate.ember.util;

import edu.colostate.ember.nlp.QuestionLexParser;
import edu.colostate.ember.nlp.SentenceTokenizer;
import edu.colostate.ember.nlp.Sentenizer;
import edu.colostate.ember.structure.DependencyTreeFactory;
import edu.colostate.ember.structure.DependencyTreeNode;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TypedDependency;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class NLSYUtil {

//    private static String nlsyroot = "rawData/NLSY97/NLSY97_Public";
//    private static String nlsyoutput = "data/input/NLSY_question_text";

    private static MaxentTagger tagger = new MaxentTagger(StaticFields.POS_TAGGER_MODEL);
    private static DependencyParser parser = DependencyParser.loadFromModelFile(StaticFields.DEPENDENCY_PARSER_MODEL);
    private static QuestionLexParser qp = new QuestionLexParser();

    private static void processNLSYCodebook(Path path) {

        try {
            BufferedReader bufferedReader = new BufferedReader(new FileReader(path.toString()));
            System.out.println("Processing file: " + path.toString() + "\t File size; " + Files.size(path) / 1024.0 / 1024.0);

//            System.out.println(bufferedReader.readLine());
            String line;
            String ref, year;
            String title, text;
            BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(StaticFields.NLSY_INPUT_PATH, true));

            while ((line = bufferedReader.readLine()) != null) {


//                line = bufferedReader.readLine();

                if (line.matches(StaticFields.NLSY_REF_PATTERN)) {
                    ref = line.split("\\s+")[0].replace(".", "");

                    year = line.split("\\s+")[4];
                    if (!year.matches("\\d+")) {
                        continue;
                    }
                    skipLines(bufferedReader, 3);
                    title = bufferedReader.readLine().trim();
                    if (title.contains("ROS ITEM")) {
                        continue;
                    }
//                    System.out.println(path + ":" + ref + ":" + title);
                    skipLines(bufferedReader, 1);
                    text = appendUntil(bufferedReader, StaticFields.NLSY_FREQ_TABLE_PATTERN).trim();
//                    System.out.println(text);
                    String[] counts = readUntil(bufferedReader, StaticFields.NLSY_COUNT_PATTERN).split("\\s+");
                    Double totalCount = Double.parseDouble(counts[StaticFields.NLSY_COUNT_TOTAL_IDX]);
                    Double skipCount = Double.parseDouble(counts[StaticFields.NLSY_COUNT_SKIP_IDX]);
                    Double nonInterviewCount = Double.parseDouble(counts[StaticFields.NLSY_COUNT_NON_INTERVIEW_IDX]);
//                    LogUtil.printErr(totalCount + ":" + skipCount + ":" + nonInterviewCount);
                    readUntil(bufferedReader, StaticFields.NLSY_DASH_PATTERN);

                    Double validPercent = totalCount / (totalCount + skipCount + nonInterviewCount);
                    if (validPercent >= StaticFields.NLSY_VALID_QUESTIONNAIRE_THRESHOLD) {
                        bufferedWriter.write(ref + "|" + title + "|" + text + "\n");
                    }

                }

            }
            bufferedReader.close();
            bufferedWriter.flush();
            bufferedWriter.close();

        } catch (IOException e1) {
            e1.printStackTrace();
        }

    }

    private static void skipLines(BufferedReader reader, int number) throws IOException {
        for (int i = 0; i < number; i++) {
            reader.readLine();
        }

    }

    private static String appendUntil(BufferedReader reader, String pattern) throws IOException {
        String line, out = "";
        while ((line = reader.readLine()) != null) {
            if (line.matches(pattern)) {
                return out;
            } else if (line.trim().equals("")) {
                out = out.concat("\t");
            }
            out = out.concat(" " + line);
        }
        return null;
    }

    private static String readUntil(BufferedReader reader, String pattern) throws IOException {
        String line;
        while ((line = reader.readLine()) != null) {
            if (line.matches(pattern)) {
                return line;
            }
        }
        return null;
    }

    private static boolean filterCodebook(Path path) {
        return path.toString().matches(".*(?<!Survey-Methodology)\\.cdb");
//        System.out.println(path);
//        return path.toString().endsWith("cdb");
    }

    private static void phase1() {
        File out = new File(StaticFields.NLSY_INPUT_PATH);
        if (out.exists()) {
            System.out.println(StaticFields.NLSY_INPUT_PATH + " exists. Deleted");
            out.delete();
        }

        try (Stream<Path> paths = Files.walk(Paths.get(StaticFields.NLSY_RAW_PATH))) {
            paths.filter(NLSYUtil::filterCodebook)
                    .forEach(NLSYUtil::processNLSYCodebook);

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    private static DependencyTreeNode extractDependencyTree(String input) {
        List<? extends HasWord> words = new SentenceTokenizer(input).tokenize();
        List<TaggedWord> taggedWords = tagger.tagSentence(words);
        GrammaticalStructure gs = parser.predict(taggedWords);
        Collection<TypedDependency> dependencies = gs.typedDependencies();

        DependencyTreeNode dependencyTree = DependencyTreeFactory.constructDependencyTree((ArrayList<TypedDependency>) dependencies);
        return dependencyTree;
    }

    private static String getCoreforNP(String input) {
        DependencyTreeNode tree = extractDependencyTree(input);
        return tree.getChildren().iterator().next().getWord().value();
    }

    private static String parsingBrackets(String input) {
        List<String> brackets = TextUtil.extractPatterns(input, StaticFields.PAREN_PATTERN);
        List<String> subs = new ArrayList<>();

        for (String bracket : brackets) {
            bracket = bracket.replaceAll("[\\(\\[\\{\\)\\]\\}]", "").trim();
            Tree parse = qp.parseToken(bracket);

            String firstLabel = parse.firstChild().label().value();

            if (bracket.contains("loop") || bracket.equals("figure") || TextUtil.isUpperCase(bracket)) {
                subs.add("");
            } else if (bracket.contains("/")) {
                subs.add(bracket.split("\\/")[0].trim());
            } else if (firstLabel.equals("FRAG")) {
                String secondLabel = parse.firstChild().firstChild().label().value();
                if (secondLabel.equals("NP")) {
                    subs.add(getCoreforNP(bracket));
                } else {
                    subs.add("");
                }
            } else if (firstLabel.equals("NP")) {
                subs.add(getCoreforNP(bracket).replaceAll("\\$", ""));
            } else {
                subs.add("");
            }
        }

        for (String sub : subs) {
            input = input.replaceFirst(StaticFields.PAREN_PATTERN, sub);
        }
//        LogUtil.printInfo(input);
        return input;


    }

    private static void phase2() throws IOException {

        BufferedReader bufferedReader = new BufferedReader(new FileReader(StaticFields.NLSY_INPUT_PATH));
        File out = new File(StaticFields.NLSY_INTERMEDIATE_PATH);
        if (out.exists()) {
            System.out.println(StaticFields.NLSY_INTERMEDIATE_PATH + " exists. Deleted");
            out.delete();
        }

        String line, ref, main_text;
        List<String> supplement;

        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(StaticFields.NLSY_INTERMEDIATE_PATH, true));

        while ((line = bufferedReader.readLine()) != null) {
            String[] parts = line.split("\\|");
            ref = parts[0];
            main_text = "";
            supplement = new ArrayList<>();
            // Deal with nested bracket, some stupid lines like: "When did you start [ ( kindergarten , first grade , . . . nth year in college ) ] for [ this school ] ( [ ( loop ) ] ) for the enrollment period [ beginning on date/ending on date/from start to end date/at this school ] ( [ ( loop ) ] :[ ( loop ) ] ) ?"
            // Replace all brackets to paren, then replace nested with single ones.
            line = parts[2].replaceAll("[\\[\\{]", "(").replaceAll("[\\]\\}]", ")").replaceAll("(\\(\\s*)+", " ( ").replaceAll("(\\)\\s*)+", ") ").replaceAll("\t", "\n");

            if (ref.equals("S3701000")) {
                System.out.println();
            }
            //extract response choice
            Pattern p = Pattern.compile(StaticFields.NLSY_RESPONSE_PATTERN);
            Matcher m = p.matcher(line);
            while (m.find()) {
                String group = m.group();
                line = line.replace(group, "");
//                System.out.println(group);
                supplement.add(group);
            }

//            System.out.println(line);
            List<String> sentences = new Sentenizer(new StringReader(line)).setPuncWord(new String[]{".", "?", "!"}).parseSentences().tokenize();
//            sentences.forEach(LogUtil::printErr);
            for (String sentence : sentences) {

                if (sentences.size() == 1) {
                    main_text = sentence;
                }

                if (sentence.matches("^.*(UNIVERSE|COMMENT) :.*")) {//Skip Universe/Comment
                    continue;
                } else if (sentence.matches(StaticFields.BRACKETORPAREN_PATTERN)) {// Skip paren/bracket
                    continue;
//                    LogUtil.printErr(sentence);
                } else if (TextUtil.isUpperCase(sentence)) {// Skip Upper case
                    continue;
                }
                sentence = parsingBrackets(sentence).trim();

                if (sentence.contains("?")) {
                    main_text = sentence;
                } else {
                    supplement.add(sentence);
                }
//                System.out.println(sentence);
            }
            main_text = main_text.replaceAll("\\s+", " ").replaceAll("^[\\W\\(]", "").replaceAll("[\\(\\)]", "");

            if (main_text.equals("") && supplement.size() == 0) {
                continue;
            }

            bufferedWriter.write(ref + "|" + main_text + "|" + TextUtil.listToString(supplement) + "\n");

        }
        bufferedWriter.flush();
        bufferedWriter.close();
        bufferedReader.close();
    }

    public static void main(String[] args) throws IOException {
//        phase1();
        phase2();
    }

}
