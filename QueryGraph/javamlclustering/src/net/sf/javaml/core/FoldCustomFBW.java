

package net.sf.javaml.core;

import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.ListIterator;
import java.util.Random;
import java.util.Set;
import java.util.SortedSet;
import java.util.Vector;

import net.sf.javaml.distance.DistanceMeasure;
import net.sf.javaml.distance.DistanceMeasureCustomFBW;

class FoldCustomFBW implements DatasetCustomFBW {
    private int[] indices;

    private DatasetCustomFBW parent;

    public FoldCustomFBW(DatasetCustomFBW parent, int[] indices) {
        // System.out.println("construction: "+parent.classes());
        this.indices = indices;
        this.parent = parent;
    }

    @Override
    public boolean add(InstanceCustomFBW i) {
        throw new UnsupportedOperationException("Cannot do this on a fold of a dataset");
    }

    @Override
    public SortedSet<Object> classes() {
        // System.out.println("Call");
        return parent.classes();
    }

    @Override
    public DatasetCustomFBW[] folds(int numFolds, Random rg) {
        // TODO this method can be implemented on a fold.
        throw new UnsupportedOperationException("Method is not yet implemented");
    }

    @Override
    public InstanceCustomFBW instance(int index) {
        // System.out.println(parent);
        // System.out.println(parent.size());
        // System.out.println(index);
        return parent.instance(indices[index]);
    }

    @Override
    public Set<InstanceCustomFBW> kNearest(int k, InstanceCustomFBW inst,DistanceMeasureCustomFBW dm) {
        // TODO this method can be implemented on a fold.
        throw new UnsupportedOperationException("Method is not yet implemented");
    }

    @Override
    public void add(int index, InstanceCustomFBW element) {
        throw new UnsupportedOperationException("Cannot do this on a fold of a dataset");
    }

    @Override
    public boolean addAll(Collection<? extends InstanceCustomFBW> c) {
        throw new UnsupportedOperationException("Cannot do this on a fold of a dataset");
    }

    @Override
    public boolean addAll(int index, Collection<? extends InstanceCustomFBW> c) {
        throw new UnsupportedOperationException("Cannot do this on a fold of a dataset");
    }

    @Override
    public void clear() {
        throw new UnsupportedOperationException("Cannot do this on a fold of a dataset");

    }

    @Override
    public boolean contains(Object o) {
        // TODO this method can be implemented on a fold.
        throw new UnsupportedOperationException("Method is not yet implemented");
    }

    @Override
    public boolean containsAll(Collection<?> c) {
        // TODO this method can be implemented on a fold.
        throw new UnsupportedOperationException("Method is not yet implemented");
    }

    @Override
    public InstanceCustomFBW get(int index) {
        return instance(index);
    }

    @Override
    public int indexOf(Object o) {
        // TODO this method can be implemented on a fold.
        throw new UnsupportedOperationException("Method is not yet implemented");
    }

    @Override
    public boolean isEmpty() {
        return false;
    }

    class FoldIterator implements ListIterator<InstanceCustomFBW> {

        private int currentIndex = 0;

        public FoldIterator(int index) {
            this.currentIndex = index;
        }

        public FoldIterator() {
            this(0);
        }

        @Override
        public boolean hasNext() {
            return currentIndex < indices.length;
        }

        @Override
        public InstanceCustomFBW next() {
            currentIndex++;
            return instance(currentIndex - 1);
        }

        @Override
        public void remove() {
            throw new UnsupportedOperationException("You cannot do this on a fold.");

        }

        @Override
        public void add(InstanceCustomFBW arg0) {
            throw new UnsupportedOperationException("You cannot do this on a fold.");

        }

        @Override
        public boolean hasPrevious() {
            return currentIndex > 0;
        }

        @Override
        public int nextIndex() {
            return currentIndex;
        }

        @Override
        public InstanceCustomFBW previous() {
            currentIndex--;
            return instance(currentIndex);
        }

        @Override
        public int previousIndex() {
            return currentIndex;
        }

        @Override
        public void set(InstanceCustomFBW arg0) {
            throw new UnsupportedOperationException("You cannot do this on a fold.");

        }

    }

    @Override
    public Iterator<InstanceCustomFBW> iterator() {
        return new FoldIterator();
    }

    @Override
    public int lastIndexOf(Object o) {
        // TODO this method can be implemented on a fold.
        throw new UnsupportedOperationException("Method is not yet implemented");
    }

    @Override
    public ListIterator<InstanceCustomFBW> listIterator() {
        return new FoldIterator();
    }

    @Override
    public ListIterator<InstanceCustomFBW> listIterator(int index) {
        return new FoldIterator(index);
    }

    @Override
    public boolean remove(Object o) {
        throw new UnsupportedOperationException("You cannot do this on a fold.");
    }

    @Override
    public InstanceCustomFBW remove(int index) {
        throw new UnsupportedOperationException("You cannot do this on a fold.");
    }

    @Override
    public boolean removeAll(Collection<?> c) {
        throw new UnsupportedOperationException("You cannot do this on a fold.");
    }

    @Override
    public boolean retainAll(Collection<?> c) {
        throw new UnsupportedOperationException("You cannot do this on a fold.");
    }

    @Override
    public InstanceCustomFBW set(int index, InstanceCustomFBW element) {
        throw new UnsupportedOperationException("You cannot do this on a fold.");
    }

    @Override
    public int size() {
        return indices.length;
    }

    @Override
    public List<InstanceCustomFBW> subList(int fromIndex, int toIndex) {
        throw new UnsupportedOperationException("You cannot do this on a fold.");
    }

    @Override
    public Object[] toArray() {
        Object[] out = new Object[indices.length];
        for (int i = 0; i < size(); i++) {
            out[i] = instance(i);
        }
        return out;

    }

    @SuppressWarnings("unchecked")
    @Override
    public <T> T[] toArray(T[] a) {
        Vector<T> tmp = new Vector<T>();
        for (InstanceCustomFBW i : this) {
            tmp.add((T) i);
        }
        return tmp.toArray(a);
    }

    @Override
    public int noAttributes() {
        return parent.noAttributes();
    }

    @Override
    public int classIndex(Object clazz) {
        return parent.classIndex(clazz);
    }

    @Override
    public Object classValue(int index) {
        return parent.classValue(index);
    }

    @Override
    public DatasetCustomFBW copy() {
        DatasetCustomFBW out=new DefaultDatasetCustomFBW();
        for(InstanceCustomFBW i:this)
            out.add(i.copy());
        return out;
    }
}