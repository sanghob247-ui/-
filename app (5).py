"""강가의 제비뽑기 — 실행: streamlit run app.py
GitHub에 이 파일과 requirements.txt를 올린 뒤 Streamlit Community Cloud에서 배포하세요.
QR은 배포 주소로 접속하는 기능입니다. 여러 기기의 참가자 명단을 동기화하지 않습니다.
"""
import io
import json
import secrets

import qrcode
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="강가의 제비뽑기", page_icon="🎣", layout="centered")
st.markdown('''<style>
.stApp{background:linear-gradient(180deg,#eef9ff,#f6fbf5);color:#153747}
.block-container{max-width:780px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3{color:#123d51!important}
.stButton>button{border-radius:14px;min-height:48px;font-weight:700}
.hero{padding:24px;border-radius:24px;background:#123d51;color:white;margin-bottom:20px}
.hero h1{color:white!important;font-size:2rem!important;margin:0}
.hero p{color:#d5f0f4;margin-bottom:0}
.step{color:#496777;font-size:14px;margin-bottom:12px}
</style>''', unsafe_allow_html=True)

if "stage" not in st.session_state:
    st.session_state.update(stage="task", task="설거지", people=[0], next_id=1,
                            result=None, round_no=0)


def go(stage):
    st.session_state.stage = stage
    st.rerun()


def fishing_scene(names, winner, task):
    # JSON data is escaped so names cannot close the script element or inject HTML.
    payload = json.dumps({"names": names, "winner": winner, "task": task}, ensure_ascii=True).replace("<", "\\u003c")
    return r'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}body{margin:0;font-family:system-ui,'Apple SD Gothic Neo',sans-serif;color:#153747}
.scene{position:relative;height:310px;overflow:hidden;border-radius:22px;background:linear-gradient(#ceefff 0%,#eefaff 49%,#83ad68 50%,#83ad68 58%,#43afcb 59%,#137a9e 100%)}
.sun{position:absolute;top:25px;right:35px;font-size:48px}.cloud{position:absolute;top:22px;left:25px;font-size:50px}
.mountains{position:absolute;top:80px;left:0;width:100%;font-size:80px;letter-spacing:12px;opacity:.35;white-space:nowrap}
.fisher{position:absolute;left:12%;top:108px;font-size:58px;z-index:2;transform-origin:bottom center}
.fisher.pull{animation:pull .6s ease-in-out 2}.line{position:absolute;top:151px;left:43%;height:115px;border-left:2px solid #f5fcff;transform:rotate(-12deg);transform-origin:top}
.ripple{position:absolute;left:35%;top:235px;width:90px;height:22px;border:2px solid #b7f3ff;border-radius:50%;animation:ripple 1.5s infinite}
.water{position:absolute;bottom:20px;left:0;width:200%;color:#a4edf3;font-size:30px;letter-spacing:25px;white-space:nowrap;animation:water 8s linear infinite}
.fish{position:absolute;left:48%;top:235px;font-size:62px;opacity:0;z-index:3}.fish.caught{animation:catch 1.6s ease-out forwards}
.name{position:absolute;top:16px;left:50%;transform:translateX(-50%);max-width:65%;overflow-wrap:anywhere;background:#fff;padding:8px 16px;border-radius:16px;text-align:center;font-weight:800;z-index:4}
#status{text-align:center;min-height:65px;font-weight:750;padding:16px 8px;font-size:18px}
#cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(125px,1fr));gap:8px;max-height:190px;overflow:auto;padding:4px}
.card{background:white;border:1px solid #d1e4e9;border-radius:14px;padding:12px;text-align:center;overflow-wrap:anywhere}.card.win{background:#fff1ba;border:2px solid #bb7d00}.card.active{border:2px solid #1685a2}
#reveal{display:block;width:100%;padding:11px;border:1px solid #a3c9d5;border-radius:12px;background:#fff;color:#153747;font-weight:bold;cursor:pointer;margin-top:10px}
@keyframes water{to{transform:translateX(-25%)}}@keyframes ripple{to{transform:scale(1.5);opacity:0}}@keyframes pull{50%{transform:rotate(-16deg)}}
@keyframes catch{0%{opacity:1;transform:translate(0,0) rotate(0)}60%{opacity:1;transform:translate(-25px,-140px) rotate(-25deg)}100%{opacity:1;transform:translate(-70px,-105px) rotate(10deg)}}
@media(prefers-reduced-motion:reduce){.water,.ripple{animation:none}.fish.caught{animation-duration:.01s}}
</style></head><body>
<div class="scene"><div class="sun">☀️</div><div class="cloud">☁️</div><div class="mountains">⛰️ ⛰️ ⛰️</div><div class="name" id="name">낚시 준비 중</div><div class="fisher" id="fisher">🎣</div><div class="line"></div><div class="ripple"></div><div class="water">〜 〜 〜 〜 〜 〜 〜 〜 〜</div><div class="fish" id="fish">🐟</div></div>
<div id="status" role="status" aria-live="polite">강에 낚싯줄을 던졌어요…</div><div id="cards"></div><button id="reveal" type="button">기다리지 않고 결과 보기</button>
<script>
const data=PAYLOAD;
const cards=document.getElementById('cards'),statusEl=document.getElementById('status'),fish=document.getElementById('fish'),fisher=document.getElementById('fisher'),label=document.getElementById('name');
const nodes=data.names.map(n=>{const d=document.createElement('div');d.className='card';d.textContent=n+' · 대기';cards.appendChild(d);return d});
let index=0,timers=[],finished=false;
function later(f,t){timers.push(setTimeout(f,t))}
function finish(){if(finished)return;finished=true;timers.forEach(clearTimeout);nodes.forEach((d,i)=>{d.className='card'+(i===data.winner?' win':'');d.textContent=data.names[i]+(i===data.winner?' 🐟 당첨!':' 🐠 통과')});label.textContent='오늘의 당첨자';statusEl.textContent='🎉 '+data.names[data.winner]+'님 당첨! 오늘의 '+data.task+' 담당입니다.';fish.className='fish caught';document.getElementById('reveal').hidden=true;nodes[data.winner].scrollIntoView({block:'nearest',behavior:'smooth'})}
function next(){if(finished)return;if(index>=data.names.length){finish();return}const i=index++;label.textContent=data.names[i]+'님의 낚시';statusEl.textContent='입질이 왔어요! 어떤 물고기일까요?';nodes[i].className='card active';nodes[i].scrollIntoView({block:'nearest',behavior:'smooth'});fish.className='fish';fisher.className='fisher';later(()=>{fish.textContent=i===data.winner?'🐟':'🐠';fish.className='fish caught';fisher.className='fisher pull';nodes[i].className='card'+(i===data.winner?' win':'');nodes[i].textContent=data.names[i]+(i===data.winner?' 🐟 당첨!':' 🐠 통과');statusEl.textContent=i===data.winner?'🎉 당첨 물고기를 낚았어요!':'당첨 물고기가 아니에요. 통과!';later(next,1300)},900)}
document.getElementById('reveal').onclick=finish;later(next,650);
</script></body></html>'''.replace('PAYLOAD', payload)

st.markdown('<div class="hero"><h1>🎣 강가의 제비뽑기</h1><p>물고기 한 마리가 정해 주는 오늘의 집안일</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📱 QR로 앱 열기")
    st.caption("배포 후 실제 앱 주소(https://…streamlit.app)를 입력하세요. QR은 앱 접속용이며 참가자 명단은 기기 간 공유되지 않습니다.")
    url = st.text_input("배포된 앱 주소", placeholder="https://your-app.streamlit.app")
    if url:
        from urllib.parse import urlparse
        parsed = urlparse(url.strip())
        if parsed.scheme == "https" and parsed.netloc:
            image = qrcode.make(url.strip())
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            st.image(buffer.getvalue(), caption="카메라로 스캔하면 앱이 열려요", width=220)
            st.download_button("QR 이미지 다운로드", buffer.getvalue(), "fishing-qr.png", "image/png")
        else:
            st.warning("https://로 시작하는 올바른 배포 주소를 입력해 주세요.")
    st.divider()
    st.caption("모든 참가자의 당첨 확률은 같으며, 한 번의 추첨에서 딱 1명이 당첨됩니다. 새로고침하거나 세션이 종료되면 명단과 결과가 초기화될 수 있습니다.")

if st.session_state.stage == "task":
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
    for pid in list(st.session_state.people):
        key = f"person_{pid}"
        if key not in st.session_state:
            st.session_state[key] = f"사용자{pid + 1}"
        col, delete = st.columns([6, 1])
        col.text_input("참가자 이름", key=key, max_chars=24, label_visibility="collapsed", placeholder="이름을 입력하세요")
        if delete.button("✕", key=f"delete_{pid}", disabled=len(st.session_state.people) == 1, help="참가자 삭제"):
            st.session_state.people.remove(pid)
            st.rerun()
    if st.button("＋ 참가자 추가", use_container_width=True, disabled=len(st.session_state.people) >= 30):
        pid = st.session_state.next_id
        st.session_state.people.append(pid)
        st.session_state.next_id += 1
        st.rerun()
    st.divider()
    back, start = st.columns([1, 2])
    if back.button("← 집안일 선택", use_container_width=True):
        go("task")
    if start.button("🎣 낚시 시작!", type="primary", use_container_width=True):
        names = [st.session_state.get(f"person_{pid}", "").strip() for pid in st.session_state.people]
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
    st.markdown('<div class="step">STEP 3 / 3 · 물고기를 낚아 결과 확인</div>', unsafe_allow_html=True)
    result = st.session_state.result
    st.subheader(f"🎣 오늘의 {result['task']} 담당은?")
    components.html(f"<!-- round:{st.session_state.round_no} -->" + fishing_scene(result['names'], result['winner'], result['task']), height=660, scrolling=False)
    st.caption("당첨 물고기를 잡은 사람이 선택한 집안일을 맡아요. 결과는 시작할 때 한 번 정해지며, 애니메이션을 건너뛰어도 바뀌지 않습니다.")
    again, edit = st.columns(2)
    if again.button("🎲 같은 명단으로 다시 뽑기", use_container_width=True):
        st.session_state.result = {**result, "winner": secrets.randbelow(len(result['names']))}
        st.session_state.round_no += 1
        st.rerun()
    if edit.button("✏️ 이름 / 집안일 변경", use_container_width=True):
        go("names")
