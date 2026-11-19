# Corpus de introduções da UFCG — Atividade 1 (GPT-2 do zero em português)

Introduções de 23.026 trabalhos acadêmicos da UFCG: TCCs, monografias, dissertações, teses, relatórios de estágio e artigos, de 11 centros e 7 campi. O texto foi extraído dos PDFs e limpo para treino de modelo de linguagem.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `train.txt` / `train.parquet` | 20.722 documentos para treino |
| `val.txt` / `val.parquet` | 1.152 documentos para validação |
| `tokenizer_16k/` | BPE em nível de byte, vocabulário de 16.000, treinado só no treino (`tokenizer.json`, `vocab.json`, `merges.txt`) |

Nos `.txt`, os documentos são separados por uma linha contendo só `<|endoftext|>`. Esse é o token especial de fim de documento do tokenizador: com `tokenizer.json`, ele vira um único id.

Os `.parquet` têm o mesmo texto (coluna `texto`) e metadados: `id`, `url`, `ano`, `campus`, `sigla_centro`, `curso`, `tipo_trabalho`, `modalidade_academica`, `titulo`. Os metadados permitem análises por área, por exemplo a perplexidade por centro ou a especialização dos experts do MoE por área.

Há ainda um conjunto de teste, com o mesmo tamanho da validação, que será liberado só depois do prazo final. Registre no README do seu repositório o hash SHA-256 dos checkpoints finais (`sha256sum modelo.pt`) antes do prazo: o BPB de teste só vale para checkpoints com o hash registrado.

## Tamanho

| Partição | Documentos | Palavras | Tokens (BPE 16k) |
|---|---|---|---|
| Treino | 20.722 | 20,0 M | 27,4 M |
| Validação | 1.152 | 1,15 M | 1,57 M |

Uma introdução tem em média cerca de 970 palavras (mediana de 720). Com o tokenizador de 16k, a fertilidade é de cerca de 1,37 token por palavra (1,51 com 8k e 1,29 com 32k).

## Como o corpus foi preparado

1. Junção das introduções com os metadados dos trabalhos, pelo `id`.
2. Limpeza dos artefatos da extração de PDF: tabelas e tags HTML, imagens, fórmulas em LaTeX (as simples viram texto, as demais são removidas), marcadores de nota de rodapé, escapes e títulos de markdown, legendas de figuras e tabelas, números de página soltos. Normalização Unicode (NFKC) e de espaços.
3. Remoção de 625 documentos: menos de 500 caracteres após a limpeza (33), introdução em inglês ou espanhol (162), caractere inválido de extração (23), OCR corrompido, com mais de 1% de caracteres atípicos (286), e introduções duplicadas (121).
4. Partição aleatória estratificada por centro: 90% treino, 5% validação, 5% teste. As proporções de cada centro são as mesmas nas três partições.

O texto ainda tem ruído típico de PDF, como palavras coladas ("fungosMoniliophtera") e títulos de seção numerados ("1.1 Problemática"). Isso faz parte do corpus.

## Uso do tokenizador

```python
from tokenizers import Tokenizer
tok = Tokenizer.from_file("tokenizer_16k/tokenizer.json")
eot = tok.token_to_id("<|endoftext|>")
ids = tok.encode(open("val.txt", encoding="utf-8").read()).ids
```

O tokenizador fornecido é o padrão da turma. Quem treinar o próprio deve usar apenas `train.txt`.
