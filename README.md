# Animal Health Analysis

Projeto desenvolvido para o **Hackatoon FMU**.

## Sobre o Projeto

O **Animal Health Analysis** é uma plataforma web inovadora para análise e gestão de exames de saúde animal. Utilizando inteligência artificial (Gemini API), integração com Firebase (Firestore e Storage) e processamento automático de documentos, a solução permite que clínicas veterinárias, tutores e pesquisadores tenham uma visão clara e rápida do estado de saúde dos pets, facilitando diagnósticos, acompanhamento e tomada de decisão.

---

## Benefícios da Aplicação

- **Automação de Diagnóstico:**  
  Analisa exames enviados (PDFs, imagens, textos) e gera automaticamente um resumo explicativo e uma nota de saúde, simulando a avaliação de um veterinário.

- **Centralização de Dados:**  
  Todos os exames, documentos e análises ficam organizados em um só lugar, acessíveis de qualquer dispositivo.

- **Facilidade para Tutores e Clínicas:**  
  Tutores podem acompanhar a saúde de seus pets e clínicas podem otimizar o fluxo de atendimento e análise.

- **Apoio à Decisão:**  
  O sistema sugere quando o animal está saudável, precisa de tratamento ou está em situação de risco, auxiliando o profissional veterinário.

- **Segurança e Escalabilidade:**  
  Utiliza Firebase para autenticação, armazenamento seguro de arquivos e dados, e pode ser facilmente expandido.

---

## Dados Técnicos

- **Frontend:**  
  - HTML5, CSS3 (Bootstrap 5)
  - JavaScript (ES6)
  - Integração com Firebase Auth, Firestore e Storage

- **Backend:**  
  - Python 3 (Flask)
  - Integração com Firebase Admin SDK
  - Processamento de PDFs: `pdfplumber`
  - OCR de imagens: `pytesseract`, `Pillow`
  - Inteligência Artificial: `google-generativeai` (Gemini API)
  - CORS habilitado para integração frontend-backend

- **Infraestrutura:**  
  - Firebase (Firestore, Storage, Authentication)
  - Gemini API (Google AI Studio)
  - Deploy local ou em nuvem (Heroku, Google Cloud, etc.)

- **Funcionalidades principais:**  
  - Cadastro e login de usuários
  - Cadastro de exames com upload de múltiplos arquivos
  - Análise automática dos exames via IA
  - Visualização de exames, documentos e diagnósticos
  - Interface amigável e responsiva

---

## Como executar

1. **Backend:**  
   - Instale as dependências:  
     `pip install flask flask-cors firebase-admin pdfplumber pillow pytesseract google-generativeai requests`
   - Configure o arquivo `credentials.json` do Firebase na pasta backend.
   - Defina a variável de ambiente `GEMINI_API_KEY` com sua chave Gemini.
   - Execute:  
     `python app.py`

2. **Frontend:**  
   - Configure o arquivo `firebaseConfig.js` com suas credenciais Firebase.
   - Abra `frontend/public/index.html` em seu navegador.

---

## Licença

Projeto acadêmico desenvolvido para o Hackatoon FMU.  
Uso livre para fins educacionais e de demonstração.

##########################################################
##########################################################

## Animal Health Analysis Project

This project is designed to analyze animal health by allowing users to upload files and provide descriptions of animals. The application consists of a frontend built with Node.js and Express, and a backend developed in Python using Flask. Data is stored in Firebase.

## Project Structure

```
animal-health-analysis
├── frontend
│   ├── public
│   │   ├── index.html        # HTML structure for the frontend application
│   │   ├── styles.css        # CSS styles for the frontend application
│   │   └── script.js         # JavaScript code for handling form submissions and file uploads
│   ├── src
│   │   └── app.js            # Main entry point for the frontend application
│   ├── package.json          # npm configuration file
│   └── README.md             # Documentation for the frontend part of the project
├── backend
│   ├── app.py                # Main entry point for the backend application
│   ├── requirements.txt      # Python dependencies for the backend application
│   └── README.md             # Documentation for the backend part of the project
└── README.md                 # Overall documentation for the entire project
```

## Frontend

The frontend application allows users to upload files and enter animal descriptions. It is built using HTML, CSS, and JavaScript. The main components include:

- **index.html**: Contains the form for uploading files and entering animal details.
- **styles.css**: Defines the layout and appearance of the frontend.
- **script.js**: Handles form submissions and communicates with the backend.

### Setup Instructions

1. Navigate to the `frontend` directory.
2. Install dependencies using npm:
   ```
   npm install
   ```
3. Start the frontend application:
   ```
   npm start
   ```

## Backend

The backend application is built using Python and Flask. It processes incoming requests, handles file uploads, and saves data to Firebase.

### Setup Instructions

1. Navigate to the `backend` directory.
2. Install dependencies using pip:
   ```
   pip install -r requirements.txt
   ```
3. Start the backend server:
   ```
   python app.py
   ```

## Usage

Once both the frontend and backend are running, users can access the frontend application through their web browser, upload files, and enter animal descriptions. The backend will process the data and store it in Firebase for further analysis.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.