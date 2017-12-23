package edu.colostate.ember.util;

public class StaticFields {
    public static final String ANSI_RED = "\u001B[31m";
    public static final String ANSI_RESET = "\u001B[0m";
    public static final String ANSI_YELLOW = "\u001B[33m";
    public static final String ANSI_BLUE = "\u001B[34m";


    public static final String ADDHEALTH_INPUT_PATH = "data/input/Add_health_question_text.txt";
    public static final String ADDHEALTH_INTERMEDIATE_PATH = "data/intermediate/add_health_interm";
    public static final String NLSY_RAW_PATH = "data/input/nlsy_response";
    public static final String NLSY_INPUT_PATH = "data/input/NLSY_question_text_response";
    public static final String NLSY_INTERMEDIATE_PATH = "data/intermediate/nlsy_interm";

    // model path
    public static final String LEXPARSER_MODEL = "model/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
    public static final String SHIFTPARSER_MODEL = "model/edu/stanford/nlp/models/srparser/englishSR.ser.gz";
    public static final String POS_TAGGER_MODEL = "model/edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger";
    public static final String DEPENDENCY_PARSER_MODEL = "model/edu/stanford/nlp/models/parser/nndep/english_SD.gz";


    public static final String BRACKET_PATTERN = "\\[[^\\[\\]]*\\]";
    public static final String PAREN_PATTERN = "\\([^\\(\\)]*\\)|\\(([^\\(\\)]*\\([^\\(\\)]*\\)[^\\(\\)]*)*\\)"; //Can handle one level nested parenthesis.
    //    public static final String PAREN_PATTERN = "\\([^\\(\\)]*\\)";
    public static final String BRACKETORPAREN_PATTERN = "[\\(\\[\\{][^\\(\\)\\[\\]\\{\\}]*[\\)\\]\\}]";
    public static final String REFLINE_PATTERN = "^\\d+\\)\\s[\\dA-Z_]*$";
    public static final String PUNCWORDINBRACKET_PATTERN = "[:.!](?=[^\\(]*\\))";


    public static final String NLSY_REF_PATTERN = "^[A-Z][0-9]{5}.[0-9]{2}.*$";
    public static final String NLSY_FREQ_TABLE_PATTERN = "^Refusal\\(-1\\).*|^\\s+\\d+.*";
    public static final String NLSY_DASH_PATTERN = "^-+";
    public static final String NLSY_COUNT_PATTERN = "^TOTAL =+>\\s+\\d+\\s+VALID SKIP\\(-4\\)\\s+\\d+\\s+NON-INTERVIEW\\(-5\\)\\s+\\d+.*";
    public static final String NLSY_RESPONSE_PATTERN = "RESPONSE CHOICE: \".*\"";
    public static final String NLSY_NESTED_BRACKET_PATTERN = "(\\s\\()*";
    public static final int NLSY_COUNT_TOTAL_IDX = 2;
    public static final int NLSY_COUNT_SKIP_IDX = 5;
    public static final int NLSY_COUNT_NON_INTERVIEW_IDX = 7;
    public static final double NLSY_VALID_QUESTIONNAIRE_THRESHOLD = 0.1;

    public static final String ADDHEALTH_WEBPAGE_URLBASE = "http://www.cpc.unc.edu/projects/addhealth/documentation/ace/tool/codebookssearch?field=varname&match=contains&text=";


    public static void main(String[] args) {
        String a = "When did you start [ ( kindergarten , first grade , . . . nth year in college ) ] for [ this school ] ( [ ( loop ) ] ) for the enrollment period [ beginning on date/ending on date/from start to end date/at this school ] ( [ ( loop ) ] :[ ( loop ) ] ) ?\n";
        String b = "( HAND R SHOWCARD D )";
        String c = "The lowest value for the top 2 percent of cases is used as the truncation level ( $ 23,000 for this variable ) .";
        String d = "( During the enrollment period beginning ( date ) / During the enrollment period ending in ( date ) / During this enrollment period/Between start and stop date ) were there any periods of four weeks or more during which you did not attend ( this school ) ( loop ) ?";
//        a = TextUtil.removePuncWordInBracket(a);
//        a = a.replaceAll("[\\[\\{]", "(").replaceAll("[\\]\\}]",")").replaceAll("(\\(\\s)+"," ( ").replaceAll("(\\)\\s)+",") ");

        String e = "oo(aa(bb)aa(bb))";
        String f = "RESPONSE CHOICE: \"Medical, surgical or hospitalization insurance which covers                        injuries or major illnesses of the job\"";

        System.out.println(f.replaceAll("\\s+", " "));
//        System.out.println(d.replaceFirst("\\([^\\(\\)]*\\)|\\(([^\\(\\)]*\\([^\\(\\)]*\\)[^\\(\\)]*)*\\)", "cc"));
//        Pattern p = Pattern.compile("\\([^\\(\\)]*\\)|\\([^\\(\\)]*\\([^\\(\\)]*\\)*\\)\\)");
//        Matcher m = p.matcher(e);
//        while (m.find()) {
//            System.out.println(m.groupCount());
//            System.out.println(m.group(0));
//        }
//        String[] b = a.split("\\s+");
//        System.out.println(b[2] + "," + b[5] + "," + b[7]);

    }
}
