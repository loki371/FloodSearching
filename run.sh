sudo ufw allow 8080
sudo ufw allow 8000
uvicorn main:app --reload
