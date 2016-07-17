package cobraj;

import org.python.util.PythonInterpreter;

public class App {

	public static void main(String[] args) {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("import sys");
		interpreter.exec("print(sys.path)");
		interpreter.exec("import cobra.mit.naming");
		interpreter.exec("print(dir(cobra.mit.naming))");

		// This example comes from the Cisco APIC Python API Documentation
		// (Release 0.1), section 6.2: Connecting and Authenticating
//		LoginSessionType loginSession = LoginSessionFactory.create(
//				new PyString("https://192.168.10.80"),
//				new PyString("admin"),
//				new PyString("mypassword"));
//		MoDirectoryType moDir = MoDirectoryFactory.create(loginSession);
//		moDir.login();
//		// # Use the connected moDir queries and configuration...
//		moDir.logout();

//		DnFactory dnFactory = new DnFactory();
//		DnType dn = dnFactory.create(Arrays.<PyObject> asList(
//				new PyString("uni"),
//				new PyString("userext"),
//				new PyString("user-john")));
//		System.out.println(dn.__str__());

		interpreter.close();
	}
}
