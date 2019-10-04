package net.sf.javaml.core;

import java.io.Serializable;
import java.util.Map;
import java.util.Set;
import java.util.SortedSet;


public interface InstanceCustomFBW extends Map<Integer, String>, Iterable<String>, Serializable{
    public Object classValue();

    public void setClassValue(Object value);

    public int noAttributes();

    @Override
    @Deprecated
    public int size();

    public String value(int pos);

	public InstanceCustomFBW copy();

    
}
