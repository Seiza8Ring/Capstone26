// Shared client behaviors
(function(){
  // Theme toggle (persist simple flag)
  const btn = document.getElementById('themeToggle');
  if(btn){
    const set = (dark)=>{
      document.documentElement.classList.toggle('dark', !!dark);
      localStorage.setItem('gs_dark', dark? '1':'');
    }
    set(localStorage.getItem('gs_dark')==='1');
    btn.addEventListener('click', ()=> set(!(localStorage.getItem('gs_dark')==='1')));
  }

  // Dashboard history fill
  const recent = document.getElementById('recentTranslations');
  if(recent){
    const hist = JSON.parse(localStorage.getItem('gs_history')||'[]');
    if(hist.length){
      recent.innerHTML = hist.slice(0,5).map(h=>{
        const d = new Date(h.t);
        return `<div class="flex items-center justify-between py-1"><div class="text-slate-700 truncate pr-2">${h.src.substring(0,40)}</div><div class="text-xs text-slate-500">${d.toLocaleTimeString()}</div></div>`
      }).join('');
    }
  }

  // Titlebar controls using pywebview API
  function bind(id, fn){ const el = document.getElementById(id); if(el) el.addEventListener('click', fn); }
  const api = (window.pywebview && window.pywebview.api) ? window.pywebview.api : null;
  bind('btnMin', (e)=>{ e.preventDefault(); if(api && api.minimize) api.minimize(); });
  bind('btnMax', (e)=>{ e.preventDefault(); if(api && api.toggle_maximize) api.toggle_maximize(); });
  bind('btnFull', (e)=>{ e.preventDefault(); if(api && api.toggle_fullscreen) api.toggle_fullscreen(); });
  bind('btnClose', (e)=>{ e.preventDefault(); if(api && api.close) api.close(); });

  // If API not available, hide the titlebar controls to avoid confusion
  if(!api){
    const ctrls = document.querySelector('.titlebar .controls');
    if(ctrls) ctrls.style.display = 'none';
  }
})();
