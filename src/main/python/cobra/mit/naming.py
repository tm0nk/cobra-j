from cobraj.mit.naming import DnType

class Dn(DnType):
	"""
	The distinguished name (Dn) uniquely identifies a managed object (MO).
	A Dn is an ordered list of relative names, such as:

	dn = rn1/rn2/rn3/....

	In this example, the Dn provides a fully qualified path for **user-john**
	from the top of the Mit to the Mo.

	dn = "uni/userext/user-john"
	"""

	def __init__(self, rns=None):
		"""
		Create a Dn from a list of Rn objects.
		
		:param rns: list of Rns
		:type rns: list
		"""

		self.__dnStr = None
		self.__hash = None
		self.__rns = []
		if rns is None:
			rns = []
		for rn in rns:
			self.__rns.append(rn)

	def __str__(self):
		result = ""
		first = True
		for rn in self.__rns:
			if first:
				first = False
			else:
				result += "/"
			result += rn
		return result;
