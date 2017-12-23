package edu.colostate.ember.util;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TextUtil {

    public static List<String> extractPatterns(String sentence, String pattern) {

        List<String> patterns = new ArrayList<>();
        Pattern p = Pattern.compile(pattern);
        Matcher m = p.matcher(sentence);

        while (m.find()) {
            String group = m.group();
//            System.out.println(group);
            patterns.add(group);
        }
//        System.out.println(m.group(1));
        return patterns;
    }

    public static List<String> extractTopLevelBrackets(String input) {
        List<String> brackets = new ArrayList<>();


        return brackets;
    }

    public static String removePuncWordInBracket(String input) {
        input = input.replaceAll(StaticFields.PUNCWORDINBRACKET_PATTERN, "");

        return input;
    }

    public static String listToString(List<String> list) {
        String out = "";
        if (list.size() == 0) {
            return out;
        } else {
            for (String s : list) {
                out = out.concat(s.replaceAll("\\s+", " ").replaceAll("^\\W", "")).replaceAll("[\\(\\)]", "").concat("|");
            }
            return out.substring(0, out.length() - 1);
        }
    }

    public static boolean isUpperCase(String s) {

        for (int i = 0; i < s.length(); i++) {
            if (Character.isLowerCase(s.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        String sentence = "UNIVERSE : R > = 14 has valid employer ; not military ; employer stopdate > = 16 ; job last 13 + weeks ; job last 2 + weeks since DLI ; not self-employed\n";
        String ss = "12) H1GI2";
        System.out.println(sentence.matches(".*(UNIVERSE|COMMENT).*\n"));
//        extractPatterns(ss, StaticFields.REFLINE_PATTERN);
//        extractPatterns(sentence, StaticFields.BRACKET_PATTERN);
//        extractPatterns(sentence, StaticFields.BRACKET_PAREN_PATTERN);
//        sentence = sentence.replaceAll(StaticFields.BRACKET_PATTERN, "");
//        sentence = sentence.replaceFirst(StaticFields.BRACKET_PATTERN, "{}").replaceFirst(StaticFields.BRACKET_PATTERN, "[]");

//        sentence = replacePatterns(sentence, StaticFields.BRACKET_PATTERN, "[]");
//        extractPatterns(sentence, "e.", "R");
//        System.out.println(sentence);
    }

}
