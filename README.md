Aplicativo local de registro de ponto desenvolvido em Python utilizando Django para o backend e Tkinter para a interface gráfica.

A aplicação é executada localmente como um programa de computador, sem necessidade de navegador ou acesso à internet.

Funcionalidades
Cadastro e gerenciamento de registros de ponto

Interface gráfica via Tkinter
Armazenamento local em banco SQLite
Compilação para .exe via PyInstaller

Requisitos de desenvolvimento:
Python 3.12+
.venv
pip
Ambiente virtual recomendado

Instalação para desenvolvimento:
# Clone o repositório
git clone https://github.com/seu-usuario/AppPonto.git
cd AppPonto
# Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate 
# Instale as dependências
pip install -r requirements.txt

# Execute o sistema
python appponto/main.py
Gerar executável (.exe)
Para compilar o sistema como um executável:
pyinstaller appponto/main.spec
O executável será gerado em:
AppPonto/dist/AppPonto.exe

Estrutura do projeto:
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
