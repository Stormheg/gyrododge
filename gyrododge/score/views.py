from rest_framework.views import APIView
from rest_framework.response import Response

from gyrododge.score.serializers import PositionSerializer, ScoreSerializer

class PostScoreApi(APIView):
    def post(self, request):
        # Serializer aanmaken met meegestuurde data.
        ser = ScoreSerializer(data=request.data)

        # Checken of het veld 'points' wel is meegestuurd.
        # Zo niet, geef foutmelding.
        ser.is_valid(raise_exception=True)

        # Alles oke, sla op in database.
        our_score = ser.save()

        # Haal de plek van deze score in het klassement op
        position = our_score.get_position()

        # Serializeer position
        ser = PositionSerializer(data={"position": position})
        ser.is_valid()

        # Laat de raspberry pi weten dat we de score succesvol verwerkt hebben
        # en geef de positie in het klassement terug.
        return Response(ser.data)
