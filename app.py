import os
import tempfile
import requests
import pdfplumber
from PIL import Image
import pytesseract
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, storage, firestore
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Caminho absoluto para o arquivo de credenciais
cred_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
cred = credentials.Certificate(cred_path)

options = {
    'storageBucket': 'animal-health-analysis.appspot.com'  # Confirme o nome no console do Firebase
}

try:
    firebase_admin.initialize_app(cred, options)
    print("SDK Admin do Firebase inicializado com sucesso.")
except ValueError as e:
    if "The default Firebase app already exists" in str(e):
        print("Aplicativo padrão do Firebase já inicializado.")
    else:
        logging.error(f"Erro ao inicializar o SDK Admin do Firebase: {e}")
        raise

try:
    bucket = storage.bucket()
    print("Referência do bucket obtida com sucesso.")
except Exception as e:
    logging.error(f"Erro ao obter o bucket de storage: {e}")
    raise

db = firestore.client()

# Configure Gemini (adicione sua chave Gemini como variável de ambiente)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_image(file_path):
    img = Image.open(file_path)
    return pytesseract.image_to_string(img, lang="por")

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'files' not in request.files:
            print("Nenhum arquivo enviado")
            return jsonify({'error': 'No files part'}), 400

        files = request.files.getlist('files')
        name = request.form.get('name')
        animal_id = request.form.get('id')

        if not name or not animal_id:
            print("Nome ou ID não enviados")
            return jsonify({'error': 'Nome e ID são obrigatórios'}), 400

        file_urls = []
        bucket = storage.bucket()
        for file in files:
            if file.filename == '':
                continue
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file)
            file_urls.append(blob.public_url)

        print("Tentando salvar no Firestore:", {'nome': name, 'id': animal_id, 'documentos': file_urls})
        # Salva os dados no Firestore na coleção Exames
        doc_ref = db.collection('Exames').add({
            'nome': name,
            'id': animal_id,
            'documentos': file_urls
        })
        print(f"Documento salvo no Firestore: {doc_ref}")

        return jsonify({'message': 'Arquivos enviados com sucesso', 'file_urls': file_urls}), 200
    except Exception as e:
        import traceback
        print("Erro ao salvar no Firestore:", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/exames', methods=['GET'])
def listar_exames():
    id_filtro = request.args.get('id')
    exames_ref = db.collection('Exames')
    if id_filtro:
        exames = exames_ref.where('id', '==', id_filtro).stream()
    else:
        exames = exames_ref.stream()
    lista = []
    for exame in exames:
        data = exame.to_dict()
        lista.append({
            'nome': data.get('nome'),
            'id': data.get('id'),
            'documentos': data.get('documentos', [])
        })
    return jsonify(lista)

@app.route('/analisar', methods=['GET'])
def analisar_exame():
    animal_id = request.args.get('id')
    exames_ref = db.collection('Exames').where('id', '==', animal_id).stream()
    for exame in exames_ref:
        data = exame.to_dict()
        # Aqui você pode chamar sua lógica de análise, por exemplo, IA ou processamento dos arquivos
        resultado = f"Análise dos arquivos: {', '.join(data.get('documentos', []))}"
        return jsonify({
            'nome': data.get('nome'),
            'id': data.get('id'),
            'resultado': resultado
        })
    return jsonify({'erro': 'Exame não encontrado'}), 404

@app.route('/api/analisar-exame-gemini', methods=['POST'])
def analisar_exame_gemini():
    data = request.json
    exame_id = data.get('exame_id')
    if not exame_id:
        return jsonify({'erro': 'exame_id não informado'}), 400

    exame_ref = db.collection('Exames').document(exame_id)
    exame_doc = exame_ref.get()
    if not exame_doc.exists:
        return jsonify({'erro': 'Exame não encontrado'}), 404

    exame = exame_doc.to_dict()
    arquivos = exame.get('documentos', [])
    texto_extraido = ""

    # Baixa e extrai texto de todos os arquivos
    for url in arquivos:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            r = requests.get(url, stream=True)
            for chunk in r.iter_content(chunk_size=8192):
                tmp.write(chunk)
            tmp.flush()
            if url.lower().endswith('.pdf'):
                texto_extraido += extract_text_from_pdf(tmp.name) + "\n"
            elif any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']):
                texto_extraido += extract_text_from_image(tmp.name) + "\n"
            # Adicione outros tipos se necessário

    if not texto_extraido.strip():
        return jsonify({'erro': 'Não foi possível extrair texto dos arquivos.'}), 400

    # Agente 2: Pesquisa (simulada, Gemini não faz busca real)
    prompt_pesquisa = f"""
Você é um agente de busca. Pesquise na internet informações relevantes sobre os termos e exames abaixo, focando em contexto veterinário:
"{texto_extraido}"
Resuma os principais achados e referências.
"""
    model = genai.GenerativeModel("gemini-pro")
    pesquisa = model.generate_content(prompt_pesquisa).text

    # Agente 3: Resumo e diagnóstico
    prompt_resumo = f"""
Você é um veterinário especialista. Analise o exame abaixo e o resultado da pesquisa na internet.
Exame:
{texto_extraido}

Pesquisa:
{pesquisa}

Gere um resumo explicativo do exame e um diagnóstico veterinário.
"""
    resumo_diag = model.generate_content(prompt_resumo).text

    # Agente 4: Nota de saúde
    prompt_nota = f"""
Com base no diagnóstico abaixo, atribua uma nota de saúde:
- 5: Exame normal, tudo bem.
- 3: Necessita tratamento.
- 1 ou 2: Saúde frágil, dependendo da gravidade.

Diagnóstico:
{resumo_diag}

Responda apenas com a nota (1, 2, 3 ou 5) e uma justificativa curta.
"""
    nota = model.generate_content(prompt_nota).text

    # Salva resultado no Firestore
    exame_ref.update({
        'analise': {
            'texto_extraido': texto_extraido,
            'pesquisa': pesquisa,
            'resumo_diagnostico': resumo_diag,
            'nota': nota
        }
    })

    return jsonify({
        'texto_extraido': texto_extraido,
        'pesquisa': pesquisa,
        'resumo_diagnostico': resumo_diag,
        'nota': nota
    })

if __name__ == '__main__':
    app.run(debug=True)