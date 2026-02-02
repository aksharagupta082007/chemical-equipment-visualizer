import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from rest_framework.permissions import IsAuthenticated 

from .models import Dataset
from .serializers import DatasetSerializer


class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        file_path = default_storage.save(f'uploads/{file.name}', file)
        df = pd.read_csv(default_storage.open(file_path))

       
        equipment_type_distribution = (
            df['Type']
            .value_counts()
            .to_dict()
            if 'Type' in df.columns
            else {}
        )

        dataset = Dataset.objects.create(
            filename=file.name,
            total_equipment=len(df),
            avg_flowrate=df['Flowrate'].mean(),
            avg_pressure=df['Pressure'].mean(),
            avg_temperature=df['Temperature'].mean(),
            equipment_type_distribution=equipment_type_distribution,  
        )

       
        if Dataset.objects.count() > 5:
            Dataset.objects.order_by('uploaded_at').first().delete()

        return Response(
            DatasetSerializer(dataset).data,
            status=status.HTTP_201_CREATED
        )


class DatasetHistoryView(APIView):
    def get(self, request):
        datasets = Dataset.objects.order_by('-uploaded_at')[:5]
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)
