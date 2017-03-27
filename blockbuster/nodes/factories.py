import factory
from nodes.models import Node


class NodeModelFactory(factory.DjangoModelFactory):
    host = factory.Sequence(lambda n: "http://www.host%d.com/" % n)
    username_for_node = 'pleasework'
    password_for_node = 'test'

    class Meta:
        model = Node
