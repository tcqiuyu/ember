package edu.colostate.ember.util.networking;

import edu.colostate.ember.util.StaticFields;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.io.*;

public class WebpageParser {

    private static String getAddHealthQuestionText(String variableName) throws IOException {
        Document doc = Jsoup.connect(StaticFields.ADDHEALTH_WEBPAGE_URLBASE + variableName).get();
        String out = "";
        try {
            out = doc.getElementById("searchresults").getElementsByTag("td").get(2).html();
        } catch (IndexOutOfBoundsException e) {
            System.err.println(variableName);
        }
        return out;
    }


    public static void main(String[] args) throws IOException {
        System.out.println(getAddHealthQuestionText("H1WS6E"));

        BufferedReader bufferedReader = new BufferedReader(new FileReader("input/Add Health Wave I.TXT"));

        String line = "";
        String ref = "";
        String question = "";
        String supplement = "";


        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter("input/Add_health_question_text.txt", true));

        while (bufferedReader.ready()) {
            line = bufferedReader.readLine();

            if (line.matches(StaticFields.REFLINE_PATTERN)) {
                ref = line.split("\\s")[1];
                String questionText = WebpageParser.getAddHealthQuestionText(ref);
                if (!questionText.equals("")) {
                    bufferedWriter.write(ref + "|" + questionText + "\n");
                }
            }
        }
        bufferedReader.close();
        bufferedWriter.flush();
        bufferedWriter.close();
    }
}
