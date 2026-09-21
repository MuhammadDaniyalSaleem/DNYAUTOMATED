from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Lead(models.Model):
    KIND=[('contact','Contact'),('quote','Quote'),('audit','Automation Audit'),('booking','Consultation')]
    STATUS=[('New','New'),('Qualified','Qualified'),('Meeting','Meeting'),('Proposal','Proposal'),('Negotiation','Negotiation'),('Won','Won'),('Lost','Lost')]
    kind=models.CharField(max_length=20,choices=KIND,default='contact'); reference=models.CharField(max_length=24,blank=True,unique=True,null=True)
    name=models.CharField(max_length=120); email=models.EmailField(); phone=models.CharField(max_length=40,blank=True); company=models.CharField(max_length=150,blank=True); country=models.CharField(max_length=80,blank=True)
    service=models.CharField(max_length=150,blank=True); budget=models.CharField(max_length=80,blank=True); timeline=models.CharField(max_length=80,blank=True); tools=models.CharField(max_length=250,blank=True); source=models.CharField(max_length=120,blank=True)
    message=models.TextField(); attachment=models.FileField(upload_to='lead_files/',blank=True,null=True); created_at=models.DateTimeField(auto_now_add=True); status=models.CharField(max_length=30,choices=STATUS,default='New'); notes=models.TextField(blank=True); next_follow_up=models.DateField(blank=True,null=True); estimated_value=models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)
    def save(self,*a,**kw):
        super().save(*a,**kw)
        if not self.reference:
            prefix={'quote':'QUOTE','audit':'AUDIT','booking':'BOOK','contact':'LEAD'}.get(self.kind,'LEAD'); self.reference=f'DNY-{prefix}-{self.pk:04d}'; super().save(update_fields=['reference'])
    def __str__(self): return f'{self.reference or "DNY"} — {self.name}'

class Project(models.Model):
    STATUSES=[(x,x) for x in ['Discovery','Requirements','Development','Testing','Client Review','Deployment','Completed']]
    client=models.ForeignKey(User,on_delete=models.CASCADE); title=models.CharField(max_length=160); service=models.CharField(max_length=120); description=models.TextField(blank=True); status=models.CharField(max_length=50,choices=STATUSES,default='Discovery'); progress=models.PositiveIntegerField(default=10); next_milestone=models.CharField(max_length=180,blank=True); confidential=models.BooleanField(default=False); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.title
class Milestone(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='milestones'); title=models.CharField(max_length=160); due_date=models.DateField(blank=True,null=True); completed=models.BooleanField(default=False)
    def __str__(self): return self.title
class ProjectFile(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='files'); title=models.CharField(max_length=160); file=models.FileField(upload_to='project_files/'); uploaded_at=models.DateTimeField(auto_now_add=True)
class SupportTicket(models.Model):
    PRIORITY=[('Normal','Normal'),('High','High'),('Urgent','Urgent')]; STATUS=[('Open','Open'),('In Progress','In Progress'),('Resolved','Resolved')]
    client=models.ForeignKey(User,on_delete=models.CASCADE); project=models.ForeignKey(Project,on_delete=models.SET_NULL,null=True,blank=True); subject=models.CharField(max_length=180); message=models.TextField(); priority=models.CharField(max_length=20,choices=PRIORITY,default='Normal'); status=models.CharField(max_length=20,choices=STATUS,default='Open'); created_at=models.DateTimeField(auto_now_add=True)
class Proposal(models.Model):
    STATUS=[('Draft','Draft'),('Sent','Sent'),('Viewed','Viewed'),('Accepted','Accepted'),('Declined','Declined')]
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='proposals'); title=models.CharField(max_length=180); scope=models.TextField(); deliverables=models.TextField(); timeline=models.CharField(max_length=100,blank=True); price=models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True); terms=models.TextField(blank=True); status=models.CharField(max_length=20,choices=STATUS,default='Draft'); created_at=models.DateTimeField(auto_now_add=True)
class CaseStudy(models.Model):
    title=models.CharField(max_length=180); slug=models.SlugField(unique=True); category=models.CharField(max_length=100); summary=models.TextField(); challenge=models.TextField(blank=True); solution=models.TextField(blank=True); workflow=models.CharField(max_length=300,blank=True); tech_stack=models.CharField(max_length=300,blank=True); image=models.ImageField(upload_to='case_studies/',blank=True,null=True); confidential=models.BooleanField(default=False); published=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
class BlogPost(models.Model):
    title=models.CharField(max_length=180); slug=models.SlugField(unique=True); category=models.CharField(max_length=80,default='Automation'); excerpt=models.TextField(); body=models.TextField(); published=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class ChatSession(models.Model):
    session_key=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    visitor_name=models.CharField(max_length=120,blank=True)
    visitor_email=models.EmailField(blank=True)
    visitor_phone=models.CharField(max_length=40,blank=True)
    language=models.CharField(max_length=20,default='auto')
    lead=models.ForeignKey(Lead,on_delete=models.SET_NULL,null=True,blank=True,related_name='chat_sessions')
    started_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_closed=models.BooleanField(default=False)
    def __str__(self): return f'Chat {str(self.session_key)[:8]} — {self.visitor_name or "Visitor"}'

class ChatMessage(models.Model):
    ROLES=[('user','User'),('assistant','Assistant')]
    session=models.ForeignKey(ChatSession,on_delete=models.CASCADE,related_name='messages')
    role=models.CharField(max_length=12,choices=ROLES)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['created_at']
    def __str__(self): return f'{self.role}: {self.content[:50]}'

class ChatbotSetting(models.Model):
    bot_name=models.CharField(max_length=80,default='DNY AI Assistant')
    welcome_message=models.TextField(default='Hi! I can help you choose the right automation, AI or software service. What would you like to improve?')
    business_summary=models.TextField(blank=True,default='DNYAUTOMATED provides AI agents, business automation, n8n workflows, Python automation, API integrations, document AI, custom software and WordPress solutions.')
    whatsapp_number=models.CharField(max_length=40,blank=True)
    is_active=models.BooleanField(default=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.bot_name
