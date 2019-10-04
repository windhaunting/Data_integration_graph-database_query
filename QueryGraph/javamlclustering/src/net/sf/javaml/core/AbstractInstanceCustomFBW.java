package net.sf.javaml.core;
import java.util.Collection;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

public class AbstractInstanceCustomFBW implements InstanceCustomFBW {

	private static final long serialVersionUID = -1712202124913999825L;

	static int nextID = 0;

    private final int ID;

    public int getID() {
        return ID;
    }

    class InstanceValueIterator implements Iterator<String> {

        private int index = 0;

        @Override
        public boolean hasNext() {
            return index < noAttributes();
        }

        @Override
        public String next() {
            index++;
            return value(index - 1);
        }

        @Override
        public void remove() {
            throw new UnsupportedOperationException("Cannot remove from instance using the iterator.");

        }

    }

    private Object classValue;

    protected AbstractInstanceCustomFBW() {
        this(null);
    }

    protected AbstractInstanceCustomFBW(Object classValue) {
        ID = nextID;
        nextID++;
        this.classValue = classValue;
    }

    
    
	@Override
	public int size() {
		// TODO Auto-generated method stub
		return 0;
	}

	@Override
	public boolean isEmpty() {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean containsKey(Object key) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean containsValue(Object value) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public String get(Object key) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String put(Integer key, String value) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String remove(Object key) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void putAll(Map<? extends Integer, ? extends String> m) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void clear() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public Set<Integer> keySet() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Collection<String> values() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Set<java.util.Map.Entry<Integer, String>> entrySet() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Iterator<String> iterator() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Object classValue() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setClassValue(Object value) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public int noAttributes() {
		// TODO Auto-generated method stub
		return 0;
	}

	@Override
	public String value(int pos) {
		// TODO Auto-generated method stub
		return null;
	}

	public void removeAttribute(int i) {
		// TODO Auto-generated method stub
		
	}

	public void removeAttributes(Set<Integer> indices) {
		// TODO Auto-generated method stub
		
	}

	public InstanceCustomFBW copy() {
		// TODO Auto-generated method stub
		return null;
	}

}
