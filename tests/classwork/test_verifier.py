from unittest import TestCase

from mockito import mock, when, verify

from classwork.assignment import Assignment
from classwork.verifier import ClassworkVerifier


class TestClassworkVerifier(TestCase):
    the_assignment = Assignment('an-ord', 'a-name')

    classwork_repository = mock()
    verification_pipeline = mock()

    def setUp(self):
        self.classwork_verifier = ClassworkVerifier(self.classwork_repository, self.verification_pipeline)

    def test_verification_pipeline_should_verify_each_classwork(self):
        classworks = self.__given_classworks()

        self.classwork_verifier.verify_for_assignment(self.the_assignment)

        for classwork in classworks:
            verify(self.verification_pipeline).verify(classwork)

    def __given_classworks(self):
        classworks = [mock(), mock()]
        when(self.classwork_repository).find_by_assignment(self.the_assignment).thenReturn(classworks)
        return classworks
