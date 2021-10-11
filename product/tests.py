from django.test import TestCase
from collections import Counter
# Create your tests here.
test = [(1,),(1,),(1,),(2,)]

test2= Counter(test)

print(test2)

