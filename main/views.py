from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer
from .utils import calculate_notes

"""
Serve frontend
"""
def vending_machine_view(request):
    return render(request, 'vending_machine.html')


"""
Serve backend API
"""
class ItemListAPIView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class ItemPurchaseAPIView(APIView):
    def post(self, request):
        item_id = request.data.get('item_id')
        amount_paid = int(request.data.get('amount_paid'))

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'error': 'Invalid item ID.'}, status=400)

        if amount_paid < item.price:
            return Response({'error': 'Insufficient amount paid.'}, status=400)

        change = amount_paid - item.price
        note_count = calculate_notes(change)

        return Response({
            'change': change,
            'notes_to_return': note_count
        })