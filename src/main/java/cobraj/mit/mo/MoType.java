package cobraj.mit.mo;

import org.python.core.PyObject;
import org.python.core.PyString;

public interface MoType {

	public PyObject __getattr__(PyString propName);

	public PyObject __hash__();

}
