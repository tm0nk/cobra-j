package cobraj.mit.session;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

public class LoginSessionFactory {
	private PyObject py_LoginSessionClass;
	
	public LoginSessionFactory() {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("from cobra.mit.session import LoginSession as py_LoginSession");
		this.py_LoginSessionClass = interpreter.get("py_LoginSession");
	}

	public AbstractSessionType create(PyString controllerUrl, PyString user, PyString password) {
		PyObject dnObject = py_LoginSessionClass.__call__(controllerUrl, user, password);
		AbstractSessionType loginSession = (AbstractSessionType) dnObject.__tojava__(AbstractSessionType.class);
		return loginSession;
	}
}
