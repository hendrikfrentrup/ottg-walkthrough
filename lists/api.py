import json
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ObjectDoesNotExist


def list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
        if request.method == 'POST':
            item = Item.objects.create(list=list_, text=request.POST['text'])
            item_dicts = {'id': item.id, 'text': item.text}
            status = 201
        else:
            item_dicts = [
                {'id': item.id, 'text': item.text}
                for item in list_.item_set.all()
            ]
            status = 200
        return HttpResponse(
            content=json.dumps(item_dicts),
            status=status,
            content_type='application/json'
        )
    except ObjectDoesNotExist:
        return HttpResponse(
            status=404,
            content_type='application/json'
        )
