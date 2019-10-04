package customFBW;


import java.io.File;

import net.sf.javaml.clustering.Clusterer;
import net.sf.javaml.clustering.ClustererCustomFBW;
//import net.sf.javaml.clustering.KMedoids;
import net.sf.javaml.clustering.KMedoidsCustom;
import net.sf.javaml.core.Dataset;
import net.sf.javaml.core.DatasetCustomFBW;
import net.sf.javaml.tools.data.FileHandler;
import net.sf.javaml.distance.*;
/**
 * Customised code
 * 
 * 
 * @author fubao
 * 
 */
public class KMedoidClustering {

    /**
     * Tests the k-means algorithm with default parameter settings.
     */
	//public static String dataSetInput = "/home/fubao/Fubao/CiscoWish/QueryGraph/clusteringJava/output/outputtOrder1.csv";
	public static String dataSetInput = "/home/fubao/Fubao/CiscoWish/QueryGraph/clusteringJava/output/test2.csv";
    public static void main(String[] args) throws Exception {

        /* Load a dataset */
        DatasetCustomFBW data = FileHandler.loadDatasetCustomFBW(new File(dataSetInput), 4, ",");
        /*
         * Create a new instance of the KMeans algorithm, with no options
         * specified. By default this will generate 4 clusters.
         */
        CosineDistance cosDis = new CosineDistance();
        
        //Clusterer km = new KMedoids(3,100, cosDis);
       // ClustererCustomFBW km = new KMedoidsCustom(3,100, cosDis);
        ClustererCustomFBW km = new KMedoidsCustom();
        
        /*
         * Cluster the data, it will be returned as an array of data sets, with
         * each dataset representing a cluster
         */
        DatasetCustomFBW[] clusters = km.cluster(data);
        System.out.println("Cluster count: " + clusters.length);

    }

}
