# Project 0303
## 설명
가족 사진을 쉽게 공유할 수 있는 디지털 액자를 위한 앱

## 용어
* 앨범: 배포자에 의해 생성된 사진 묶음
* 채널: 구독자에 의해 생성된 앨범 묶음
* 슬라이드 쇼: 선택된 채널을 통해 꾸며진 디지털 액자를 위한 화면
* 토큰 : 채널에 앨범을 추가할 때 사용되는 4자리 랜덤 문자열 (유효기한 3분)

## 사용 시나리오
* 관리자 로그인 및 비밀번호 변경
* 사용자 가입 및 로그인 (기본 구독 권한만 보유, 배포 권한 요청시 추가)
* 배포자
  * 앨범 생성 (업로더 계정 귀속)
  * 앨범에 사진 추가
* 구독자
  * 기본 설정 진행 (구글 캘린더 연동 등)
  * 채널 생성
  * 배포자에 의해 앨범 토큰 획득 (배포자는 본인 앨범 토큰 생성 가능)
  * 앨범 토큰을 이용하여 채널에 앨범 추가 (보기 권한)
  * 한 채널을 선택 후 슬라이드 쇼 기능을 통해 디지털 액자로 전환

## 구성 요소
* 인증 서버
* API 서버 (Stateless)
* 데이터베이스
* 오브젝트 스토리지
* 웹애플리케이션

## 아키텍처
![Diagram](https://viewer.diagrams.net/?target=blank&highlight=0000ff&edit=_blank&layers=1&nav=1&title=archeture#RjZJNa4QwEIZ%2FTY6FqFuXHlvX3V4KBRfaW0nNrAlEIzGu2l%2FfWCd%2BsCwUPMw885HxnSFRUvYnw2rxpjkoElLek%2BhAwjDYhSEZP8qHieyfdhMojOSYtIBM%2FgBCirSVHJpNotVaWVlvYa6rCnK7YcwY3W3TLlptX61ZATcgy5m6pR%2BSW4E0pnQJvIIshH869JGS%2BWwEjWBcdysUpSRKjNZ2sso%2BATWq54WZ6o53ovNkBir7nwJ5Msfk%2B%2FkrLtP94%2FlK3w%2FF5wN2uTLV4h%2BfobE4sB28DEa3FYexESXRSyekhaxm%2BRjt3OIdE7ZUzguciS3BWOjvzhrMCrjbAV2CNYNL8QVeRTybGN1utQOvq1jJ7%2FMYrr2YOy%2FCOAO18e6yg7%2FY6pSj9Bc%3D)

## 사용 언어 및 도구
* Flutter
* Python
 * FastAPI
* Mongo DB
* MinIO
* Docker

## API
* 회원가입
* 로그인
* 
