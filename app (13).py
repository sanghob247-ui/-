"""오늘도 낚였다 — 실행: streamlit run app.py
GitHub에 이 파일과 requirements.txt를 올린 뒤 Streamlit Community Cloud에서 배포하세요.
QR은 배포 주소로 접속하는 기능입니다. 여러 기기의 참가자 명단을 동기화하지 않습니다.
"""
import io

import json
import secrets

try:
    import qrcode
    from PIL import Image  # QR PNG 생성에 필요한 이미지 라이브러리
except ImportError:
    qrcode = None
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="오늘도 낚였다", page_icon="🎣", layout="centered")
st.markdown('''<style>
:root{color-scheme:dark}
.stApp{background:radial-gradient(ellipse at 80% 0%,#193b42,transparent 55%),#261e27;color:#e4eee9}
.block-container{max-width:850px;padding-top:2.4rem;padding-bottom:3rem}
h1,h2,h3{color:#edf5eb!important;letter-spacing:-.04em}
.stButton>button,.stDownloadButton>button{border-radius:14px;min-height:50px;font-weight:700;background:#15353e;color:#e8f1eb;border:1px solid #3b5d62}
.stButton>button:hover{border-color:#dbbd7b;color:#ffe1a0;background:#20464d}
.stButton>button[kind="primary"]{background:#e4c487;color:#152c31;border-color:#e4c487}
.hero{padding:22px 0 26px;border-bottom:1px solid #325058;margin-bottom:26px}
.hero h1{font-size:clamp(2rem,7vw,3.3rem)!important;font-weight:900!important;margin:0;letter-spacing:-.06em}
.hero p{color:#99bdb5;margin-top:8px;font-size:14px}
.brand{font-size:10px;letter-spacing:4px;color:#dfc18a;margin-bottom:12px}
.step{color:#9bbfb5;font-size:11px;letter-spacing:1.5px;margin-bottom:12px}
[data-testid="stSidebar"]{background:#102b34;color:#e4eee9}
[data-testid="stTextInput"] input{background:#12313b;color:#eef5ed;border:1px solid #37545e;border-radius:12px}
[data-testid="stWidgetLabel"], [data-testid="stCaptionContainer"]{color:#afc9c1!important}
iframe{border-radius:24px}
</style>''', unsafe_allow_html=True)


if "stage" not in st.session_state:
    st.session_state.update(stage="home", task="설거지", people=[0], next_id=1,
                            result=None, round_no=0)


if st.session_state.stage in ("home", "task", "names"):
    st.markdown('''<style>
:root{color-scheme:light}
.stApp{background:#fff1df;color:#382724}
h1,h2,h3{color:#382724!important}
.hero{border-bottom:1px solid #e6d9d5}.hero p,.step{color:#795c58}.brand{color:#ad5758}
.stButton>button{background:#fff6f2;color:#4c302e;border-color:#d5b8b1}
.stButton>button:hover{background:#f6e2dc;border-color:#ba5c60;color:#673333}
[data-testid="stCaptionContainer"]{color:#795c58!important}
.greeting-wrap{text-align:center;padding:5px 0 15px}
.greeting{width:245px;max-width:70%;height:270px;object-fit:contain;transform-origin:50% 88%;animation:hello 2.8s ease-in-out infinite;filter:drop-shadow(0 13px 12px #88565025)}
@keyframes hello{0%,100%{transform:perspective(700px) rotateY(-7deg) rotate(-3deg) translateY(0)}50%{transform:perspective(700px) rotateY(7deg) rotate(3deg) translateY(-7px)}}
@media(prefers-reduced-motion:reduce){.greeting{animation:none}}
</style>''', unsafe_allow_html=True)


def go(stage):
    st.session_state.stage = stage
    st.rerun()


def fishing_scene(names, winner, task):
    payload = json.dumps({"names": names, "winner": winner, "task": task}, ensure_ascii=True).replace("<", "\\u003c")
    return r'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}body{margin:0;background:#261e27;color:#edf6f3;font-family:system-ui,'Apple SD Gothic Neo',sans-serif}button{font:inherit;cursor:pointer}.stage{position:relative;height:430px;overflow:hidden;border-radius:24px;border:1px solid #36535a;background:#173a44}canvas{display:block;width:100%;height:100%;cursor:pointer;touch-action:manipulation}#cast{display:block;width:100%;margin-top:12px;border:1px solid #e4c487;border-radius:14px;padding:14px;background:#e4c487;color:#152c31;font-weight:800}#cast:disabled{opacity:.5;cursor:default}.mascot{width:110px;height:110px;object-fit:contain;border:0;border-radius:0;background:transparent;display:block;margin:12px auto 0}.big{font-size:62px!important;margin:2px 0!important}.panel{padding:14px!important}.top{position:absolute;top:20px;left:22px;right:22px;display:flex;justify-content:space-between;gap:10px;align-items:start}.tag{font-size:10px;letter-spacing:3px;color:#d6eee2}.who{margin-top:8px;font-size:20px;font-weight:800;overflow-wrap:anywhere;max-width:280px;text-shadow:0 2px 8px #081c24}.live{font-size:10px;letter-spacing:2px;border:1px solid #93c2ad80;border-radius:30px;padding:7px 10px;color:#d5efd9;background:#0d2b3480}.caption{position:absolute;bottom:20px;left:22px;right:22px;font-size:12px;color:#def3ec;text-shadow:0 1px 6px #000}.result{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#04131c99;backdrop-filter:blur(5px);opacity:0;visibility:hidden;transition:opacity .45s;z-index:4;padding:18px}.result.show{opacity:1;visibility:visible}.panel{text-align:center;max-width:100%;width:390px;border:1px solid #e7c98980;border-radius:24px;padding:28px 16px;background:linear-gradient(145deg,#17383df2,#091d29f5);box-shadow:0 18px 70px #0007}.eyebrow{color:#e2bd75;letter-spacing:5px;font-size:10px}.big{font-weight:950;font-size:clamp(55px,14vw,92px);line-height:1.15;color:#ffe3a5;letter-spacing:-5px;margin:10px 0;text-shadow:0 0 35px #e8b34c50}.winner{font-size:24px;font-weight:800;overflow-wrap:anywhere}.duty{margin-top:12px;font-size:14px;color:#d0e3dd}.continue{margin-top:18px;background:transparent;border:1px solid #627e7b;color:#e3eee8;padding:9px 17px;border-radius:30px;font-size:12px}
#status{font-size:14px;min-height:52px;padding:16px 4px;color:#b4d4cc}#cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(115px,1fr));gap:8px;max-height:150px;overflow:auto}.card{padding:12px;background:#112c35;border:1px solid #284953;border-radius:12px;font-size:12px;overflow-wrap:anywhere;color:#bdd3d2}.card.active{border-color:#72b5a3;color:#fff}.card.win{border-color:#e1bc77;background:#3c3629;color:#ffe1a2}#reveal{width:100%;margin-top:14px;border-radius:12px;border:1px solid #34535a;background:#122c35;color:#d3e6df;padding:12px;font-size:12px}button[hidden]{display:none!important}@media(max-width:450px){.stage{height:390px}.who{font-size:17px;max-width:200px}}
html,body{height:100%;overflow:hidden}body{display:flex;flex-direction:column;gap:4px}.stage{height:auto!important;flex:1;min-height:115px;border-radius:16px}#cards{display:none}#cast{margin:0;padding:9px;flex-shrink:0}#status{font-size:12px;min-height:0;padding:3px;flex-shrink:0}#reveal{margin:0;padding:6px;flex-shrink:0}#sound{margin:0!important;padding:5px 12px!important;font-size:12px;align-self:start;flex-shrink:0}.panel{padding:8px!important}.panel>div[aria-hidden]{display:none}.big{font-size:42px!important;margin:0!important}.winner{font-size:19px}.duty{margin-top:4px}.continue{margin-top:6px;padding:5px 12px}.top{top:10px}.caption{bottom:8px}.who{font-size:16px}
body{background:#fffaf3;color:#493d36}.stage{border-color:#dfc6af;box-shadow:0 3px 14px #75513716}.result{background:#fff3dc66}.panel{background:linear-gradient(145deg,#fffdf7,#ffeedb);border:1px solid #ddb993;box-shadow:0 14px 45px #845b3433}.eyebrow{color:#95613e}.big{color:#ad4d2c;text-shadow:none}.winner{color:#493d36}.duty{color:#705a49}.continue{border-color:#d6b493;color:#654d3c;background:#fff9ef}#status{color:#705a49}#cast{background:#b75532;color:white;border-color:#b75532;border-radius:12px}#reveal{background:#fff4e7;border-color:#e3cbb2;color:#705a49}#sound{background:#e9f3ed!important;color:#355e50!important;border-color:#c2d7ca!important}.tag{color:#fff9eb}.live{background:#fff8ecdd;color:#5c493b;border-color:#fff3df}
</style></head><body><div class="stage"><canvas id="river" aria-label="반사광이 흐르는 가을 바다에서 물고기를 낚는 애니메이션"></canvas><div class="top"><div><div class="tag">ONE CAST. ONE DESTINY.</div><div class="who" id="who">가을 바다의 흐름을 읽는 중</div></div><div class="live">● FISHING</div></div><div class="caption" id="caption">잔잔한 수면 아래, 오늘의 운명이 기다립니다.</div><div class="result" id="result" role="dialog" aria-modal="true" aria-label="당첨 결과"><div class="panel"><div class="eyebrow">YOU GOT HOOKED</div><div style="font-size:48px" aria-hidden="true">🐟</div><div class="big">당첨!</div><div class="winner" id="winner"></div><div class="duty" id="duty"></div><button class="continue" id="continue">물고기 구경하기 ↗</button></div></div></div><button id="cast" type="button" disabled>낚시 준비 중…</button><div id="status" role="status" aria-live="polite">낚싯줄을 던졌습니다…</div><div id="cards"></div><button id="reveal">애니메이션 건너뛰고 결과 보기</button>
<button id="sound" type="button" style="margin:10px 0;border:1px solid #bb9572;background:#49352e;color:#fff1df;padding:10px 16px;border-radius:20px">🔊 가을 물소리 켜기</button>
<script>

let audioCtx=null,master=null,soundEnabled=true,audioReady=false,fadeTimer=null;
const soundButton=document.getElementById('sound');
async function startSound(){if(!soundEnabled)return;try{if(!audioCtx){const AC=window.AudioContext||window.webkitAudioContext;if(!AC){soundButton.textContent='소리를 지원하지 않는 브라우저';return}audioCtx=new AC();const n=audioCtx.sampleRate*12,buffer=audioCtx.createBuffer(1,n,audioCtx.sampleRate),out=buffer.getChannelData(0);let brown=0;for(let i=0;i<n;i++){brown=(brown+Math.random()*.04-.02)/1.02;out[i]=brown*2}// Crossfade the loop seam so repeated water noise has no click.
const fade=Math.floor(audioCtx.sampleRate*.6);for(let j=0;j<fade;j++){let a=j/fade;out[n-fade+j]=out[n-fade+j]*(1-a)+out[j]*a}const loop=audioCtx.createBuffer(1,n-fade,audioCtx.sampleRate);loop.copyToChannel(out.subarray(fade),0);
const src=audioCtx.createBufferSource();src.buffer=loop;src.loop=true;const filter=audioCtx.createBiquadFilter();filter.type='lowpass';filter.frequency.value=580;filter.Q.value=.4;const gain=audioCtx.createGain();gain.gain.value=.10;const lfo=audioCtx.createOscillator(),depth=audioCtx.createGain();lfo.frequency.value=.10;depth.gain.value=.018;lfo.connect(depth);depth.connect(gain.gain);src.connect(filter);filter.connect(gain);master=audioCtx.createGain();master.gain.value=0;gain.connect(master);master.connect(audioCtx.destination);src.start();lfo.start()}clearTimeout(fadeTimer);await audioCtx.resume();master.gain.cancelScheduledValues(audioCtx.currentTime);master.gain.setTargetAtTime(1,audioCtx.currentTime,.65);audioReady=audioCtx.state==='running';soundButton.textContent=audioReady?'🔇 물소리 끄기':'🔊 물소리 켜기'}catch(e){soundButton.textContent='🔊 눌러서 물소리 켜기'}}
soundButton.addEventListener('click',async()=>{if(audioReady&&soundEnabled){soundEnabled=false;master.gain.cancelScheduledValues(audioCtx.currentTime);master.gain.setTargetAtTime(0,audioCtx.currentTime,.15);fadeTimer=setTimeout(()=>{if(!soundEnabled)audioCtx.suspend()},800);audioReady=false;soundButton.textContent='🔊 물소리 켜기'}else{soundEnabled=true;startSound()}});
document.addEventListener('pointerdown',e=>{if(e.target!==soundButton&&soundEnabled)startSound()});
startSound();

const data=PAYLOAD,canvas=document.getElementById('river'),ctx=canvas.getContext('2d');

const $=id=>document.getElementById(id),nodes=data.names.map(n=>{let e=document.createElement('div');e.className='card';e.textContent=n+' · 대기';$('cards').appendChild(e);return e});
let W=700,H=430,phase='wait',started=performance.now(),current=-1,done=false,timers=[],particles=[],seed=8241;
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function rand(){seed=(seed*16807)%2147483647;return(seed-1)/2147483646}
const waves=Array.from({length:240},()=>({x:rand(),y:rand(),w:rand(),s:rand(),a:rand()}));
const trees=Array.from({length:75},()=>({x:rand(),h:rand(),w:rand()}));
function resize(){const r=canvas.getBoundingClientRect();W=r.width;H=r.height;const d=Math.min(devicePixelRatio||1,2);canvas.width=W*d;canvas.height=H*d;ctx.setTransform(d,0,0,d,0,0)}new ResizeObserver(resize).observe(canvas);
function path(points,color){ctx.fillStyle=color;ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();ctx.fill()}
function fish(x,y,t,gold){ctx.save();ctx.translate(x,y);let flap=reduced?0:Math.sin(t*23);ctx.rotate(flap*.18-.12);const sz=Math.min(W/550,1.1);ctx.scale(sz,sz);ctx.lineWidth=2.5;ctx.strokeStyle='#925247';ctx.save();ctx.translate(-32,0);ctx.rotate(flap*.5);path([[0,0],[-28,-20],[-22,0],[-28,20]],gold?'#f7bd55':'#ef9c88');ctx.stroke();ctx.restore();path([[-12,-12],[0,-31],[20,-12]],'#f3b885');let g=ctx.createLinearGradient(0,-25,0,25);g.addColorStop(0,gold?'#ffd071':'#ffa992');g.addColorStop(1,gold?'#fff1b8':'#ffe8c9');ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(0,0,42,29,0,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle='#422c30';for(let ex of [12,29]){ctx.beginPath();ctx.ellipse(ex,-5,3.5,5,0,0,7);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(ex+1,-7,1.3,0,7);ctx.fill();ctx.fillStyle='#422c30'}ctx.strokeStyle='#845048';ctx.lineWidth=2;ctx.beginPath();ctx.arc(21,3,5,0,Math.PI);ctx.stroke();ctx.fillStyle='#f0808070';for(let ex of [6,34]){ctx.beginPath();ctx.ellipse(ex,7,6,3,0,0,7);ctx.fill()}ctx.save();ctx.translate(-7,12);ctx.rotate(flap*.2);path([[0,0],[-6,15],[12,5]],'#efa275');ctx.restore();ctx.restore()}
function caught(x,y,t,isWinner){fish(x,y,t,isWinner)}
function draw(now){const t=(now-started)/1000,clock=reduced?0:now/1000,horizon=H*.37;ctx.clearRect(0,0,W,H);
let sky=ctx.createLinearGradient(0,0,0,horizon);sky.addColorStop(0,'#e6ac91');sky.addColorStop(1,'#f7d39c');ctx.fillStyle=sky;ctx.fillRect(0,0,W,horizon+5);
let glow=ctx.createRadialGradient(W*.72,H*.22,1,W*.72,H*.22,100);glow.addColorStop(0,'#ffe8b5a0');glow.addColorStop(1,'#e6d7ae00');ctx.fillStyle=glow;ctx.fillRect(0,0,W,H*.45);ctx.fillStyle='#ffe8b7';ctx.beginPath();ctx.arc(W*.72,H*.22,16,0,7);ctx.fill();
for(let layer=0;layer<3;layer++){let points=[[0,horizon+15]];for(let i=0;i<=50;i++){let x=i/50*W;points.push([x,horizon-12-layer*13-Math.sin(i*.16+layer)*15-Math.sin(i*.39+layer)*8])}points.push([W,horizon+15]);path(points,['#9a6055','#b97b5b','#d6a375'][layer])}
for(const tr of trees){const x=tr.x*W,y=horizon+4;ctx.fillStyle=['#a84f38','#c37939','#d9a74b'][Math.floor(tr.h*3)%3];ctx.fillRect(x-1,y-24,2,24);ctx.beginPath();ctx.ellipse(x,y-16-tr.h*10,8+tr.w*9,12+tr.h*12,0,0,7);ctx.fill()}
let water=ctx.createLinearGradient(0,horizon,0,H);water.addColorStop(0,'#bc9b83');water.addColorStop(.25,'#95b5ad');water.addColorStop(1,'#648f9c');ctx.fillStyle=water;ctx.fillRect(0,horizon,W,H);
for(const v of waves){const depth=v.y*v.y,y=horizon+depth*(H-horizon),x=((v.x*W+Math.sin(clock*.55+v.y*22)*12+clock*(3+depth*8))%(W+80))-40;const highlight=Math.max(0,1-Math.abs(x-W*.72)/(24+depth*130));ctx.strokeStyle=`rgba(${highlight>.2?'245,218,163':'161,203,203'},${(.07+v.a*.12+highlight*.32).toFixed(3)})`;ctx.lineWidth=.4+depth*1.4;ctx.beginPath();ctx.ellipse(x,y,3+v.w*(10+depth*32),.4+depth*.8,0,0,Math.PI*2);ctx.stroke()}
// Floating autumn leaves.
for(let k=0;k<13;k++){const lx=((k*89+clock*17)%(W+40))-20,ly=(k*43+clock*12)%H;ctx.save();ctx.translate(lx,ly);ctx.rotate(k+clock*.7);ctx.fillStyle=['#dc965a','#be6245','#edbe65'][k%3];ctx.beginPath();ctx.ellipse(0,0,5,2.5,0,0,7);ctx.fill();ctx.restore()}
// Near bank and a small timber fishing deck.
path([[0,H*.83],[W*.08,H*.77],[W*.21,H*.86],[W*.28,H],[0,H]],'#152f2e');path([[0,H*.88],[W*.22,H*.88],[W*.3,H],[0,H]],'#574c3c');ctx.strokeStyle='#2c342f';for(let i=0;i<5;i++){ctx.beginPath();ctx.moveTo(0,H*.90+i*9);ctx.lineTo(W*.24+i*5,H*.90+i*9);ctx.stroke()}
const baseX=W*.13,baseY=H*.87,tipX=W*.55,tipY=H*.22-(phase==='lift'?Math.min(t,1)*18:0);ctx.strokeStyle='#171e21';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(baseX,baseY);ctx.quadraticCurveTo(W*.30,H*.28,tipX,tipY);ctx.stroke();ctx.strokeStyle='#b8b09b';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(baseX+3,baseY);ctx.quadraticCurveTo(W*.30,H*.28+4,tipX,tipY);ctx.stroke();
const catchX=W*.59,waterY=H*.70;let fy=waterY;
if(phase==='lift'||phase==='hold'){let p=phase==='hold'?1:Math.min(t/1.1,1);fy=waterY-(1-Math.pow(1-p,3))*H*.30+(reduced?0:Math.sin(clock*7)*3);ctx.strokeStyle='#e6eee3b0';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(tipX,tipY);ctx.lineTo(catchX+39*Math.min(W/650,1.1),fy-2);ctx.stroke();caught(catchX,fy,clock,current===data.winner)}else{const bob=waterY+Math.sin(clock*4)*3;ctx.strokeStyle='#ebeee6a0';ctx.lineWidth=.8;ctx.beginPath();ctx.moveTo(tipX,tipY);ctx.lineTo(catchX,bob);ctx.stroke();ctx.fillStyle='#ef9376';ctx.beginPath();ctx.ellipse(catchX,bob,3,7,0,0,7);ctx.fill();for(let k=0;k<3;k++){let p=(clock*.5+k/3)%1;ctx.strokeStyle=`rgba(220,235,215,${(1-p)*.35})`;ctx.beginPath();ctx.ellipse(catchX,bob+5,p*40+4,p*9+2,0,0,7);ctx.stroke()}}
if(phase==='lift'&&t<.8){for(let i=0;i<14;i++){const a=i*2.4,age=t;let x=catchX+Math.cos(a)*age*80,y=waterY-Math.sin(i+1)*age*70+age*age*160;ctx.fillStyle=`rgba(201,233,233,${Math.max(0,1-age*1.3)})`;ctx.beginPath();ctx.ellipse(x,y,1.5,3,0,0,7);ctx.fill()}}
// Reeds frame the water without covering the catch.
ctx.strokeStyle='#294a3d';ctx.lineWidth=2;for(let i=0;i<16;i++){let x=W-5-i*5;ctx.beginPath();ctx.moveTo(x,H);ctx.quadraticCurveTo(x-10,H-40,x-8+Math.sin(clock+i)*2,H-35-(i%5)*13);ctx.stroke()}
requestAnimationFrame(draw)}resize();requestAnimationFrame(draw);
function later(fn,ms){timers.push(setTimeout(fn,ms))}function setPhase(p){phase=p;started=performance.now()}
function showWin(){ $('winner').textContent=data.names[data.winner]+' 님';$('duty').textContent='오늘의 '+data.task+' 담당으로 낚였습니다.';$('result').classList.add('show');$('continue').focus() }
function finish(){if(done)return;done=true;timers.forEach(clearTimeout);$('cast').hidden=true;current=data.winner;setPhase('hold');nodes.forEach((e,i)=>{e.className='card'+(i===data.winner?' win':'');e.textContent=data.names[i]+(i===data.winner?' · 당첨!':' · 통과')});$('who').textContent='오늘의 운명이 정해졌습니다';$('status').textContent=data.names[data.winner]+' 님 당첨! · '+data.task;$('caption').textContent='한 번의 캐스팅, 오늘의 주인공.';$('reveal').textContent='당첨 결과 다시 보기';$('reveal').onclick=showWin;showWin()}
function next(){if(done)return;current++;if(current>=data.names.length){finish();return}setPhase('wait');$('who').textContent=data.names[current]+' 님의 차례';$('caption').textContent='화면을 터치해서 낚싯줄을 끌어올리세요.';$('status').textContent='준비 완료 · 수면을 누르거나 아래 버튼을 누르세요.';nodes[current].className='card active';$('cast').disabled=false;$('cast').textContent='🎣 화면을 클릭하거나 여기를 눌러 낚기'}
function cast(){if(done||current<0||phase!=='wait')return;const i=current;$('cast').disabled=true;$('cast').textContent='끌어올리는 중…';setPhase('lift');$('status').textContent='잡았다! 무엇이 올라올까요?';later(()=>{setPhase('hold');nodes[i].className='card'+(i===data.winner?' win':'');nodes[i].textContent=data.names[i]+(i===data.winner?' · 당첨!':' · 통과');if(i===data.winner){$('status').textContent=data.names[i]+' 님이 당첨 물고기를 낚았어요!';showWin()}else{$('status').textContent='은빛 물고기! '+data.names[i]+' 님은 통과입니다.'}later(()=>{$('result').classList.remove('show');next()},i===data.winner?4000:1800)},1400)}
canvas.addEventListener('pointerdown',cast);$('cast').onclick=cast;
$('continue').onclick=()=>{$('result').classList.remove('show')};document.addEventListener('keydown',e=>{if(e.key==='Escape')$('result').classList.remove('show')});$('reveal').onclick=finish;later(next,700);

</script></body></html>'''.replace('PAYLOAD', payload)

@st.dialog("🎣 오늘도 낚였다 · 게임 방법")
def game_help():
    st.markdown("""**가을 바다에서 오늘의 집안일 담당을 뽑아요!**

1. **설거지 / 분리수거하기** 중 하나를 선택해요.
2. **＋**로 참가자를 추가하고 이름을 바꿔요. 최소 2명이 필요해요.
3. 자기 차례에 **바다 화면이나 낚기 버튼**을 눌러요.
4. 귀여운 물고기는 통과! **금빛 물고기를 낚으면 당첨**이에요.

모든 참가자의 당첨 확률은 같아요. 결과는 시작할 때 결정되고 클릭 속도와 무관해요.

🔊 물소리는 첫 터치 후 시작될 수 있어요. 소리 버튼으로 끌 수 있어요.
📱 QR은 앱 접속용이며 기기 사이에 명단이 공유되지는 않아요.
""")
    if st.button("알겠어요!", type="primary", use_container_width=True):
        st.rerun()

st.markdown("""<style>
.block-container{padding-top:.7rem!important;padding-bottom:.5rem!important;max-width:760px}
.hero{padding:4px 0 8px;margin-bottom:8px}.hero h1{font-size:clamp(23px,5vw,35px)!important}.hero p{margin:2px 0;font-size:12px}
[data-testid="stVerticalBlock"]{gap:.45rem}
h2,h3{font-size:20px!important;margin:0!important;padding:3px 0!important}
.stButton>button{min-height:40px!important}
[data-testid="stHeader"]{background:transparent;height:0}
footer{display:none}
[data-testid="stMain"] iframe{height:clamp(290px,calc(100dvh - 260px),460px)!important;min-height:290px}
.welcome{text-align:center;padding:clamp(8px,3vh,26px) 15px;border:1px solid #d1a779;border-radius:24px;background:radial-gradient(ellipse at 70% 10%,#f6bf7b99,transparent 65%),linear-gradient(#f7d7b9,#dcab83 52%,#6c8384 53%,#405765);color:#fff9ed;margin:6px 0 12px}
.welcome .fish-icon{font-size:66px;display:block;animation:bob 3s ease-in-out infinite}.welcome h2{color:#fff9ed!important;font-size:26px!important;text-shadow:0 2px 8px #52393288}.welcome p{font-size:13px}
@keyframes bob{50%{transform:translateY(-8px) rotate(-5deg)}}
@media(prefers-reduced-motion:reduce){.welcome .fish-icon{animation:none}}

:root{color-scheme:light}
.stApp{background:radial-gradient(ellipse at 95% 0%,#ffe2cb80,transparent 55%),radial-gradient(ellipse at 0% 90%,#d9ebe580,transparent 60%),#fffaf3!important;color:#493d36!important}
h1,h2,h3{color:#493d36!important}
.hero{border-bottom:1px solid #ebded0!important}.hero p,.step,.brand,[data-testid="stCaptionContainer"]{color:#746356!important}
.stButton>button,.stDownloadButton>button{background:#fffcf8!important;border:1px solid #dfcebb!important;color:#55463b!important;border-radius:14px!important;box-shadow:0 3px 10px #81552d09;transition:background .2s,transform .2s}
.stButton>button:hover{background:#ffead8!important;border-color:#c78256!important;transform:translateY(-1px)}
.stButton>button[kind="primary"]{background:#b75532!important;color:#fff!important;border-color:#b75532!important;box-shadow:0 4px 12px #ad613327}
[data-testid="stTextInput"] input{background:#fff!important;color:#493d36!important;caret-color:#b75532}
[data-testid="stTextInput"] [data-baseweb="input"]{background:#fff!important;border:1px solid #dfcebb!important;border-radius:12px}
[data-testid="stSidebar"]{background:#f5eee3!important;color:#493d36!important}
[data-testid="stDialog"] [role="dialog"]{background:#fffaf3!important;color:#493d36!important;border:1px solid #e8d8c6;border-radius:24px}
.welcome{border:1px solid #edd2b6!important;box-shadow:0 8px 28px #9b694311;background:radial-gradient(circle at 76% 18%,#fff8d4 0 7%,transparent 7.4%),linear-gradient(#ffe5c8 0%,#f4bd97 51%,#b9d6cf 52%,#83b4b6 100%)!important;color:#493d36!important}
.welcome h2{color:#493d36!important;text-shadow:none!important}.welcome p{color:#55463b}

</style>""", unsafe_allow_html=True)
nav_home, nav_help = st.columns(2)
if nav_home.button("⌂ 메인", use_container_width=True):
    go("home")
if nav_help.button("? 게임 설명", use_container_width=True):
    game_help()

st.markdown('<div class="hero"><div class="brand">THE DAILY CATCH / FISHING LOTTERY</div><h1>오늘도 낚였다.</h1><p>낚싯대는 가볍게, 운명은 공평하게.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📱 QR로 앱 열기")
    st.caption("배포 후 실제 앱 주소(https://…streamlit.app)를 입력하세요. QR은 앱 접속용이며 참가자 명단은 기기 간 공유되지 않습니다.")
    url = st.text_input("배포된 앱 주소", placeholder="https://your-app.streamlit.app")
    if url:
        from urllib.parse import urlparse
        parsed = urlparse(url.strip())
        if qrcode is None:
            st.info("QR 기능을 사용하려면 requirements.txt에 qrcode[pil]을 추가하고 앱을 재배포해 주세요. 제비뽑기는 그대로 이용할 수 있습니다.")
            if parsed.scheme == "https" and parsed.netloc:
                st.link_button("앱 주소 열기", url.strip())
        elif parsed.scheme == "https" and parsed.netloc:
            image = qrcode.make(url.strip())
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            st.image(buffer.getvalue(), caption="카메라로 스캔하면 앱이 열려요", width=220)
            st.download_button("QR 이미지 다운로드", buffer.getvalue(), "fishing-qr.png", "image/png")
        else:
            st.warning("https://로 시작하는 올바른 배포 주소를 입력해 주세요.")
    st.divider()
    st.caption("모든 참가자의 당첨 확률은 같으며, 한 번의 추첨에서 딱 1명이 당첨됩니다. 새로고침하거나 세션이 종료되면 명단과 결과가 초기화될 수 있습니다.")

if st.session_state.stage == "home":
    st.markdown('<div class="welcome"><span class="fish-icon">🐟</span><h2>가을 바다에 운명을 던져요.</h2><p>통통한 물고기, 따뜻한 노을.<br>오늘의 집안일은 누가 낚일까요?</p></div>', unsafe_allow_html=True)
    if st.button("🎣 게임 시작", type="primary", use_container_width=True):
        go("task")
    st.caption("설거지 · 분리수거 / 2~30명 / 화면을 눌러 낚기")

elif st.session_state.stage == "task":
    st.caption("오늘의 당첨 물고기 · 이 친구를 낚으면 당첨!")
    st.markdown('<div class="step">STEP 1 / 3 · 집안일 선택</div>', unsafe_allow_html=True)
    st.subheader("오늘은 어떤 일을 뽑을까요?")
    left, right = st.columns(2)
    if left.button("🧼 설거지", use_container_width=True):
        st.session_state.task = "설거지"
        go("names")
    if right.button("♻️ 분리수거하기", use_container_width=True):
        st.session_state.task = "분리수거하기"
        go("names")

elif st.session_state.stage == "names":
    st.markdown('<div class="step">STEP 2 / 3 · 참가자 입력</div>', unsafe_allow_html=True)
    st.subheader(f"{'🧼' if st.session_state.task == '설거지' else '♻️'} {st.session_state.task}")
    st.caption("＋를 누르면 사용자1, 사용자2…가 추가됩니다. 입력 칸을 눌러 이름을 바꿔 주세요. (최대 30명)")
    total_pages = max(1, (len(st.session_state.people) + 2) // 3)
    page = min(st.session_state.get("name_page", 0), total_pages - 1)
    previous, page_label, following = st.columns([1, 2, 1])
    if previous.button("◀", disabled=page == 0, use_container_width=True):
        st.session_state.name_page = page - 1
        st.rerun()
    page_label.caption(f"참가자 {len(st.session_state.people)}명 · {page + 1} / {total_pages} 페이지")
    if following.button("▶", disabled=page >= total_pages - 1, use_container_width=True):
        st.session_state.name_page = page + 1
        st.rerun()
    # Save all names outside widget state: Streamlit removes widgets on other pages.
    saved = st.session_state.setdefault("saved_names", {})
    for pid in st.session_state.people:
        saved[pid] = st.session_state.get(f"person_{pid}", saved.get(pid, f"사용자{pid + 1}"))
    for pid in list(st.session_state.people)[page * 3:page * 3 + 3]:
        key = f"person_{pid}"
        if key not in st.session_state:
            st.session_state[key] = saved.get(pid, f"사용자{pid + 1}")
        col, delete = st.columns([6, 1])
        col.text_input("참가자 이름", key=key, max_chars=24, label_visibility="collapsed", placeholder="이름을 입력하세요")
        if delete.button("✕", key=f"delete_{pid}", disabled=len(st.session_state.people) == 1, help="참가자 삭제"):
            st.session_state.people.remove(pid)
            st.rerun()
    if st.button("＋ 참가자 추가", use_container_width=True, disabled=len(st.session_state.people) >= 30):
        pid = st.session_state.next_id
        st.session_state.people.append(pid)
        st.session_state.next_id += 1
        st.session_state.name_page = (len(st.session_state.people) - 1) // 3
        st.rerun()
    st.divider()
    back, start = st.columns([1, 2])
    if back.button("← 집안일 선택", use_container_width=True):
        go("task")
    if start.button("🎣 낚시 시작!", type="primary", use_container_width=True):
        names = [st.session_state.get(f"person_{pid}", saved.get(pid, f"사용자{pid + 1}")).strip() for pid in st.session_state.people]
        if any(not name for name in names):
            st.error("모든 참가자의 이름을 입력해 주세요.")
        elif len(names) < 2:
            st.warning("두 명 이상 추가하면 낚시를 시작할 수 있어요.")
        elif len(set(names)) != len(names):
            st.error("누가 당첨됐는지 구분할 수 있도록 이름을 다르게 입력해 주세요.")
        else:
            st.session_state.result = {"names": names, "winner": secrets.randbelow(len(names)), "task": st.session_state.task}
            st.session_state.round_no += 1
            go("fishing")

else:
    st.markdown('<div class="step">STEP 3 / 3 · 화면을 눌러 직접 낚기</div>', unsafe_allow_html=True)
    result = st.session_state.result
    st.subheader(f"🎣 오늘의 {result['task']} 담당은?")
    components.html(f"<!-- round:{st.session_state.round_no} -->" + fishing_scene(result['names'], result['winner'], result['task']), height=460, scrolling=False)

    again, edit = st.columns(2)
    if again.button("🎲 같은 명단으로 다시 뽑기", use_container_width=True):
        st.session_state.result = {**result, "winner": secrets.randbelow(len(result['names']))}
        st.session_state.round_no += 1
        st.rerun()
    if edit.button("✏️ 이름 / 집안일 변경", use_container_width=True):
        go("names")
