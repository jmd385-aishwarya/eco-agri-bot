from django.shortcuts import render
from django.http import JsonResponse
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

SYSTEM_PROMPT = (
    "You are a helpful Eco-Agriculture and Botanical Advisor. "
    "You specialise in plant identification, crop advice, soil health, "
    "sustainable farming, and ecological gardening. "
    "Always provide practical, science-based guidance."
)


def index(request):
    return render(request, 'chat/index.html')


def chat_view(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    try:
        user_message = request.POST.get('message', '').strip()

        if not user_message:
            return JsonResponse({'status': 'error', 'message': 'Please provide a message.'}, status=400)

        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAdvisor:"

        payload = {
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False,
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()

        response_data = response.json()
        bot_reply = response_data.get('response', '').strip()

        return JsonResponse({'status': 'success', 'response': bot_reply})

    except requests.exceptions.ConnectionError:
        return JsonResponse(
            {'status': 'error', 'message': 'Cannot connect to Ollama. Make sure it is running (run: ollama serve)'},
            status=500
        )
    except requests.exceptions.Timeout:
        return JsonResponse(
            {'status': 'error', 'message': 'Ollama took too long to respond. Try a shorter message.'},
            status=500
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)