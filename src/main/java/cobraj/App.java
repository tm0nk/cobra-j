package cobraj;

import org.python.core.PyInteger;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

import cobraj.mit.access.MoDirectoryFactory;
import cobraj.mit.access.MoDirectoryType;
import cobraj.mit.mo.MoType;
import cobraj.mit.session.LoginSessionFactory;

public class App {

	public static void main(String[] args) {
		PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.exec("import sys");
		interpreter.exec("print(sys.path)");
		interpreter.exec("import cobra.mit.access");
		interpreter.exec("print(dir(cobra.mit.access))");

		// This example comes from the Cisco APIC Python API Documentation
		// (Release 0.1), section 6.2: Connecting and Authenticating
		PyString apicUrl = new PyString("https://192.168.10.80");
		LoginSessionFactory loginSessionFactory = new LoginSessionFactory();
		PyObject loginSession = loginSessionFactory.create(
				apicUrl,
				new PyString("admin"),
				new PyString("mypassword"));
		MoDirectoryFactory moDirectoryFactory = new MoDirectoryFactory();
		MoDirectoryType moDir = moDirectoryFactory.create(loginSession);
		moDir.login();
		// Use the connected moDir queries and configuration...
		MoType tnCommonMo = moDir.lookupByDn(new PyString("uni/tn-common"));
		MoType tnMgmtMo = moDir.lookupByDn(new PyString("uni/tn-mgmt"));
		MoType tnInfraMo = moDir.lookupByDn(new PyString("uni/tn-infra"));

		PyInteger tnCommonHash = tnCommonMo.__hash__();
		PyInteger tnMgmtHash = tnMgmtMo.__hash__();
		PyInteger tnInfraHash = tnInfraMo.__hash__();
//		TenantFactory tenantFactory = new TenantFactory();
//		PyObject fvTenantMo = tenantFactory.create(uniMo, new PyString("tomonkJython"));
//		ConfigRequestFactory configRequestFactory = new ConfigRequestFactory();
//		ConfigRequestType cfgRequest = configRequestFactory.create();
//		cfgRequest.addMo(fvTenantMo);
//		PyObject response = moDir.commit(Py.java2py(cfgRequest));
//		PyObject polUniMo = moDir.lookupByClass(new PyString("polUni"));
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
