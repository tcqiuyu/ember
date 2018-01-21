package edu.colostate.ember.util.visualization;

import org.graphstream.graph.Graph;
import org.graphstream.graph.implementations.SingleGraph;

public class GraphStreamCreator {

    public static void main(String[] args) {
        System.setProperty("org.graphstream.ui.renderer", "org.graphstream.ui.j2dviewer.J2DGraphRenderer");
        Graph graph = new SingleGraph("HELLO");
        graph.addNode("A" );
        graph.addNode("B" );
        graph.addNode("C" );
        graph.addEdge("AB", "A", "B");
        graph.addEdge("BC", "B", "C");
        graph.addEdge("CA", "C", "A");
        graph.display();


    }


}
