import requests

url = "https://api.signnow.com/document/ba311e45f7c3489c9151995b9e6968b22e4fe39c/invite"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer a3a87cf75dd5d859f3519728fd3eedac454f3acc051d2a37036820cfb48d14c9",
    "Content-Type": "application/json"
}
data = {
    "document_id": "ba311e45f7c3489c9151995b9e6968b22e4fe39c",
    "to": "ananbbm23@gmail.com",
    "from": "ananyabesufekad@gmail.com",
    "subject": "You have been invited to sign a document",
    "message": "You have been invited to sign a document",
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())
