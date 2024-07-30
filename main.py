from flask import Flask, request, jsonify
from CanalDeStiri import *
app=Flask(__name__)
mysqlconnection=CanalDeStiri()

@app.route('/news', methods=['POST'])
def CreateNews():
    try:
        listaStiri=request.form.to_dict #baza de date e ca un formular la care ne legam, ca sa scoatem info. cerem(request) asta folosind inputuri
        if not listaStiri:
            return jsonify({"eroare":"nu exista lista de stiri"}), 400
        if 'titlu' not in listaStiri or 'nume' not in listaStiri or 'fapta' not in listaStiri:
            return jsonify({"eroare":"trebuie sa avem si nume si fapta si autorul intamplarii"}), 400
        if not listaStiri['titlu'] or not listaStiri['nume'] or not listaStiri['fapta']:
            return jsonify({"eroare":"nu trb sa fie campuri goale!!"})
    
        query="INSERT INTO stiri.stiri(id, titlu, fapta, nume) VALUES (%s, %s, %s, %s)"#evitam nerecunoasterea caracterlor si sql injections
        valori=(listaStiri['id'], listaStiri['titlu'], listaStiri['fapta'], listaStiri['nume'])
        mysqlconnection.insert(query,valori)
        return jsonify({"mesaj":"stire adaugata cu succes"}), 200
    except Exception as e:
        return jsonify({"eroare":"ceva nu a mers cum trb"}), 500



@app.route('/news/<id>', methods=['GET'])
def DisplayNews(id):
    try:
        query="select * from stiri where id =%s"
        rezultatLucru= mysqlconnection.select(query, (id,)) # inregistrarile care sunt numerotate se pun in vb asta
        if not rezultatLucru:
            return jsonify({"eroare":"stirea nu a fost gasita"}), 404
        return jsonify({"mesaj":"operatiune efectuata cu succes"}), 200
    except Exception as e:
        return jsonify({"eroare:": f"ceva nu a mers cum trebuie, {str(e)}"}), 500
    
@app.route('/news/<titlu>', methods=['PUT'])
def UpdateNews(titlu):
    try:
        listaStiri=request.form.to_dict #dictionar mutabil, putem muta siscoate elm 
        updates=[]#aici vom pune valorile noi updatate
        valori=[]#aici vom pune numedict[cheie]
        if 'nume' in listaStiri and listaStiri['nume']:
            updates.append('nume=%s')
            valori.append(listaStiri['nume'])
        if 'fapta' in listaStiri and listaStiri['fapta']:
            updates.append('valoare=%s')#nu precizam aici valoare de introdus !! ci in db 
            valori.append(listaStiri['valori'])
        if not updates:
            return jsonify({"mesaj":"nimic de actualizat"}),400
        query = "UPDATE stiri SET " + ", ".join(updates) + " WHERE titlu = %s"
        valori.append(titlu)
        mysqlconnection.update(query, tuple(valori))
        return jsonify({"mesaj":"modifcarea a fost realizata"}), 200   
    except Exception as e:
        return jsonify({"mesaj":f"ceva nu a mers cum trb, {str(e)}"}), 500

@app.route('/news/<titlu>', methods=['DELETE'])
def DeleteNews(titlu):
    try:
        query="DELETE FROM stiri WHERE titlu = %s"
        mysqlconnection.delete(query, (titlu,) )
        return jsonify({"mesaj":"stegrerea a fost realizata"}), 200
    except Exception as e:
        return jsonify({"msj":f"ceva nu a mers bine, {str(e)}"}), 500

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    
