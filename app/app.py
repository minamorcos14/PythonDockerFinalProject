import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'taxiData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Taxi Fare Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTaxiImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, taxis=result)


@app.route('/view/<int:taxi_id>', methods=['GET'])
def record_view(taxi_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTaxiImport WHERE id=%s', taxi_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', taxi=result[0])

@app.route('/edit/<int:taxi_id>', methods=['GET'])
def form_edit_get(taxi_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTaxiImport WHERE id=%s', taxi_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', taxi=result[0])


@app.route('/edit/<int:taxi_id>', methods=['POST'])
def form_update_post(taxi_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('distance_miles'), request.form.get('fare'), taxi_id)
    sql_update_query = """UPDATE tblTaxiImport t SET t.distance_miles = %s, t.fare = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/taxis/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Taxi Fare Form')


@app.route('/taxis/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('distance_miles'), request.form.get('fare'))
    sql_insert_query = """INSERT INTO tblTaxiImport (distance_miles,fare) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:taxi_id>', methods=['POST'])
def form_delete_post(taxi_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblTaxiImport WHERE id = %s """
    cursor.execute(sql_delete_query,taxi_id)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/api/v1/taxis', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTaxiImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/taxis/<int:taxi_id>', methods=['GET'])
def api_retrieve(taxi_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTaxiImport WHERE id=%s', taxi_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/taxis/', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['Distance'], content['Fare'])
    sql_insert_query = """INSERT INTO tblTaxiImport (distance_miles, fare) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')


@app.route('/api/v1/taxis/<int:taxi_id>', methods=['PUT'])
def api_edit(taxi_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Distance (Miles)'], content['Fare'] , taxi_id)
    sql_update_query = """UPDATE tblTaxiImport t SET t.distance_miles = %s, t.fare = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/taxis/<int:taxi_id>', methods=['DELETE'])
def api_delete(taxi_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblTaxiImport WHERE id=%s """
    cursor.execute(sql_delete_query, taxi_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)