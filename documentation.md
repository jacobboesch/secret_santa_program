# Table of Contents
1. [Participant Endpoint](#participant_endpoint)
2. [Email Participants Endpoint](#email_participants_endpoint)

## Participant Endpoint <a name="participant_endpoint"> </a>
# `GET /participant`

Description:
Returns a list of participants from the database

## Required headers

* `content-type: application/json`

<details>
    <summary> Click to see Sample Output </summary>
    
```json
{
    "participants": [
        {
            "id": 1,
            "name": "Person1",
            "household": 1,
            "email": "person1@example.com",
            "giftee": null,
            "is_selected": false
        },
        {
            "id": 2,
            "name": "Person2",
            "household": 2,
            "email": "person2@example.com",
            "giftee": null,
            "is_selected": false
        }
    ]
}
```

</details>

# `GET /participant/{id}`

Description:
Gets a specific participant from the database


## Required headers

* `content-type: application/json`


<details>
    <summary> Click to see sample output </summary>
    
```json
{
    "id": 1,
    "name": "Person1",
    "household": 1,
    "email": "person1@example.com",
    "giftee": null,
    "is_selected": false
}
```

</details>

# `POST /participant`

Description:
Creates a new participant in the database


## Required headers

* `content-type: application/json`


<details>
    <summary> Click to see sample input </summary>
    
```json
{
    "name": "Person1",
    "email": "person1@example.com",
    "household": 1
}
```

</details>

STATUS CODE: 201 

<details>
    <summary> Click to see sample output </summary>
    
```json
{
    "success": true,
    "message": "Entry created in table: participants"
}
```
</details>


# `PUT /participant/{id}`

Description:
Updates a participant in the Database


## Required headers

* `content-type: application/json`


<details>
    <summary> Click to see sample input </summary>
    
```json
{
    "name": "Person1",
    "email": "person1@example.com",
    "household": 1
}
```
</details>

STATUS CODE: 200 

<details>
    <summary> Click to see sample output </summary>
    
```json
{
    "success": true,
    "message": "Successfully updated entry in table participants"
}
```
</details>


# `DELETE /participant/{id}`

Description:
Deletes a participant from the database

## Required headers

* `content-type: application/json`

STATUS CODE: 200

<details>
    <summary> Click to see sample output </summary>
    
```json
{
    "success": true,
    "message": "Successfully deleted entry in table participants"
}
```
</details>

## Email Participants Endpoint <a name="email_participants_endpoint"> </a>

# `GET /email_participants`

## Required headers

* `content-type: application/json`

Example:

STATUS CODE: 200

<details>
    <summary> Click to see sample output </summary>
    
```json
{
    "success": true,
    "message": "Success"
}
```
</details>
