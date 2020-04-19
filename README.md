# API spec

### Sign-up API 
`HTTP POST /users/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| username | string | **Required** 회원 아이디 |
| password | string | **Required** 회원 비밀번호 |
| email | string | **Required** 회원 이메일 주소 |
| name | string | **Required** 회원 이름 |  
```JSON
201 Created
{
  "id": 1,
  "username": "sekyo95",
  "email": "myungsekyo@gmail.com",
  "name": "명세교"
}
```




### Login API 
`HTTP POST /users/login/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| username | string | **Required** 회원 아이디 |
| password | string | **Required** 회원 비밀번호 |  

```JSON
200 OK
{
    "token": "3ffb63046f4c2adf400dbeeee5608cb2e63b375b"
}
```




### User list API 
`HTTP GET /users/`
```JSON
200 OK
[
  {
    "id": 1,
    "username": "sekyo95",
    "email": "myungsekyo@gmail.com",
    "name": "명세교"
  },  
  {
    "id": 2,
    "username": "chaemoon",
    "email": "chaemoon@gmail.com",
    "name": "정채문"
  }
]
```




### User detail API 
`HTTP POST /users/<pk>/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| pk | int | **Required** 회원 pk |  

```JSON
200 OK
{
  "id": 1,
  "username": "sekyo95",
  "email": "myungsekyo@gmail.com",
  "name": "명세교"
}
```




### User update API 
`HTTP PATCH /users/<id>/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| id | int | 회원 pk |
| username | string | 회원 아이디 |
| password | string | 회원 비밀번호 |
| email | string | 회원 이메일 주소 |
| name | string | 회원 이름 |  

```JSON
201 Created
{
  "id": 1,
  "username": "sekyo95",
  "email": "myungsekyo@gmail.com",
  "name": "명세교"
}
```










### Meeting list API 
`HTTP GET /meetings/`
```JSON
200 OK
[
  {
    "id": 1,
    "title": "캡스톤 디자인",
    "host": "명세교",
  },  
  {
    "id": 2,
    "title": "객체지향 프로그래밍",
    "host": "명세교",
  }
]
```
### Meeting create API 
`HTTP POST /meetings/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| title | string | **Required** 미팅 제목  |
```JSON
201 Created
{
  "id": 1,
  "title": "캡스톤 디자인",
  "host": "명세교"
}
```
### Meeting detail API 
`HTTP POST /meetings/<pk>/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| pk | int | **Required** 미팅의 pk |
```JSON
200 OK
{
  "id": 1,
  "title": "캡스톤 디자인",
  "host": "명세교"
}
```
### Meeting update API 
`HTTP PATCH /meetings/<pk>/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| pk | int | **Required** 미팅 pk |
| title | string | **Required** 미팅 제목  |
```JSON
200 OK
{
  "id": 1,
  "title": "캡스톤 디자인",
  "host": "명세교"
}
```
### Member list API 
`HTTP GET /meetings/<meeting_pk>/members/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| meeting_pk | int | **Required** 미팅 pk |
```JSON
200 OK
[
  {
    "id": 1,
    "meeting": 1,
    "member": 1,
    "type": "manager"
  },
  {
    "id": 2,
    "meeting": 2,
    "member": 2,
    "type": "student"
  },
]
```
### Member add API 
`HTTP POST /meetings/<meeting_pk>/members/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| meeting_pk | int | **Required** 미팅 pk |
| member | int | **Required** 멤버 유저 pk |
| type | string | **Required** 멤버 타입 manager or student |
```JSON
201 Created
{
  "id": 2,
  "meeting": 2,
  "member": 2,
  "type": "student"
}
```
### Member delete API 
`HTTP DELETE /meetings/<meeting_pk>/members/<pk>/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| meeting_pk | int | **Required** 미팅 pk |
| pk | int | **Required** 멤버 pk |
```JSON
200 OK
{
  "id": 2,
  "meeting": 2,
  "member": 2,
  "type": "student"
}
```
### Code run API 
`HTTP POST /codes/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| std_in | string | **Required** 사용자 input |
| code | string | **Required** 사용자 코드 |
| language | string | **Required** 사용자 사용 언어 c or java or python |
```JSON
200 OK
{
  "id": 1,
  "std_in": "10 10 10",
  "std_out": null,
  "status": "queued",
  "author": 1,
  "code": "System.out.println('hello world');",
  "language": "java"
}
```
### Code detail API 
`HTTP GET /codes/<pk>/`
| Parameter | Type | Description |
| :--- | :--- | :--- |
| pk | int | **Required** 코드 pk |
```JSON
200 OK
{
  "id": 1,
  "std_in": "10 10 10",
  "std_out": "1 0 1",
  "status": "completed",
  "author": 1,
  "code": "System.out.println('hello world');",
  "language": "java"
}
```
