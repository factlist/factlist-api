## Users

### User Registration

```
POST /api/v1/users/register/
```

Example request:

```
POST /api/v1/users/register/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json

{
    "username": "enis",
    "email": "enis@factlist.org",
    "password": "123456"
}
```

Example response:

```
HTTP/1.1 201 CREATED
Content-Type: application/json; charset=utf-8

{
    "id": "2",
    "username": "enis",
    "email": "enis@factlist.org",
    "token": "example_token"
}
```

### User Authentication

```
POST /api/v1/users/login/
```

Example request:

```
POST /api/v1/users/login/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json

{
    email: "enis@factlist.org",
    password: "123456"
}
```

Example response:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
    "id": "2",
    "username": "enis",
    "email": "enis@factlist.org",
    "token": "example_token"
}
```

### Get another user's profile

```
GET /api/v1/users/:username/
```

Example request:

```
GET /api/v1/users/enis/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json
```

Example response:

```
{
    "id": 7,
    "username": "enis",
    "name": "Enis B. Tuysu",
    "bio": "bio",
    "claim_count": 105,
    "avatar": null
}
```

`NOTE:` For claims of the user, you should make request like this `http://factlist.org/api/v1/claims/?filter=from:username` For the docs head over to: [List of claims](#list-of-claims)


### Change user password

```
POST /api/v1/users/password/
```

Example request:

```
POST /api/v1/users/password/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json
Authorization: Token <YOUR-API-TOKEN>

{
    current_password: "current_password",
    new_password: "new_password"
}
```

## Forgot password routine

When a user forgets his/her password, we need to go through some steps to change the user's password. These steps are in order:

1. User request a password reset email from client with their username or email
2. An email with password reset link referring the user to client is being sent to the user. The email is valid for 24 hours
3. User returns to the client with a password reset key
4. User enters the new password and client will send the key and the new password to the API
5. API verifies the code and password then changes the password

### Create password change key

Example request:

```
POST /api/v1/users/forgot_password/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json

{
    "user_identifier": "enis" // Username or email
}
```

This endpoint will return 200 no matter what to protect users privacy.

After this, an email will be sent to the user, containing a link like this:

`factlist.com/change_password/?key=ABCDE1234567`

You will use the key in the URL to change the user's password

### Change a password with password change key

Example request:

```
POST /api/v1/users/change_password/ HTTP/1.1
Host: https://factlist.org
Content-Type: application/json

{
    "key": "ABCDE123456", // The key in the URL
    "password": "#factlist"
}
```
