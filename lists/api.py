import json
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

def list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
        if request.method == 'POST':
            try:
                if not request.POST['text']:
                    item_dicts = {'error': EMPTY_ITEM_ERROR}
                    status = 400
                else:
                    item = Item.objects.create(list=list_, text=request.POST['text'])
                    item_dicts = {'id': item.id, 'text': item.text}
                    status = 201
            except IntegrityError:
                item_dicts = {'error': DUPLICATE_ITEM_ERROR}
                status = 400
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
            content=json.dumps({'error':'list not found'}),
            status=404,
            content_type='application/json'
        )
