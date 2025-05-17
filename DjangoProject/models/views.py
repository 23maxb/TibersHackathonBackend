import json

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt


def is_image_file(filename):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    image_extensions = {'.png'}
    ext = os.path.splitext(filename)[1].lower()
    return ext in image_extensions


def handle_uploaded_file(f, filename, id):
    downloads_dir = os.path.join('downloads')
    os.makedirs(downloads_dir, exist_ok=True)
    file_path = os.path.join(downloads_dir, str(id) + '_' + filename)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


upload_counter = 0


@csrf_exempt
def reset(request):
    global upload_counter
    upload_counter = 0
    # remove downloads folder
    downloads_dir = os.path.join('downloads')
    if os.path.exists(downloads_dir):
        for filename in os.listdir(downloads_dir):
            file_path = os.path.join(downloads_dir, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        os.rmdir(downloads_dir)
    else:
        return JsonResponse({"status": "error", "message": "Downloads directory does not exist."})
    return JsonResponse({"status": "success", "message": "Counter reset successfully."})


@csrf_exempt
def hello(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        filename = uploaded_file.name
        if not is_image_file(filename):
            return HttpResponseBadRequest("Only png files are accepted.\n")
        if os.path.exists('downloads'):
            if filename in os.listdir('downloads'):
                return HttpResponseBadRequest("File already exists.\n")
        global upload_counter
        upload_counter += 1
        handle_uploaded_file(uploaded_file, uploaded_file.name, upload_counter)
        return JsonResponse(
            {
                "status": "success",
                "id": (upload_counter)
            }
        )
    return HttpResponseBadRequest("Only POST with a file is accepted.\n")


def runModel(id):
    print('hi')


@csrf_exempt
def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        my_param = data.get('id')
        return JsonResponse(
            {
                "status": "success",
                "id": my_param,
                "classification": runModel(my_param)
            }
        )
    return JsonResponse({"status": "need post request"})
