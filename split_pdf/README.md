# Split PDF - Divisor Inteligente de Documentos PDF por Tamanho

Script utilitário em Python para dividir documentos PDF em partes menores que um limite de tamanho especificado (por padrão < 200 MB), ideal para contornar limites de upload de LLMs, portais governamentais, e-mail ou nuvem.

## Características

- **Algoritmo de Busca Binária $O(\log N)$**: Determina os pontos exatos de corte em segundos, mesmo em livros ou documentos com centenas ou milhares de páginas.
- **Suporte a Unidades Binárias e Decimais**:
  - `MiB` (binário: $1024^2$ bytes = 1.048.576 bytes)
  - `MB` (decimal: $1000^2$ bytes = 1.000.000 bytes)
- **Dois Modos de Divisão**:
  - `greedy` (padrão): Preenche cada arquivo o máximo possível até o limite.
  - `balanced` (`--balance`): Divide o documento equilibrando a quantidade de páginas entre o menor número de partes necessárias.
- **Segurança e Preservação**:
  - Preserva metadados originais do documento (Título, Autor, etc.).
  - Modo `--dry-run` para simular os cortes antes de salvar em disco.
  - Alerta caso uma única página exceda o limite total configurado.
- **Wrapper Automático**:
  - Executável `./split_pdf` que cria o ambiente virtual `.venv` e instala a biblioteca `pypdf` automaticamente na primeira execução.

---

## Como Usar

### 1. Via Wrapper Bash (Recomendado)

O script `./split_pdf` já configura automaticamente o ambiente virtual local:

```bash
# Divisão padrão (limite de 195 MiB, modo ganancioso)
./split_pdf "meu_livro.pdf"

# Garantir limite estrito decimal (< 195 MB decimal) em modo balanceado
./split_pdf -u MB -s 195 --balance "meu_livro.pdf"

# Dividir em exatamente 2 partes (< 199 MiB binário)
./split_pdf -s 199 "meu_livro.pdf"

# Apenas simular sem gravar nada em disco (--dry-run)
./split_pdf --dry-run "meu_livro.pdf"

# Definir pasta de saída customizada
./split_pdf -o /caminho/para/pasta "meu_livro.pdf"
```

### 2. Via Python Diretamente

```bash
python3 split_pdf.py [argumentos]
```
*(O próprio script detecta o `.venv` local e se re-executa nele automaticamente se necessário).*

---

## Parâmetros Disponíveis

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `input` | *(obrigatório)* | Caminho do arquivo PDF a ser dividido. |
| `-s`, `--max-size` | `195.0` | Tamanho máximo permitido para cada parte. |
| `-u`, `--unit` | `MiB` | Unidade do limite: `MiB` ($1024^2$ bytes) ou `MB` ($1000^2$ bytes). |
| `-m`, `--mode` | `greedy` | Estratégia de corte: `greedy` ou `balanced`. |
| `--balance` | `False` | Atalho para usar `--mode balanced`. |
| `-o`, `--output-dir` | Diretório do input | Pasta onde os arquivos divididos serão salvos. |
| `--prefix` | Nome do PDF | Prefixo dos arquivos gerados. |
| `--dry-run` | `False` | Apenas simula e exibe a tabela de cortes sem salvar em disco. |
| `-q`, `--quiet` | `False` | Exibe apenas avisos essenciais e o resumo final. |
