from rest_framework import viewsets
from .serializers import StravaActivitySerializer
from .models import StravaActivity


class StravaActivityViewSet(viewsets.ModelViewSet):
    queryset = StravaActivity.objects.all().order_by('-datetime')
    serializer_class = StravaActivitySerializer
