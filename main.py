from src.app import app


@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
