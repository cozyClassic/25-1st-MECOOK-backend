# PEACOCK Clone Project (MECOOK)
  e-commerce사이트인 peacock 웹사이트 클론.

## 개발 기간 / 개발 인원
  개발 기간: 2021-10-4 ~ 2021-10-15
  <br>
  개발 인원: 김도훈(**백엔드**), 김민찬(**백엔드**)
  정민지(**프론트엔트**), 김용현(**프론트엔트**), 손호영(**프론트엔트**), 서고운(**프론트엔트**)
  
## DB modeling
  
## Technologies
* Python
* Django
* MySQL
* AWS EC2, RDS
* Git, Github
* Slack, Trello

## Features
**김민찬**
* 상품 리스트 API (``GET``)
* 상품 상세보기 API (``GET``)
* 상품 리스트 검색, 정렬 API(``GET``)
* 로그인 시 좋아요 여부 표시 (``GET``)
* 전체 URL 쿼리 파라미터 사용

**김도훈**
* 로그인, 회원가입 API (POST)
* 장바구니 상품 추가, 조회, 삭제 API (``POST``, ``GET``, ``DELETE``)
* 상품 리뷰 생성, 조회, 삭제 API (``POST``, ``GET``, ``DELETE``)
* 상품 즐겨찾기(좋아요) 생성, 삭제 API (``POST``)
* 주문 (포인트 차감 기능만) API (``POST``, ``GET``)

## Endpoint
* ``POST``/user/signup (회원가입)
* ``POST``/user/login (로그인)
* ``POST``/cart (장바구니 넣기)
* ``GET``/cart (장바구니 조회)
* ``DELETE``/cart/<int:cart_id> (장바구니 삭제)
* ``POST``/review/comment (리뷰 남길때)
* ``GET``/review/list?product={product_id}&limit={int}&offset={int} (리뷰 가져올때)
* ``DELETE``/review/ccomment<int:review_id> (리뷰 삭제할때)
* ``POST``/like/user (좋아요 누를때)
* ``GET``/order (주문 누르기후 포인트 차감)
* ``GET``/product/?$product=${상품ID}&category=${카테고리ID}&detail=${상세보기표시여부(1,0}&search=${검색 단어1}&search=${검색 단어2}&sort=${priority|id|name 정렬기준}
  -> query Param의 모든 조건은 선택사항임
