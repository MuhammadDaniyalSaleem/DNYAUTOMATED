# DNYAUTOMATED Premium Website v3

Django agency website for Digital Neural Yield (DNYAUTOMATED).

## Local setup (Windows)
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open `http://127.0.0.1:8000/`. Admin: `/admin/`. Staff dashboard: `/dny-dashboard/`.

## What is included
Premium multi-page public site, mega services navigation, detailed service pages, solutions, industries, integrations, tech stack, pricing, Automation Lab demos, real-project CaseStudy CMS with image uploads/confidential flag, lead/quote/audit/booking persistence with DNY reference IDs and source tracking, save/resume browser drafts, thank-you pages, CRM fields, proposals, client projects/milestones/files, support tickets, client portal, staff dashboard, site search, legal placeholders, sitemap/robots, favicon/logo, accessibility and responsive styling.

## External integrations
The AI chat shown publicly is a clearly labelled local demo/website guide. Real OpenAI/Gemini, WhatsApp, email, calendar and analytics require your own credentials/configuration. Never put API keys in frontend JavaScript. Use environment variables and a backend integration before production.

## Real project screenshots
Add approved projects in Django Admin → Case Studies. Upload real screenshots there. Mark confidential projects with the confidential option. Do not publish client-sensitive information without permission.

## Production checklist
Set `DEBUG=False`, use a strong `SECRET_KEY`, restrict `ALLOWED_HOSTS`, configure PostgreSQL/static/media/HTTPS/email, review Privacy/Terms with appropriate legal advice, configure backups/logging, and run security/deployment checks.

## Validation note
Python source was syntax-compiled in the delivery environment. Full Django runtime checks could not be executed there because package installation had no network access; run `python manage.py check` after installing requirements locally.

V4.10: Case Studies rebuilt with two real-work showcases and clearly labelled concept demos. No fake client/result claims.

## Email notifications (v4.12)
Contact, Free Audit, Request Quote and Consultation submissions are saved to the lead database first. The site then sends:
1. a detailed new-lead email to `LEAD_NOTIFICATION_EMAIL`; and
2. a branded confirmation email to the visitor.

### Gmail setup
Copy `.env.example` to `.env`, set `EMAIL_HOST_USER` and `LEAD_NOTIFICATION_EMAIL` to your receiving Gmail/Workspace address, and set `EMAIL_HOST_PASSWORD` to a Google App Password (not your normal Google password). Keep `.env` private and out of source control.

If SMTP is temporarily unavailable, the lead remains saved in the CRM/database; email failure does not discard the submission.

## v4.13 — Pricing Funnel Update
- Expanded Starter, Business/Growth and Custom scope-based plans.
- Added one-time/recurring cost clarification, comparison, process, included items and add-ons.
- Added smaller-task option for scripts, n8n workflows, API integrations and WordPress improvements.
- Pricing CTAs pre-fill the selected service and preserve lead-source tracking.
- Added selected-plan confirmation, expanded FAQ and Free Automation Audit CTA.
- Existing CRM/database and email-notification flow remains intact.


## V5.0 FINAL POLISH — Motion layer
- Site-wide scroll reveal animations using IntersectionObserver.
- Subtle hover lift/glow for service, pricing, insight and project cards.
- Workflow arrow motion, project UI hover depth and dashboard chart entrance.
- Sticky navigation gains a polished scrolled state.
- Buttons, logo, contact and AI controls have lightweight micro-interactions.
- `prefers-reduced-motion` is respected for accessibility.
- No animation library dependency; motion uses CSS + small vanilla JavaScript.

## V5.0.2 visible animation update
- Stronger scroll reveal with staggered cards
- Floating hero workflow panel
- Animated hero arrows, active node glow and status sweep
- Animated Before/After process handoffs
- Sequential connected-workflow node pulses
- More noticeable card/button hover micro-interactions
- Reduced-motion accessibility remains supported


## V5.1 Final QA / Deployment checklist

This build adds production-safe environment controls for allowed hosts, CSRF trusted origins, HTTPS redirect, secure cookies and HSTS. Invalid service slugs now return a real 404 instead of silently opening another service. Static asset cache keys were bumped to v5.1.0.

Before production launch:
1. Copy `.env.example` to `.env` and use a long random `SECRET_KEY`.
2. Set `DEBUG=False` and set `ALLOWED_HOSTS` to your real domain(s).
3. Set `CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`.
4. Configure SMTP and send a real Contact, Audit, Quote and Booking test.
5. Run `python manage.py migrate`, `python manage.py check --deploy`, and `python manage.py test`.
6. Run `python manage.py collectstatic --noinput` on the production host.
7. After HTTPS is confirmed, enable `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`; enable HSTS only after HTTPS/domain configuration is proven stable.
8. Verify `/`, `/services/`, `/solutions/`, `/case-studies/`, `/pricing/`, `/insights/`, `/contact/`, `/quote/`, `/free-audit/`, `/book/`, `/client/login/`, `/robots.txt`, and `/sitemap.xml` on desktop and mobile.

QA note: Python source compilation and ZIP integrity can be verified offline. Full Django runtime tests require the packages in `requirements.txt`; if the environment cannot download dependencies, run the commands above on the deployment machine before launch.

## V5.2 — DNY AI Chatbot
- Replaced the browser-only keyword demo with a Django backend chat API.
- Conversations and messages are stored in the database and visible in Django Admin.
- Supports English, Urdu and Roman Urdu prompts, service guidance, quick replies and enquiry capture.
- Chat enquiries create normal CRM leads with a DNY reference number and existing email notifications.
- Gemini is supported through server-side environment variables; the API key is never sent to the browser.
- A safe DNY knowledge fallback keeps core service answers working when no AI key is configured or the provider is unavailable.

### Chatbot setup
1. Run `python manage.py migrate` after upgrading.
2. In `.env`, set `AI_PROVIDER=gemini`, `AI_API_KEY=...`, and optionally `AI_MODEL=gemini-2.0-flash`.
3. In `/admin/`, use Chatbot settings to update the business summary, bot name and WhatsApp number.
4. Review stored Chat sessions, Chat messages and chatbot-created Leads from the admin panel.
