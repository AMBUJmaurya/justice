import json

from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .forms import ContactInquiryForm
from .models import PracticeArea


PAGES = {
    'home': {'template': 'main/index.html', 'title': 'ByLaw Site - Your SUPER-power'},
    'about': {'template': 'main/about.html', 'title': 'About Us - JurisForge'},
    'practice_areas': {'template': 'main/practice-areas.html', 'title': 'Practice Areas - JurisForge'},
    'courts': {'template': 'main/courts.html', 'title': 'Courts - JurisForge'},
    'advocates': {'template': 'main/advocates.html', 'title': 'Advocates - JurisForge'},
    'contacts': {'template': 'main/contacts.html', 'title': 'Contact Us - ByLaw Site'},
}


def render_page(request, page_key, extra_context=None):
    page = PAGES[page_key]
    context = {
        'current_page': page_key,
        'page_title': page['title'],
    }
    if extra_context:
        context.update(extra_context)
    return render(request, page['template'], context)


@ensure_csrf_cookie
def home(request):
    practice_areas = PracticeArea.objects.filter(is_active=True, show_on_home=True).order_by("order", "title")[:9]
    return render_page(request, 'home', {"practice_areas": practice_areas})


@ensure_csrf_cookie
def about(request):
    return render_page(request, 'about')


@ensure_csrf_cookie
def practice_areas(request):
    practice_areas = PracticeArea.objects.filter(is_active=True).order_by("order", "title")
    return render_page(request, 'practice_areas', {"practice_areas": practice_areas})


@ensure_csrf_cookie
def courts(request):
    return render_page(request, 'courts')


@ensure_csrf_cookie
def advocates(request):
    return render_page(request, 'advocates')


@ensure_csrf_cookie
def contacts(request):
    if request.method == 'POST':
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            notify_to = [settings.CONTACT_NOTIFY_EMAIL] if getattr(settings, "CONTACT_NOTIFY_EMAIL", "") else []
            if notify_to:
                subject = f"[ByLaw Contact] {inquiry.subject}"
                body = (
                    "New contact inquiry received:\n\n"
                    f"Name: {inquiry.first_name} {inquiry.last_name}\n"
                    f"Email: {inquiry.email}\n"
                    f"Phone: {inquiry.phone}\n"
                    f"Service: {inquiry.service}\n"
                    f"Submitted: {inquiry.created_at}\n\n"
                    "Message:\n"
                    f"{inquiry.message}\n"
                )
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=notify_to,
                    reply_to=[inquiry.email],
                )
                try:
                    email.send(fail_silently=False)
                except Exception:
                    messages.warning(
                        request,
                        "Your message was saved, but email notification could not be sent. Please check email settings.",
                    )

            messages.success(request, 'Thank you for your message. Our legal team will contact you soon.')
            return redirect('main:contacts')
    else:
        form = ContactInquiryForm()

    return render_page(request, 'contacts', {'form': form})


@require_POST
def ai_ask(request):
    """
    Lightweight AI Q&A endpoint for court/case related questions.
    Returns general information only (not legal advice).
    """
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "answer": "Invalid request."}, status=400)

    question = (payload.get("question") or "").strip()
    if not question:
        return JsonResponse({"ok": False, "answer": "Please type a question."}, status=400)

    # Always have an offline fallback so the widget never feels "dead".
    from .ai_offline import answer_offline

    api_key = getattr(settings, "OPENAI_API_KEY", "") or ""
    if not api_key:
        offline = answer_offline(question)
        return JsonResponse({"ok": True, "answer": "[Offline]\n" + offline.answer})

    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return JsonResponse(
            {
                "ok": False,
                "answer": "AI library is missing. Run: pip install openai",
            },
            status=503,
        )

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are a helpful assistant for a law website in India (Uttar Pradesh). "
        "Answer questions about court process, documents, hearings, and general legal procedure. "
        "Do NOT provide final legal advice, do NOT promise outcomes, and do NOT instruct illegal actions. "
        "If the user asks for case-specific advice, ask for missing basic facts and recommend consulting an advocate. "
        "Keep answers concise, step-by-step, and in simple Hinglish where helpful."
    )

    try:
        resp = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.2,
            max_tokens=350,
        )
        answer = (resp.choices[0].message.content or "").strip()
    except Exception as e:
        # Common issues: quota/billing, networking, invalid key. Fallback offline.
        offline = answer_offline(question)
        debug_hint = f"\n\n[Debug]\n{e}" if settings.DEBUG else ""
        return JsonResponse(
            {
                "ok": True,
                "answer": "[Offline]\n"
                + offline.answer
                + ("\n\n(Online AI unavailable right now.)" + debug_hint),
            }
        )

    if not answer:
        answer = "I couldn't generate an answer. Please rephrase your question."

    return JsonResponse({"ok": True, "answer": answer})
