# Fase 3. Divisão em treino, validação e teste

**Código:** `src/split/`
**Registro da divisão:** `configs/split.csv` (imagem, origem, grupo e conjunto de cada uma das 845 imagens)

## Resumo

A divisão foi feita **por grupo**, e não imagem a imagem. Embeddings de uma rede pré-treinada mostraram que a base tem imagens da mesma cena em mais de um arquivo: a mesma torre de ângulos parecidos, entre as normais, e a mesma montagem ou o mesmo recorte de isolador reaproveitado, entre as imagens com defeito. Imagens do mesmo grupo ficam sempre no mesmo conjunto, e cada conjunto mantém a mesma proporção de imagens com defeito.

| Conjunto | Imagens | Com defeito | Normais | % com defeito | Caixas de isolador | Caixas de defeito |
|---|---|---|---|---|---|---|
| Treino | 591 (70%) | 174 | 417 | 29,4% | 932 | 174 |
| Validação | 127 (15%) | 37 | 90 | 29,1% | 196 | 37 |
| Teste | 127 (15%) | 37 | 90 | 29,1% | 190 | 37 |
| **Total** | **845** | **248** | **597** | **29,3%** | **1.318** | **248** |

## Como os grupos foram formados

1. **Embeddings:** cada imagem passou por uma ResNet18 pré-treinada no ImageNet, sem a última camada, gerando um vetor de 512 números que resume o conteúdo.
2. **Similaridade de cosseno** entre todos os pares de imagens.
3. **Calibração:** a mediana entre pares quaisquer é 0,777 e o percentil 99 é 0,884. Um par acima de 0,90 está no topo de 1% da base.
4. **Inspeção visual** de pares em níveis diferentes: a partir de ~0,94 aparecem a mesma cena ou a mesma montagem; em 0,90 já são cenas diferentes.
5. **Grupos por ligação:** imagens com similaridade ≥ limiar ficam no mesmo grupo, e grupos que se tocam se unem (*union-find*).

| Limiar | Grupos | Maior grupo | Decisão |
|---|---|---|---|
| 0,90 | 452 | 333 imagens | Rejeitado: o encadeamento junta 40% da base num grupo só |
| **0,92** | **723** | **40 imagens** | **Escolhido** |
| 0,94 | 826 | 3 imagens | Rejeitado: deixa escapar pares da mesma cena entre 0,92 e 0,94 |

Com 0,92, nenhum grupo mistura as duas origens.

## Achados

| # | Achado | Tratamento |
|---|---|---|
| 14 | Imagens da mesma cena dentro de cada origem (até 0,97 de similaridade); nenhuma cena compartilhada entre as origens | Divisão por grupo |
| 15 | O maior grupo (40 imagens normais) junta fotos de **composição** parecida, não da mesma cena: excesso de agrupamento. O segundo maior (10 imagens com defeito) reúne montagens com **o mesmo recorte de isolador** | Excesso de agrupamento só custa equilíbrio, não honestidade: aceito. Grupos com mais de 5 imagens vão inteiros para o treino |

## Regra de divisão

Para cada origem separadamente (estratificação):

1. Grupos com mais de 5 imagens vão para o treino.
2. Os demais grupos são embaralhados com semente 42 e alocados: primeiro o teste até 15% das imagens, depois a validação até 15%, o resto no treino.
3. O script verifica com `assert` que nenhum grupo aparece em dois conjuntos e que nenhuma imagem está repetida. Se a regra for alterada e quebrar isso, ele para com erro.

## Limitação: o teste é pequeno

O teste tem **37 imagens com defeito**. Com esse tamanho, cada defeito perdido vale 2,7 pontos de recall:

| Defeitos perdidos no teste | Recall por imagem |
|---|---|
| 0 | 100% |
| 1 | 97,3% |
| 2 | 94,6% (abaixo da meta de 0,95) |

A meta da Fase 1 fica, na prática, "perder no máximo 1 defeito no teste". O intervalo de confiança de 95% em torno de um recall observado de 95% com n = 37 é de cerca de ±7 pontos. Os resultados da Fase 5 serão reportados com intervalo, não só com o número.

## Reprodução

```powershell
python src/split/similaridade.py   # embeddings e pares mais parecidos (reports/fase3)
python src/split/grupos.py         # grupos com limiar 0,92 (reports/fase3/grupos.csv)
python src/split/dividir.py        # divisão, verificação e cópia para data/processed
```

Os scripts `ver_pares.py` e `ver_grupo.py` geram as figuras usadas na inspeção visual. Como elas contêm imagens da base, ficam fora do repositório.
