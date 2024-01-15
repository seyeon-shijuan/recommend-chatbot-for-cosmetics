# python packaging
  1. build.sh 이용
    - `$ sh build.sh -d`
      - 소스포함하지 않고 패키징
    - `$ sh build.sh -s`
      - 소스포함 패키징
  2. root 경로에서 `pip install .`
  3. `cosmetic-rec` 커맨드로 애플리케이션 실행

# run recommend
- `$ sh run`

# settings
- config.env.example 같은 형식으로 config.env 생성하여 사용

# caution
- 패키지 경로 추가될 때마다 `setup.py` 의 `packages`에 경로 추가 필요...

# API
- `recommend.http` 참고
  - VS Code Extension 에서 `REST Client` 설치 후 http 파일 내 SendRequest 클릭으로 response 확인