from django.contrib import admin
from .models import *
admin.site.site_header='DNYAUTOMATED Administration'; admin.site.site_title='DNYAUTOMATED'; admin.site.index_title='Business Operations'
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display=('reference','name','kind','service','status','source','next_follow_up','created_at'); list_filter=('kind','status','source'); search_fields=('reference','name','email','company','service'); list_editable=('status',)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin): list_display=('title','client','status','progress','updated_at'); list_filter=('status',)
for m in [Milestone,ProjectFile,SupportTicket,Proposal,CaseStudy,BlogPost]: admin.site.register(m)
@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display=('session_key','visitor_name','visitor_email','visitor_phone','lead','started_at','updated_at','is_closed')
    search_fields=('visitor_name','visitor_email','visitor_phone','session_key')
    list_filter=('is_closed','language','started_at')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display=('session','role','short_content','created_at')
    list_filter=('role','created_at')
    search_fields=('content','session__visitor_name','session__visitor_email')
    def short_content(self,obj): return obj.content[:90]

@admin.register(ChatbotSetting)
class ChatbotSettingAdmin(admin.ModelAdmin):
    list_display=('bot_name','is_active','whatsapp_number','updated_at')
