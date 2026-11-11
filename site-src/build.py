#!/usr/bin/env python3
"""Builds the static site into ../dist. Run: python3 site-src/build.py (from the repo root)"""
import hashlib
import html
import os
import shutil

from content import PILLARS, PROJECTS, SERVICES, SITE, STORY, VALUES
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.normpath(os.path.join(ROOT, "..", "dist"))
BASE = "https://www.gerberconstructioninc.com"
try:
    import PIL  # noqa: F401
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False
# Search Console HTML-tag verification for the URL-prefix property (leave empty if verified by DNS instead).
GOOGLE_VERIFY = "vzRTv1Tp06VH-u1WSMuMH3w7qGj0JQQhEKewuVMSvKQ"
GOOGLE_VERIFY_FILE = "google33a93ba306aff332.html"  # Search Console file check; keep it published
# Old Squarespace addresses that may still be in Google or in bookmarks -> where they live now.
OLD_URLS = {"services": "#services", "about": "#about", "contact": "#contact", "projects": "#projects",
            "careers": SITE["careers"], "our-work": "#projects", "home": ""}

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@600;700;800'
         '&family=Michroma&display=swap">')

CSS = r"""
/* Layout: plan-sheet rhythm. Full-width bands alternate paper and brand green, content sits left on a
   1180px column, and the section-cut drawing in the hero is the one loud element. */
:root{
  --green:#0B422E; --green-deep:#062A1D; --green-mid:#145A40;
  --gold:#F9AE40; --gold-deep:#D98F22;
  --paper:#F2F3EE; --paper-2:#E4E8DF; --ink:#0F1F18; --muted:#55665E;
  --line:rgba(11,66,46,.18); --line-on-green:rgba(242,243,238,.22);
  --font-display:"Barlow Condensed","Arial Narrow",Impact,sans-serif;
  --font-body:"Barlow","Segoe UI",Helvetica,Arial,sans-serif;
  --font-label:"Michroma","Eurostile","Bank Gothic",Verdana,sans-serif;
  color-scheme:light;
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
html{scroll-behavior:smooth;scroll-padding-top:84px}
[id]{scroll-margin-top:84px}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font-body);font-size:17px;line-height:1.55;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:30;background:var(--green)}
img,svg{max-width:100%;height:auto;display:block}
a{color:inherit}
p{margin:0 0 1em}
ul,ol{margin:0;padding:0}
:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.skip{position:absolute;left:-999px;top:8px;background:var(--gold);color:var(--ink);padding:8px 12px;z-index:50}
.skip:focus{left:12px}

.wrap{max-width:1180px;margin-inline:auto;min-width:0;
  padding-left:max(clamp(16px,4vw,40px),env(safe-area-inset-left,0px));
  padding-right:max(clamp(16px,4vw,40px),env(safe-area-inset-right,0px))}
.band>.wrap{padding-block:clamp(28px,4vw,48px)}
.band--green{background:var(--green);color:var(--paper)}
.band--deep{background:var(--green-deep);color:var(--paper)}
.band--paper2{background:var(--paper-2)}

h1,h2,h3,h4{margin:0;text-wrap:balance}
.display{font-family:var(--font-display);font-weight:800;text-transform:uppercase;line-height:.92;letter-spacing:-.005em}
h1.display{font-size:clamp(50px,9.5vw,118px)}
h2.display{font-size:clamp(36px,5.4vw,70px);font-weight:700}
h3{font-family:var(--font-display);font-weight:700;font-size:clamp(26px,2.8vw,32px);text-transform:uppercase;line-height:1}
h4{font-family:var(--font-body);font-weight:600;font-size:18px}
.lede{font-size:clamp(18px,2vw,21px);line-height:1.5;max-width:36em}
.label{font-family:var(--font-label);font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.section-head{display:grid;gap:14px;margin-bottom:clamp(20px,3vw,32px);max-width:52em}
.section-head p{margin:0}
.section-head--tight{margin-bottom:clamp(16px,2vw,24px)}
.muted{color:var(--muted)}
.band--green .muted,.band--deep .muted{color:rgba(242,243,238,.72)}
.prose{max-width:60ch}
.prose p{margin-bottom:1.1em}

/* Buttons */
.btn{display:inline-block;background:var(--gold);color:var(--ink);text-decoration:none;font-family:var(--font-display);font-weight:700;text-transform:uppercase;letter-spacing:.04em;font-size:19px;line-height:1;padding:14px 22px 13px;border:2px solid var(--gold);cursor:pointer}
.btn:hover{background:var(--gold-deep);border-color:var(--gold-deep)}
.btn--ghost{background:transparent;color:var(--paper);border-color:var(--paper)}
.btn--ghost:hover{background:var(--paper);color:var(--green);border-color:var(--paper)}
.btn--ink{background:transparent;color:var(--green);border-color:var(--green)}
.more-link{margin-top:14px;font-weight:600}.more-link a{color:var(--green);text-decoration:none}.more-link a:hover{text-decoration:underline}
.btn--ink:hover{background:var(--green);color:var(--paper);border-color:var(--green)}
.cta-row{display:flex;flex-wrap:wrap;gap:12px}

/* Nav */
.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--green);color:var(--paper);border-bottom:1px solid var(--line-on-green)}
.nav>.wrap{display:flex;align-items:center;justify-content:space-between;gap:24px;padding-block:14px}
.brand{display:block;flex:none;line-height:0}
.brand__img{height:46px;width:auto}
@media (max-width:860px){.brand__img{height:40px}}
.nav__links{display:flex;gap:clamp(18px,2.6vw,38px);align-items:center;list-style:none}
.nav__links a{text-decoration:none;font-weight:500;font-size:16px;padding:6px 0;border-bottom:2px solid transparent;white-space:nowrap}
.nav__links a[aria-current="page"]{border-bottom-color:var(--gold)}
.nav__links a:hover{border-bottom-color:var(--paper)}
.nav__links a.is-active{border-bottom-color:var(--gold)}
.nav__links .btn{font-size:16px;font-weight:700;padding:10px 16px 9px;border-bottom:2px solid var(--gold)}
.nav__links .btn:hover{border-bottom-color:var(--gold-deep)}
.nav__toggle{display:none;background:none;border:2px solid var(--paper);color:var(--paper);font:600 15px/1 var(--font-body);padding:9px 12px;cursor:pointer}
.nav__panel{display:none}
@media (max-width:860px){
  .nav__links{display:none}
  .nav__toggle{display:inline-block}
  .nav__panel{display:block;background:var(--green-deep);border-top:1px solid var(--line-on-green)}
  .nav__panel[hidden]{display:none}
  .nav__panel ul{list-style:none;display:grid;gap:4px;padding-block:12px 18px}
  .nav__panel a{display:block;text-decoration:none;font-weight:500;font-size:19px;padding:10px 0;border-bottom:1px solid var(--line-on-green)}
  .nav__panel a[aria-current="page"]{color:var(--gold)}
  .nav__panel .btn{display:inline-block;margin-top:12px;padding:14px 22px 13px;font-weight:700;font-size:19px;border-bottom:2px solid var(--gold)}
}

/* Hero */
.hero{background:var(--green);color:var(--paper)}
.hero>.wrap{padding-block:clamp(44px,7vw,88px) 0}
.hero__grid{display:grid;grid-template-columns:1fr;gap:36px;align-items:end}
@media (min-width:900px){.hero__grid{grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:56px}}
.hero__lede{color:rgba(242,243,238,.86);margin:22px 0 0}
.hero__cta{margin-top:30px}
.facts{display:grid;gap:0;margin:0;border-top:1px solid var(--line-on-green)}
.facts>div{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr);gap:12px;padding-block:12px;border-bottom:1px solid var(--line-on-green)}
.facts dt{color:var(--gold);font-weight:500}
.facts dd{margin:0}
.sheet{margin-top:clamp(36px,5vw,64px);border-top:1px solid var(--line-on-green);overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%}
.sheet__meta{display:flex;justify-content:space-between;gap:16px;padding:12px 0 6px;color:rgba(242,243,238,.6)}
.sheet svg{width:100%;height:auto}
@media (max-width:900px){.sheet .lbl{display:none}}

/* Photo slots: these become <img> once the Dropbox originals are in. */
.ph{position:relative;background:var(--green-deep);background-image:repeating-linear-gradient(135deg,rgba(249,174,64,.2) 0 1px,transparent 1px 12px);border:1px solid var(--line-on-green);max-width:100%;overflow:hidden;aspect-ratio:4/3}
.ph--wide{aspect-ratio:16/9}
.ph--tall{aspect-ratio:3/4}
.ph>span{position:absolute;left:12px;bottom:10px;right:12px;color:rgba(242,243,238,.72);font-family:var(--font-label);font-size:9px;letter-spacing:.14em;text-transform:uppercase;line-height:1.4}
.ph--light{background:var(--paper-2);background-image:repeating-linear-gradient(135deg,rgba(11,66,46,.22) 0 1px,transparent 1px 12px);border-color:var(--line)}
.ph--light>span{color:var(--muted)}
.ph--img{background:var(--green-deep);background-image:none;border:0}
.ph--img picture{display:contents}
.ph--img img{width:100%;height:100%;object-fit:cover;display:block}
.strip{display:grid;gap:12px;grid-template-columns:repeat(2,minmax(0,1fr));margin-top:clamp(20px,3vw,32px)}
@media (min-width:700px){.strip{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media (min-width:700px){.strip{grid-template-columns:repeat(4,minmax(0,1fr))}}
.strip .ph{aspect-ratio:3/4}
.gallery{display:grid;gap:16px;grid-template-columns:1fr;margin-top:clamp(20px,3vw,32px)}
@media (min-width:700px){.gallery{grid-template-columns:repeat(2,minmax(0,1fr))}}
.gallery .ph{aspect-ratio:3/2}
@media (min-width:700px){.gallery>.ph:last-child:nth-child(odd){grid-column:1/-1;aspect-ratio:16/9}}
/* Home hero: the photo (or video) comes first. Stacked on phones, full-bleed with the headline over it on desktop. */
.hero--media{position:relative;background:var(--green);color:var(--paper);overflow:hidden}
.hero__media{position:relative;width:100%;aspect-ratio:4/3;background:var(--green-deep)}
.hero__media img,.hero__media video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%;display:block}
.hero__media .ph{position:absolute;inset:0;aspect-ratio:auto}
.hero__video{object-position:50% 50%;opacity:0;transition:opacity .6s ease}
.hero__video[hidden]{display:none}
.hero__media--playing .hero__video{opacity:1}
.hero__body{position:relative;padding-top:clamp(28px,5vw,48px);padding-bottom:clamp(40px,6vw,64px)}
.hero--media h1.display{font-size:clamp(46px,8.5vw,96px);max-width:9em}
@media (min-width:900px){
  .hero--media{display:grid;min-height:min(84vh,780px)}
  .hero__media{position:absolute;inset:0;aspect-ratio:auto;height:100%}
  .hero__media::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(6,42,29,.93) 0%,rgba(6,42,29,.62) 24%,rgba(6,42,29,.12) 52%,rgba(6,42,29,0) 100%),linear-gradient(90deg,rgba(6,42,29,.22) 0%,rgba(6,42,29,0) 40%)}
  .hero__body{align-self:end;padding-top:clamp(160px,22vh,240px);padding-bottom:clamp(72px,9vw,120px)}
  .hero__body>*{max-width:720px}
}
.hero__after>.wrap{padding-block:clamp(28px,4vw,48px) clamp(40px,6vw,72px)}
@media (min-width:900px){
  .hero__facts--row{grid-template-columns:repeat(4,minmax(0,1fr));gap:0 32px;border-top:1px solid var(--line-on-green)}
  .hero__facts--row>div{grid-template-columns:1fr;gap:4px;padding-block:16px 18px;border-bottom:1px solid var(--line-on-green)}
}
.pillar .ph{margin-bottom:16px;aspect-ratio:3/2}

/* Pillars */
.pillars{display:grid;gap:36px;grid-template-columns:1fr}
@media (min-width:760px){.pillars{grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(28px,4vw,56px)}}
.pillar{min-width:0;border-top:3px solid var(--green);padding-top:18px}
.pillar h3{margin-bottom:12px}
.pillar p{margin:0}
.ticks{list-style:none;display:grid;gap:8px;margin-top:14px;color:var(--muted)}
.ticks li{display:flex;gap:10px;align-items:baseline}
.ticks li::before{content:"";flex:none;width:12px;height:3px;background:var(--gold);position:relative;top:-4px}
.band--green .ticks,.band--deep .ticks{color:rgba(242,243,238,.8)}

/* Projects */
.lead{margin-bottom:clamp(20px,3vw,32px)}
.proj{color:inherit;text-decoration:none;display:flex;flex-direction:column;gap:12px;min-width:0}
.proj__text{display:flex;flex-direction:column;gap:12px;min-width:0}
.proj--lead{display:grid;gap:24px;grid-template-columns:1fr}
@media (min-width:860px){.proj--lead{grid-template-columns:minmax(0,3fr) minmax(0,2fr);gap:48px;align-items:end}}
.proj__title{font-family:var(--font-display);font-weight:700;font-size:clamp(26px,2.6vw,32px);text-transform:uppercase;line-height:.98}
.proj--lead .proj__title{font-size:clamp(34px,4.2vw,56px)}
.proj__town{color:var(--gold);font-weight:500}
.proj__line{margin:0;color:rgba(242,243,238,.82)}
.proj:hover .proj__title{text-decoration:underline;text-decoration-color:var(--gold);text-underline-offset:6px;text-decoration-thickness:3px}
.proj-grid{display:grid;gap:28px 24px;grid-template-columns:1fr}
@media (min-width:640px){.proj-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:1000px){.proj-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
.band--paper .proj__line,.band--paper2 .proj__line{color:var(--muted)}
.band--paper .proj__town,.band--paper2 .proj__town{color:var(--green-mid)}
.more{margin-top:clamp(20px,3vw,32px)}

/* Values */
.values{display:grid;gap:24px 48px;grid-template-columns:1fr}
@media (min-width:760px){.values{grid-template-columns:repeat(2,minmax(0,1fr))}}
.value{min-width:0;border-top:1px solid var(--line);padding-top:18px}
.value .how{color:var(--muted);font-weight:500;margin-bottom:8px}
.value h3{margin-bottom:10px;font-size:clamp(28px,3.2vw,38px)}
.value p{margin:0;max-width:44ch}
.safety{margin-top:clamp(40px,6vw,64px);border-left:4px solid var(--gold);padding-left:20px;font-family:var(--font-display);font-weight:600;font-size:clamp(22px,2.6vw,30px);line-height:1.15;max-width:26em}

/* Two column text block */
.cols{display:grid;gap:28px;grid-template-columns:1fr}
@media (min-width:860px){.cols{grid-template-columns:minmax(0,3fr) minmax(0,2fr);gap:64px;align-items:start}}
.cols>*{min-width:0}

/* Footer */
.foot{background:var(--green-deep);color:var(--paper)}
.foot>.wrap{padding-block:clamp(48px,7vw,88px) 32px}
.foot__logo{height:52px;width:auto;margin-bottom:clamp(28px,4vw,40px)}
.foot__tag{font-size:clamp(32px,5vw,64px);max-width:12em;margin-bottom:clamp(32px,5vw,56px)}
.foot__grid{display:grid;gap:28px;grid-template-columns:1fr;border-top:1px solid var(--line-on-green);padding-top:32px}
@media (min-width:640px){.foot__grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:1000px){.foot__grid{grid-template-columns:repeat(5,minmax(0,auto));justify-content:space-between}}
.foot__grid a{overflow-wrap:anywhere}
.foot__grid h4{color:var(--gold);margin-bottom:8px}
.foot__grid a{text-decoration:none}
.foot__grid a:hover{text-decoration:underline;text-underline-offset:4px}
.foot__grid p{margin:0 0 4px}
.foot__bottom{display:flex;flex-wrap:wrap;gap:8px 28px;margin-top:40px;padding-top:18px;border-top:1px solid var(--line-on-green);color:rgba(242,243,238,.6);font-size:14px}

/* Page hero (interior) */
.page-hero{background:var(--green);color:var(--paper)}
.page-hero>.wrap{padding-block:clamp(44px,7vw,88px)}
.page-hero .kicker{color:var(--gold);font-weight:500;margin-bottom:14px}
.page-hero h1.display{font-size:clamp(44px,7.5vw,96px)}
.page-hero .lede{margin:20px 0 0;color:rgba(242,243,238,.86)}
.page-hero .opening{color:var(--paper)}
.page-hero .facts-line{margin:14px 0 0;max-width:52em;font-size:15px;line-height:1.55;color:var(--gold)}

/* Project page */
.factbar{background:var(--paper-2);border-bottom:1px solid var(--line)}
.factbar>.wrap{padding-block:22px}
.factbar dl{display:grid;gap:16px 32px;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));margin:0}
.factbar dt{color:var(--muted);font-size:14px;font-weight:500}
.factbar dd{margin:0;font-weight:600;font-size:18px}
.numbers{display:grid;gap:20px;grid-template-columns:1fr;margin:28px 0 8px}
@media (min-width:600px){.numbers{grid-template-columns:repeat(2,minmax(0,1fr))}}
.numbers div{border-left:3px solid var(--gold);padding-left:16px}
.numbers strong{display:block;font-family:var(--font-display);font-weight:800;font-size:clamp(40px,5vw,60px);line-height:.95;font-variant-numeric:tabular-nums}
.numbers span{color:var(--muted)}
.aside h4{margin-bottom:10px}
.pager{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:20px;margin-top:clamp(20px,3vw,32px)}
.pager a{text-decoration:none;font-weight:500;max-width:48%}
.pager a:hover{text-decoration:underline;text-underline-offset:4px}
.pager small{display:block;color:var(--muted);font-size:14px}
.figure{margin:0}
.figure figcaption{margin-top:10px;color:var(--muted);font-size:14px}

/* Services */
.steps{list-style:none;counter-reset:step;display:grid;gap:0;max-width:60ch}
.steps li{counter-increment:step;display:grid;grid-template-columns:56px minmax(0,1fr);gap:16px;padding-block:20px;border-top:1px solid var(--line)}
.steps li::before{content:counter(step,decimal-leading-zero);font-family:var(--font-display);font-weight:800;font-size:40px;line-height:.9;color:var(--green);font-variant-numeric:tabular-nums}
.steps h4{margin-bottom:6px}
.steps p{margin:0;color:var(--muted)}
.util{list-style:none;display:grid;gap:10px;max-width:32em}
.util li{display:flex;gap:12px;align-items:center}
.util li::before{content:"";flex:none;width:28px;height:6px;background:var(--mark)}
.util .water{--mark:#2F6FD6}.util .sewer{--mark:#2E9A4E}.util .electric{--mark:#D23B2E}.util .gas{--mark:#F2C300}.util .comm{--mark:#F28C1E}
.svc{display:grid;gap:36px;grid-template-columns:1fr;padding-block:clamp(24px,4vw,40px);border-top:1px solid var(--line)}
@media (min-width:860px){.svc{grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:64px}}
.svc>*{min-width:0}

/* Contact */
.contact{display:grid;gap:36px;grid-template-columns:1fr}
@media (min-width:860px){.contact{grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:64px;align-items:start}}
.contact>*{min-width:0}
.card{border-top:3px solid var(--green);padding-top:16px;margin-bottom:28px}
.card h3{margin-bottom:8px}
.card a{text-decoration:none;font-weight:600;font-size:20px;word-break:break-word}
.card a:hover{text-decoration:underline;text-underline-offset:4px}
.card p{margin:4px 0 0;color:var(--muted)}
.form{display:grid;gap:16px}
.form label{display:grid;gap:6px;font-weight:500}
.form input,.form textarea{font:inherit;padding:12px 14px;border:1px solid var(--line);background:#fff;color:var(--ink);width:100%;min-width:0}
.form textarea{min-height:140px;resize:vertical}
.form .two{display:grid;gap:16px;grid-template-columns:1fr}
@media (min-width:600px){.form .two{grid-template-columns:1fr 1fr}}
.form__note{color:var(--muted);font-size:15px;margin:0}

@media (prefers-reduced-motion:no-preference){
  .nav__links a,.btn{transition:background-color .15s,border-color .15s,color .15s}
}
"""

JS = r"""
(function(){
  var t=document.querySelector('.nav__toggle'),p=document.getElementById('menu');
  if(t&&p){t.addEventListener('click',function(){var open=!p.hidden;p.hidden=open;t.setAttribute('aria-expanded',String(!open));t.textContent=open?'Menu':'Close';});}
  var spy=document.querySelectorAll('a[data-spy]');
  if(spy.length&&'IntersectionObserver' in window){
    var map={};spy.forEach(function(a){(map[a.dataset.spy]=map[a.dataset.spy]||[]).push(a);});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;spy.forEach(function(a){a.classList.remove('is-active');});(map[e.target.id]||[]).forEach(function(a){a.classList.add('is-active');});});},{rootMargin:'-40% 0px -55% 0px'});
    Object.keys(map).forEach(function(id){var el=document.getElementById(id);if(el)io.observe(el);});
  }
  if(p){p.addEventListener('click',function(e){if(e.target.tagName==='A'&&t){p.hidden=true;t.setAttribute('aria-expanded','false');t.textContent='Menu';}});}
  var f=document.getElementById('contact-form');
  if(f){f.addEventListener('submit',function(e){
    e.preventDefault();
    var n=document.getElementById('form-note'),b=f.querySelector('button[type=submit]'),key=f.querySelector('[name=access_key]');
    var fb='Email '+f.getAttribute('data-fallback')+' and we will get right back to you.';
    if(!key||!key.value){if(n){n.textContent='Message sending turns on when the site goes live. Until then, email '+f.getAttribute('data-fallback')+'.';}return;}
    if(b){b.disabled=true;b.textContent='Sending\u2026';}
    fetch(f.action,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)}).then(function(r){return r.json();}).then(function(j){
      if(j&&j.success){f.reset();if(n){n.textContent='Thanks, your message is on its way. We will get back to you within a business day.';}}
      else{if(n){n.textContent='Something went wrong sending that. '+fb;}}
    }).catch(function(){if(n){n.textContent='Something went wrong sending that. '+fb;}}).then(function(){if(b){b.disabled=false;b.textContent='Send message';}});
  });}
})();
"""


def esc(s):
    return html.escape(s, quote=True)


def rel(depth, path):
    return "../" * depth + path


NAV_ITEMS = [("About", "#about"), ("Services", "#services"), ("Projects", "#projects"),
             ("Careers", None), ("Contact", "#contact")]


def home_link(depth, anchor):
    """A link to a section of the one page: '#about' on the page itself, '../index.html#about' from a project page."""
    return (rel(depth, "index.html") if depth else "") + anchor


def nav(depth):
    def link(label, anchor):
        if anchor is None:
            return f'<a href="{SITE["careers"]}" target="_blank" rel="noopener">{label}</a>'
        return f'<a href="{home_link(depth, anchor)}" data-spy="{anchor[1:]}">{label}</a>'
    items = "".join(f"<li>{link(l, a)}</li>" for l, a in NAV_ITEMS)
    cta = f'<li><a class="btn" href="{home_link(depth, "#contact")}">Request pricing</a></li>'
    return f"""
<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="{rel(depth, 'index.html')}"><img class="brand__img" src="{rel(depth, 'assets/logo-white.png')}" alt="Gerber Construction Inc." width="760" height="207"></a>
    <nav aria-label="Main"><ul class="nav__links">{items}{cta}</ul></nav>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  </div>
  <div class="nav__panel" id="menu" hidden><div class="wrap"><ul>{items}{cta}</ul></div></div>
</header>
"""


def footer(depth):
    return f"""
<footer class="foot">
  <div class="wrap">
    <img class="foot__logo" src="{rel(depth, 'assets/logo-white.png')}" alt="Gerber Construction Inc." width="760" height="207">
    <p class="display foot__tag">{esc(SITE['tagline'])}</p>
    <div class="foot__grid">
      <div><h4>Office</h4><p>{SITE['address1']}<br>{SITE['address2']}</p><p><a href="{SITE['phone_href']}">{SITE['phone']}</a></p><p><a href="{SITE['maps']}" target="_blank" rel="noopener">Directions</a></p></div>
      <div><h4>Pricing and bids</h4><p><a href="mailto:{SITE['email_pricing']}">{SITE['email_pricing']}</a></p><p class="muted">Send plans, specs and bid invitations here.</p></div>
      <div><h4>General</h4><p><a href="mailto:{SITE['email_general']}">{SITE['email_general']}</a></p><p><a href="{SITE['careers']}" target="_blank" rel="noopener">Careers at Gerber</a></p></div>
      <div><h4>Services</h4>{"".join(f'<p><a href="{rel(depth, "services/" + sv["slug"] + ".html")}">{esc(sv["kicker"])}</a></p>' for sv in SERVICES)}</div>
      <div><h4>Follow</h4><p><a href="{SITE['instagram']}" target="_blank" rel="noopener">Instagram</a></p><p><a href="{SITE['facebook']}" target="_blank" rel="noopener">Facebook</a></p><p><a href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn</a></p></div>
    </div>
    <div class="foot__bottom"><span>&copy; {SITE['year']} Gerber Construction Inc.</span><span>Heavy civil and utility contractor, Ellington, Connecticut</span><span>Prequalified with CTDOT, CT DAS and MassDOT</span></div>
  </div>
</footer>
"""


def head(title, desc, depth, main=False, path="", jsonld=None, jsonld_extra=()):
    """path: the page's address under the site root, e.g. "" for home, "projects/osgood-park.html"."""
    url = f"{BASE}/{path}"
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">']
    parts.append(f"<title>{esc(title)}</title>")
    parts.append('<meta name="claude:viewport-fit-sides" content="cover">')
    parts.append(f'<meta name="description" content="{esc(desc)}">')
    parts.append(f'<link rel="canonical" href="{url}">')
    if GOOGLE_VERIFY:
        parts.append(f'<meta name="google-site-verification" content="{GOOGLE_VERIFY}">')
    og_img = f"{BASE}/assets/og-image.jpg"
    parts.append(f'<meta property="og:type" content="website"><meta property="og:site_name" content="Gerber Construction Inc.">'
                 f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
                 f'<meta property="og:url" content="{url}"><meta property="og:image" content="{og_img}">'
                 f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
                 f'<meta name="twitter:card" content="summary_large_image">')
    parts.append(f'<link rel="icon" type="image/png" sizes="32x32" href="{rel(depth, "assets/favicon-32.png")}">'
                 f'<link rel="icon" type="image/png" sizes="512x512" href="{rel(depth, "assets/favicon-512.png")}">'
                 f'<link rel="apple-touch-icon" href="{rel(depth, "assets/apple-touch-icon.png")}">')
    if jsonld:
        parts.append('<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>")
    for extra in jsonld_extra:  # each in its own tag (Organization on the home page)
        parts.append('<script type="application/ld+json">' + json.dumps(extra, ensure_ascii=False) + "</script>")
    parts.append(FONTS)
    parts.append(f"<style>{CSS}</style>")
    if not main:
        parts.append("</head><body>")
    return "\n".join(parts)


ORG_ID = BASE + "/#organization"


def org_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": BASE + "/#localbusiness",
        "parentOrganization": {"@id": ORG_ID},
        "name": "Gerber Construction Inc.",
        "description": "Heavy civil and underground utility contractor: earthwork, underground utilities and turnkey site packages for schools, campuses, towns and states across New England.",
        "url": BASE + "/",
        "logo": BASE + "/assets/logo-green.png",
        "image": BASE + "/assets/og-image.jpg",
        "telephone": "+1-860-875-6684",
        "email": SITE["email_general"],
        "foundingDate": "1984",
        "founder": {"@type": "Person", "name": "Ron Gerber"},
        "address": {"@type": "PostalAddress", "streetAddress": SITE["address1"], "addressLocality": "Ellington",
                    "addressRegion": "CT", "postalCode": "06029", "addressCountry": "US"},
        "areaServed": [{"@type": "State", "name": "Connecticut"}, {"@type": "State", "name": "Massachusetts"}],
        "knowsAbout": ["Heavy civil construction", "Underground utilities", "Earthwork", "Site work", "Storm drainage",
                       "Sanitary sewer", "Water mains", "Electrical ductbank", "Excavation", "Grading"],
        "sameAs": [SITE["instagram"], SITE["facebook"], SITE["linkedin"]],
    }


# Organization entity (MARKETING handoff "Organization Schema + llms.txt", Evan approved Nov 11). Home page only.
def organization_jsonld():
    svc = lambda n, slug: {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": f"{BASE}/services/{slug}.html"}}
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "Gerber Construction Inc.",
        "legalName": "Gerber Construction Inc.",
        "url": BASE + "/",
        "logo": BASE + "/assets/logo-green.png",
        "foundingDate": "1984",
        "description": "Heavy civil sitework contractor (site development, earthwork and underground utilities) for public and private owners across New England since 1984.",
        "disambiguatingDescription": "Heavy civil sitework and underground utility contractor based in Ellington, Connecticut. Not a general contractor or residential builder. Not affiliated with Gerber Construction of Utah.",
        "address": {"@type": "PostalAddress", "streetAddress": "1 Nutmeg Drive", "addressLocality": "Ellington",
                    "addressRegion": "CT", "postalCode": "06029", "addressCountry": "US"},
        "telephone": "+1-860-875-6684",
        "email": "office@gerberconstructioninc.com",
        "contactPoint": [
            {"@type": "ContactPoint", "contactType": "bids and estimating", "email": "estimating@gerber.build"},
            {"@type": "ContactPoint", "contactType": "general inquiries", "email": "office@gerberconstructioninc.com", "telephone": "+1-860-875-6684"},
        ],
        "areaServed": [{"@type": "State", "name": n} for n in
                       ("Connecticut", "Massachusetts", "Rhode Island", "New York", "New Hampshire", "Vermont", "Maine")],
        "knowsAbout": ["Sitework", "Site work", "Site development", "Earthwork", "Excavation", "Mass grading",
                       "Underground utilities", "Storm drainage", "Sanitary sewer", "Water main",
                       "Electrical ductbank", "Contaminated soils", "Heavy civil construction"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
            svc("Underground utilities", "underground-utilities"), svc("Earthwork", "earthwork"), svc("Site work", "site-work")]},
        "sameAs": [
            "https://www.google.com/maps/place/?q=place_id:ChIJwVUw2hD35okRSR4f2bV_QRI",
            "https://www.linkedin.com/company/gerber-construction-inc",
            "https://www.instagram.com/gerberconstructioninc",
            "https://www.facebook.com/GerberConstructionIncorporated/",
        ],
    }


# Served at /llms.txt as plain text (same handoff). Exact approved text.
LLMS_TXT = '# Gerber Construction Inc.\n\n> Heavy civil sitework contractor (site development, earthwork and underground utilities) based in Ellington, Connecticut, working for public and private owners across New England since 1984. Gerber Construction is not a general contractor or residential builder, and is not affiliated with Gerber Construction of Utah.\n\n## Key facts\n\n- Our crews self-perform excavation, mass grading, storm drainage, sanitary sewer, water main, electrical ductbank and controlled materials handling, including contaminated and regulated soils (HAZWOPER-trained crews).\n- When a contract includes site concrete, curbing or paving, we carry it and subcontract it.\n- We work for towns and cities, state and federal agencies, developers, private owners, and general contractors and construction managers, as the prime contractor or as a subcontractor, on full turnkey site packages or any part of the site scope.\n- We work across Connecticut and Massachusetts every day and take on projects throughout New England and beyond.\n- Fully bonded. Prequalified with the CT Department of Administrative Services (DAS), CTDOT and MassDOT. We work on Project Labor Agreement (PLA) jobs.\n- Address: 1 Nutmeg Drive, Ellington, CT 06029. Phone: (860) 875-6684.\n- Invitations to bid: estimating@gerber.build. General inquiries: office@gerberconstructioninc.com.\n\n## Services\n\n- [Underground utilities](https://www.gerberconstructioninc.com/services/underground-utilities.html): storm drainage, sanitary sewer, water main and services, electrical ductbank, precast structures and manholes.\n- [Earthwork](https://www.gerberconstructioninc.com/services/earthwork.html): mass excavation, GPS machine-control grading, crushing and screening, soil stabilization, contaminated soils, trucking.\n- [Site work](https://www.gerberconstructioninc.com/services/site-work.html): full turnkey site packages or any part of the site scope, from clearing to curb.\n\n## Projects\n\n- [Norwalk High School](https://www.gerberconstructioninc.com/projects/norwalk-high-school.html): City of Norwalk, Norwalk, CT, 2024-present. Site and utility contractor.\n- [UConn South Campus Infrastructure, Phase 1](https://www.gerberconstructioninc.com/projects/uconn-south-campus-infrastructure.html): University of Connecticut, Storrs, CT, 2023-2024. Utility backbone reroute.\n- [Bowers Elementary School](https://www.gerberconstructioninc.com/projects/bowers-elementary-school.html): Town of Manchester, Manchester, CT, 2022-2024. Site and utility contractor.\n- [Osgood Park](https://www.gerberconstructioninc.com/projects/osgood-park.html): City of New Britain, New Britain, CT, 2022-2023. Prime contractor.\n- [Route 140 over Charters Brook](https://www.gerberconstructioninc.com/projects/route-140-charters-brook.html): CTDOT, Ellington, CT, 2020-2021. Prime contractor, bridge replacement.\n- [UConn Athletic District](https://www.gerberconstructioninc.com/projects/uconn-athletic-district.html): University of Connecticut, Storrs, CT, 2019-2021. Site and utility contractor.\n- [UConn Innovation Partnership Building](https://www.gerberconstructioninc.com/projects/uconn-innovation-partnership-building.html): University of Connecticut, Storrs, CT, 2016-2017. Site and utility contractor.\n\n## Profiles\n\n- [LinkedIn](https://www.linkedin.com/company/gerber-construction-inc)\n- [Instagram](https://www.instagram.com/gerberconstructioninc)\n- [Facebook](https://www.facebook.com/GerberConstructionIncorporated/)\n- [Careers](https://careers.gerber.build)\n'


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def tail(main=False):
    return f"<script>{JS}</script></body></html>"


IMG_DIR = os.path.join(ROOT, "img")
_VERS = {}


def asset(depth, path):
    """URL for a file under site-src that is published at assets/<path>, with ?v=<content hash> so browsers
    refetch it when it changes (browsers and the host cache assets/*)."""
    src = {"img": IMG_DIR, "video": os.path.join(ROOT, "video")}
    top, _, rest = path.partition("/")
    full = os.path.join(src.get(top, ROOT), rest) if top in src else os.path.join(ROOT, path)
    if full not in _VERS:
        try:
            with open(full, "rb") as f:
                _VERS[full] = hashlib.md5(f.read()).hexdigest()[:8]
        except OSError:
            _VERS[full] = None
    v = _VERS[full]
    return rel(depth, f"assets/{path}") + (f"?v={v}" if v else "")


def has_img(slug):
    return os.path.exists(os.path.join(IMG_DIR, f"{slug}-2400.jpg"))


def ph(label, cls="", light=False, slug=None, depth=0, alt=None, eager=False, style=None, pos=None):
    """A photo. Renders the real image when site-src/img/<slug>-2400.jpg exists, else a labeled slot.
    style: extra CSS on the box (e.g. "aspect-ratio:4/3"); pos: object-position for the image (e.g. "50% 65%")."""
    c = "ph" + (" " + cls if cls else "")
    if slug and has_img(slug):
        src = asset(depth, f"img/{slug}-1200.jpg")
        big = asset(depth, f"img/{slug}-2400.jpg")
        load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
        box = f' style="{style}"' if style else ""
        img = f' style="object-position:{pos}"' if pos else ""
        sizes = 'sizes="(min-width: 1200px) 1180px, 100vw"'
        webp = ""
        if HAVE_PIL:
            w1, w2 = asset(depth, f"img/{slug}-1200.jpg").replace(".jpg", ".webp"), asset(depth, f"img/{slug}-2400.jpg").replace(".jpg", ".webp")
            webp = f'<source type="image/webp" srcset="{w1} 1200w, {w2} 2400w" {sizes}>'
        return (f'<div class="{c} ph--img"{box}><picture>{webp}<img src="{src}" srcset="{src} 1200w, {big} 2400w" '
                f'{sizes} alt="{esc(alt or label)}"{img} {load}></picture></div>')
    c += " ph--light" if light else ""
    return f'<div class="{c}" role="img" aria-label="Photo: {esc(label)}"><span>Photo: {esc(label)}</span></div>'


VIDEO_DIR = os.path.join(ROOT, "video")
HERO_SLUG = "crew-three"


def hero_media(d):
    """The home hero: a muted looping video when site-src/video/hero-1080.mp4 exists, else the crew photo.
    A tiny script attaches the source and plays it; anyone who prefers reduced motion, or whose browser can't
    play MP4, keeps the photo. The photo is also the no-JS fallback and shows until the video is playing."""
    if not os.path.exists(os.path.join(VIDEO_DIR, "hero-1080.mp4")):
        return ph("Three crew members in front of a Gerber truck", "hero__photo", slug=HERO_SLUG, depth=d,
                  alt="Three Gerber crew members arm in arm in front of a Gerber dump truck", eager=True)
    poster_src = asset(d, "video/hero-poster.jpg")
    photo = (f'<div class="ph ph--img hero__photo"><img src="{poster_src}" alt="A Gerber excavator loading a red Gerber dump truck" '
             f'loading="eager" fetchpriority="high"></div>')
    big = asset(d, "video/hero-1080.mp4")
    small = asset(d, "video/hero-720.mp4") if os.path.exists(os.path.join(VIDEO_DIR, "hero-720.mp4")) else big
    poster = asset(d, "video/hero-poster.jpg")
    return (f'<div class="hero__fallback">{photo}</div>'
            f'<video class="hero__video" muted loop playsinline preload="none" poster="{poster}" '
            f'aria-label="Gerber crews moving dirt and setting pipe" data-src-l="{big}" data-src-s="{small}" hidden></video>'
            '<script>(function(){var v=document.querySelector(".hero__video");if(!v||!v.canPlayType||!v.canPlayType("video/mp4"))return;'
            'if(window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;'
            'v.addEventListener("playing",function(){v.hidden=false;setTimeout(function(){v.parentNode.classList.add("hero__media--playing");},40);});'
            'v.src=window.matchMedia("(min-width: 900px)").matches?v.dataset.srcL:v.dataset.srcS;v.autoplay=true;'
            'var p=v.play();if(p&&p.catch){p.catch(function(){});}})();</script>')


def pillar_slug(pl):
    """A pillar's photo slug, or its photo_fallback while the chosen file isn't in site-src/img yet."""
    slug = pl["photo"][0]
    if has_img(slug):
        return slug
    fb = pl.get("photo_fallback")
    return fb if fb and has_img(fb) else slug


def pick_img(p):
    """The project's lead image: its img if the file exists, else the first gallery shot that does."""
    for sl in [p.get("img")] + [g[0] for g in p.get("gallery", [])]:
        if sl and has_img(sl):
            return sl
    return None


def proj_card(p, depth, lead=False):
    href = rel(depth, f"projects/{p['slug']}.html")
    slot = ph(p["photo"], "ph--wide" if lead else "", slug=pick_img(p), depth=depth)
    cls = "proj proj--lead" if lead else "proj"
    return f"""<a class="{cls}" href="{href}">{slot}<div class="proj__text"><div><div class="proj__town">{esc(p['town'])}</div><div class="proj__title">{esc(p['title'])}</div></div><p class="proj__line">{esc(p['line'])}</p></div></a>"""


def page_home():
    d = 0
    pillars = "".join(
        f"<div class=\"pillar\">{ph(pl['photo'][1], slug=pillar_slug(pl), depth=d, alt=pl['photo'][1])}<h3>{esc(pl['title'])}</h3><p>{esc(pl['body'])}</p><ul class=\"ticks\">"
        + "".join(f"<li>{esc(i)}</li>" for i in pl["items"]) + "</ul>" + svc_link(pl["title"], d) + "</div>"
        for pl in PILLARS)
    lead = PROJECTS[0]
    grid = "".join(proj_card(p, d) for p in PROJECTS[1:])
    story = "".join(f"<p>{esc(x)}</p>" for x in STORY)
    values = "".join(
        f"<div class=\"value\"><div class=\"how\">{esc(v['how'])}</div><h3>{esc(v['name'])}</h3><p>{esc(v['body'])}</p></div>"
        for v in VALUES)
    body = f"""
{nav(d)}
<main id="main">
<section class="hero hero--media" aria-label="Gerber Construction">
  <div class="hero__media">{hero_media(d)}</div>
  <div class="wrap hero__body">
    <h1 class="display">Built from the ground down.</h1>
    <p class="lede hero__lede">Gerber Construction is a heavy civil and underground utility contractor based in Connecticut. Since 1984 our crews have moved dirt, laid pipe and delivered turnkey site packages for schools, campuses, towns and states across New England.</p>
    <div class="cta-row hero__cta"><a class="btn" href="#projects">See the work</a><a class="btn btn--ghost" href="#contact">Request pricing</a></div>
  </div>
</section>

<section class="band band--paper" id="about" aria-labelledby="h-about">
  <div class="wrap">
    <div class="section-head section-head--tight"><div class="kicker">About Gerber</div><h2 class="display" id="h-about">From milking cows to moving dirt.</h2></div>
    <div class="cols">
      <div class="prose">{story}</div>
      <div style="display:grid;gap:16px">{ph("Four crew members at the spring kickoff, 2026", slug="crew-four", depth=d, light=True, alt="Four Gerber crew members in Gerber hoodies and high-visibility gear, smiling")}{ph("The whole crew in the shop for the spring kickoff, 2026", slug="crew-shop", depth=d, light=True)}</div>
    </div>
    <figure class="figure" style="margin-top:clamp(20px,3vw,32px)">{ph("The fleet and the crew at the Ellington yard, May 2024", "ph--wide", slug="fleet-aerial", depth=d, light=True, alt="The Gerber fleet lined up at the Ellington yard with the crew gathered in the middle, from the air")}<figcaption>The fleet and the crew at the yard in Ellington, May 2024.</figcaption></figure>
  </div>
</section>

<section class="band band--paper2" aria-labelledby="h-values">
  <div class="wrap">
    <div class="section-head section-head--tight"><h2 class="display" id="h-values">Values lived by</h2></div>
    <div class="values">{values}</div>
    <div class="gallery">{ph("Two crew members talking it through, spring kickoff 2026", slug="crew-talk", depth=d, light=True)}{ph("Lunch in the shop at the spring kickoff, 2026", slug="crew-lunch", depth=d, light=True, alt="Three crew members talking over lunch in the Gerber shop")}</div>
  </div>
</section>

<section class="band band--paper" id="services" aria-labelledby="h-services">
  <div class="wrap">
    <div class="section-head"><div class="kicker">Services</div><h2 class="display" id="h-services">Dig dirt. Lay pipe. Deliver the site.</h2><p class="lede">Three things. Our own crews and equipment do the dirt and the pipe.</p></div>
    <div class="pillars">{pillars}</div>
    <div class="cta-row more"><a class="btn btn--ink" href="#contact">Request pricing</a></div>
  </div>
</section>

<section class="band band--green" id="projects" aria-labelledby="h-work">
  <div class="wrap">
    <div class="section-head"><div class="kicker">Projects</div><h2 class="display" id="h-work">The work</h2><p class="lede muted">Schools, campuses, parks and state bridges. Here is what the ground looks like when we're done with it.</p></div>
    <div class="lead">{proj_card(lead, d, lead=True)}</div>
    <div class="proj-grid">{grid}</div>
  </div>
</section>

<section class="band band--deep" id="careers" aria-labelledby="h-crew">
  <div class="wrap">
    <div class="cols">
      <div>
        <h2 class="display" id="h-crew">Join the crew.</h2>
        <p class="lede muted" style="margin-top:18px">Operators, pipe crews, laborers, foremen, CDL drivers, mechanics and project managers. We run our own equipment and do our own work, so there's always something to learn and someone to learn it from. Our people come up through the Operating Engineers Local 478 and Laborers Local 230 apprenticeships and through training in-house.</p>
        <div class="cta-row" style="margin-top:28px"><a class="btn" href="{SITE['careers']}" target="_blank" rel="noopener">See open positions</a></div>
      </div>
      {ph("Three crew members in front of a Gerber truck, spring kickoff 2026", slug="crew-three", depth=d, alt="Three Gerber crew members arm in arm in front of a Gerber dump truck")}
    </div>
    <div class="strip">{ph("Spotting the excavator at Norwalk, November 2024", slug="norwalk-nov-direct", depth=d, pos="38% 50%")}{ph("In the shop at the spring kickoff, 2026", slug="crew-laugh", depth=d, pos="100% 50%", alt="A Gerber crew member in a Gerber hoodie, smiling in the shop")}{ph("On site at Norwalk High School, June 2024", slug="norwalk-crew", depth=d, pos="84% 50%", alt="A Gerber crew member in a Gerber shirt and hard hat at Norwalk High School")}{ph("Operator at Bowers Elementary, April 2023", slug="bowers-operator", depth=d, pos="50% 42%", alt="A Gerber operator in the cab of an excavator at Bowers Elementary")}</div>
  </div>
</section>

<section class="band band--paper" id="contact" aria-labelledby="h-contact">
  <div class="wrap">
    <div class="section-head"><div class="kicker">Contact</div><h2 class="display" id="h-contact">Send us the plans.</h2><p class="lede">Pricing requests go straight to estimating. Everything else goes to the office. A person answers both.</p></div>
    <div class="contact">
      <div>
        <div class="card" id="pricing"><h3>Pricing and bids</h3><a href="mailto:{SITE['email_pricing']}">{SITE['email_pricing']}</a><p>Bid invitations, plans and specs, budget pricing and design-assist requests.</p></div>
        <div class="card"><h3>General</h3><a href="mailto:{SITE['email_general']}">{SITE['email_general']}</a><p>Everything that isn't a bid.</p></div>
        <div class="card"><h3>Office</h3><a href="{SITE['phone_href']}">{SITE['phone']}</a><p>{SITE['address1']}, {SITE['address2']}<br><a href="{SITE['maps']}" target="_blank" rel="noopener" style="font-size:17px">Directions</a></p></div>
        <div class="card"><h3>Careers</h3><a href="{SITE['careers']}" target="_blank" rel="noopener">careers.gerber.build</a><p>Open positions and applications.</p></div>
      </div>
      <form class="form" id="contact-form" method="POST" action="https://api.web3forms.com/submit" data-fallback="{SITE['email_general']}">
        <input type="hidden" name="access_key" value="{SITE['form_key']}">
        <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="two"><label>Name<input type="text" id="f-name" name="name" autocomplete="name" required></label><label>Company<input type="text" id="f-company" name="company" autocomplete="organization"></label></div>
        <div class="two"><label>Email<input type="email" id="f-email" name="email" autocomplete="email" required></label><label>Phone<input type="tel" id="f-phone" name="phone" autocomplete="tel"></label></div>
        <label>What can we help with?<textarea id="f-message" name="message" required></textarea></label>
        <div class="cta-row"><button class="btn" type="submit">Send message</button></div>
        <p class="form__note" id="form-note" aria-live="polite">Plans and specs? Email them to {SITE['email_pricing']} instead of the form.</p>
      </form>
    </div>
  </div>
</section>
</main>
{footer(d)}
"""
    return head("Gerber Construction | Heavy Civil & Utility Contractor, CT", "Heavy civil, underground utilities and turnkey site packages for schools, campuses, towns and states across New England since 1984.", d, main=True, path="", jsonld=org_jsonld(), jsonld_extra=(organization_jsonld(),)) + body + tail(main=True)


def lede_html(t):
    return '<p class="lede">' + esc(t) + '</p>'


def opening_block(x, fallback=""):
    # Plain-fact first sentence + one-line facts, directly under the H1 (Nov 11 AEO pass).
    if not x.get("opening"):
        return fallback
    out = f'<p class="lede opening">{esc(x["opening"])}</p>'
    if x.get("facts_line"):
        out += f'<p class="facts-line">{esc(x["facts_line"])}</p>'
    return out


def page_project(i):
    d = 1
    p = PROJECTS[i]
    prev_p = PROJECTS[i - 1] if i > 0 else None
    next_p = PROJECTS[i + 1] if i < len(PROJECTS) - 1 else None
    facts = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in p["facts"])
    paras = "".join(f"<p>{esc(x)}</p>" for x in p["paras"])
    nums = ""
    if p["numbers"]:
        nums = '<div class="numbers">' + "".join(f"<div><strong>{esc(n)}</strong><span>{esc(t)}</span></div>" for n, t in p["numbers"]) + "</div>"
    scope = "".join(f"<li>{esc(s)}</li>" for s in p["scope"])
    gallery = ""
    lead_img = pick_img(p)
    shots = [(sl, cap) for sl, cap in p.get("gallery", []) if has_img(sl) and sl != lead_img]
    if shots:
        gallery = '<div class="gallery">' + "".join(ph(cap, slug=sl, depth=d, light=True) for sl, cap in shots) + '</div>'
    pager = ""
    if prev_p:
        pager += f'<a href="{prev_p["slug"]}.html"><small>Previous project</small>{esc(prev_p["title"])}</a>'
    else:
        pager += '<span></span>'
    if next_p:
        pager += f'<a href="{next_p["slug"]}.html" style="text-align:right"><small>Next project</small>{esc(next_p["title"])}</a>'
    else:
        pager += f'<a href="{home_link(d, "#projects")}" style="text-align:right"><small>Back to</small>All projects</a>'
    body = f"""
{nav(d)}
<main id="main">
<section class="page-hero"><div class="wrap"><div class="kicker">{esc(p['town'])}</div><h1 class="display">{esc(p['title'])}</h1>{opening_block(p, lede_html(p['line']))}</div></section>
<section class="factbar"><div class="wrap"><dl>{facts}</dl></div></section>
<section class="band band--paper">
  <div class="wrap">
    <figure class="figure">{ph(p['photo'], 'ph--wide', slug=lead_img, depth=d, eager=True, style=p.get('img_style'), pos=p.get('img_pos'))}<figcaption>{esc(p['title'])}, {esc(p['town'])}</figcaption></figure>
    <div class="cols" style="margin-top:clamp(20px,3vw,32px)">
      <div class="prose">{paras}{nums}</div>
      <div class="aside"><h4>Gerber's scope</h4><ul class="ticks">{scope}</ul></div>
    </div>
    {gallery}
    <nav class="pager" aria-label="More projects">{pager}</nav>
  </div>
</section>
</main>
{footer(d)}
"""
    path = f"projects/{p['slug']}.html"
    return head(f"{p['title']} | Gerber Construction", p["line"], d, path=path,
                jsonld=crumbs([("Home", BASE + "/"), ("Projects", BASE + "/#projects"), (p["title"], f"{BASE}/{path}")])) + body + tail()


def svc_link(pillar_title, depth):
    sv = next((x for x in SERVICES if x["pillar"] == pillar_title), None)
    if not sv:
        return ""
    return f'<p class="more-link"><a href="{rel(depth, "services/" + sv["slug"] + ".html")}">More on {esc(sv["kicker"].lower())} &rarr;</a></p>'


def page_service(sv):
    d = 1
    pl = next(x for x in PILLARS if x["title"] == sv["pillar"])
    paras = "".join(f"<p>{esc(x)}</p>" for x in sv["paras"])
    items = "".join(f"<li>{esc(i)}</li>" for i in pl["items"])
    projs = [p for slug in sv["projects"] for p in PROJECTS if p["slug"] == slug]
    grid = "".join(proj_card(p, d) for p in projs)
    others = "".join(f'<a class="btn" href="{x["slug"]}.html">{esc(x["kicker"])}</a> ' for x in SERVICES if x is not sv)
    pslug, cap = sv["photo"] if sv.get("photo") and has_img(sv["photo"][0]) else (pillar_slug(pl), pl["photo"][1])
    body = f"""
{nav(d)}
<main id="main">
<section class="page-hero"><div class="wrap"><div class="kicker">{esc(sv['kicker'])}</div><h1 class="display">{esc(sv['h1'])}</h1>{opening_block(sv)}<p class="lede">{esc(pl['body'])}</p></div></section>
<section class="band band--paper">
  <div class="wrap">
    <figure class="figure">{ph(cap, 'ph--wide', slug=pslug, depth=d, eager=True, alt=cap)}<figcaption>{esc(cap)}</figcaption></figure>
    <div class="cols" style="margin-top:clamp(20px,3vw,32px)">
      <div class="prose">{paras}</div>
      <div class="aside"><h4>{esc(sv.get("aside_title", "What we self-perform"))}</h4><ul class="ticks">{items}</ul></div>
    </div>
    <div class="cta-row more"><a class="btn btn--ink" href="{home_link(d, '#contact')}">Request pricing</a></div>
  </div>
</section>
<section class="band band--green" aria-labelledby="h-svc-work">
  <div class="wrap">
    <div class="section-head"><div class="kicker">Projects</div><h2 class="display" id="h-svc-work">Where we've done it</h2></div>
    <div class="proj-grid">{grid}</div>
    <div class="cta-row more">{others}</div>
  </div>
</section>
</main>
{footer(d)}
"""
    path = f"services/{sv['slug']}.html"
    ld = [crumbs([("Home", BASE + "/"), ("Services", BASE + "/#services"), (sv["kicker"], f"{BASE}/{path}")]),
          {"@context": "https://schema.org", "@type": "Service", "name": sv["kicker"], "serviceType": sv["kicker"],
           "description": sv["desc"], "url": f"{BASE}/{path}", "provider": {"@id": ORG_ID},
           "areaServed": [{"@type": "State", "name": "Connecticut"}, {"@type": "State", "name": "Massachusetts"}]}]
    return head(sv["title"], sv["desc"], d, path=path, jsonld=ld) + body + tail()


def redirect_page(target):
    t = esc(target)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Gerber Construction</title>'
            f'<link rel="canonical" href="{t}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={t}">'
            f'<script>location.replace({json.dumps(target)});</script></head>'
            f'<body><p>This page has moved: <a href="{t}">{t}</a></p></body></html>')



def page_404():
    body = f"""
{nav(0)}
<main id="main"><section class="page-hero"><div class="wrap"><div class="kicker">Page not found</div><h1 class="display">That page moved.</h1>
<p class="lede"><a href="{BASE}/">Go to the home page</a>, see <a href="{BASE}/#projects">our projects</a>, or <a href="{BASE}/#contact">get in touch</a>.</p></div></section></main>
"""
    return head("Page not found | Gerber Construction", "Page not found.", 0, path="404.html").replace(
        '<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"') + body.replace('src="assets/', f'src="{BASE}/assets/') + tail()


def make_icons_and_webp():
    """Favicons and the link-preview image go into dist/assets; WebP copies of every photo go into dist/assets/img.
    Needs Pillow (the publish workflow installs it). Without it the site still builds, just without these."""
    try:
        from PIL import Image
    except ImportError:
        print("Pillow not installed: skipping favicons, preview image and WebP")
        return
    out = os.path.join(DIST, "assets")
    logo = Image.open(os.path.join(ROOT, "logo-green.png")).convert("RGBA")
    em = logo.crop((0, 0, 215, logo.height))
    em = em.crop(em.getbbox())
    side = max(em.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(em, ((side - em.size[0]) // 2, (side - em.size[1]) // 2))
    sq.resize((32, 32), Image.LANCZOS).save(os.path.join(out, "favicon-32.png"))
    sq.resize((512, 512), Image.LANCZOS).save(os.path.join(out, "favicon-512.png"))
    touch = Image.new("RGBA", (180, 180), "white")
    touch.alpha_composite(sq.resize((160, 160), Image.LANCZOS), (10, 10))
    touch.convert("RGB").save(os.path.join(out, "apple-touch-icon.png"))
    src = os.path.join(IMG_DIR, "norwalk-nov-aerial-2400.jpg")
    if os.path.exists(src):
        o = Image.open(src).convert("RGB")
        w, h = o.size
        ch = int(w * 630 / 1200)
        if ch <= h:
            o = o.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch))
        o.resize((1200, 630), Image.LANCZOS).save(os.path.join(out, "og-image.jpg"), quality=82)
    for name in os.listdir(IMG_DIR):
        if name.endswith(("-1200.jpg", "-2400.jpg")):
            Image.open(os.path.join(IMG_DIR, name)).save(
                os.path.join(out, "img", name[:-4] + ".webp"), "WEBP", quality=78, method=4)


def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "projects"))
    pages = {"index.html": page_home()}
    for i, p in enumerate(PROJECTS):
        pages[f"projects/{p['slug']}.html"] = page_project(i)
    os.makedirs(os.path.join(DIST, "assets"), exist_ok=True)
    for name in ("logo-green.png", "logo-white.png"):
        shutil.copy(os.path.join(ROOT, name), os.path.join(DIST, "assets", name))
    if os.path.isdir(IMG_DIR):
        shutil.copytree(IMG_DIR, os.path.join(DIST, "assets", "img"), dirs_exist_ok=True)
    if os.path.isdir(VIDEO_DIR):
        shutil.copytree(VIDEO_DIR, os.path.join(DIST, "assets", "video"), dirs_exist_ok=True)
    make_icons_and_webp()
    os.makedirs(os.path.join(DIST, "services"), exist_ok=True)
    for sv in SERVICES:
        pages[f"services/{sv['slug']}.html"] = page_service(sv)
    sitemap_paths = [""] + [p for p in pages if p != "index.html"]
    for old, target in OLD_URLS.items():
        url = target if target.startswith("http") else f"{BASE}/{target}"
        pages[f"{old}/index.html"] = redirect_page(url)
        pages[f"{old}.html"] = redirect_page(url)
    for path, content in pages.items():
        os.makedirs(os.path.dirname(os.path.join(DIST, path)), exist_ok=True)
        with open(os.path.join(DIST, path), "w", encoding="utf-8") as f:
            f.write(content)
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(DIST, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(LLMS_TXT)
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in sitemap_paths:
            f.write(f"  <url><loc>{BASE}/{p}</loc></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(DIST, GOOGLE_VERIFY_FILE), "w") as f:
        f.write(f"google-site-verification: {GOOGLE_VERIFY_FILE}")
    with open(os.path.join(DIST, "404.html"), "w", encoding="utf-8") as f:
        f.write(page_404())
    print(f"built {len(pages)} pages into {DIST}")


if __name__ == "__main__":
    build()
