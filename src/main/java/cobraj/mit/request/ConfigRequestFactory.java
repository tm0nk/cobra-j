package cobraj.mit.request;

import org.python.core.PyObject;
import org.python.util.PythonInterpreter;

public class ConfigRequestFactory {

	private PyObject py_ConfigRequestClass;
	
	public ConfigRequestFactory() {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("from cobra.mit.request import ConfigRequest as py_ConfigRequest");
		this.py_ConfigRequestClass = interpreter.get("py_ConfigRequest");
	}

	public ConfigRequestType create() {
		PyObject configRequestObject = py_ConfigRequestClass.__call__();
		ConfigRequestType configRequest = (ConfigRequestType) configRequestObject.__tojava__(ConfigRequestType.class);
		return configRequest;
	}

}
