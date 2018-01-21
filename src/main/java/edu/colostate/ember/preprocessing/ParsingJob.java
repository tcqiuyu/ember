package edu.colostate.ember.preprocessing;

import edu.colostate.ember.nlp.legacy.LazyLexicalizedParser;
import edu.colostate.ember.util.StaticFields;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.SentenceUtils;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.trees.Tree;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.util.Arrays;
import java.util.List;

public class ParsingJob {

    private static Logger logger = LoggerFactory.getLogger(ParsingJob.class);

    public static void parse(String input, String output) throws IOException {
        logger.info("Start parsing from " + input + "to " + output);
        LexicalizedParser lexicalizedParser = LazyLexicalizedParser.getInstance();

        BufferedReader bufferedReader = new BufferedReader(new FileReader(input));

        File out = new File(output);
        if (out.exists()) {
            logger.warn(StaticFields.ADDHEALTH_INTERMEDIATE2_PATH + " exists, deleted");
            out.delete();
        }

        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(output, true));

        String line = "";
        int i = 0;
        while ((line = bufferedReader.readLine()) != null) {
            i++;
            if (i % 1000 == 0) {
                logger.trace("In progress... parsed " + i + " lines");
            }

            String[] linesplit = line.split("\\|");
            String ref = linesplit[0];
            bufferedWriter.write(ref);

            for (String sect : Arrays.copyOfRange(linesplit, 1, linesplit.length)) {

                bufferedWriter.write("||" + sect);
                if (sect.equals("")) {
                    bufferedWriter.write(" ");
                    continue;
                }
                List<CoreLabel> rawWords = SentenceUtils.toCoreLabelList(sect);
                Tree parseTree = lexicalizedParser.apply(rawWords);
                bufferedWriter.write("|" + parseTree.toString());
            }
            bufferedWriter.write("\n");
        }
        logger.info("Done! Parsed " + i + " lines");
        logger.trace("Closing buffered reader and buffered writer...");
        bufferedReader.close();
        bufferedWriter.flush();
        bufferedWriter.close();
    }

    public static void main(String[] args) throws IOException {
        parse(StaticFields.ADDHEALTH_INTERMEDIATE_PATH, StaticFields.ADDHEALTH_INTERMEDIATE2_PATH);
        parse(StaticFields.NLSY_INTERMEDIATE_PATH, StaticFields.NLSY_INTERMEDIATE2_PATH);
    }
}
