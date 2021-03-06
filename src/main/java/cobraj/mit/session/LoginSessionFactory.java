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

	public PyObject create(PyString controllerUrl, PyString user, PyString password) {
		PyObject loginSessionObject = py_LoginSessionClass.__call__(controllerUrl, user, password);
		return loginSessionObject;
	}
}
