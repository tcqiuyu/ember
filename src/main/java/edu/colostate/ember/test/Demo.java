package edu.colostate.ember.test;


import edu.stanford.nlp.coref.CorefCoreAnnotations;
import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.ie.util.RelationTriple;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.naturalli.NaturalLogicAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;

import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Properties;

public class Demo {

    public static String inputPath = "input/Add Health Wave I.TXT";


    public static void main(String[] args) {

        // creates a StanfordCoreNLP object, with POS tagging, lemmatization, NER, parsing, and coreference resolution
        Properties props = new Properties();
//        String modPath = "model/edu/stanford/nlp/models/";
        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref, depparse, natlog, openie");
//        props.put("pos.model", modPath + "pos-tagger/english-left3words/english-left3words-distsim.tagger");
//        props.put("ner.model", modPath + "ner/english.all.3class.distsim.crf.ser.gz");
//        props.put("parse.model", modPath + "lexparser/englishPCFG.ser.gz");
////        props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
//        props.put("sutime.binders", "0");
//        props.put("sutime.rules", modPath + "sutime/defs.sutime.txt, " + modPath + "sutime/english.sutime.txt");
//        props.put("dcoref.demonym", modPath + "dcoref/demonyms.txt");
//        props.put("dcoref.states", modPath + "dcoref/state-abbreviations.txt");
//        props.put("dcoref.animate", modPath + "dcoref/animate.unigrams.txt");
//        props.put("dcoref.inanimate", modPath + "dcoref/inanimate.unigrams.txt");
//        props.put("dcoref.big.gender.number", modPath + "dcoref/gender.data.gz");
//        props.put("dcoref.countries", modPath + "dcoref/countries");
//        props.put("dcoref.states.provinces", modPath + "dcoref/statesandprovinces");
//        props.put("dcoref.singleton.model", modPath + "dcoref/singleton.predictor.ser");

        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        // read some text in the text variable
//        String text = "For how many years have you and [NAME] lived in the same household? How old are you? I am happy to see you. Do you think I am right?";
        String text = "NUMBER OF DAYS PER WEEK R EXERCISES 30+ MINUTES";
        // create an empty Annotation just with the given text
        Annotation document = new Annotation(text);

        // run all Annotators on this text
        pipeline.annotate(document);

        // these are all the sentences in this document
        // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
        List<CoreMap> sentences = document.get(CoreAnnotations.SentencesAnnotation.class);

        for (CoreMap sentence : sentences) {
            // traversing the words in the current sentence
            // a CoreLabel is a CoreMap with additional token-specific methods
            System.out.println(sentence.get(CoreAnnotations.TextAnnotation.class));
            for (CoreLabel token : sentence.get(CoreAnnotations.TokensAnnotation.class)) {
                // this is the text of the token
                String word = token.get(CoreAnnotations.TextAnnotation.class);
                // this is the POS tag of the token
                String pos = token.get(CoreAnnotations.PartOfSpeechAnnotation.class);
                // this is the NER label of the token
                String ne = token.get(CoreAnnotations.NamedEntityTagAnnotation.class);

                System.out.println(word + ":" + pos + ":" + ne);
            }
            Collection<RelationTriple> triples = sentence.get(NaturalLogicAnnotations.RelationTriplesAnnotation.class);

            for (RelationTriple triple : triples) {
                System.out.println(triple.confidence + ":" + triple.subjectLemmaGloss() + ":" + triple.relationLemmaGloss() + ":" + triple.objectLemmaGloss());
            }
//            }


            // this is the parse tree of the current sentence
            Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);

            // this is the Stanford dependency graph of the current sentence
            SemanticGraph dependencies = sentence.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation.class);
        }

        // This is the coreference link graph
        // Each chain stores a set of mentions that link to each other,
        // along with a method for getting the most representative mention
        // Both sentence and token offsets start at 1!
        Map<Integer, CorefChain> graph =
                document.get(CorefCoreAnnotations.CorefChainAnnotation.class);

    }
}
