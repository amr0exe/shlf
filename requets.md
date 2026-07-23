# requests

## Author endpoints
POST /api/authors/create/
```bash
curl -X POST http://127.0.0.1:8000/api/authors/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "George Orwell",
    "email": "orwell@example.com"
  }'
```

GET /api/authors/list/
```bash
curl -X GET http://127.0.0.1:8000/api/authors/list/
```

GET /api/authors/<id>/
```bash
curl -X GET http://127.0.0.1:8000/api/authors/1/
```

DELETE /api/authors/delete/<id>/
```bash
curl -X DELETE http://127.0.0.1:8000/api/authors/delete/1/
```

---

## Book endpoints
POST /api/books/create/
```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "isbn": "978-0451524935",
    "published_year": 1949,
    "language": "English",
    "page_count": 328,
    "tag": "fiction",
    "author_id": 1,
    "copy_count": 3
  }'
```

GET /api/books/
```bash
curl -X GET http://127.0.0.1:8000/api/books/
```

GET /api/books/<id>/
```bash
curl -X GET http://127.0.0.1:8000/api/books/1/
```

PATCH /api/books/<id>/update/
```bash
curl -X PATCH http://127.0.0.1:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nineteen Eighty-Four"
  }'
```

PUT /api/books/<id>/update/
```bash
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "isbn": "978-0451524935",
    "published_year": 1949,
    "language": "English",
    "page_count": 328,
    "tag": "fiction",
    "author_id": 1
  }'
```

DELETE /api/books/<id>/delete/
```bash
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/
```

---

## Member endpoints
POST /api/members/
```bash
curl -X POST http://127.0.0.1:8000/api/members/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

GET /api/members/
```bash
curl -X GET http://127.0.0.1:8000/api/members/
```

GET /api/members/<id>/
```bash
curl -X GET http://127.0.0.1:8000/api/members/1/
```

PATCH /api/members/<id>/update/
```bash
curl -X PATCH http://127.0.0.1:8000/api/members/1/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com"
  }'
```

PUT /api/members/<id>/update/
```bash
curl -X PUT http://127.0.0.1:8000/api/members/1/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com"
  }'
```

DELETE /api/members/<id>/delete/
```bash
curl -X DELETE http://127.0.0.1:8000/api/members/1/delete/
```

---

## Borrowing endpoints
POST /api/borrowings/checkout/
```bash
curl -X POST http://127.0.0.1:8000/api/borrowings/checkout/ \
  -H "Content-Type: application/json" \
  -d '{
    "member_id": 1,
    "book_id": 1,
    "days": 14
  }'
```

POST /api/borrowings/return/
```bash
curl -X POST http://127.0.0.1:8000/api/borrowings/return/ \
  -H "Content-Type: application/json" \
  -d '{
    "borrowing_id": 1
  }'
```

GET /api/borrowings/
```bash
curl -X GET http://127.0.0.1:8000/api/borrowings/
```

GET /api/borrowings/ (with filters)
```bash
curl -X GET "http://127.0.0.1:8000/api/borrowings/?status=borrowed"
curl -X GET "http://127.0.0.1:8000/api/borrowings/?member_id=1"
curl -X GET "http://127.0.0.1:8000/api/borrowings/?overdue=true"
```

GET /api/borrowings/<id>/
```bash
curl -X GET http://127.0.0.1:8000/api/borrowings/1/
```
