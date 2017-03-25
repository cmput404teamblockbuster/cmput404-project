import factory
from nodes.models import Node


class NodeModelFactory(factory.DjangoModelFactory):
    host = factory.Sequence(lambda n: "http://www.host%d.com/" % n)

    class Meta:
        model = Node
