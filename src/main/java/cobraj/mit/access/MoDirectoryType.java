package cobraj.mit.access;

import org.python.core.PyObject;
import org.python.core.PyString;

import cobraj.mit.mo.MoType;

public interface MoDirectoryType {

	public void login();

	public void logout();

	public MoType lookupByDn(PyString dn);

	public PyObject lookupByClass(PyString className);

	public PyObject commit(PyObject cfgRequest);
}
