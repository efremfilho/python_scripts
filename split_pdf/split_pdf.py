#!/usr/bin/env python3
"""
split_pdf.py - Utilitário genérico e de alta performance para dividir arquivos PDF por tamanho máximo.

Características:
- Busca binária rápida O(log N) para determinar os pontos ideais de corte.
- Modos 'greedy' (preenche até o limite máximo) e 'balanced' (distribui páginas igualmente).
- Suporte a unidades binárias (MiB = 1024^2) e decimais (MB = 1000^2).
- Preservação de metadados do documento original.
- Modo de simulação (--dry-run).
- Auto-detecção de ambiente virtual (.venv) local.
"""

import argparse
import io
import math
import os
import sys
import time
from pathlib import Path

# Auto-reexecução com venv local se pypdf não estiver disponível no Python atual
try:
    import pypdf
except ImportError:
    script_dir = Path(__file__).resolve().parent
    venv_python = script_dir / ".venv" / "bin" / "python3"
    if venv_python.exists() and sys.executable != str(venv_python):
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)
    else:
        sys.stderr.write(
            "ERRO: A biblioteca 'pypdf' não está instalada no ambiente Python atual.\n"
            "Instale com:\n"
            "    pip install pypdf\n"
            "Ou execute através do wrapper:\n"
            f"    {script_dir}/split_pdf\n"
        )
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Divide arquivos PDF em partes menores que um tamanho especificado (em MB/MiB)."
    )
    parser.add_argument(
        "input",
        type=str,
        help="Caminho do arquivo PDF de entrada.",
    )
    parser.add_argument(
        "-s", "--max-size",
        type=float,
        default=195.0,
        help="Tamanho máximo de cada parte (padrão: 195.0).",
    )
    parser.add_argument(
        "-u", "--unit",
        choices=["MiB", "MB"],
        default="MiB",
        help="Unidade de medida: 'MiB' (binário: 1024^2 bytes) ou 'MB' (decimal: 1000^2 bytes). Padrão: MiB.",
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["greedy", "balanced"],
        default="greedy",
        help="Modo de divisão: 'greedy' (preenche ao máximo cada parte) ou 'balanced' (distribui páginas equilibradamente). Padrão: greedy.",
    )
    parser.add_argument(
        "--balance",
        action="store_true",
        help="Atalho para '--mode balanced'.",
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=None,
        help="Diretório de saída para os arquivos divididos (padrão: mesmo diretório do arquivo de entrada).",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=None,
        help="Prefixo customizado para os arquivos gerados (padrão: nome original do arquivo).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas simula a divisão e exibe as partes planejadas sem gravar nenhum arquivo em disco.",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Modo silencioso (exibe apenas avisos de erro e o resumo final).",
    )

    return parser.parse_args()


def format_size(bytes_val: int) -> str:
    """Retorna o tamanho formatado em MiB e MB."""
    mib = bytes_val / (1024 * 1024)
    mb = bytes_val / (1000 * 1000)
    return f"{mib:6.2f} MiB ({mb:6.2f} MB)"


def measure_pages_size(reader: pypdf.PdfReader, start: int, end: int, metadata=None) -> int:
    """Gera um PDF em memória com as páginas do intervalo [start, end] (inclusivo) e retorna seu tamanho em bytes."""
    writer = pypdf.PdfWriter()
    for i in range(start, end + 1):
        writer.add_page(reader.pages[i])
    if metadata:
        try:
            writer.add_metadata(metadata)
        except Exception:
            pass
    buf = io.BytesIO()
    writer.write(buf)
    return buf.tell()


def compute_greedy_chunks(reader: pypdf.PdfReader, max_bytes: int, quiet: bool = False) -> list[tuple[int, int, int]]:
    """
    Calcula cortes de forma gananciosa (greedy) usando busca binária O(log N) para cada bloco.
    Retorna lista de tuplas: (start_page_idx, end_page_idx, estimated_bytes).
    """
    total_pages = len(reader.pages)
    chunks = []
    start = 0

    while start < total_pages:
        # 1. Verifica se todas as páginas restantes já cabem no limite
        rem_size = measure_pages_size(reader, start, total_pages - 1)
        if rem_size <= max_bytes:
            chunks.append((start, total_pages - 1, rem_size))
            break

        # 2. Verifica se a página individual já excede o limite
        single_page_size = measure_pages_size(reader, start, start)
        if single_page_size > max_bytes:
            if not quiet:
                print(
                    f"  [AVISO] Página individual {start + 1} possui {format_size(single_page_size)}, "
                    f"que já excede o limite configurado de {format_size(max_bytes)}. Ela será isolada em uma parte própria."
                )
            chunks.append((start, start, single_page_size))
            start += 1
            continue

        # 3. Busca binária para encontrar a maior página final válida
        low = start
        high = total_pages - 2
        best = start
        best_size = single_page_size

        while low <= high:
            mid = (low + high) // 2
            size = measure_pages_size(reader, start, mid)
            if size <= max_bytes:
                best = mid
                best_size = size
                low = mid + 1
            else:
                high = mid - 1

        chunks.append((start, best, best_size))
        start = best + 1

    return chunks


def compute_balanced_chunks(reader: pypdf.PdfReader, max_bytes: int, quiet: bool = False) -> list[tuple[int, int, int]]:
    """
    Calcula cortes buscando distribuir as páginas de maneira homogênea entre o menor número de partes necessárias.
    """
    total_pages = len(reader.pages)
    total_bytes = measure_pages_size(reader, 0, total_pages - 1)

    if total_bytes <= max_bytes:
        return [(0, total_pages - 1, total_bytes)]

    k_parts = math.ceil(total_bytes / max_bytes)
    target_bytes = total_bytes / k_parts

    chunks = []
    start = 0

    for part_idx in range(1, k_parts + 1):
        if part_idx == k_parts:
            # Última parte pega o restante
            last_size = measure_pages_size(reader, start, total_pages - 1)
            # Se por ventura a última parte exceder (por variação de densidade de páginas),
            # recorre à divisão gananciosa do restante
            if last_size > max_bytes:
                rem_chunks = compute_greedy_chunks(reader, max_bytes, quiet=quiet)
                # Filtra apenas a partir de start
                chunks = [c for c in chunks if c[1] < start]
                # Re-executa greedy total para evitar partições inconsistentes
                return compute_greedy_chunks(reader, max_bytes, quiet=quiet)
            chunks.append((start, total_pages - 1, last_size))
            break

        # Procura a página de corte mais próxima de target_bytes sem ultrapassar max_bytes
        low = start
        high = total_pages - (k_parts - part_idx) - 1
        best = start
        best_size = measure_pages_size(reader, start, start)

        while low <= high:
            mid = (low + high) // 2
            size = measure_pages_size(reader, start, mid)
            if size <= target_bytes:
                best = mid
                best_size = size
                low = mid + 1
            elif size <= max_bytes and (best_size < target_bytes * 0.9):
                best = mid
                best_size = size
                low = mid + 1
            else:
                high = mid - 1

        chunks.append((start, best, best_size))
        start = best + 1

    return chunks


def write_chunk_to_disk(
    reader: pypdf.PdfReader,
    start: int,
    end: int,
    output_path: Path,
    metadata=None,
) -> int:
    """Grava as páginas no arquivo de saída e retorna o tamanho final em bytes."""
    writer = pypdf.PdfWriter()
    for i in range(start, end + 1):
        writer.add_page(reader.pages[i])
    if metadata:
        try:
            writer.add_metadata(metadata)
        except Exception:
            pass

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path.stat().st_size


def main() -> None:
    args = parse_arguments()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        sys.exit(f"ERRO: Arquivo de entrada não encontrado: {input_path}")
    if not input_path.is_file():
        sys.exit(f"ERRO: O caminho informado não é um arquivo: {input_path}")

    # Determina o valor em bytes do limite
    multiplier = 1024 * 1024 if args.unit == "MiB" else 1000 * 1000
    max_bytes = int(args.max_size * multiplier)

    # Modo de operação
    mode = "balanced" if args.balance else args.mode

    # Diretório de saída
    output_dir = Path(args.output_dir).resolve() if args.output_dir else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    prefix = args.prefix if args.prefix else input_path.stem

    if not args.quiet:
        print("=" * 72)
        print(" SPLIT PDF - Divisor Inteligente de Documentos PDF")
        print("=" * 72)
        print(f" Arquivo de entrada : {input_path.name}")
        print(f" Caminho completo   : {input_path}")
        print(f" Limite máximo      : {args.max_size:.2f} {args.unit} ({format_size(max_bytes)})")
        print(f" Estratégia         : {mode.upper()}")
        print(f" Pasta de saída     : {output_dir}")
        if args.dry_run:
            print(" MODO SIMULAÇÃO     : Ativado (--dry-run: nenhum arquivo será salvo)")
        print("-" * 72)

    # Leitura do documento
    t0 = time.time()
    try:
        reader = pypdf.PdfReader(str(input_path))
    except Exception as e:
        sys.exit(f"ERRO: Falha ao abrir o arquivo PDF: {e}")

    total_pages = len(reader.pages)
    original_size = input_path.stat().st_size

    if not args.quiet:
        print(f" Total de páginas   : {total_pages}")
        print(f" Tamanho original   : {format_size(original_size)}")
        print("-" * 72)

    if original_size <= max_bytes:
        print(f"[OK] O arquivo original ({format_size(original_size)}) já é menor ou igual ao limite de {format_size(max_bytes)}.")
        print("Nenhuma divisão é necessária.")
        return

    # Extrai metadados básicos
    metadata = None
    try:
        if reader.metadata:
            metadata = {k: v for k, v in reader.metadata.items() if v is not None}
    except Exception:
        pass

    if not args.quiet:
        print(f"Calculando pontos de corte ideais ({mode})...")

    calc_start = time.time()
    if mode == "balanced":
        chunks = compute_balanced_chunks(reader, max_bytes, quiet=args.quiet)
    else:
        chunks = compute_greedy_chunks(reader, max_bytes, quiet=args.quiet)
    calc_time = time.time() - calc_start

    num_parts = len(chunks)
    digits = max(2, len(str(num_parts)))

    if not args.quiet:
        print(f"Cálculo concluído em {calc_time:.2f}s! O arquivo será dividido em {num_parts} partes.")
        print("-" * 72)

    total_written = 0
    generated_files = []

    for idx, (p_start, p_end, est_size) in enumerate(chunks, 1):
        num_pages_chunk = p_end - p_start + 1
        part_name = f"{prefix}_parte_{idx:0{digits}d}_pags_{p_start + 1}-{p_end + 1}.pdf"
        out_file = output_dir / part_name

        if args.dry_run:
            actual_size = est_size
            status_msg = "[SIMULADO]"
        else:
            actual_size = write_chunk_to_disk(reader, p_start, p_end, out_file, metadata=metadata)
            status_msg = "[GERADO]"

        total_written += actual_size
        generated_files.append((out_file, p_start + 1, p_end + 1, num_pages_chunk, actual_size))

        if not args.quiet:
            print(
                f" {status_msg} Parte {idx:0{digits}d}/{num_parts:0{digits}d}: "
                f"páginas {p_start + 1:4d} a {p_end + 1:4d} ({num_pages_chunk:3d} págs) -> {format_size(actual_size)}"
            )
            print(f"          -> {out_file.name}")

    total_time = time.time() - t0

    print("=" * 72)
    print(" RESUMO DA EXECUÇÃO")
    print("=" * 72)
    print(f" Partes geradas     : {num_parts}")
    print(f" Páginas processadas: {total_pages}")
    print(f" Tamanho total ger. : {format_size(total_written)}")
    print(f" Tempo total        : {total_time:.2f}s")
    print(f" Pasta de destino   : {output_dir}")
    print("=" * 72)


if __name__ == "__main__":
    main()
