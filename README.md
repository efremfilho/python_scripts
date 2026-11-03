# Python Scripts 🐍

Coleção de scripts, utilitários de automação e notebooks para análise de dados, processamento de mídia, IA e produtividade no dia a dia.

---

## 📁 Estrutura do Repositório

```text
python_scripts/
├── split_pdf/                      # Ferramenta avançada para divisão inteligente de PDFs
│   ├── split_pdf                   # Wrapper CLI executável com auto-venv
│   ├── split_pdf.py                # Script em Python com busca binária O(log N)
│   ├── pdf_splitter_by_parts.py    # Divisor legado de PDF por quantidade fixa de partes
│   ├── requirements.txt            # Dependências (pypdf)
│   └── README.md                   # Documentação detalhada da ferramenta
│
├── audio_video/                    # Processamento de áudio, vídeo e transcrição
│   ├── extract_audio_from_video.py # Extração rápida de áudio MP4 para MP3 com moviepy
│   ├── yt_to_audio.ipynb           # Download e extração de áudio do YouTube (Colab)
│   ├── youtube_2_audio_2_transcribe.ipynb # Download + extração + transcrição via Whisper
│   └── audio_from_google_drive_video.ipynb # Extração de áudio de vídeos no Google Drive
│
├── ai_agents/                      # Pipelines de IA, LLMs e Agentes
│   ├── academic_translation_pipeline_v3.ipynb # Tradução acadêmica com chunking de tokens
│   └── test_agentKit.ipynb         # Execução e testes iterativos de agentes
│
├── data_tools/                     # Utilitários de dados, web scraping e finanças
│   ├── discovery_locale_from_csv.py # Detecção de charset/encoding de arquivos CSV
│   ├── get_page_title_from_google_play_packages.py # Web scraping na Google Play Store
│   ├── qr_code_generator.ipynb     # Gerador de QR Codes customizados
│   └── financial_merge.ipynb       # Consolidação e merge de dados no Google Drive
│
└── tutorials/                      # Materiais de estudo e introdução a Python
    ├── intro-to-python.py          # Guia prático de tipos, estruturas e chamadas de API
    └── intro_to_python_notebook.ipynb # Versão interativa em Jupyter Notebook
```

---

## 🛠️ Destaques e Como Usar

### 📄 Divisão Inteligente de PDFs (`split_pdf/`)
Ferramenta de alta performance para cortar arquivos PDF pesados (livros, scans) garantindo que cada parte fique abaixo de um limite específico de tamanho (ex: `< 200 MB`), preservando a qualidade original e metadados.

```bash
# Executar diretamente através do wrapper (cria venv e instala pypdf automaticamente)
./split_pdf/split_pdf "meu_livro.pdf"

# Dividir garantindo limite decimal estrito (< 195 MB) em modo balanceado
./split_pdf/split_pdf -u MB -s 195 --balance "meu_livro.pdf"

# Apenas simular cortes sem gravar arquivos
./split_pdf/split_pdf --dry-run "meu_livro.pdf"
```

Consulte a [documentação detalhada do split_pdf](split_pdf/README.md) para todos os parâmetros.

---

### 🎙️ Processamento de Áudio e Vídeo (`audio_video/`)
- **`extract_audio_from_video.py`**: Converte arquivos de vídeo locais (`.mp4`) para áudio (`.mp3`) com controle de bitrate via `moviepy`.
- **`youtube_2_audio_2_transcribe.ipynb`**: Pipeline de automação para baixar vídeos do YouTube, separar a faixa de áudio e transcrever o conteúdo com IA.
- **`audio_from_google_drive_video.ipynb`**: Integração direta com Google Drive no Google Colab para extrair áudios sem precisar baixar vídeos pesados para a máquina local.

---

### 🤖 IA e Agentes (`ai_agents/`)
- **`academic_translation_pipeline_v3.ipynb`**: Tradução de documentos longos (DOCX/HTML) mantendo formatação e consistência terminológica, utilizando chunking inteligente baseado em contagem de tokens (`tiktoken`) e chamadas de API com modelos OpenAI.
- **`test_agentKit.ipynb`**: Notebook para prototipagem e execução dinâmica de frameworks de agentes com interface iterativa de aprovação/rejeição.

---

### 📊 Ferramentas de Dados (`data_tools/`)
- **`discovery_locale_from_csv.py`**: Identifica rapidamente o encoding (UTF-8, ISO-8859-1, Windows-1252, etc.) de arquivos CSV corrompidos ou mal formatados usando `chardet`.
- **`get_page_title_from_google_play_packages.py`**: Realiza web scraping na Google Play Store para extrair metadados (nome do app, desenvolvedor e categoria) a partir de uma lista de package IDs.
- **`qr_code_generator.ipynb`**: Criação de QR Codes estilizados para links e textos.
- **`financial_merge.ipynb`**: Autenticação com PyDrive e fusão de dados financeiros.

---

## 🔒 Boas Práticas e Segurança

- **Credenciais e Chaves de API**: Nunca commite chaves de API, senhas ou tokens de autenticação diretamente no código. Utilize variáveis de ambiente (`os.getenv`), o gerenciador de secrets do Google Colab (`userdata.get`) ou arquivos `.env`.
- **Arquivos Ignorados**: O repositório conta com um [`.gitignore`](.gitignore) configurado para ignorar automaticamente ambientes virtuais (`.venv`, `venv`), caches do Python (`__pycache__`), checkpoints do Jupyter (`.ipynb_checkpoints`), saídas pesadas de mídia (`*.mp3`, `*.mp4`, `*.pdf`) e arquivos de segredos.
