from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def get_view(request):
    if request.method != 'GET':
        data = json.loads(request.body.decode("utf-8"))
        d = data
        del data['id']
        print(data)
    return render(request, 'my_api/index.html', {})


@csrf_exempt
def get_it(request):
    with open('my_api/media/my_app/data.json', 'r') as f:
        response = json.load(f)
    if request.method == 'GET':
        return JsonResponse(response, content_type="application/json", safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        if data['id']:

            if int(data['id']) != len(response) + 2:
                olid = data['id']
                data.update({'id': len(response) + 2})
                print(data)
                with open('my_api/media/my_app/data.json', "a") as file:
                    json.dump(data, file)

                file.close()
                return JsonResponse(
                    [{'code': 200,
                      'description': f'id ({olid}) is not in the correct order changed to -> {len(response) + 2} and '
                                     f'successfully created raw'}],
                    content_type="application/json", safe=False)


@csrf_exempt
def get_it_id(request, id):
    id = int(id)
    with open('my_api/media/my_app/data.json', 'r') as f:
        response = json.load(f)
    if id > 0 and id < len(response):
        if request.method == 'GET':
            return JsonResponse(response[int(id) - 1], content_type="application/json", safe=False)

        elif request.method == 'DELETE':
            # f.write(request.data)
            print(request.body)
    else:
        return JsonResponse([{'code': 404,
                              'description': f'{id} is out of indexing range try number from 1 to {len(response)}'
                              }], content_type="application/json", safe=False)
