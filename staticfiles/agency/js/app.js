const menu=document.querySelector('.menu');if(menu)menu.addEventListener('click',()=>{document.body.classList.toggle('navopen');menu.setAttribute('aria-expanded',document.body.classList.contains('navopen'))});
function quickAutomate(){const t=document.getElementById('quickTask').value.trim(),r=document.getElementById('quickResult');r.textContent=t?`Possible direction: Trigger → capture data → validate/process → update your system → notify or request review. For “${t.slice(0,90)}${t.length>90?'…':''}”, the exact tools and exception handling should be confirmed in an audit.`:'Describe a repetitive task first.'}
function automationFinder(){const t=document.getElementById('finderTask').value.trim(),tools=document.getElementById('finderTools').value.trim();document.getElementById('finderResult').textContent=t?`Suggested structure: Trigger → capture → validate → automate decision/process → ${tools||'business system'} → notification/human review. This is a demo direction; feasibility needs process discovery.`:'Describe the task first.'}
function roiCalc(){let e=+employees.value||0,h=+hours.value||0,c=+cost.value||0,p=Math.min(100,Math.max(0,+percent.value||0))/100;let wh=e*h*p,mh=wh*4.33,mc=mh*c;roiResult.innerHTML=`Estimated automatable time: <b>${wh.toFixed(1)} hrs/week</b> · ${mh.toFixed(1)} hrs/month<br>Estimated labor-time value: <b>${mc.toFixed(2)}/month</b> in the currency you entered. This is an estimate, not guaranteed savings.`}
function workflowBuild(){workflowResult.textContent=`${trigger.value} → ${process.value} → ${system.value} → ${action.value}`}
function filterIntegrations(q){q=q.toLowerCase();document.querySelectorAll('#integrations .card').forEach(x=>x.style.display=x.innerText.toLowerCase().includes(q)?'block':'none')}
const forms=document.querySelectorAll('.smartform[data-save]');forms.forEach(f=>{const key='dny-draft-'+f.dataset.save;try{let d=JSON.parse(localStorage.getItem(key)||'{}');f.querySelectorAll('input:not([type=file]):not([type=hidden]),textarea,select').forEach(x=>{if(d[x.name]&&!x.value)x.value=d[x.name];x.addEventListener('input',()=>{let o={};f.querySelectorAll('input:not([type=file]):not([type=hidden]),textarea,select').forEach(y=>o[y.name]=y.value);localStorage.setItem(key,JSON.stringify(o))})});f.addEventListener('submit',()=>localStorage.removeItem(key))}catch(e){}});
(()=>{
  const chat=document.getElementById('chat'),open=document.getElementById('aiOpen'),close=document.getElementById('aiClose'),form=document.getElementById('chatForm'),input=document.getElementById('chatInput'),body=document.getElementById('chatBody'),leadForm=document.getElementById('chatLeadForm');
  if(!chat||!form)return;
  const csrf=()=>document.cookie.split('; ').find(x=>x.startsWith('csrftoken='))?.split('=')[1]||'';
  let session=localStorage.getItem('dny-chat-session')||'';
  const add=(type,text)=>{const el=document.createElement('div');el.className=type;el.textContent=text;body.appendChild(el);body.scrollTop=body.scrollHeight;return el};
  const showChat=()=>{chat.classList.add('open');setTimeout(()=>input.focus(),100)};
  open.onclick=showChat; close.onclick=()=>chat.classList.remove('open');
  async function send(message){
    const q=message.trim();if(!q)return;add('userbubble',q);input.value='';input.disabled=true;
    const typing=add('bot typing','Thinking…');
    try{
      const response=await fetch('/api/chat/',{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},body:JSON.stringify({message:q,session_id:session})});
      const data=await response.json();typing.remove();
      if(!response.ok)throw new Error(data.error||'Unable to reply.');
      session=data.session_id;localStorage.setItem('dny-chat-session',session);add('bot',data.reply);
    }catch(error){typing.remove();add('bot',error.message||'Connection issue. Please try again or use the contact form.');}
    finally{input.disabled=false;input.focus()}
  }
  form.onsubmit=e=>{e.preventDefault();send(input.value)};
  body.querySelectorAll('[data-chat-prompt]').forEach(button=>button.onclick=()=>send(button.dataset.chatPrompt));
  document.getElementById('chatLeadOpen').onclick=()=>{body.hidden=true;form.hidden=true;leadForm.hidden=false};
  document.getElementById('chatLeadCancel').onclick=()=>{leadForm.hidden=true;body.hidden=false;form.hidden=false};
  leadForm.onsubmit=async e=>{
    e.preventDefault();const submit=leadForm.querySelector('[type=submit]');submit.disabled=true;
    const payload=Object.fromEntries(new FormData(leadForm));payload.session_id=session;
    try{
      const response=await fetch('/api/chat/lead/',{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},body:JSON.stringify(payload)});const data=await response.json();
      if(!response.ok)throw new Error(data.error||'Unable to save enquiry.');
      leadForm.reset();leadForm.hidden=true;body.hidden=false;form.hidden=false;add('bot',`${data.message} Reference: ${data.reference}`);
    }catch(error){alert(error.message)}finally{submit.disabled=false}
  };
})();
if('IntersectionObserver'in window){let io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('seen')}),{threshold:.1});document.querySelectorAll('.reveal').forEach(x=>io.observe(x))}


// V5.0 site-wide premium motion. Progressive enhancement + reduced-motion support.
(()=>{
  const reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduced)return;
  document.documentElement.classList.add('motion-ready');
  const selectors=['main > section','main > .wrap','main > .hero','.grid > .card','.cards > .card','.insight-card','.case-v410-project','.demo-case-grid > article','.pricing-process > div','.scopebox','.price'];
  const items=[...new Set(selectors.flatMap(s=>[...document.querySelectorAll(s)]))];
  items.forEach(el=>el.classList.add('motion-reveal'));
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('motion-in');observer.unobserve(entry.target)}
    }),{threshold:.08,rootMargin:'0px 0px -35px'});
    items.forEach(el=>observer.observe(el));
  }else items.forEach(el=>el.classList.add('motion-in'));
  const nav=document.querySelector('.nav');
  const syncNav=()=>nav&&nav.classList.toggle('scrolled',window.scrollY>18);
  syncNav(); window.addEventListener('scroll',syncNav,{passive:true});
})();

// V5.0.2: stagger cards inside a section so scroll motion is clearly visible.
(()=>{
  if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  const groups=['.service-feature-grid','.project-showcase','.demo-case-grid','.insight-grid','.pricing-process','.method-list','.industry-list'];
  groups.forEach(sel=>document.querySelectorAll(sel).forEach(group=>{
    [...group.children].forEach((item,index)=>{
      item.style.transitionDelay=`${Math.min(index,5)*90}ms`;
      if(!item.classList.contains('motion-reveal')) item.classList.add('motion-reveal');
    });
  }));
  if('IntersectionObserver' in window){
    const io=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('motion-in');io.unobserve(entry.target)}
    }),{threshold:.08,rootMargin:'0px 0px -25px'});
    document.querySelectorAll('.motion-reveal:not(.motion-in)').forEach(el=>io.observe(el));
  }else document.querySelectorAll('.motion-reveal').forEach(el=>el.classList.add('motion-in'));
})();
