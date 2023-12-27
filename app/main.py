from api.availability import API

if __name__ == '__main__':
    # if table does not exist create one

    API.run(debug=True, port=8080)
