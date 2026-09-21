from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Lead,ChatSession,ChatMessage
import json

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='DNYAUTOMATED <test@dny.local>',
    LEAD_NOTIFICATION_EMAIL='owner@dny.local',
)
class LeadNotificationTests(TestCase):
    def _submit(self, route):
        return self.client.post(reverse(route), {
            'name':'Test Client','email':'client@example.com','phone':'','company':'Example Co',
            'country':'UK','service':'AI Automation','budget':'','timeline':'','tools':'Google Sheets',
            'message':'Please automate this workflow.'
        })

    def test_contact_saves_and_sends_two_emails(self):
        response=self._submit('contact')
        self.assertEqual(response.status_code,302)
        lead=Lead.objects.get()
        self.assertEqual(lead.kind,'contact')
        self.assertTrue(lead.reference.startswith('DNY-LEAD-'))
        self.assertEqual(len(mail.outbox),2)
        self.assertEqual(mail.outbox[0].to,['owner@dny.local'])
        self.assertEqual(mail.outbox[1].to,['client@example.com'])
        self.assertIn(lead.reference,mail.outbox[0].subject)
        self.assertIn(lead.reference,mail.outbox[1].subject)

    def test_all_lead_forms_trigger_notifications(self):
        for route,kind in [('quote','quote'),('audit','audit'),('booking','booking')]:
            mail.outbox.clear()
            response=self._submit(route)
            self.assertEqual(response.status_code,302)
            self.assertEqual(Lead.objects.latest('id').kind,kind)
            self.assertEqual(len(mail.outbox),2)

@override_settings(AI_API_KEY='',EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',LEAD_NOTIFICATION_EMAIL='owner@dny.local')
class ChatbotTests(TestCase):
    def test_chat_creates_session_and_messages(self):
        response=self.client.post(reverse('chat_api'),json.dumps({'message':'I need an AI chatbot'}),content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertIn('reply',response.json())
        self.assertEqual(ChatSession.objects.count(),1)
        self.assertEqual(ChatMessage.objects.count(),2)

    def test_chat_lead_is_saved_and_linked(self):
        first=self.client.post(reverse('chat_api'),json.dumps({'message':'Hello'}),content_type='application/json').json()
        response=self.client.post(reverse('chat_lead_api'),json.dumps({'session_id':first['session_id'],'name':'Chat Visitor','email':'visitor@example.com','phone':'+923001234567','requirement':'I need lead automation.'}),content_type='application/json')
        self.assertEqual(response.status_code,200)
        lead=Lead.objects.get(source='website-chatbot')
        self.assertEqual(ChatSession.objects.get().lead,lead)

    def test_invalid_email_is_rejected(self):
        response=self.client.post(reverse('chat_lead_api'),json.dumps({'name':'Visitor','email':'bad','requirement':'A project'}),content_type='application/json')
        self.assertEqual(response.status_code,400)
