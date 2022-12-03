# Name: Blake Mann
# ID: 1832387
# Final project: Sprint 1
import flask
from flask import jsonify, make_response
from flask import request
from sql import create_connection, execute_read_query, execute_query
import creds
import hashlib

# setting up application
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key='somethingsecret'

# creating password and username for authentication
# password 'chosen123' hashed

masterPassword = "e18a9cee6b5399db442788f3c23c3816b28ac045b505d509a96fde9b3b7a7ff0"
masterUsername = 'username'
token = {
    "0"
}

# authentication

# changed authentication method


# created authorized users table with hashed passwords and two users
authorizedUsers=[
    {
        # default user
        'username': 'username',
        'password' : "e18a9cee6b5399db442788f3c23c3816b28ac045b505d509a96fde9b3b7a7ff0",
        # 'role': 'default',
        'token': '0',
        # 'admininfo': None
    },
    {
      # admin user
        'username': 'admin',
        'password' : '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
        # 'role': 'default',
        'token': '1',
        # 'admininfo': None
    }

    ]
# API checks if there are users in the authorized users table and hashes the password
@app.route('/login', methods=['GET','POST'])
def usernamepw():
    username = request.headers['username']
    encoded = request.headers['password'].encode()
    hashedresult = hashlib.sha256(encoded) #hashing
    pw = hashedresult.hexdigest()
    for au in authorizedUsers:
        if au['username'] == username and au['password'] == pw:
            sessiontoken = au['token']
            returninfo = [sessiontoken]
            return jsonify(returninfo)
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
# anything other than the tokens that are in the tables are not accepted.








# ---------------------------------------- airports table API -----------------------------------------------

# GET API
@app.route('/airports', methods=['GET'])
def airports_get_api():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM airports"
    airports = execute_read_query(conn, sql)
    results = []

    for airport in airports:
        results.append(airport)
    return jsonify(results)

# POST API
@app.route('/airports', methods=['POST'])
def airports_post_api():
    request_data = request.get_json()
    newcode = request_data['airportcode']
    newName = request_data['airportname']
    newcountry = request_data['country']
    # creating connection
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    # query to be executed on db
    query = "INSERT INTO airports(airportcode, airportname, country) VALUES ('{}','{}','{}')".format(newcode, newName,newcountry)

    execute_query(conn, query)  # executing the query with the connection

    return 'Add request successful'

# PUT API
@app.route('/airports', methods=['PUT'])
def airports_put_api():
    if 'id' in request.args:  # only if an id is provided as an argument, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: no ID provided!'

    request_data = request.get_json()
    newcode = request_data['airportcode']
    newName = request_data['airportname']
    newcountry = request_data['country']
    # creating connection
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    # query to be executed
    query = """ 
                       UPDATE airports
                       SET  = '%s', airportname = '%s', country = '%s'
                       WHERE id = '%s'""" % (newcode, newName,newcountry, id)
    execute_query(conn, query)  # executing query
    return 'Update request successful'

# DELETE API
@app.route('/airports', methods=['DELETE'])
def airports_delete_api():
    if 'id' in request.args:  # only if an id is provided as an argument, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: no ID provided!'

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    query = "DELETE FROM airports WHERE id = %s" % id
    execute_query(conn, query)

    return 'Delete request successful'


# -------------------------------------Airports CRUD EOF ----------------------------------------------


# ---------------------------------------- planes table API -----------------------------------------------

# GET API
@app.route('/planes', methods=['GET'])
def planes_get_api():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM planes"
    plane = execute_read_query(conn, sql)
    results = []

    for planes in plane:
        results.append(planes)
    return jsonify(results)

# POST API
@app.route('/planes', methods=['POST'])
def planes_post_api():
    request_data = request.get_json()
    newmake = request_data['make']
    newmodel = request_data['model']
    newyr = request_data['year']
    newcap = request_data['capacity']
    # creating connection
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    # query to be executed on db
    query = "INSERT INTO planes(make, model, year, capacity) VALUES ('{}','{}','{}','{}')".format(newmake, newmodel, newyr, newcap)

    execute_query(conn, query)  # executing the query with the connection

    return 'Add request successful'

# PUT API
@app.route('/planes', methods=['PUT'])
def planes_put_api():
    if 'id' in request.args:  # only if an id is provided as an argument, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: no ID provided!'

    request_data = request.get_json()
    newmake = request_data['make']
    newmodel = request_data['model']
    newyr = request_data['year']
    newcap = request_data['capacity']
    # creating connection
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    # query to be executed
    query = """
                       UPDATE planes
                       SET make = '%s', model = '%s', year = '%s', capacity = '%s'
                       WHERE id = '%s'""" % (newmake, newmodel, newyr, newcap, id)
    execute_query(conn, query)  # executing query
    return 'Update request successful'

# DELETE API
@app.route('/planes', methods=['DELETE'])
def planes_delete():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR: no ID provided'

    myCreds = creds.Creds
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    query = "DELETE FROM planes WHERE id = %s" % id
    execute_query(conn, query)

    return 'Delete request successful'
# ---------------------------------------- planes table EOF -----------------------------------------------

# ---------------------------------------- flights table api -----------------------------------------------

@app.route('/flights', methods=['GET'])
def flights_get_api():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM flights"
    plane = execute_read_query(conn, sql)
    results = []

    for planes in plane:
        results.append(planes)
    return jsonify(results)

# POST API
@app.route('/flights', methods=['POST'])
def flights_post_api():
    request_data = request.get_json()
    newplaneid = request_data['planeid']
    newairportidF = request_data['airportfromid']
    newairportidT = request_data['airporttoid']
    newdate = request_data['date']
    # creating connection
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    # query to be executed on db
    query = "INSERT INTO flights (planeid, airportfromid, airporttoid, date) VALUES ({},{},'{}','{}')".format(newplaneid,newairportidF, newairportidT, newdate)

    execute_query(conn, query)  # executing the query with the connection

    return 'Add request successful'

# DELETE API
@app.route('/flights', methods=['DELETE'])
def flights_delete():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR: no ID provided'

    myCreds = creds.Creds
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    query = "DELETE FROM flights WHERE id = %s" % id
    execute_query(conn, query)

    return 'Delete request successful'
# ------------------------------------------------EOF--------------------------------------------

@app.route('/flight_o', methods=['GET'])
def flight_o():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM FinalProject.flights_overview"
    flights = execute_read_query(conn, sql)
    results = []

    for flight in flights:
        results.append(flight)
    return jsonify(results)
app.run()