import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Sleep Rescue", page_icon="🌙", layout="wide")

st.markdown("""
<style>
.block-container {max-width:1100px;padding-top:1.6rem;padding-bottom:3rem}
.hero {padding:1.4rem 1.6rem;border-radius:20px;background:linear-gradient(135deg,rgba(90,100,190,.17),rgba(100,180,210,.12));border:1px solid rgba(120,120,150,.22)}
.card {padding:1rem 1.1rem;border:1px solid rgba(120,120,140,.25);border-radius:14px;margin:.5rem 0}
.big {font-size:2.2rem;font-weight:800}
.small {opacity:.75;font-size:.9rem}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="hero"><h1>🌙 Sleep Rescue</h1>
<b>청소년 수면 습관을 기록하고, 나에게 맞는 회복 전략을 찾아보는 프로젝트</b><br>
<span class="small">충분한 수면을 대체하는 방법을 찾는 앱이 아니라, 수면 부족을 발견하고 생활습관을 개선하기 위한 교육용 웹앱입니다.</span>
</div>""", unsafe_allow_html=True)

st.warning("일부러 잠을 줄여 실험하지 마세요. 평소 생활에서 관찰된 수면을 기록하는 프로젝트입니다.")

if "records" not in st.session_state:
    st.session_state.records = []

tab1, tab2, tab3, tab4 = st.tabs(["📝 오늘 기록", "📊 7일 분석", "🛟 Rescue Plan", "🧠 Sleep Science"])

def score_row(sleep, phone, caffeine, nap, regular, fatigue):
    score = 100
    if sleep < 5: score -= 40
    elif sleep < 6: score -= 30
    elif sleep < 7: score -= 20
    elif sleep < 8: score -= 10
    if phone >= 120: score -= 15
    elif phone >= 60: score -= 10
    if caffeine == "있음": score -= 10
    if nap == "60분 초과": score -= 10
    elif nap == "20~60분": score -= 5
    if regular == "아니요": score -= 5
    if fatigue >= 4: score -= 10
    return max(score, 0)

with tab1:
    st.header("오늘의 수면 기록")
    c1, c2, c3 = st.columns(3)
    with c1:
        d = st.date_input("날짜", date.today())
        sleep = st.slider("수면시간 (시간)", 3.0, 10.0, 6.5, .5)
    with c2:
        fatigue = st.slider("아침/현재 피로도", 1, 5, 3, help="1=매우 개운함, 5=매우 피곤함")
        phone = st.slider("취침 전 스마트폰 (분)", 0, 180, 60, 10)
    with c3:
        caffeine = st.selectbox("늦은 오후/저녁 카페인", ["없음","있음"])
        nap = st.selectbox("낮잠", ["없음","20분 이내","20~60분","60분 초과"])
        regular = st.selectbox("평소와 비슷한 시간에 기상", ["네","아니요"])

    if st.button("➕ 기록 저장", type="primary", use_container_width=True):
        sc = score_row(sleep, phone, caffeine, nap, regular, fatigue)
        # 같은 날짜가 있으면 최신 기록으로 교체
        st.session_state.records = [r for r in st.session_state.records if r["날짜"] != str(d)]
        st.session_state.records.append({
            "날짜": str(d), "수면시간": sleep, "피로도": fatigue, "스마트폰(분)": phone,
            "늦은 카페인": caffeine, "낮잠": nap, "규칙적 기상": regular, "Rescue Score": sc
        })
        st.session_state.records = sorted(st.session_state.records, key=lambda x:x["날짜"])[-7:]
        st.success(f"{d} 기록을 저장했습니다. 현재 {len(st.session_state.records)}일 기록이 있습니다.")

    if st.session_state.records:
        st.subheader("저장된 기록")
        df_show = pd.DataFrame(st.session_state.records)
        st.dataframe(df_show, use_container_width=True, hide_index=True)
        st.download_button("📥 내 기록 CSV로 저장", df_show.to_csv(index=False).encode("utf-8-sig"),
                           "sleep_rescue_records.csv", "text/csv")
        if st.button("🗑️ 기록 초기화"):
            st.session_state.records = []
            st.rerun()

with tab2:
    st.header("나의 7일 수면 패턴")
    if not st.session_state.records:
        st.info("먼저 '오늘 기록'에서 데이터를 저장하세요. 실제 수행평가에서는 5~7일 정도 기록하면 좋습니다.")
    else:
        df = pd.DataFrame(st.session_state.records)
        a,b,c,dcol = st.columns(4)
        a.metric("평균 수면시간", f"{df['수면시간'].mean():.1f} h")
        b.metric("평균 피로도", f"{df['피로도'].mean():.1f} / 5")
        c.metric("평균 스마트폰", f"{df['스마트폰(분)'].mean():.0f} min")
        dcol.metric("평균 Rescue Score", f"{df['Rescue Score'].mean():.0f}")

        st.subheader("수면시간 변화")
        st.line_chart(df.set_index("날짜")[["수면시간"]])
        st.subheader("피로도 변화")
        st.line_chart(df.set_index("날짜")[["피로도"]])

        st.subheader("수면시간과 피로도")
        st.scatter_chart(df, x="수면시간", y="피로도")

        if len(df) >= 3:
            corr = df["수면시간"].corr(df["피로도"])
            if pd.notna(corr):
                st.caption(f"이 기록에서 수면시간–피로도 Pearson 상관계수: {corr:.2f}")
                st.info("상관관계는 인과관계를 의미하지 않으며, 기록 일수가 적기 때문에 탐색적 관찰로만 해석하세요.")

with tab3:
    st.header("오늘의 개인 맞춤 Rescue Plan")
    if not st.session_state.records:
        st.info("오늘의 기록을 먼저 입력해 주세요.")
    else:
        r = st.session_state.records[-1]
        st.markdown(f"<div class='big'>{r['Rescue Score']} / 100</div>", unsafe_allow_html=True)
        st.caption("이 점수는 프로젝트용 휴리스틱이며 의학적으로 검증된 임상 수면점수가 아닙니다.")

        recs = []
        if r["수면시간"] < 8:
            recs.append(("🛏️ 충분한 수면시간 우선", "수면 부족을 카페인이나 다른 방법으로 완전히 대신할 수는 없습니다. 오늘 밤 가능한 범위에서 수면시간을 확보하세요."))
        if r["스마트폰(분)"] >= 60:
            recs.append(("📱 취침 전 스마트폰 줄이기", "잠들기 전 화면과 자극적인 콘텐츠 사용시간을 줄여 잠들 준비를 해보세요."))
        if r["늦은 카페인"] == "있음":
            recs.append(("☕ 늦은 카페인 피하기", "카페인은 아데노신 수용체의 작용을 방해해 덜 졸리게 느끼게 하지만 필요한 수면을 대체하지는 못합니다."))
        if r["낮잠"] in ["20~60분","60분 초과"]:
            recs.append(("😴 낮잠 조절", "낮잠이 필요하다면 너무 길거나 늦지 않도록 조절해 밤 수면을 방해하지 않게 해보세요."))
        if r["규칙적 기상"] == "아니요":
            recs.append(("⏰ 기상시간 일정하게", "비슷한 기상시간은 일주기 리듬을 일정하게 유지하는 데 도움이 됩니다."))
        if r["피로도"] >= 4:
            recs.append(("☀️ 낮 동안 밝은 빛과 활동", "낮에는 밝은 환경에서 지내고 가볍게 움직여 생활 리듬을 유지해 보세요."))
        if not recs:
            recs.append(("🌙 현재 습관 유지", "입력한 항목에서 큰 위험 습관이 보이지 않습니다. 규칙적인 수면 기록을 이어가세요."))

        for title, body in recs[:4]:
            st.markdown(f"<div class='card'><b>{title}</b><br><span class='small'>{body}</span></div>", unsafe_allow_html=True)

        st.subheader("오늘 실천 체크")
        st.checkbox("충분한 수면시간 확보하기")
        st.checkbox("잠들기 전 스마트폰 줄이기")
        st.checkbox("늦은 카페인 피하기")
        st.checkbox("내일 피로도 다시 기록하기")

with tab4:
    st.header("왜 이런 추천을 하나요?")
    with st.expander("청소년과 수면"):
        st.write("청소년기의 충분한 수면은 학습, 기억, 정서 조절과 신체 건강에 중요합니다. 개인차는 있지만 수면시간 자체를 생활요령으로 완전히 대체할 수는 없습니다.")
    with st.expander("아데노신과 카페인"):
        st.write("깨어 있는 시간이 길어지면서 수면 압력이 증가합니다. 카페인은 아데노신 수용체를 차단해 일시적으로 덜 졸리게 느끼게 할 수 있지만, 수면 필요량을 없애는 것은 아닙니다.")
    with st.expander("스마트폰과 취침"):
        st.write("취침 전 스마트폰은 화면의 빛뿐 아니라 영상, 게임, 메시지 같은 자극과 취침시간 지연을 통해 수면 습관에 영향을 줄 수 있습니다.")
    with st.expander("이 프로젝트에서 배울 수 있는 것"):
        st.write("7일간 자신의 생활 데이터를 수집하고, 수면시간·스마트폰 사용·카페인 같은 행동과 다음 날 피로도의 관계를 관찰합니다. 이는 개인의 생활습관을 데이터로 이해하는 간단한 디지털 헬스 프로젝트입니다.")

st.divider()
st.caption("Sleep Rescue · 청소년 수면습관 교육 프로젝트 | 의료 진단·치료용이 아닙니다.")
