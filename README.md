
# DragOn_Back
이화여자대학교 멋쟁이 사자처럼 11기 졸업 프로젝트 1팀 

### 백엔드 개발자

|                           이지원                            |                             심예원                             |
| :---------------------------------------------------------: | :------------------------------------------------------------: |
|               <img src="https://github.com/11th-LikeLion-DragOn/DragOn_Back/assets/127853111/a70f6bad-e2f4-4dc1-a62f-dd37d9ea9454" width="100" height="100"/>               |                <img src="https://github.com/11th-LikeLion-DragOn/DragOn_Back/assets/127853111/4158e04e-9cda-40d0-b38f-623382d29359" width="100" height="100"/>                 |
| 메인페이지  | 회원가입&로그인 <br />  마이페이지 |


### 기술 스택 및 라이브러리

<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"/> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">  <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"> 

### 개발 기능
 - 나만의 챌린지와 목표 생성, 관리 <br />
 - 친구를 추가하여 댓글, 리액션 남기기<br />
 - 여의주를 충전하여 목표 메꾸기 <br />
 - 성향 테스트를 통한 프로필 생성<br />
 - 자체 회원가입 및 소셜로그인<br />
 

### 📁폴더구조
```
📦Dragon
 ┣ 📂.github
 ┃ ┗ 📂workflows
 ┃ ┃ ┗ 📜deploy.yml
 ┣ 📂accounts
 ┃ ┣ 📂migrations
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📂config
 ┃ ┣ 📂docker
 ┃ ┣ 📂nginx
 ┃ ┣ 📂scripts
 ┃ ┗ 📜__init__.py
 ┣ 📂dragon
 ┃ ┣ 📂settings
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┣ 📜base.py
 ┃ ┃ ┣ 📜dev.py
 ┃ ┃ ┣ 📜prod.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📜asgi.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜wsgi.py
 ┃ ┗ 📜__init__.py
 ┣ 📂main
 ┃ ┣ 📂migrations
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📂mypage
 ┃ ┣ 📂migrations
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📜.env
 ┣ 📜.env.prod
 ┣ 📜.gitignore
 ┣ 📜docker-compose.prod.yml
 ┣ 📜docker-compose.yml
 ┣ 📜Dockerfile
 ┣ 📜Dockerfile.prod
 ┣ 📜manage.py
 ┣ 📜README.md
 ┗ 📜requirements.txt
```
