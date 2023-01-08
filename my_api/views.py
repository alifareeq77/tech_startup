from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json


def update_json(data):
    with open('my_api/media/my_app/data.json', "r+") as file:
        d = json.load(file)
        d.append(data)  # make a new dict with the new data
        print('updating ....')
        file.seek(0)  # resetting my file pointer to zero  so i can dump data
        json.dump(d, file, indent=2)  # add data to json


@csrf_exempt
def get_view(request):
    if request.method != 'GET':
        data = json.loads(request.body.decode("utf-8"))
        d = data
        del data['id']

    return render(request, 'my_api/index.html', {})


@csrf_exempt
def get_it(request):
    with open('my_api/media/my_app/data.json', 'r') as f:
        response = json.load(f)
    if request.method == 'GET':
        return JsonResponse(response, content_type="application/json", safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        # if id is already in post request
        try:
            if int(data['id']) != len(response) + 1:
                olid = data['id']  # store given id to give an error
                data.update({'id': len(response) + 1})  # make the post id in sync with others
                print(data)  # debug
                update_json(data=data)
                return JsonResponse(
                    [{'code': 200,
                      'description': f'id ({olid}) is not in the correct order changed to -> {len(response) + 2} and '
                                     f'successfully created raw'}],
                    content_type="application/json", safe=False)
            else:  # given id is in sync with other
                update_json(data=data)
                return JsonResponse(
                    [{'code': 200, 'description': 'successfully created raw'}], content_type="application/json",
                    safe=False)
        except KeyError as e:  # auto generate id
            data.update({'id': len(response) + 1})
            with open('my_api/media/my_app/data.json', "r+") as file:
                d = json.load(file)
                d.append(data)
                file.seek(0)
                json.dump(d, file, indent=2)
            return JsonResponse(
                [{'code': 200, 'description': f'successfully created row with id = {len(response) + 1}'}],
                content_type="application/json",
                safe=False)


@csrf_exempt
def get_it_id(request, id):
    id = int(id)
    with open('my_api/media/my_app/data.json', 'r+') as f:
        response = json.load(f)
    if id > 0 and id < len(response):
        if request.method == 'GET':
            return JsonResponse(response[int(id) - 1], content_type="application/json", safe=False)
        elif request.method == 'DELETE':  # TODO make efficient way to update json file
            with open('my_api/media/my_app/data.json', "r+") as file:
                d = json.load(file)
                d.pop(id - 1)  # make a new dict with the new data
                print('updating ....')
                json.dump(d, file, indent=2)  # add data to json
                return JsonResponse(
                    [{'code': 200, 'description': f'successfully deleted row with id = {len(response) + 1}'}],
                    content_type="application/json",
                    safe=False)
    else:
        return JsonResponse([{'code': 404,
                              'description': f'{id} is out of indexing range try number from 1 to {len(response)}'
                              }], content_type="application/json", safe=False)
