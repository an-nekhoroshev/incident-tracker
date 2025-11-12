from rest_framework import viewsets, status
from rest_framework.response import Response  # Обязательно импортируйте Response
from .models import Incident
from .serializers import IncidentSerializer

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all().order_by('-created_at')
    serializer_class = IncidentSerializer

    def list(self, request):
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = Incident.objects.filter(status=status_filter)
        else:
            queryset = Incident.objects.all()
        return Response(IncidentSerializer(queryset, many=True).data)
