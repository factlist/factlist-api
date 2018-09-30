## Perspective

### Create a topic

```Authentication token is required in this endpoint```

```
POST /api/v1/topics/
```

Example request:

```
POST /api/v1/topics/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json
Authorization: Token <YOUR-API-TOKEN>

{
    "topic": "American and Saudi role in Yemeni Civil War",
    "links": ["https://factlist.com"]
}
```

`links` are not required.

Example response:

```
HTTP/1.1 201 CREATED
Content-Type: application/json; charset=utf-8

{
    "id": 4,
    "title": "American and Saudi role in Yemeni Civil War",
    "user": {
        "id": 7,
        "username": "enis",
        "name": "Enis B. Tuysuz",
        "avatar": null
    },
    "created_at": "2018-09-28T19:24:20.809906Z",
    "updated_at": null,
    "links": []
}
```

### Get list of topics

```
GET /api/v1/topics/
```

Example request:

```
GET /api/v1/topics/ HTTP/1.1
Host: https://factlist.org
```

Example response:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "title": "American and Saudi role in Yemeni Civil War",
            "user": {
                "id": 7,
                "username": "enis",
                "name": "Enis B. Tuysuz",
                "avatar": null
            },
            "created_at": "2018-09-28T19:24:20.809906Z",
            "updated_at": null,
            "links": []
        },
        ...
    ]
}
```

### Get a topic

```
GET /api/v1/topics/:topic_id/
```

Example request:

```
GET /api/v1/topics/:topic_id/ HTTP/1.1
Host: https://factlist.org
```

Example response:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
    "id": 4,
    "title": "American and Saudi role in Yemeni Civil War",
    "user": {
        "id": 7,
        "username": "enis",
        "name": "Enis B. Tuysuz",
        "avatar": null
    },
    "created_at": "2018-09-28T19:24:20.809906Z",
    "updated_at": null,
    "links": []
}
```

### Update a topic

```Authentication token is required in this endpoint```

```
PATCH /api/v1/topics/:topic_id/
```

Example request:

```
PATCH /api/v1/topics/:topic_id/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json
Authorization: Token <YOUR-API-TOKEN>

{
    "topic": "American and Saudi role in Yemeni Civil War",
    "links": ["https://factlist.com"]
}
```

Example response:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
    "id": 4,
    "title": "American and Saudi role in Yemeni Civil War",
    "user": {
        "id": 7,
        "username": "enis",
        "name": "Enis B. Tuysu",
        "avatar": null
    },
    "created_at": "2018-09-28T19:24:20.809906Z",
    "updated_at": null,
    "links": []
}
```

### Delete a topic

```Authentication token is required in this endpoint```

```
DELETE /api/v1/topics/:topic_id/
```

Example request:

```
DELETE /api/v1/topics/:topic_id/ HTTP/1.1
Host: https://factlist.org
Authorization: Token <YOUR-API-TOKEN>
```

Example response:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
```

### Post a link to a topic

```Authentication token is required in this endpoint```

```
POST /api/v1/topics/:topic_id/links/
```

Example request:

```
POST /api/v1/topics/:topic_id/links/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json
Authorization: Token <YOUR-API-TOKEN>

{
	"link": "https://factlist.org"
}
```

Example response:

```
HTTP/1.1 201 CREATED
Content-Type: application/json; charset=utf-8

{
    "id": 916,
    "link": "https://factlist.org",
    "created_at": "2018-09-28T19:35:43.928761Z",
    "updated_at": null,
    "tags": [],
    "embed": null
}
```

### Get list of links

```
GET /api/v1/topics/:topic_id/links/
```

Example request:

```
GET /api/v1/topics/:topic_id/links/ HTTP/1.1
Host: https://factlist.org
```

Example response:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 916,
            "link": "https://factlist.org",
            "created_at": "2018-09-28T19:35:43.928761Z",
            "updated_at": null,
            "tags": [],
            "embed": null
        }
    ]
}
```

### Tag a link

```Authentication token is required in this endpoint```

```
POST /api/v1/topics/:topic_id/links/:link_id/tags/
```

Example request:

```
POST /api/v1/topics/:topic_id/links/:link_id/tags/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json
Authorization: Token <YOUR-API-TOKEN>

{
	"title": "Yes"
}
```

Example response:

```
HTTP/1.1 201 CREATED
Content-Type: application/json; charset=utf-8

{
    "id": 5,
    "title": "Yes",
    "created_at": "2018-09-28T19:42:58.866056Z",
    "updated_at": null
}
```

### Get list of tags of links under a topic

```
GET /api/v1/topics/:topic_id/tags/
```

Example request:

```
GET /api/v1/topics/:topic_id/tags/ HTTP/1.1
Host: https://factlist.org
```

Example response:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "title": "Yes",
            "created_at": "2018-09-28T19:42:58.866056Z",
            "updated_at": null
        }
    ]
}
```

### Remove tag from a link

```Authentication token is required in this endpoint```

```
DELETE /api/v1/topics/:topic_id/links/:link_id/tags/:tag_id
```

Example request:

```
DELETE /api/v1/topics/:topic_id/links/:link_id/tags/:tag_id HTTP/1.1
Host: https://factlist.org
Authorization: Token <YOUR-API-TOKEN>
```

Example response:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
```

`NOTE:` Only the user that sent the link can remove tags
