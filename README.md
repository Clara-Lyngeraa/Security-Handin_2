# Security7Sem

# Repeat for 3 patients, Alice, Bob and Charlie, and 1 hospital
### To generate certificates
```command
openssl req -new -x509 -days 365 -nodes -out aliceCert.pem -keyout aliceKey.pem -subj "/C=DK/ST=Denmark/O=ITU/CN=localhost/emailAddress=alice@itu.dk" 

openssl req -new -x509 -days 365 -nodes -out bobCert.pem -keyout bobKey.pem -subj "/C=DK/ST=Denmark/O=ITU/CN=localhost/emailAddress=bob@itu.dk"   

openssl req -new -x509 -days 365 -nodes -out charlieCert.pem -keyout charlieKey.pem -subj "/C=DK/ST=Denmark/O=ITU/CN=localhost emailAddress=charlie@itu.dk"

openssl req -new -x509 -days 365 -nodes -out hospitalCert.pem -keyout hospitalKey.pem -subj "/C=DK/ST=Denmark/O=ITU/CN=localhost/emailAddress=hospital@itu.dk"
```

# To run: 
```python 
python3 main.py
```