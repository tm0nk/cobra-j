package cobraj.mit.access;

import org.python.core.PyObject;
import org.python.util.PythonInterpreter;

public class MoDirectoryFactory {
	private PyObject py_MoDirectoryClass;
	
	public MoDirectoryFactory() {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("from cobra.mit.access import MoDirectory as py_MoDirectory");
		this.py_MoDirectoryClass = interpreter.get("py_MoDirectory");
	}

	public MoDirectoryType create(PyObject session) {
		PyObject dnObject = py_MoDirectoryClass.__call__(session);
		MoDirectoryType moDirectory = (MoDirectoryType) dnObject.__tojava__(MoDirectoryType.class);
		return moDirectory;
	}
}
