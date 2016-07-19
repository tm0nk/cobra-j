package cobraj;

import org.python.core.PyString;
import org.python.util.PythonInterpreter;

import cobraj.mit.access.MoDirectoryFactory;
import cobraj.mit.access.MoDirectoryType;
import cobraj.mit.session.AbstractSessionType;
import cobraj.mit.session.LoginSessionFactory;

public class App {

	public static void main(String[] args) {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("import sys");
		interpreter.exec("print(sys.path)");
		interpreter.exec("import cobra.mit.session");
		interpreter.exec("print(dir(cobra.mit.session))");

		// This example comes from the Cisco APIC Python API Documentation
		// (Release 0.1), section 6.2: Connecting and Authenticating
		PyString apicUrl = new PyString("https://192.168.10.80");
		LoginSessionFactory loginSessionFactory = new LoginSessionFactory();
		AbstractSessionType loginSession = loginSessionFactory.create(
				apicUrl,
				new PyString("admin"),
				new PyString("mypassword"));
		MoDirectoryFactory moDirectoryFactory = new MoDirectoryFactory();
		MoDirectoryType moDir = moDirectoryFactory.create(loginSession);
		moDir.login();
		// Use the connected moDir queries and configuration...
		moDir.logout();

//		DnFactory dnFactory = new DnFactory();
//		DnType dn = dnFactory.create(Arrays.<PyObject> asList(
//				new PyString("uni"),
//				new PyString("userext"),
//				new PyString("user-john")));
//		System.out.println(dn.__str__());

		interpreter.close();
	}
}
