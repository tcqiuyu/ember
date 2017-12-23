package edu.colostate.ember.test;

import edu.colostate.ember.structure.DependencyTreeFactory;
import edu.colostate.ember.util.StaticFields;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.TreeGraphNode;
import edu.stanford.nlp.trees.TypedDependency;
import edu.stanford.nlp.util.logging.Redwood;

import java.io.StringReader;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class TEST_QuestionDependencyParser {
    private static Redwood.RedwoodChannels log = Redwood.channels(TEST_QuestionDependencyParser.class);

    //    public static void extractCore
    public static void main(String[] args) {
        String modelPath = "model/edu/stanford/nlp/models/parser/nndep/english_SD.gz";
        String taggerPath = "model/edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger";

        for (int argIndex = 0; argIndex < args.length; ) {
            switch (args[argIndex]) {
                case "-tagger":
                    taggerPath = args[argIndex + 1];
                    argIndex += 2;
                    break;
                case "-model":
                    modelPath = args[argIndex + 1];
                    argIndex += 2;
                    break;
                default:
                    throw new RuntimeException("Unknown argument " + args[argIndex]);
            }
        }

        String text = "$ 23,000 for this variable";

//        String text = "How many PARTNERS have you had sexual intercourse with since the last interview  on [date of last interview]?";
        MaxentTagger tagger = new MaxentTagger(StaticFields.POS_TAGGER_MODEL);
        DependencyParser parser = DependencyParser.loadFromModelFile(StaticFields.DEPENDENCY_PARSER_MODEL);
        DocumentPreprocessor tokenizer = new DocumentPreprocessor(new StringReader(text));
        for (List<HasWord> sentence : tokenizer) {
            List<TaggedWord> tagged = tagger.tagSentence(sentence);
            GrammaticalStructure gs = parser.predict(tagged);
            Collection<TypedDependency> dependencies = gs.typedDependencies();

            TreeGraphNode root = gs.root();
//            for (TypedDependency dependency : dependencies) {
//                System.out.println(dependency.gov().get(CoreAnnotations.IndexAnnotation.class));
//            }

//             Print typed dependencies
//            log.info(gs);
            ArrayList<TypedDependency> dependencies1 = (ArrayList<TypedDependency>) gs.typedDependencies(GrammaticalStructure.Extras.NONE);

            DependencyTreeFactory.constructDependencyTree(dependencies1);
            gs.root().pennPrint();
            System.out.println(gs);
        }
    }

}
