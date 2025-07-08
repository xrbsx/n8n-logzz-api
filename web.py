from flask import Flask, request, jsonify
from form_filler import LogzzFormFiller
from browser import Browser

app = Flask(__name__)

@app.route('/preencher', methods=['POST'])
def preencher():
    dados_cliente = request.json
    browser = Browser(headless=True)
    filler = LogzzFormFiller(browser)
    sucesso = filler.fill_stage_one(dados_cliente)
    return jsonify({"sucesso": sucesso})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)