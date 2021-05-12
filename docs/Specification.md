# Project 0303
## 설명
가족 사진을 쉽게 공유할 수 있는 디지털 액자를 위한 앱

## 용어
* 토큰 : 채널에 앨범을 추가할 때 사용되는 4자리 랜덤 문자열 (유효기한 3분)
* 앨범: 배포자에 의해 생성된 사진 묶음
* 채널: 구독자에 의해 생성된 앨범 묶음
* 슬라이드 : 채널 내 표시될 사진 조각
* 슬라이드 쇼: 선택된 채널을 통해 꾸며진 디지털 액자를 위한 화면

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
[![아키텍쳐](https://raw.githubusercontent.com/onetop21/Project0303/main/docs/images/archeture.svg "아키텍쳐")](https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=archeture.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fonetop21%2FProject0303%2Fmain%2Fdocs%2Fassets%2Farcheture.drawio)<br>
[[Edit]](https://app.diagrams.net/#Honetop21%2FProject0303%2Fmain%2Fdocs%2Fassets%2Farcheture.drawio)

## 사용 언어 및 도구
* Flutter
* Python
  * FastAPI
    * OAuth2 (Google?)
 * UVicorn
* Redis (Cache)
* Mongo DB
* MinIO
* Docker

## API
|기능|메소드|API|HEADER|BODY|
|---|---|---|---|---|
|유저 인증 요청(토큰 발급)|GET|/auth|
|유저 목록|GET|/user|
|가입|POST|/user|
|유저 정보|GET|/user/$USERNAME|
|유저 갱신|PUT|/user/$USERNAME|
|탈퇴(계정 소멸)|DELETE|/user/$USERNAME|
|앨범 목록|GET|/album|
|앨범 생성|POST|/album|
|앨범 다운로드|GET|/album/$ALBUM_ID/bundle|
|토큰 발급|GET|/album/$ALBUM_ID/token|
|사진 목록|GET|/album/$ALBUM_ID/photo|
|사진 추가(업로드)|POST|/album/$ALBUM_ID/photo|
|사진 삭제|DELETE|/album/$ALBUM_ID/photo/$PHOTO_ID|
|앨범 삭제|DELETE|/album/$ALBUM_ID|
|채널 목록|GET|/channel|
|채널 생성|POST|/channel|
|구독 앨범|GET|/channel/$CHANNEL_ID/subscription|
|앨범 구독|POST|/channel/$CHANNEL_ID/subscription|
|앨범 해지|DELETE|/channel/$CHANNEL_ID/subscription/$SUBS_ID|
|슬라이드 목록|GET|/channel/$CHANNEL_ID/slide|
|슬라이드 정보|GET|/channel/$CHANNEL_ID/slide/$SLIDE_ID|
|슬라이드 보이기/숨기기|PUT|/channel/$CHANNEL_ID/slide/$SLIDE_ID|
|채널 삭제|DELETE|/channel/$CHANNEL_ID|

## Database Schema
|Collection|Document|비고|
|---|---|---|
|user|{_id: ObjectId, username: str, password: str(hashed)}||
|album|{_id: ObjectId, name: str, owner: ObjectID(user._id)}||
|photo|{_id: ObjectId, bucket: str, path: str, verified: boolean, owner: ObjectId(album._id)}||
|thumb|{_id: ObjectId, small: str, medium: str, large: str, owner: ObjectId(photo._id)}||
|channel|{_id: ObjectId, name: str, owner: ObjectId(user._id)}||
|subscription|{_id: ObjectId, subscribed: ObjectId(album._id), owner: ObjectId(channel._id)}||
|slide|{_id: ObjectId, photo: ObjectId(photo._id), channel: ObjectId(channel._id), visibility: boolean, owner: ObjectId(subscription._id)}||


