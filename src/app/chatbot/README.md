# python packaging
  1. build.sh 이용
    - `$ sh build.sh -d`
      - 소스포함하지 않고 패키징
    - `$ sh build.sh -s`
      - 소스포함 패키징
  2. root 경로에서 `pip install .`
  3. `cosmetic-chat` 커맨드로 애플리케이션 실행

# run chatbot
- `$ sh run.sh`
  - default port: 8000

# settings
- config.env.example 같은 형식으로 config.env 생성하여 사용

# caution
- 패키지 경로 추가될 때마다 `setup.py` 의 `packages`에 경로 추가 필요...