package net.sf.javaml.core;

import java.util.List;
import java.util.Random;
import java.util.Set;
import java.util.SortedSet;

import net.sf.javaml.distance.DistanceMeasure;
import net.sf.javaml.distance.DistanceMeasureCustomFBW;

public interface DatasetCustomFBW extends List<InstanceCustomFBW>{
	
	 public SortedSet<Object> classes();
	 
    public boolean add(InstanceCustomFBW i);
    
    public InstanceCustomFBW instance(int index);

    /**
     * Create a number of folds from the data set and return them. The supplied
     * random generator is used to determine which instances are assigned to
     * each of the folds.
     * 
     * @param numFolds
     *            the number of folds to create
     * @param rg
     *            the random generator
     * @return an array of data sets that contains <code>numFolds</code> data
     *         sets.
     */
    public DatasetCustomFBW[] folds(int numFolds, Random rg);

    /**
     * The number of attributes in each instance. This value can be off when
     * instances have different number of attributes. When the data set contains
     * no instances, this method should return 0.
     * 
     * @return
     */
    public int noAttributes();

    /**
     * Returns the index of the class value in the supplied data set. This
     * method will return -1 if the class value of this instance is not set.
     * 
     * @param data
     *            the data set to give the index for
     * @return the index of the class value
     */
    public int classIndex(Object clazz);

    /**
     * Returns the class value of the supplied class index.
     * 
     * @param index
     *            the index to give the class value for
     * @return the class value of the index
     */
    public Object classValue(int index);

    /**
     * Create a deep copy of the data set. This method should also create deep
     * copies of the instances in the data set.
     * 
     * @return deep copy of this data set.
     */
    public DatasetCustomFBW copy();

    /**
     * Returns the k closest instances.
     * 
     * @param k
     *            the number of neighbors to select
     * @param instance
     *            the instance to determine the neighbors for
     * @param dm
     *            the distance metric to use
     * @return a set of closest neighbors
     */
    public Set<InstanceCustomFBW> kNearest(int k, InstanceCustomFBW instance, DistanceMeasureCustomFBW dm);
}
