package cobraj;

import java.util.Arrays;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

import cobraj.mit.naming.DnFactory;
import cobraj.mit.naming.DnType;

public class App {

	public static void main(String[] args) {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("import sys");
		interpreter.exec("print(sys.path)");
		interpreter.exec("import cobra.mit");
		interpreter.exec("print(dir(cobra.mit))");

		DnFactory dnFactory = new DnFactory();
		DnType dn = dnFactory.create(Arrays.<PyObject> asList(
				new PyString("uni"), new PyString("userext"), new PyString("user-john")));
		System.out.println(dn.__str__());

	}
}
