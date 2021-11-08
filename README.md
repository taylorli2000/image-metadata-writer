# image-metadata-writer

Writes metadata to uploaded images and stores on local system.</br>
Built using Python + Flask, SQLite, and React

## Initial Setup

In the server folder, install dependencies:

```shell
cd server
py -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```

You must set up the .flaskenv file:

FLASK_APP=app<br/>
FLASK_ENV=development<br/>

In the client folder, install dependencies:

```shell
cd client
npm install
```

### Running the application locally

In one terminal, start the back end:

```shell
cd server
flask run
```

In another terminal, start the front end:

```shell
cd client
npm start
```
