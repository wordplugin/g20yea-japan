const { chromium } = require('playwright');
const fs=require('fs'),path=require('path');
const root=process.argv[2];
const pages=[];(function w(d){for(const f of fs.readdirSync(d)){const p=path.join(d,f);if(fs.statSync(p).isDirectory()){if(!/wp-(content|includes)/.test(p))w(p)}else if(f==='index.html')pages.push(path.relative(root,p))}})(root);
(async()=>{const b=await chromium.launch();const bad=new Map();
for(const p of pages){const pg=await b.newPage();
 pg.on('response',r=>{const u=r.url();if(u.startsWith('http://localhost')&&r.status()>=400)bad.set(u,(bad.get(u)||[]).concat(p))});
 pg.on('requestfailed',r=>{const u=r.url();if(u.startsWith('http://localhost'))bad.set(u,(bad.get(u)||[]).concat(p))});
 await pg.goto('http://localhost:8765/'+encodeURI(p),{waitUntil:'networkidle'}).catch(e=>console.log('ERR',p,e.message));
 const links=await pg.$$eval('a[href]',as=>as.map(a=>a.href).filter(h=>h.startsWith('http://localhost')));
 for(const l of new Set(links)){const r=await pg.request.get(l.split('#')[0]);if(r.status()>=400)bad.set(l,(bad.get(l)||[]).concat('link@'+p))}
 await pg.close()}
console.log(pages.length,'pages');for(const[k,v]of bad)console.log(k,'<-',[...new Set(v)].slice(0,2).join(','));await b.close()})();
