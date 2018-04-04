#!/usr/bin/env python

import unittest


class PredicatePart(object):
	def __init__(self, positive_tags=None, negative_tags=None):
		self.positive_tags = positive_tags or []
		self.negative_tags = negative_tags or []


class NF(object):
	def __init__(self, parts):
		self.parts = parts or []

	def __call__(self, tags=None):
		tags = tags or []
		non_empty_parts = []
		for part in self.parts:
			if part.positive_tags or part.negative_tags:
				non_empty_parts.append(part)
		is_trivial = not non_empty_parts
		if is_trivial:
			return True
		result = self.default_value
		for part in non_empty_parts:
			part_result = not self.default_value
			for tag in part.positive_tags:
				part_result = self.internal_op(part_result, tag in tags)
			for tag in part.negative_tags:
				part_result = self.internal_op(part_result, not tag in tags)
			result = self.external_op(result, part_result)
		return result


class CNF(NF):
	def __init__(self, parts):
		super(CNF, self).__init__(parts)
		self.default_value = True

	def internal_op(self, arg1, arg2):
		return arg1 or arg2

	def external_op(self, arg1, arg2):
		return arg1 and arg2


class DNF(NF):
	def __init__(self, parts):
		super(DNF, self).__init__(parts)
		self.default_value = False

	def internal_op(self, arg1, arg2):
		return arg1 and arg2

	def external_op(self, arg1, arg2):
		return arg1 or arg2


class Predicate(object):
	def __init__(self, dnf=True, parts=None):
		if dnf:
			self.form = DNF(parts)
		else:
			self.form = CNF(parts)

	def __call__(self, tags=None):
		return self.form(tags)


class TestDNF(unittest.TestCase):
	def test_empty(self):
		predicate = Predicate(dnf=True)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([0, 1]))

	def test_empty_part(self):
		# () and ()
		parts = [PredicatePart(), PredicatePart()]
		predicate = Predicate(dnf=True, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([0, 1]))
		parts = [PredicatePart(negative_tags=[]), PredicatePart()]
		predicate = Predicate(dnf=True, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([0, 1]))
		parts = [PredicatePart(), PredicatePart(positive_tags=[])]
		predicate = Predicate(dnf=True, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([0, 1]))

	def test_positive_tags_rule_1(self):
		# 0 and 1
		parts = [PredicatePart(positive_tags=[0, 1])]
		predicate = Predicate(dnf=True, parts=parts)
		self.assertTrue(predicate([0, 1]))
		self.assertTrue(predicate([0, 1, 2]))
		self.assertFalse(predicate([]))
		self.assertFalse(predicate([0]))
		self.assertFalse(predicate([1, 2]))

	def test_positive_tags_rule_2(self):
		# 0 or 1
		parts = [PredicatePart(positive_tags=[0]), PredicatePart(positive_tags=[1])]
		predicate = Predicate(dnf=True, parts=parts)
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([1]))
		self.assertTrue(predicate([0, 1]))
		self.assertTrue(predicate([0, 1, 2]))
		self.assertFalse(predicate())
		self.assertFalse(predicate([]))
		self.assertFalse(predicate([2]))

	def test_negative_tags_rule_1(self):
		# not 0 and not 1
		parts = [PredicatePart(negative_tags=[0, 1])]
		predicate = Predicate(dnf=True, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([2]))
		self.assertFalse(predicate([0]))
		self.assertFalse(predicate([1]))
		self.assertFalse(predicate([0, 1]))
		self.assertFalse(predicate([0, 2]))
		self.assertFalse(predicate([1, 2]))
		self.assertFalse(predicate([0, 1, 2]))

	def test_negative_tags_rule_2(self):
		# not 0 or not 1
		parts = [PredicatePart(negative_tags=[0]), PredicatePart(negative_tags=[1])]
		predicate = Predicate(dnf=True, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([2]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([1]))
		self.assertFalse(predicate([0, 1]))
		self.assertTrue(predicate([0, 2]))
		self.assertTrue(predicate([1, 2]))
		self.assertFalse(predicate([0, 1, 2]))

	def test_false(self):
		# 0 and not 0
		parts = [PredicatePart(positive_tags=[0], negative_tags=[0])]
		predicate = Predicate(dnf=True, parts=parts)
		self.assertFalse(predicate())
		self.assertFalse(predicate([]))
		self.assertFalse(predicate([0]))
		self.assertFalse(predicate([1]))
		self.assertFalse(predicate([0, 1]))

	def test_true(self):
		# 0 or not 0
		parts = [PredicatePart(positive_tags=[0]), PredicatePart(negative_tags=[0])]
		predicate = Predicate(dnf=True, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([1]))
		self.assertTrue(predicate([0, 1]))


class TestCNF(unittest.TestCase):
	def test_empty(self):
		predicate = Predicate(dnf=False)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([0, 1]))

	def test_empty_part(self):
		# () or ()
		parts = [PredicatePart(), PredicatePart()]
		predicate = Predicate(dnf=False, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([0, 1]))
		parts = [PredicatePart(negative_tags=[]), PredicatePart()]
		predicate = Predicate(dnf=False, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([0, 1]))
		parts = [PredicatePart(), PredicatePart(positive_tags=[])]
		predicate = Predicate(dnf=False, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([0, 1]))

	def test_positive_tags_rule_1(self):
		# 0 or 1
		parts = [PredicatePart(positive_tags=[0, 1])]
		predicate = Predicate(dnf=False, parts=parts)
		self.assertFalse(predicate())
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([1]))
		self.assertTrue(predicate([1, 0]))
		self.assertTrue(predicate([0, 2]))
		self.assertTrue(predicate([1, 2]))
		self.assertFalse(predicate([2]))

	def test_positive_tags_rule_2(self):
		# 0 and 1
		parts = [PredicatePart(positive_tags=[0]), PredicatePart(positive_tags=[1])]
		predicate = Predicate(dnf=False, parts=parts)
		self.assertFalse(predicate())
		self.assertFalse(predicate([0]))
		self.assertFalse(predicate([1]))
		self.assertFalse(predicate([1, 2]))
		self.assertTrue(predicate([1, 0]))
		self.assertFalse(predicate([0, 2]))
		self.assertFalse(predicate([1, 2]))
		self.assertFalse(predicate([2]))

	def test_negative_tags_rule_1(self):
		# not 0 or not 1
		parts = [PredicatePart(negative_tags=[0, 1])]
		predicate = Predicate(dnf=False, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([1]))
		self.assertFalse(predicate([0, 1]))
		self.assertTrue(predicate([1, 2]))
		self.assertFalse(predicate([1, 0, 1]))
		self.assertFalse(predicate([0, 1, 2]))

	def test_negative_tags_rule_2(self):
		# not 0 and not 1
		parts = [PredicatePart(negative_tags=[0]), PredicatePart(negative_tags=[1])]
		predicate = Predicate(dnf=False, parts=parts)
		self.assertTrue(predicate())
		self.assertFalse(predicate([0]))
		self.assertFalse(predicate([1]))
		self.assertFalse(predicate([0, 1]))
		self.assertTrue(predicate([2]))
		self.assertFalse(predicate([0, 2]))
		self.assertFalse(predicate([1, 2]))
		self.assertFalse(predicate([0, 1, 2]))

	def test_true(self):
		# 0 or not 0
		parts = [PredicatePart(positive_tags=[0], negative_tags=[0])]
		predicate = Predicate(dnf=False, parts=parts)
		self.assertTrue(predicate())
		self.assertTrue(predicate([]))
		self.assertTrue(predicate([0]))
		self.assertTrue(predicate([1]))
		self.assertTrue(predicate([0, 1]))

	def test_false(self):
		# 0 and not 0
		parts = [PredicatePart(positive_tags=[0]), PredicatePart(negative_tags=[0])]
		predicate = Predicate(dnf=False, parts=parts)
		self.assertFalse(predicate())
		self.assertFalse(predicate([]))
		self.assertFalse(predicate([0]))
		self.assertFalse(predicate([1]))
		self.assertFalse(predicate([0, 1]))


if __name__ == '__main__':
	unittest.main()
