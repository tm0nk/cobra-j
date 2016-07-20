package cobraj.model.fv;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

public class TenantFactory {

	private PyObject py_TenantClass;
	
	public TenantFactory() {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("from cobra.model.fv import Tenant as py_Tenant");
		this.py_TenantClass = interpreter.get("py_Tenant");
	}

	public PyObject create(PyObject parentMoOrDn, PyString name) {
		PyObject tenantObject = py_TenantClass.__call__(parentMoOrDn, name);
		return tenantObject;
	}

	
}
