from flask import request, jsonify, abort
from server import app, mysql


# Info del perfil de un usuario
# User profile information
@app.route('/user/<nick>', methods=['GET'])
def user_info(nick):
    try:
        cur = mysql.connection.cursor()
        cur.execute("select * from usuarios inner join userinfo on usuarios.id=userinfo.id where usuarios.nick='"+nick+"' LIMIT 1")
        resultado = cur.fetchall()
        cur.close()

        return jsonify({ 'id': resultado[0][0], 'nick': resultado[0][1], 'url_foto':'', 'bio':'', 'pais':'', 'fecha_registro':resultado[0][6].strftime("%Y/%m/%d"), 'fecha_ultima_conexion':resultado[0][7].strftime("%Y/%m/%d %H:%M:%S") })
    except:
        abort(404)

# Elimina el usuario de la base de datos
# Get rid of specified user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        cur = mysql.connection.cursor()
        res = cur.execute("delete from usuarios where id='"+id+"'")
        res2 = cur.execute("delete from userinfo where id='"+id+"'")
        cur.execute("delete from usuarios_proyectos where id_usuario='"+id+"'")
        if res and res2:
            mysql.connection.commit()
            return jsonify({ 'msg':'User successfully deleted' })
        else: return jsonify({ 'msg':'User doesnt exist' }), 404
    except:
        abort(404)


# Proyectos de un usuario (en los que participa o ha participado)
# Projects of specified user (in which he is or was part)
@app.route('/user/proyects/<nick>', methods=['GET'])
def user_proyects(nick):
    try:
        cur = mysql.connection.cursor()
        cur.execute("select * from usuarios inner join usuarios_proyectos on usuarios.id=usuarios_proyectos.id_usuario where usuarios.nick='"+nick+"'")
        resultado = cur.fetchall()
        cur.close()

        print(resultado) # DEBUG

        json="{ 'id_proyect': '', 'id_usuario': '', 'fecha_entrada':'', 'fecha_salida':'' }"
        return jsonify(json)
    except:
        abort(404)
