from app import create_service

app = create_service()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])