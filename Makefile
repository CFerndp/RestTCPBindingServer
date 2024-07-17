run:
	uvicorn src.main:app --ssl-keyfile cert/key.pem --ssl-certfile cert/cert.pem