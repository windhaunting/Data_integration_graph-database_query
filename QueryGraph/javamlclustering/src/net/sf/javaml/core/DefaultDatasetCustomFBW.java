
/**
 * added by fubao
 * 

 * 
 */
package net.sf.javaml.core;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;
import java.util.Vector;

import net.sf.javaml.distance.DistanceMeasure;
import net.sf.javaml.distance.DistanceMeasureCustomFBW;

/**
 * Provides a standard data set implementation.
 * 
 * @see Dataset
 * 
 * @author Thomas Abeel
 * 
 */

public class DefaultDatasetCustomFBW extends Vector<InstanceCustomFBW> implements DatasetCustomFBW {

    private int maxAttributes = 0;

    /**
     * 
     * Creates a data set that contains the provided instances
     * 
     * @param coll
     *            collection with instances
     */
    public DefaultDatasetCustomFBW(Collection<InstanceCustomFBW> coll) {
        this.addAll(coll);
    }

    /**
     * Creates an empty data set.
     */
    public DefaultDatasetCustomFBW() {
        // nothing to do.
    }

    private void check(Collection<? extends InstanceCustomFBW> c) {
        for (InstanceCustomFBW i : c)
            check(i);
    }
    
    
    
    private void check(InstanceCustomFBW i) {

        if (i.classValue() != null)
            classes.add(i.classValue());
        if (i.noAttributes() > maxAttributes)
            maxAttributes = i.noAttributes();
    }

    @Override
    public synchronized boolean addAll(Collection<? extends InstanceCustomFBW> c) {
        check(c);
        return super.addAll(c);
    }

    @Override
    public synchronized boolean addAll(int index, Collection<? extends InstanceCustomFBW> c) {
        check(c);
        return super.addAll(index, c);
    }

    private static final long serialVersionUID = 8586030444860912681L;

    private TreeSet<Object> classes = new TreeSet<Object>();

    @Override
    public void clear() {
        classes.clear();
        super.clear();
    }

    @Override
    public synchronized boolean add(InstanceCustomFBW e) {
        check(e);
        return super.add(e);
    }

    @Override
    public void add(int index, InstanceCustomFBW e) {
        check(e);
        super.add(index, e);
    }

    @Override
    public synchronized void addElement(InstanceCustomFBW e) {
        check(e);
        super.addElement(e);
    }

    @Override
    public synchronized void insertElementAt(InstanceCustomFBW e, int index) {
        check(e);
        super.insertElementAt(e, index);
    }

    @Override
    public synchronized void setElementAt(InstanceCustomFBW e, int index) {
        check(e);
        super.setElementAt(e, index);
    }

    @Override
    public InstanceCustomFBW instance(int index) {
        return super.get(index);
    }

    @Override
    public SortedSet<Object> classes() {
        return classes;
    }

    /**
     * Returns the k instances of the given data set that are the closest to the
     * instance that is given as a parameter.
     * 
     * @param dm
     *            the distance measure used to calculate the distance between
     *            instances
     * @param inst
     *            the instance for which we need to find the closest
     * @return the instances from the supplied data set that are closest to the
     *         supplied instance
     * 
     */
    @Override
    public Set<InstanceCustomFBW> kNearest(int k, InstanceCustomFBW inst, DistanceMeasureCustomFBW dm) {
        Map<InstanceCustomFBW, Double> closest = new HashMap<InstanceCustomFBW, Double>();
        double max = dm.getMaxValue();
        for (InstanceCustomFBW tmp : this) {
            double d = dm.measure(inst, tmp);
            if (dm.compare(d, max) && !inst.equals(tmp)) {
                closest.put(tmp, d);
                if (closest.size() > k)
                    max = removeFarthest(closest,dm);
            }

        }
        return closest.keySet();
    }

    /*
     * Removes the element from the vector that is farthest from the supplied
     * element.
     */
    private double removeFarthest(Map<InstanceCustomFBW, Double> vector,DistanceMeasureCustomFBW dm) {
        InstanceCustomFBW tmp = null;// ; = vector.get(0);
        double max = dm.getMinValue();
        //System.out.println("minvalue:"+max);
        for (InstanceCustomFBW inst : vector.keySet()) {
            double d = vector.get(inst);
            
            if (dm.compare(max,d)) {
                max = d;
                tmp = inst;
            }
           // System.out.println("d="+d+"\t"+max);
        }
        vector.remove(tmp);
        return max;

    }

    @Override
    public DatasetCustomFBW[] folds(int numFolds, Random rg) {
        DatasetCustomFBW[] out = new DatasetCustomFBW[numFolds];
        List<Integer> indices = new Vector<Integer>();
        for (int i = 0; i < this.size(); i++)
            indices.add(i);
        int size = (this.size() / numFolds) + 1;
        int[][] array = new int[numFolds][size];
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < numFolds; j++) {
                if (indices.size() > 0)
                    array[j][i] = indices.remove(rg.nextInt(indices.size()));
                else
                    array[j][i] = -1;
            }
        }
        for (int i = 0; i < numFolds; i++) {
            int[] indi;
            if (array[i][size - 1] == -1) {
                indi = new int[size - 1];
                System.arraycopy(array[i], 0, indi, 0, size - 1);
            } else {
                indi = new int[size];
                System.arraycopy(array[i], 0, indi, 0, size);
            }
            out[i] = new FoldCustomFBW(this, indi);

        }
        // System.out.println(Arrays.deepToString(array));
        return out;
    }

    @Override
    public int noAttributes() {
        if (this.size() == 0)
            return 0;
        return maxAttributes;
    }

    @Override
    public int classIndex(Object clazz) {

        if (clazz != null)
            return this.classes().headSet(clazz).size();
        else
            return -1;

    }

    @Override
    public Object classValue(int index) {
        int i = 0;
        for (Object o : this.classes) {
            if (i == index)
                return o;
            i++;
        }
        return null;
    }

    @Override
    public DatasetCustomFBW copy() {
        DefaultDatasetCustomFBW out = new DefaultDatasetCustomFBW();
        for (InstanceCustomFBW i : this) {
            out.add(i.copy());
        }
        return out;
    }

}
