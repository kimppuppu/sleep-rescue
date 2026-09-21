# 🌙 Sleep Rescue

청소년이 7일간 수면 습관을 기록하고 수면시간, 피로도, 스마트폰 사용, 카페인 등의 관계를 관찰하는 Streamlit 교육용 웹앱입니다.

## 주요 기능
- 하루 수면 기록
- 최근 7일 기록 표시
- 평균 수면시간/피로도/스마트폰 사용시간
- 수면시간 및 피로도 그래프
- 수면시간–피로도 탐색적 상관관계
- 입력에 따른 개인화 Rescue Plan
- CSV 다운로드
- Sleep Science 설명

## 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud 배포
GitHub repository에 `app.py`, `requirements.txt`, `README.md`를 업로드한 뒤 Streamlit Community Cloud에서 repository와 `app.py`를 선택하여 Deploy 합니다.

## 중요
현재 버전의 데이터는 Streamlit session_state에 저장되므로 브라우저 세션이 종료되면 사라질 수 있습니다. 수행평가 시연용으로는 적합하며, 기록은 CSV로 내려받을 수 있습니다.

Sleep Rescue Score는 의학적으로 검증된 임상 척도가 아니라 교육 프로젝트를 위해 만든 휴리스틱입니다.
