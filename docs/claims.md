## Claims

### Posting a claim

```
POST /api/v1/claims/
```

Example request:

```
POST /api/v1/claims/ HTTP/1.1
Host: https://factlist.org
Content-Type: multipart/form-data
Authorization: Token <YOUR-API-TOKEN>

{
    "links": [{"link": "http://www.bbc.com/news/world-asia-42999499"}],
    "text": "Thailand woman killed taking selfie on train tracks",
    "files": []
}
```

Example response:
```
HTTP/1.1 201 OK
Content-Type: application/json; charset=utf-8

{
    'date_created': '2018-02-28T12:42:44.191315Z',
    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    'id': 9,
    'claim_links': [],
    'user': {
        'id': 1,
        'email': 'enis@factlist.org',
        'username': 'enis'
    }
    'evidences': []
}

```

### List of claims

```
GET /api/v1/claims/
```

Example request:

```
GET /api/v1/claims/ HTTP/1.1
Host: https://factlist.org
Content-Type: multipart/form-data
```

Example response:

```
{
    "count": 2,
    "next": "http://localhost:8000/api/v1/claims/?limit=50&offset=50",
    "previous": null,
    "results": [
        {
            "id": 1,
            "text": "Uma thurman's car crash footage from Kill Bill",
            "user": {
                "id": 1,
                "email": "serafettin@factlist.org",
                "username": "serafettin"
            },
            "links": [],
            "created_at": "2018-03-04T15:25:53.782821Z",
            "updated_at": null,
            "deleted_at": null,
            "files": [
                {
                    "file": "http://localhost:8000/api/v1/claims/http%3A/pics.imcdb.org/0is269/killbill2karmannghia6.3438.jpg",
                    "id": 1
                }
            ],
            "true_count": 1,
            "false_count": 0,
            "inconclusive_count": 0
        },
        {
            "id": 2,
            "text": "Women need more sleep than men",
            "user": {
                "id": 1,
                "email": "serafettin@factlist.org",
                "username": "serafettin"
            },
            "links": [],
            "created_at": "2018-03-04T15:25:53.842122Z",
            "updated_at": null,
            "deleted_at": null,
            "files": [
                {
                    "file": "http://localhost:8000/api/v1/claims/https%3A/www.helpguide.org/images/sleep/sleeping-woman-500.jpg",
                    "id": 2
                }
            ],
            "true_count": 0,
            "false_count": 1,
            "inconclusive_count": 0
        },
}
```

### Filter user's claims

```
GET /api/v1/claims/?filter=from:<username>
```

Example request:

```
GET /api/v1/claims/?filter=from:enisbt HTTP/1.1
Host: https://factlist.org
Content-Type: multipart/form-data
Authorization: Token <YOUR-API-TOKEN>
```

Example response:

```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 293,
            "text": "Test claim",
            "user": {
                "id": 2,
                "email": "enis@bob.com",
                "username": "enis"
            },
            "links": [],
            "created_at": "2018-03-09T10:38:19.469924Z",
            "updated_at": null,
            "deleted_at": null,
            "files": [],
            "true_count": 0,
            "false_count": 0,
            "inconclusive_count": 0
        }
    ]
}
```

### Get a claim

```
GET /api/v1/claims/:claim_id
```

Example request:

```
GET /api/v1/claims/:claim_id HTTP/1.1
Host: https://factlist.org
Content-Type: multipart/form-data
```

Example response:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
    'date_created': '2018-02-28T12:42:44.191315Z',
    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    'id': 9,
    'links': [],
    'user': {
        'id': 1,
        'email': 'enis@factlist.org',
        'username': 'enis'
    }
    'evidences': [],
    'files': []
}
```

### Modify a claim

```
PATCH /api/v1/claims/:claim_id
```

Example request:

```
PATCH /api/v1/claims/:claim_id HTTP/1.1
Host: https://factlist.org
Content-Type: multipart/form-data
Authorization: Token <YOUR-API-TOKEN>

{
    'date_created': '2018-02-28T12:42:44.191315Z',
    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    'id': 9,
    'links': [],
    'user': {
        'id': 1,
        'email': 'enis@factlist.org',
        'username': 'enis'
    }
    'evidences': []
}
```

### Delete a claim

```
DELETE /api/v1/claims/:claim_id
```

Example request:

```
DELETE /api/v1/claims/:claim_id HTTP/1.1
Host: https://factlist.org
Content-Type: multipart/form-data
Authorization: Token <YOUR-API-TOKEN>
```

Example response:

```
HTTP/1.1 204 NO CONTENT
Content-Type: application/json; charset=utf-8
```

### Post an evidence

```
POST /api/v1/claims/:claim_id/evidences/
```

Example request:

```
POST /api/v1/claims/:claim_id/evidences/ HTTP/1.1
Host: https://factlist.org
Content-Type: multipart/form-data
Authorization: Token <YOUR-API-TOKEN>

{
    "links": ["http://www.bbc.com/news/world-asia-42999499"],
    "files": []
    "text": "Thailand woman killed taking selfie on train tracks",
    "conclusion": true,
}
```

Example response.

```
HTTP/1.1 201 OK
Content-Type: application/json; charset=utf-8

[
    {
        "id": 1,
        "text": "Lorem",
        "conclusion": "true",
        "created_at": "2018-03-03T18:05:22Z",
        "user": {
            "id": 1,
            "email": "enis@bob.com",
            "username": "enis"
        },
        "links": [
            {
                "link": "https://github.com/serafettin",
                "id": 1
            }
        ],
        "files": [
            {
                "file": "http://localhost:8001/media/files/claims/2018/03/03/octosetup-linux_i386.bin",
                "id": 1
            }
        ]
    }
]
```

### Get list of evidences of a claim

```
GET /api/v1/claims/:claim_id/evidences/
```

Example request:

```
GET /api/v1/claims/:claim_id/evidences/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json
```

Example response:

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "text": "The footage of the unusual cloud formation was originally shot in the Canadian town of Grand Falls, New Brunswick and posted online on 1 August 2011 by Denis Laforge.",
            "conclusion": "false",
            "created_at": "2017-12-28T00:00:00Z",
            "updated_at": null,
            "deleted_at": null,
            "user": {
                "id": 1,
                "email": "serafettin@factlist.org",
                "username": "serafettin"
            },
            "links": [
                {
                    "link": "https://www.youtube.com/watch?v=gdg6WU_aqWE",
                    "id": 3
                }
            ],
            "files": []
        }
    ]
}
```

### Get an evidence

```
GET /api/v1/claims/:claim_id/evidences/:evidence_id/
```

Example request:

```
GET /api/v1/claims/:claim_id/evidences/:evidence_id/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json
```

Example response:

```
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 3,
    "text": "The footage of the unusual cloud formation was originally shot in the Canadian town of Grand Falls, New Brunswick and posted online on 1 August 2011 by Denis Laforge.",
    "conclusion": "false",
    "created_at": "2017-12-28T00:00:00Z",
    "updated_at": null,
    "deleted_at": null,
    "user": {
        "id": 1,
        "email": "serafettin@factlist.org",
        "username": "serafettin"
    },
    "links": [
        {
            "link": "https://www.youtube.com/watch?v=gdg6WU_aqWE",
            "id": 3
        }
    ],
    "files": []
}
```

### Modify an evidence

```
PATCH /api/v1/claims/:claim_id/evidences/:evidence_id/
```

Example request:

```
PATCH /api/v1/claims/:claim_id/evidences/:evidence_id/ HTTP/1.1
Host: https://factlist.org
Content-Type: multipart/form-data
Authorization: Token <YOUR-API-TOKEN>

```

Example response:

```
HTTP/1.1 201 OK
Content-Type: application/json; charset=utf-8

{
    "id": 1,
    "text": "Lorem",
    "conclusion": "true",
    "created_at": "2018-03-03T18:05:22Z",
    "user": {
    "id": 1,
    "email": "enis@bob.com",
    "username": "enis"
    },
    "links": [
        {
            "link": "https://github.com/serafettin",
            "id": 1
        }
    ],
    "files": [
        {
            "file": "http://localhost:8001/media/files/claims/2018/03/03/test_files.bin",
            "id": 1
        }
    ]
}
```

### Delete an evidence

```
DELETE /api/v1/claims/:claim_id/evidences/:evidence_id/
```

Example request:

```
DELETE /api/v1/claims/:claim_id/evidences/:evidence_id/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json
Authorization: Token <YOUR-API-TOKEN>
```

Example response:

```
HTTP/1.1 204 NO CONTENT
Content-Type: application/json; charset=utf-8
```
