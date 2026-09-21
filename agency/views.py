from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.middleware.csrf import get_token
import json
import uuid
from .forms import LeadForm,TicketForm
from .models import Lead,Project,BlogPost,CaseStudy,SupportTicket,Proposal,ChatSession,ChatMessage,ChatbotSetting
from .email_notifications import send_lead_notifications
from .chatbot import ai_reply
SERVICES=[
{'name':'AI Agents & Chatbots','slug':'ai-agents','desc':'Knowledge assistants, lead qualification and task-oriented AI agents.','category':'AI','workflow':'Question → Context → AI reasoning → Action → Human handoff','use':'Support, lead qualification, internal knowledge, task assistance'},
{'name':'Business Process Automation','slug':'business-automation','desc':'Remove repetitive work across sales, operations, HR, finance and reporting.','category':'Automation','workflow':'Trigger → Validate → Process → Update systems → Notify','use':'Operations, approvals, reporting, data movement'},
{'name':'n8n Workflow Automation','slug':'n8n','desc':'Reliable multi-step workflows connecting the tools your team already uses.','category':'Automation','workflow':'Trigger → n8n logic → APIs → Database → Notification','use':'Cross-app workflows, scheduled jobs, lead routing'},
{'name':'Python Automation','slug':'python','desc':'Custom scripts and services for workflows that need more control and logic.','category':'Automation','workflow':'Input → Python service → Business rules → Output','use':'Data processing, scheduled jobs, custom integrations'},
{'name':'Invoice & Document AI','slug':'document-ai','desc':'OCR, extraction, review, routing, Drive/Sheets sync and reporting pipelines.','category':'AI','workflow':'Document → OCR/AI → Review → Drive → Database/Sheets','use':'Invoices, receipts, forms, business documents'},
{'name':'API & Webhook Integrations','slug':'api','desc':'Connect CRMs, forms, databases, SaaS tools and custom applications.','category':'Integrations','workflow':'System A → API/Webhook → Validation → System B','use':'CRM sync, notifications, payments, custom apps'},
{'name':'Google Workspace Automation','slug':'google','desc':'Automate Sheets, Drive, Gmail and connected business processes.','category':'Integrations','workflow':'Form/Email → Logic → Drive/Sheets → Notification','use':'Records, file routing, reporting, approvals'},
{'name':'Custom Software','slug':'custom-software','desc':'Purpose-built dashboards, portals, internal tools and business applications.','category':'Software','workflow':'Requirements → UX → Backend → Database → Deployment','use':'Dashboards, portals, internal systems, SaaS'},
{'name':'WordPress & Web Systems','slug':'wordpress','desc':'Conversion-focused websites integrated with automation and business systems.','category':'Software','workflow':'Website → Lead capture → Automation → CRM/Email','use':'Corporate sites, landing pages, automated lead capture'},
]
SOLUTIONS=[('Lead Automation','Capture, qualify, route and follow up without copying data between tools.'),('Customer Support','AI-assisted answers, routing and human handoff.'),('Document Processing','Extract, validate and route invoice or document data.'),('Reporting Automation','Turn operational data into repeatable reports and alerts.'),('Internal Operations','Connect approvals, records, notifications and business systems.'),('Appointment Workflows','Capture bookings and automate confirmations and follow-ups.')]
INDUSTRIES=[('Real Estate','Lead routing, enquiry follow-up and document workflows.'),('E-commerce','Order operations, support and reporting.'),('HR & Recruitment','Candidate intake, document processing and notifications.'),('Accounting & Admin','Invoices, records, approvals and reporting.'),('Agencies','Lead intake, delivery workflows and client operations.'),('Retail & SMEs','Sales records, inventory workflows and reporting.'),('Education','Admissions, enquiries and administrative workflows.'),('Professional Services','Client intake, documents, scheduling and follow-up.')]

def ctx(page,extra=None):
    d={'page':page,'services':SERVICES,'solutions_data':SOLUTIONS,'industries_data':INDUSTRIES}; d.update(extra or {}); return d
def page(r,name,extra=None):
    get_token(r)
    return render(r,f'agency/{name}.html',ctx(name,extra))
def home(r): return page(r,'home',{'featured':CaseStudy.objects.filter(published=True)[:3]})
def services(r): return page(r,'services')
def service_detail(r,slug):
    item=next((x for x in SERVICES if x['slug']==slug),None)
    if item is None:
        from django.http import Http404
        raise Http404('Service not found')
    return page(r,'service_detail',{'item':item})
def solutions(r): return page(r,'solutions')
def industries(r): return page(r,'industries')
def integrations(r): return page(r,'integrations')
def tech_stack(r): return page(r,'tech_stack')
def pricing(r): return page(r,'pricing')
def about(r): return page(r,'about')
def lab(r): return page(r,'lab')
def case_studies(r): return page(r,'case_studies',{'cases':CaseStudy.objects.filter(published=True)})
def case_detail(r,slug): return page(r,'case_detail',{'case':get_object_or_404(CaseStudy,slug=slug,published=True)})
def blog(r): return page(r,'blog',{'posts':BlogPost.objects.filter(published=True).order_by('-created_at')})
def privacy(r): return page(r,'privacy')
def terms(r): return page(r,'terms')
def site_search(r):
    q=r.GET.get('q','').strip(); posts=BlogPost.objects.filter(Q(title__icontains=q)|Q(excerpt__icontains=q),published=True) if q else []; cases=CaseStudy.objects.filter(Q(title__icontains=q)|Q(summary__icontains=q),published=True) if q else []; sv=[s for s in SERVICES if q.lower() in (s['name']+' '+s['desc']).lower()] if q else []
    return page(r,'search',{'q':q,'posts':posts,'cases':cases,'service_results':sv})
def lead_page(r,pagename,kind):
    initial={'service':r.GET.get('service','')}; form=LeadForm(r.POST or None,r.FILES or None,initial=initial)
    if r.method=='POST' and form.is_valid():
        obj=form.save(commit=False); obj.kind=kind; obj.source=r.POST.get('source') or r.GET.get('source') or pagename; obj.save(); send_lead_notifications(obj); return redirect('thank_you',reference=obj.reference)
    return page(r,pagename,{'form':form,'kind':kind})
def contact(r): return lead_page(r,'contact','contact')
def quote(r): return lead_page(r,'quote','quote')
def audit(r): return lead_page(r,'audit','audit')
def booking(r): return lead_page(r,'booking','booking')
def thank_you(r,reference): return page(r,'thank_you',{'reference':reference})
def client_login(r):
    if r.method=='POST':
        u=authenticate(r,username=r.POST.get('username'),password=r.POST.get('password'))
        if u: login(r,u); return redirect('portal')
        messages.error(r,'Invalid username or password.')
    return page(r,'login')
@login_required
def portal(r): return page(r,'portal',{'projects':Project.objects.filter(client=r.user),'tickets':SupportTicket.objects.filter(client=r.user).order_by('-created_at')[:5]})
@login_required
def support(r):
    form=TicketForm(r.POST or None); form.fields['project'].queryset=Project.objects.filter(client=r.user)
    if r.method=='POST' and form.is_valid(): x=form.save(commit=False); x.client=r.user; x.save(); messages.success(r,'Support request created.'); return redirect('portal')
    return page(r,'support',{'form':form})
def client_logout(r): logout(r); return redirect('home')
@user_passes_test(lambda u:u.is_staff)
def staff_dashboard(r):
    leads=Lead.objects.order_by('-created_at'); return page(r,'staff_dashboard',{'leads':leads[:20],'projects':Project.objects.order_by('-updated_at')[:10],'tickets':SupportTicket.objects.order_by('-created_at')[:10],'overdue':leads.filter(next_follow_up__lt=timezone.localdate()).exclude(status__in=['Won','Lost']).count()})

def _chat_payload(request):
    try: return json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError,UnicodeDecodeError): return None

def _chat_session(key=None):
    if key:
        try: return ChatSession.objects.get(session_key=uuid.UUID(str(key)),is_closed=False)
        except (ValueError,ChatSession.DoesNotExist): pass
    return ChatSession.objects.create()

@require_POST
def chat_api(request):
    data=_chat_payload(request)
    if data is None: return JsonResponse({'error':'Invalid request.'},status=400)
    message=str(data.get('message','')).strip()
    if not message: return JsonResponse({'error':'Please enter a message.'},status=400)
    if len(message)>settings.CHATBOT_MAX_MESSAGE_LENGTH: return JsonResponse({'error':'Message is too long.'},status=400)
    bot=ChatbotSetting.objects.filter(is_active=True).order_by('-updated_at').first()
    if ChatbotSetting.objects.exists() and bot is None: return JsonResponse({'error':'Assistant is temporarily unavailable.'},status=503)
    session=_chat_session(data.get('session_id'))
    history=list(session.messages.order_by('-created_at')[:8])[::-1]
    ChatMessage.objects.create(session=session,role='user',content=message)
    reply,provider=ai_reply(message,history,bot.business_summary if bot else '')
    ChatMessage.objects.create(session=session,role='assistant',content=reply)
    return JsonResponse({'reply':reply,'session_id':str(session.session_key),'provider':provider})

@require_POST
def chat_lead_api(request):
    data=_chat_payload(request)
    if data is None: return JsonResponse({'error':'Invalid request.'},status=400)
    name=str(data.get('name','')).strip()[:120]; email=str(data.get('email','')).strip()[:254]
    phone=str(data.get('phone','')).strip()[:40]; requirement=str(data.get('requirement','')).strip()[:3000]
    if not name or not email or not requirement: return JsonResponse({'error':'Name, email and requirement are required.'},status=400)
    try: validate_email(email)
    except ValidationError: return JsonResponse({'error':'Please enter a valid email.'},status=400)
    session=_chat_session(data.get('session_id'))
    lead=Lead.objects.create(kind='contact',name=name,email=email,phone=phone,service='AI Chatbot Enquiry',message=requirement,source='website-chatbot')
    session.visitor_name=name; session.visitor_email=email; session.visitor_phone=phone; session.lead=lead
    session.save(update_fields=['visitor_name','visitor_email','visitor_phone','lead','updated_at'])
    send_lead_notifications(lead)
    return JsonResponse({'ok':True,'reference':lead.reference,'message':'Thank you. Your enquiry has been saved.'})

def sitemap(r):
    names=['home','services','solutions','industries','integrations','tech_stack','case_studies','lab','pricing','about','blog','contact','quote','audit','booking','privacy','terms']
    from django.urls import reverse
    base=r.build_absolute_uri('/').rstrip('/')
    urls=''.join(f'<url><loc>{base}{reverse(n)}</loc></url>' for n in names)
    return HttpResponse('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>',content_type='application/xml')
