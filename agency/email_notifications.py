import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _label(lead):
    return dict(lead.KIND).get(lead.kind, lead.kind.title())


def send_lead_notifications(lead):
    """Send owner + client emails. Never block/save-fail a lead if email delivery fails."""
    if not getattr(settings, 'LEAD_NOTIFICATION_EMAIL', ''):
        logger.warning('LEAD_NOTIFICATION_EMAIL is not configured; lead %s was saved without email notification.', lead.reference)
        return False

    context = {'lead': lead, 'kind_label': _label(lead), 'site_name': 'DNYAUTOMATED'}
    owner_subject = f'New {_label(lead)} — {lead.reference} — {lead.name}'
    owner_text = render_to_string('agency/emails/lead_owner.txt', context)
    owner_html = render_to_string('agency/emails/lead_owner.html', context)
    owner = EmailMultiAlternatives(owner_subject, owner_text, settings.DEFAULT_FROM_EMAIL, [settings.LEAD_NOTIFICATION_EMAIL], reply_to=[lead.email])
    owner.attach_alternative(owner_html, 'text/html')

    client_subject = f'We received your request — {lead.reference}'
    client_text = render_to_string('agency/emails/lead_client.txt', context)
    client_html = render_to_string('agency/emails/lead_client.html', context)
    client = EmailMultiAlternatives(client_subject, client_text, settings.DEFAULT_FROM_EMAIL, [lead.email], reply_to=[settings.LEAD_NOTIFICATION_EMAIL])
    client.attach_alternative(client_html, 'text/html')

    try:
        owner.send(fail_silently=False)
        client.send(fail_silently=False)
        return True
    except Exception:
        logger.exception('Email notification failed for lead %s. Lead remains saved in CRM.', lead.reference)
        return False
