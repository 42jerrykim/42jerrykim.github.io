(function(){
var d=window.T,s=window.S,w=window.W;if(!d||!s)return;

var I={
home:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"/><polyline points="5 12 3 12 12 3 21 12 19 12"/><path d="M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/><path d="M9 21v-6a2 2 0 012-2h2a2 2 0 012 2v6"/></svg>',
database:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 6c0 1.657 3.582 3 8 3s8-1.343 8-3-3.582-3-8-3-8 1.343-8 3"/><path d="M4 6v6c0 1.657 3.582 3 8 3m8-3.5V6"/><path d="M4 12v6c0 1.657 3.582 3 8 3"/><path d="M18 18m-3 0a3 3 0 106 0 3 3 0 10-6 0"/><path d="M20.2 20.2l1.8 1.8"/></svg>',
search:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"/><circle cx="10" cy="10" r="7"/><line x1="21" y1="21" x2="15" y2="15"/></svg>',
categories:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"/><line x1="5" y1="9" x2="19" y2="9"/><line x1="5" y1="15" x2="19" y2="15"/><line x1="11" y1="4" x2="7" y2="20"/><line x1="17" y1="4" x2="13" y2="20"/></svg>',
tag:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"/><path d="M11 3l9 9a1.5 1.5 0 010 2l-6 6a1.5 1.5 0 01-2 0L3 11V7a4 4 0 014-4h4"/><circle cx="9" cy="9" r="2"/></svg>',
archives:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"/><rect x="3" y="4" width="18" height="4" rx="2"/><path d="M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8"/><line x1="10" y1="12" x2="14" y2="12"/></svg>',
'brand-github':'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 00-1.3-3.2 4.2 4.2 0 00-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 00-6.2 0c-2.4-1.6-3.5-1.3-3.5-1.3a4.2 4.2 0 00-.1 3.2 4.6 4.6 0 00-1.3 3.2c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2v3.5"/></svg>',
kakao:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10 8v7"/><path d="M14 10l-2 2.5 2 2.5"/><path d="M12 4c4.97 0 9 3.358 9 7.5 0 4.142-4.03 7.5-9 7.5-.67 0-1.323-.061-1.95-.177L7 21l.592-2.962C4.851 16.754 3 14.308 3 11.5 3 7.358 7.03 4 12 4z"/></svg>',
'envelope-regular':'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 7a2 2 0 012-2h14a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V7z"/><path d="M3 7l9 6 9-6"/></svg>',
rss:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"/><circle cx="5" cy="19" r="1"/><path d="M4 4a16 16 0 0116 16"/><path d="M4 11a9 9 0 019 9"/></svg>',
infinity:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"/><path d="M9.828 9.172a4 4 0 1 0 0 5.656 a10 10 0 0 0 2.172 -2.828a10 10 0 0 1 2.172 -2.828 a4 4 0 1 1 0 5.656a10 10 0 0 1 -2.172 -2.828a10 10 0 0 0 -2.172 -2.828"/></svg>',
'toggle-left':'<svg xmlns="http://www.w3.org/2000/svg" class="icon-tabler-toggle-left" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"/><circle cx="8" cy="12" r="2"/><rect x="2" y="6" width="20" height="12" rx="6"/></svg>',
'toggle-right':'<svg xmlns="http://www.w3.org/2000/svg" class="icon-tabler-toggle-right" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z"/><circle cx="16" cy="12" r="2"/><rect x="2" y="6" width="20" height="12" rx="6"/></svg>'
};

var mainMenu=[
{n:'Home',u:'/',i:'home'},
{n:'Collections',u:'/collection/',i:'database'},
{n:'Search',u:'/search/',i:'search'},
{n:'Categories',u:'/categories/',i:'categories'},
{n:'Tags',u:'/all-tags/',i:'tag'},
{n:'Archives',u:'/archives/',i:'archives'}
];

var socialMenu=[
{n:'GitHub',u:'https://github.com/42jerrykim',i:'brand-github'},
{n:'Kakao',u:'https://open.kakao.com/o/s5FFkQWg',i:'kakao'},
{n:'Mail',u:'mailto:42jerrykim@gmail.com',i:'envelope-regular'},
{n:'RSS',u:'/index.xml',i:'rss'}
];

var PP=20,cp=1,tp=Math.ceil(d.p.length/PP);
var MO=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

function esc(t){var e=document.createElement('span');e.textContent=t;return e.innerHTML;}
function fmtDate(iso){var p=iso.split('-');return MO[parseInt(p[1],10)-1]+' '+parseInt(p[2],10)+', '+p[0];}

function pageNums(c,t){
if(t<=9){var r=[];for(var i=1;i<=t;i++)r.push(i);return r;}
var r=[1];
if(c>4)r.push('...');
for(var i=Math.max(2,c-2);i<=Math.min(t-1,c+2);i++)r.push(i);
if(c<t-3)r.push('...');
r.push(t);return r;
}

function buildSidebar(){
var h='<aside class="sidebar left-sidebar sticky">';
h+='<button class="hamburger hamburger--spin" type="button" id="toggle-menu" aria-label="Toggle Menu">';
h+='<span class="hamburger-box"><span class="hamburger-inner"></span></span></button>';
h+='<header><figure class="site-avatar"><a href="/">';
h+='<img class="site-logo" loading="lazy" src="'+s.a+'" width="300" height="300" alt="Avatar">';
h+='</a></figure>';
h+='<div class="site-meta">';
h+='<h1 class="site-name"><a href="/">'+esc(s.n)+'</a></h1>';
h+='<h2 class="site-description">'+esc(s.d)+'</h2>';
h+='</div></header>';
h+='<ol class="menu-social">';
for(var i=0;i<socialMenu.length;i++){
var m=socialMenu[i];
h+='<li><a href="'+m.u+'" target="_blank" title="'+m.n+'" rel="me">'+I[m.i]+'</a></li>';
}
h+='</ol>';
h+='<ol class="menu" id="main-menu">';
for(var i=0;i<mainMenu.length;i++){
var m=mainMenu[i];
h+='<li><a href="'+m.u+'">'+I[m.i]+'<span>'+m.n+'</span></a></li>';
}
h+='<li class="menu-bottom-section"><ol class="menu">';
h+='<li id="dark-mode-toggle">'+I['toggle-left']+I['toggle-right']+'<span>Dark Mode</span></li>';
h+='</ol></li>';
h+='</ol></aside>';
return h;
}

function buildArticles(page){
var st=(page-1)*PP,en=Math.min(st+PP,d.p.length),h='';
for(var i=st;i<en;i++){
var p=d.p[i];
h+='<article><a href="'+p[1]+'">';
h+='<div class="article-details">';
h+='<h2 class="article-title">'+esc(p[0])+'</h2>';
h+='<footer class="article-time">';
h+='<time datetime="'+p[2]+'">'+fmtDate(p[2])+'</time>';
if(p[3])h+='<span class="article-description">'+esc(p[3])+'</span>';
h+='</footer></div>';
h+='</a></article>';
}
return h;
}

function buildPagination(page){
if(tp<=1)return '';
var nums=pageNums(page,tp);
var h='<nav class="pagination" id="pagination">';
if(page>1)h+='<a class="page-link" data-page="'+(page-1)+'" href="javascript:void(0)" aria-label="Previous page"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg></a>';
else h+='<span class="page-link disabled"></span>';
for(var i=0;i<nums.length;i++){
if(nums[i]==='...')h+='<span class="page-link disabled">\u2026</span>';
else h+='<a class="page-link'+(nums[i]===page?' current':'')+'" data-page="'+nums[i]+'" href="javascript:void(0)"'+(nums[i]===page?' aria-current="page"':'')+'>'+nums[i]+'</a>';
}
if(page<tp)h+='<a class="page-link" data-page="'+(page+1)+'" href="javascript:void(0)" aria-label="Next page"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></a>';
else h+='<span class="page-link disabled"></span>';
h+='</nav>';return h;
}

function buildMain(){
var h='<main class="main full-width">';
h+='<header><h3 class="section-title">Tags</h3>';
h+='<div class="section-card"><div class="section-details">';
h+='<h3 class="section-count">'+d.c+' pages</h3>';
h+='<h1 class="section-term">'+esc(d.t)+'</h1>';
h+='</div></div></header>';
h+='<section class="article-list--compact" id="article-list">';
h+=buildArticles(1);
h+='</section>';
h+=buildPagination(1);
var yr=new Date().getFullYear();
h+='<footer class="site-footer"><section class="copyright">&copy; ';
if(s.fs&&s.fs!==yr)h+=s.fs+' - ';
h+=yr+' '+esc(s.n);
h+='</section><section class="powerby">';
h+='Built with <a href="https://gohugo.io/" target="_blank" rel="noopener">Hugo</a> <br />';
h+='Theme <b><a href="https://github.com/CaiJimmy/hugo-theme-stack" target="_blank" rel="noopener" data-version="3.34.2">Stack</a></b> designed by <a href="https://jimmycai.com" target="_blank" rel="noopener">Jimmy</a>';
h+='</section></footer>';
h+='</main>';
return h;
}

function buildRightSidebar(){
if(!w)return '';
var h='<aside class="sidebar right-sidebar sticky">';
h+='<form action="'+esc(w.su)+'" class="search-form widget"><p>';
h+='<label>Search</label>';
h+='<input name="keyword" required placeholder="Type something..." />';
h+='<button title="Search">'+I.search+'</button>';
h+='</p></form>';
if(w.c&&w.c.length){
h+='<section class="widget tagCloud"><div class="widget-icon">'+I.categories+'</div>';
h+='<h2 class="widget-title section-title">Categories</h2>';
h+='<div class="tagCloud-tags">';
for(var i=0;i<w.c.length;i++)h+='<a href="'+w.c[i][1]+'" class="font_size_'+w.c[i][2]+'">'+esc(w.c[i][0])+'</a>';
h+='</div></section>';
}
if(w.tg&&w.tg.length){
h+='<section class="widget tagCloud"><div class="widget-icon">'+I.tag+'</div>';
h+='<h2 class="widget-title section-title">Tags</h2>';
h+='<div class="tagCloud-tags">';
for(var i=0;i<w.tg.length;i++)h+='<a href="'+w.tg[i][1]+'">'+esc(w.tg[i][0])+'</a>';
h+='</div></section>';
}
if(w.ar&&w.ar.length){
h+='<section class="widget archives"><div class="widget-icon">'+I.infinity+'</div>';
h+='<h2 class="widget-title section-title">Archives</h2>';
h+='<div class="widget-archive--list">';
for(var i=0;i<w.ar.length;i++){
if(i<w.ar.length-1||w.ar.length<6){
h+='<div class="archives-year"><a href="'+esc(w.au)+'#'+w.ar[i][0]+'">';
h+='<span class="year">'+w.ar[i][0]+'</span><span class="count">'+w.ar[i][1]+'</span>';
h+='</a></div>';
}else{
h+='<div class="archives-year"><a href="'+esc(w.au)+'">';
h+='<span class="year">More</span>';
h+='</a></div>';
}
}
h+='</div></section>';
}
h+='</aside>';
return h;
}

var wrap=document.createElement('div');
wrap.className='container main-container flex on-phone--column extended';
wrap.innerHTML=buildSidebar()+buildRightSidebar()+buildMain();
document.body.appendChild(wrap);

var toggleBtn=document.getElementById('toggle-menu');
if(toggleBtn){
toggleBtn.addEventListener('click',function(){
if(document.getElementById('main-menu').classList.contains('transiting'))return;
document.body.classList.toggle('show-menu');
var menu=document.getElementById('main-menu');
if(menu.classList.contains('show')){
menu.classList.remove('show');
}else{
menu.classList.add('show');
}
toggleBtn.classList.toggle('is-active');
});
}

var darkToggle=document.getElementById('dark-mode-toggle');
if(darkToggle){
darkToggle.addEventListener('click',function(){
var key='StackColorScheme';
var scheme=document.documentElement.dataset.scheme;
var isDark=scheme==='dark';
var target=isDark?'light':'dark';
document.documentElement.dataset.scheme=target;
var sysDark=window.matchMedia('(prefers-color-scheme: dark)').matches;
var sysScheme=sysDark?'dark':'light';
localStorage.setItem(key,target===sysScheme?'auto':target);
});
}

document.addEventListener('click',function(e){
var el=e.target;
while(el&&el!==document){
if(el.dataset&&el.dataset.page){
e.preventDefault();
cp=parseInt(el.dataset.page,10);
document.getElementById('article-list').innerHTML=buildArticles(cp);
var old=document.getElementById('pagination');
if(old){old.outerHTML=buildPagination(cp);}
var sc=document.querySelector('.section-card');
if(sc)sc.scrollIntoView({behavior:'smooth'});
return;
}
el=el.parentElement;
}
});
})();
