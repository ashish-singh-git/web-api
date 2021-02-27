import flask
from flask import request, jsonify, redirect, url_for
from datetime import datetime
import sqlite3
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>conversation channel</h1>
<p>A prototype API for conversation channel</p>'''


@app.route('/conversations/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('conversations.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    sql = ''' select * from messages'''
    conversations = cur.execute(sql).fetchall()
    return jsonify(conversations)


@app.route('/conversations', methods=['GET'])
def api_id():
    if 'conversation_id' in request.args:
        id = int(request.args['conversation_id'])

        conn = sqlite3.connect('conversations.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        sql = f"select * from messages where conversation_id = {id}"
        conversations = cur.execute(sql).fetchall()
        results = []
        result_dict = {}
        result_dict.update({"id": id})
        for conversation in conversations:
            results.append({'sender': conversation['sender'], 'message': conversation['message'],
                            'created': conversation['created']})
        result_dict.update({"message": results})
        return result_dict
    else:
        return '''<h1>conversation channel</h1>
        <p>Error: No conversation_id field provided. Please specify conversation_id.</p>'''


@app.route('/messages', methods=['POST'])
def create_messages():
    conn = sqlite3.connect('conversations.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
	    conversation_id integer,
	    sender text,
	    message text,
	    created text
        );''')
    insert_sql = ''' INSERT INTO messages(conversation_id,sender,message,created)
              VALUES(?,?,?,?) '''
    current_timestamp = datetime.utcnow().isoformat()[:-3] + 'Z'
    new_message = request.get_json()
    data = (new_message['conversation_id'], new_message['sender'], new_message['message'], current_timestamp)
    cur.execute(insert_sql, data)
    conn.commit()
    return jsonify({'new_message': new_message})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
