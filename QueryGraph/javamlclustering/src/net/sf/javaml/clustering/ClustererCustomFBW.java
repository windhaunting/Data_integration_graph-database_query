
package net.sf.javaml.clustering;

import net.sf.javaml.core.DatasetCustomFBW;

/**
 * A common interface for all clustering techniques. There is only one method
 * that should be implemented.
 * 
 * @author Thomas Abeel
 * 
 */
public interface ClustererCustomFBW {
    /**
     * This method will execute the clustering algorithm on a particular
     * data set. The result will be an array of Dataset where each data set is a
     * cluster.
     * 
     * @param data
     *            the data set on which to execute the clustering.
     * @return the different clusters obtained by this clustering algorithm.
     *         Each cluster is represented as a separate data set.
     */
    public DatasetCustomFBW[] cluster(DatasetCustomFBW data);

}