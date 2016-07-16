package cobraj.mit.naming;

import java.util.List;

import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;

public class DnFactory {
	private PyObject py_DnClass;

	public DnFactory() {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("from cobra.mit.naming import Dn as py_Dn");
		this.py_DnClass = interpreter.get("py_Dn");
	}

	public DnType create(List<PyObject> rns) {
		PyObject dnObject = py_DnClass.__call__(PyList.fromList(rns));
		DnType dn = (DnType) dnObject.__tojava__(DnType.class);
		return dn;
	}

}
