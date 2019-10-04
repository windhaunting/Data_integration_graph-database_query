
/**
 *  //added by fbw
 * 
 */
package net.sf.javaml.core;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;

/**
 * Implementation of a dense instance. A dense instance is a wrapper around a
 * double array that provides a value for each attribute index.
 * 
 * 
 * 
 * @see Dataset
 * @see Instance
 * 
 * @version 0.1.7
 * 
 * @author Thomas Abeel
 * 
 */
public class DenseInstanceCustomFBW extends AbstractInstanceCustomFBW implements InstanceCustomFBW {

    private static final long serialVersionUID = 3284511291715269081L;

    /* Holds values */
    private String[] attributes;
    /**
     * Creates a new instance with the provide value for the attributes. The
     * class label will be set to null.
     * 
     * @param att
     *            the value of the instance
     */
    public DenseInstanceCustomFBW(String[] att) {
        this(att, null);
    }

    /**
     * Creates a new instance with the provided attribute values and the
     * provided class label.
     * 
     * @param att
     *            the attribute values
     * @param classValue
     *            the class label
     */
    public DenseInstanceCustomFBW(String[] att, Object classValue) {
        super(classValue);
        this.attributes = att.clone();
    }
    
    /* Hide argumentless constructor */
    private DenseInstanceCustomFBW() {
    }

    /**
     * Creates an instance that has space for the supplied number of attributes.
     * By default all attributes are initialized by zero.
     * 
     * @param size
     *            the number of attributes
     */
    public DenseInstanceCustomFBW(int size) {
        this(new String[size]);
    }
    
    @Override
    public String value(int pos) {
        return attributes[pos];
    }

    @Override
    public void clear() {
        attributes = new String[attributes.length];

    }

    @Override
    public boolean containsKey(Object key) {
        if (key instanceof Integer) {
            int i = (Integer) key;
            return i >= 0 && i < attributes.length;
        } else
            return false;
    }

    //to be implemented later fbw
    /*        
    @Override
    public boolean containsValue(Object value) {
        if (value instanceof Number) {
            double val = ((Number) value).doubleValue();
            for (int i = 0; i < attributes.length; i++) {
                if (Math.abs(val - attributes[i]) < 0.00000001)
                    return true;
            }
        }
        return false;
    }
*/
    
    public Set<java.util.Map.Entry<Integer, String>> entrySet() {
        HashMap<Integer, String> map = new HashMap<Integer, String>();
        for (int i = 0; i < attributes.length; i++)
            map.put(i, attributes[i]);
        return map.entrySet();
    }

    public String get(Object key) {
        return attributes[(Integer) key];
    }

    @Override
    public boolean isEmpty() {

        return false;
    }

    @Override
    public SortedSet<Integer> keySet() {
        TreeSet<Integer> keys = new TreeSet<Integer>();
        for (int i = 0; i < attributes.length; i++)
            keys.add(i);
        return keys;
    }

    public String put(Integer key, String value) {
    	String val = attributes[key];
        attributes[key] = value;
        return val;

    }

    public void putAll(Map<? extends Integer, ? extends String> m) {
        for (Integer key : m.keySet()) {
            attributes[key] = m.get(key);
        }

    }

    @Override
    public String remove(Object key) {
        throw new UnsupportedOperationException("Cannot unset values from a dense instance.");
    }

    @Override
    @Deprecated
    public int size() {
        return attributes.length;
    }

    public Collection<String> values() {
        Collection<String> vals = new ArrayList<String>();
        for (String v : attributes)
            vals.add(v);
        return vals;
    }

    @Override
    public int noAttributes() {
        return attributes.length;
    }

    @Override
    public String toString() {
        return "{" + Arrays.toString(attributes) + ";" + classValue() + "}";
    }

    @Override
    public void removeAttribute(int i) {
    	String[] tmp = attributes.clone();
        attributes = new String[tmp.length - 1];
        System.arraycopy(tmp, 0, attributes, 0, i);
        System.arraycopy(tmp, i + 1, attributes, i, tmp.length - i - 1);

    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + Arrays.hashCode(attributes);
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        final DenseInstanceCustomFBW other = (DenseInstanceCustomFBW) obj;
        if (!Arrays.equals(attributes, other.attributes))
            return false;
        return true;
    }

    @Override
    public InstanceCustomFBW copy() {
    	DenseInstanceCustomFBW out = new DenseInstanceCustomFBW();
        out.attributes = this.attributes.clone();
        out.setClassValue(this.classValue());
        return out;
    }

    @Override
    public void removeAttributes(Set<Integer> indices) {
    	String[] tmp = attributes.clone();
        attributes = new String[tmp.length - indices.size()];
        int index = 0;
        for (int i = 0; i < tmp.length; i++) {
            if (!indices.contains(i)) {
                attributes[index++] = tmp[i];
            }
        }
    }

	@Override
	public boolean containsValue(Object value) {
		// TODO Auto-generated method stub
		return false;
	}


}
