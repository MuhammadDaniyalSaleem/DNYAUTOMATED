from django import forms
from .models import Lead,SupportTicket
class LeadForm(forms.ModelForm):
    class Meta:
        model=Lead; fields=['name','email','phone','company','country','service','budget','timeline','tools','message','attachment']
        widgets={'message':forms.Textarea(attrs={'rows':5,'placeholder':'Describe the process, problem or outcome you need...'}),'service':forms.TextInput(attrs={'placeholder':'e.g. AI Agent, n8n, Invoice Automation'}),'tools':forms.TextInput(attrs={'placeholder':'e.g. Google Sheets, CRM, WhatsApp'})}
    def clean_attachment(self):
        f=self.cleaned_data.get('attachment')
        if f and f.size>10*1024*1024: raise forms.ValidationError('Maximum file size is 10 MB.')
        return f
class TicketForm(forms.ModelForm):
    class Meta: model=SupportTicket; fields=['project','subject','priority','message']; widgets={'message':forms.Textarea(attrs={'rows':5})}
