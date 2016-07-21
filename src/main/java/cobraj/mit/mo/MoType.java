package cobraj.mit.mo;

import org.python.core.PyInteger;
import org.python.core.PyObject;
import org.python.core.PyString;

import cobraj.mit.naming.DnType;
import cobraj.mit.naming.RnType;

public interface MoType {

	public DnType _dn();

	public RnType _rn();

	public PyObject __getattr__(PyString propName);

	public PyInteger __hash__();

}
