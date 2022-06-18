from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return super(
                MultiSerializerViewSetMixin, self
            ).get_serializer_class()


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               GenericViewSet):
    pass
