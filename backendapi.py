# Name: Blake Mann
# ID: 1832387
# Final project: Sprint 1
import flask
from flask import jsonify, make_response
from flask import request, session
from mysql.connector import cursor
from sql import create_connection, execute_read_query, execute_query
import _mysql_connector
import creds
import hashlib
import datetime


# setting up application
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key='somethingsecret'

# creating password and username for authentication
# password 'password' hashed

masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d"
masterUsername = 'username'

# authentication
@app.route('/', methods=['GET'])
def login():
    if request.authorization:
        encoded=request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> i am ready to drop out...jk </h1>'
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

# ---------------------------------------- airports table API -----------------------------------------------

# GET API
@app.route('/airports/view', methods=['GET'])
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



app.run()