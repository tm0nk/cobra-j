package cobraj.mit.access;

import org.python.core.Py;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;

import cobraj.mit.session.AbstractSessionType;

public class MoDirectoryFactory {
	private PyObject py_MoDirectoryClass;
	
	public MoDirectoryFactory() {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("from cobra.mit.access import MoDirectory as py_MoDirectory");
		this.py_MoDirectoryClass = interpreter.get("py_MoDirectory");
	}

	public MoDirectoryType create(AbstractSessionType session) {
		PyObject pySession = Py.java2py(session);
		PyObject dnObject = py_MoDirectoryClass.__call__(pySession);
		MoDirectoryType moDirectory = (MoDirectoryType) dnObject.__tojava__(MoDirectoryType.class);
		return moDirectory;
	}
}
