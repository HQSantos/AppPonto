Aplicativo local de registro de ponto desenvolvido em Python utilizando Django para o backend e Tkinter para a interface gráfica.

A aplicação é executada localmente como um programa de computador, sem necessidade de navegador ou acesso à internet.

<h2>Funcionalidades:</h2>
Cadastro e gerenciamento de registros de ponto;<br>
Interface gráfica via Tkinter;<br>
Armazenamento local em banco SQLite;<br>
Compilação para .exe via PyInstaller;<br>

<h2>Requisitos de desenvolvimento:</h2>
Python 3.12+<br>
.venv<br>
pip<br>
Ambiente virtual recomendado<br><br>

Instalação para desenvolvimento:
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/AppPonto.git
cd AppPonto
# Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate 
# Instale as dependências
pip install -r requirements.txt
```
<br>Executar o sistema via console:```python appponto/main.py```<br>
Para compilar o sistema como um executável:```pyinstaller appponto/main.spec```<br>
O executável será gerado em: ```AppPonto/dist/AppPonto.exe``` <br>

Estrutura do projeto:
```
AppPonto/
│
├── appponto/            # Projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── ponto/               # App da lógica de registro
│   ├── models.py
│   └── screens.py       # Interface gráfica (Tkinter)
│
├── main.py              # Ponto de entrada da aplicação
├── main.spec            # Configuração do PyInstaller
├── requirements.txt
└── README.md
```
