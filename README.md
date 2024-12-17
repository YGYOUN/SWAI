/* 소프트웨어 실행 구조 계획

프로젝트 폴더 SW_AI

ㄴfeatures 폴더

  ㄴ__init__.py
  
    _base.py
    
    app.py
    (Flask 서버를 통해 외부 API로부터 raw data를 받아와, 프론트에서 만든 db의 주문날짜/시간이 일치하는 row만 추려내어 열 단위로 합쳐 db화)
    
    features.py
    (db화 한 데이터에서 function 폴더안의 보조지표 수치 계산 함수들을 실행하고 수치값을 db에 추가)
    
ㄴfunctions 폴더

  ㄴ__init__.py
  
    _base.py
    
    functions.py
    (보조지표를 계산하는 함수들이 작성 된 파일)
    
ㄴmodel 폴더
(학습 모델이 담겨있는 폴더, pfhedge 모델을 수정하여 적용 예정)

ㄴtradingView 폴더

  ㄴ__init__.py
  
    _base.py
    
    tradingView.py
    (tradingView에서 custom trading strategy의 백데이터 테스팅 기능을 사용할 수 있도록 학습 결과인 보조지표 조합을 tradingView에 전송하고, 백테스팅 결과값을 저장하고 프론트로 전달) 
    
ㄴAPI 폴더
(증권사/거래소 등과 자동화 매매를 위해 API를 통한 연동 기능 폴더)

index.html
(프런트 템플릿 디자인, 이용자로부터 매매내역 csv 데이터를 받아 필요한 부분만 추려내고 매매유형별로 분류하여 4개의 basket화하여 백엔드로 전달하고, tradingView.py에서 전달하는 데이터를 받아 백테스팅 결과를 사용자에게 출력)

app.py
(현재는 flask 서버를 통해 yfinance api로부터 rawdata를 받아 프런트에서 전송한 db에 진입날짜/시간에 맞는 row를 추출하여 db에 합치는 역할을 담당, 추후에는 features 폴더 안으로 이동 예정)

이외의 폴더, 파일은 템플릿 관련이며, 24.12.17. 현재는 SW_AI 프로젝트 폴더의 index.html, app.py 외의 폴더 및 파일은 구현되어 있지않은 상태 */
