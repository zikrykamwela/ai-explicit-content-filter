import os
import tempfile
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

PREDICTION_WORKER = ThreadPoolExecutor(max_workers=1)
PREDICTION_JOBS = {}
PREDICTION_JOBS_LOCK = threading.Lock()


def _run_prediction(job_id, temp_path):
    try:
        from src.predict import predict_image

        result = predict_image(temp_path)
        with PREDICTION_JOBS_LOCK:
            PREDICTION_JOBS[job_id] = {"status": "completed", "result": result}
    except Exception as error:
        with PREDICTION_JOBS_LOCK:
            PREDICTION_JOBS[job_id] = {"status": "failed", "error": str(error)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def _predict_upload(uploaded_file):
    if not uploaded_file or not uploaded_file.name:
        return JsonResponse({"error": "Choose an image to analyze."}, status=400)

    temp_path = None
    try:
        suffix = os.path.splitext(uploaded_file.name)[1] or ".img"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name
        job_id = uuid.uuid4().hex
        with PREDICTION_JOBS_LOCK:
            PREDICTION_JOBS[job_id] = {"status": "processing"}
        PREDICTION_WORKER.submit(_run_prediction, job_id, temp_path)
        temp_path = None
        return JsonResponse({"job_id": job_id, "status": "processing"}, status=202)
    except Exception as error:
        return JsonResponse({"error": str(error)}, status=500)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == "POST":
        return _predict_upload(request.FILES.get("image"))
    return render(request, "filter_site/home.html")


@csrf_exempt
@require_http_methods(["POST"])
def predict_api(request):
    return _predict_upload(request.FILES.get("image"))


@csrf_exempt
@require_http_methods(["GET"])
def prediction_status(request, job_id):
    with PREDICTION_JOBS_LOCK:
        job = PREDICTION_JOBS.get(job_id)
    if not job:
        return JsonResponse({"error": "Prediction job was not found."}, status=404)
    return JsonResponse(job, status=500 if job["status"] == "failed" else 200)
