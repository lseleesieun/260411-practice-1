# 🍕 분수 피자 연구소

초등학교 3학년 학생이 제한 시간 동안 손님의 분수 주문을 해결하는 Streamlit 게임입니다. 주문에 표시된 분수(예: `1/6`)를 보고 피자 조각을 직접 눌러 선택하세요. 주문 하나를 해결할 때마다 별 2개를 받고, 60초 동안 많이 해결할수록 높은 셰프 등급을 받을 수 있습니다.

## 실행 방법

Python 3.9 이상이 설치된 환경에서 프로젝트 폴더로 이동한 뒤 실행합니다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Windows PowerShell에서는 가상 환경 활성화에 다음 명령을 사용합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

앱이 실행되면 터미널에 표시되는 로컬 주소를 브라우저에서 엽니다.
