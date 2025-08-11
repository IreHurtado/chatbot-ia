import json
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.conf import settings

from openai import OpenAI

SYSTEM_PROMPT = (
    "Eres un asistente útil, preciso y conciso. "
    "Si no tienes datos, dilo claramente. Responde en español por defecto."
)

def _get_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else OpenAI()

def _session_messages(request: HttpRequest):
    """
    Estructura: [{"role":"system"|"user"|"assistant", "content":"..."}]
    """
    if "messages" not in request.session:
        request.session["messages"] = [{"role":"system","content": SYSTEM_PROMPT}]
    return request.session["messages"]

def _truncate_history(messages, max_messages=20):
    """
    Recorta historial manteniendo system + últimos turnos.
    Sencillo, práctico para MVP.
    """
    system = messages[0:1]
    rest = messages[1:]
    if len(rest) > max_messages:
        rest = rest[-max_messages:]
    return system + rest

@ensure_csrf_cookie
def index(request: HttpRequest) -> HttpResponse:
    messages = _session_messages(request)
    return render(request, "index.html", {
        "messages": messages,
        "model": settings.OPENAI_MODEL,
    })

@require_POST
def chat_api(request: HttpRequest) -> JsonResponse:
    if not settings.OPENAI_API_KEY:
        return JsonResponse({"error":"Falta OPENAI_API_KEY"}, status=500)

    try:
        payload = json.loads(request.body.decode("utf-8"))
        user_msg = payload.get("message", "").strip()
        model = settings.OPENAI_MODEL
        max_output = settings.MAX_RESPONSE_TOKENS

        if not user_msg:
            return JsonResponse({"error":"Mensaje vacío"}, status=400)

        messages = _session_messages(request)
        messages.append({"role":"user", "content": user_msg})
        messages = _truncate_history(messages, max_messages=20)

        client = _get_client()
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_output,
            temperature=0.7,
        )

        reply = resp.choices[0].message.content
        usage = getattr(resp, "usage", None)
        prompt_tokens = getattr(usage, "prompt_tokens", None)
        completion_tokens = getattr(usage, "completion_tokens", None)
        total_tokens = getattr(usage, "total_tokens", None)

        # guarda respuesta y usage en sesión
        messages.append({"role":"assistant", "content": reply})
        request.session["messages"] = messages
        request.session["usage"] = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        }
        request.session.modified = True

        return JsonResponse({
            "reply": reply,
            "usage": request.session["usage"],
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_POST
def reset_session(request: HttpRequest) -> JsonResponse:
    request.session.flush()
    return JsonResponse({"ok": True})