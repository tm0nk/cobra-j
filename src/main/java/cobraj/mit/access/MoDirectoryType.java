package cobraj.mit.access;

import org.python.core.PyObject;
import org.python.core.PyString;

public interface MoDirectoryType {

	public void login();

	public void logout();

	public PyObject lookupByDn(PyString dn);

	public PyObject lookupByClass(PyString className);
}
