import json
import re
import urllib.error
import urllib.request
from django.conf import settings

SYSTEM_PROMPT='''You are DNY AI Assistant for DNYAUTOMATED. Be concise, helpful and honest.
DNYAUTOMATED offers AI agents/chatbots, business automation, n8n workflows, Python automation,
API/webhook integrations, Google Workspace automation, invoice/document AI, custom software,
and WordPress/web systems. Answer in the user's language: English, Urdu, or natural Roman Urdu.
Never invent an exact price, delivery date, client result, policy, or capability. Explain that final
pricing follows discovery. Ask at most one useful follow-up question. For a serious enquiry, invite
the visitor to share contact details through the secure lead form or use Request a Quote.
Never request passwords, payment card information, API keys, or other secrets.'''

def fallback_reply(message):
    q=message.lower()
    roman=bool(re.search(r'\b(yaar|mujhe|mujhy|kya|kia|kaise|kesy|chahiye|karna|meri|ap|batao|kitna)\b',q))
    if re.search(r'price|cost|budget|rate|charges|kitn',q):
        return ('Exact price requirements aur integrations dekh kar confirm hoti hai. Aap project type aur main features bata dein.' if roman else 'Pricing depends on scope and integrations. Tell me the project type and main features, and I’ll suggest the right next step.')
    if re.search(r'chatbot|ai agent|support bot',q):
        return ('Hum website AI chatbot bana sakte hain jo FAQs answer kare, leads collect kare, Urdu/English samjhe aur WhatsApp ya human support ko handoff kare.' if roman else 'We can build a website AI chatbot for FAQs, lead capture, multilingual support, and WhatsApp or human handoff.')
    if re.search(r'invoice|document|ocr|receipt',q):
        return ('Document automation mein OCR/AI extraction, review, Drive/database/Sheets sync aur reporting shamil ho sakti hai. Aap kis type ke documents process karte hain?' if roman else 'Document automation can include OCR/AI extraction, review, Drive/database/Sheets sync, and reporting. What document type do you process?')
    if re.search(r'n8n|workflow|automat',q):
        return ('Automation flow trigger, validation, business logic, system update aur notification par banta hai. Aap kaunsa repetitive process automate karna chahte hain?' if roman else 'A typical automation connects a trigger, validation, business logic, system updates, and notifications. Which repetitive process do you want to automate?')
    if re.search(r'wordpress|website|web ',q):
        return ('DNYAUTOMATED responsive WordPress aur custom websites ko lead capture, email, CRM aur automation ke saath integrate karta hai. New website chahiye ya existing improve karni hai?' if roman else 'DNYAUTOMATED builds responsive WordPress and custom websites with lead, email, CRM, and automation integrations. Is this a new site or an improvement?')
    if re.search(r'hello|hi|hey|salam|assalam',q):
        return ('Assalam-o-Alaikum! Main DNY AI Assistant hoon. Aap AI automation, chatbot, custom software, WordPress ya document automation ke bare mein pooch sakte hain.' if roman else 'Hello! I’m the DNY AI Assistant. Ask me about AI automation, chatbots, custom software, WordPress, or document automation.')
    return ('Main DNYAUTOMATED ki services aur aapke project ka suitable solution samjhane mein help kar sakta hoon. Aapka main business problem kya hai?' if roman else 'I can match your business problem with a DNYAUTOMATED service. What process or feature do you need?')

def ai_reply(message, history, business_summary=''):
    if not settings.AI_API_KEY or settings.AI_PROVIDER != 'gemini': return fallback_reply(message),'fallback'
    prompt=SYSTEM_PROMPT+'\nBusiness context: '+business_summary+'\nRecent conversation:\n'
    prompt+='\n'.join(f"{x.role}: {x.content}" for x in history[-8:])+'\nuser: '+message+'\nassistant:'
    url=f'https://generativelanguage.googleapis.com/v1beta/models/{settings.AI_MODEL}:generateContent?key={settings.AI_API_KEY}'
    payload={'contents':[{'parts':[{'text':prompt}]}],'generationConfig':{'temperature':0.35,'maxOutputTokens':350}}
    request=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(request,timeout=settings.AI_TIMEOUT) as response: data=json.loads(response.read().decode())
        return data['candidates'][0]['content']['parts'][0]['text'].strip(),'gemini'
    except (urllib.error.URLError,urllib.error.HTTPError,KeyError,IndexError,ValueError,TimeoutError):
        return fallback_reply(message),'fallback'
