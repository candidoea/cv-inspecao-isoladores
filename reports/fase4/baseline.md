# Fase 4. Baseline

**Código:** `src/train/treinar.py`, `configs/exp01_baseline.yaml`, `notebooks/04_treino_colab.ipynb`
**Experimento:** `exp01_baseline`, commit `b142a0e`

## Resumo

Um YOLO11n pré-treinado no COCO foi ajustado à divisão da Fase 3 com a configuração padrão da Ultralytics. Na validação, o modelo encontrou os 37 defeitos (recall de 1,00) com precision de 0,97. **Esse resultado ainda não é evidência de que o modelo aprendeu o defeito**: a auditoria mostrou que todas as imagens com defeito são colagens, distinguíveis das normais por nitidez, brilho e tamanho de arquivo. O teste contrafactual da Fase 5 separa as duas hipóteses. O conjunto de teste não foi usado.

## Configuração

| Parâmetro | Valor | Observação |
|---|---|---|
| Modelo | `yolo11n.pt` | 2,6 milhões de parâmetros, pré-treinado no COCO |
| Épocas | 50 | `patience` 20 não foi acionado |
| Tamanho de imagem | 640 | Defeito com cerca de 30 px de lado nessa escala (achado 2) |
| Batch | 16 | |
| Semente | 42 | |
| Demais | Padrão da Ultralytics 8.4.190 | Otimizador AdamW automático, mosaic desligado nas 10 últimas épocas |

## Ambiente

| Item | Valor |
|---|---|
| Hardware | Google Colab, GPU Tesla T4 |
| Software | Python 3.13, torch 2.11.0+cu130, Ultralytics 8.4.190 |
| Tempo | 50 épocas em 11 minutos |

O treino em CPU local (Intel i3-10110U) levou cerca de 7 minutos **por época**, o que tornaria cada experimento uma execução de 6 horas. Com a mesma semente, CPU e GPU deram métricas diferentes após uma época (precisão numérica e versões de biblioteca distintas). Por isso, todos os experimentos do projeto rodam no mesmo ambiente (Colab com GPU), e o registro de cada execução passa a gravar a versão do torch e o dispositivo.

## Resultados na validação

| Classe | Imagens | Caixas | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|---|
| isolador | 127 | 196 | 0,931 | 0,923 | 0,974 | 0,843 |
| defeito | 37 | 37 | 0,967 | 1,000 | 0,977 | 0,761 |
| todas | 127 | 233 | 0,949 | 0,962 | 0,975 | 0,802 |

Precision e recall acima são os que a Ultralytics informa, no limiar de confiança que maximiza o F1 médio. Não são o ponto de operação, que será escolhido pelo custo do erro na Fase 5.

## Leitura

1. **Alto demais para a base.** Recall de 100% num objeto que ocupa 0,31% da imagem é compatível com duas explicações: o modelo aprendeu o defeito, ou aprendeu que imagens de colagem sempre contêm um defeito. A validação não distingue as duas, porque tem as mesmas colagens que o treino.
2. **Incerteza grande.** 37 acertos em 37 têm intervalo de confiança de 95% (Clopper-Pearson) de **90,5% a 100%**. O recall real pode estar abaixo da meta de 0,95.
3. **Localização do defeito é o ponto fraco real.** O mAP50-95 do defeito (0,761) é menor que o do isolador (0,843): o modelo encontra o defeito, mas a caixa é menos justa. Efeito esperado de objeto pequeno.
4. **Convergência.** O mAP50 estabilizou em torno de 0,975 nas últimas épocas, enquanto as perdas de validação ainda caíam devagar (`box_loss` de 0,643 para 0,618 entre as épocas 46 e 50). Mais épocas podem melhorar o ajuste das caixas: hipótese para a Fase 7.

## Próximo passo

Fase 5: precision e recall por classe no limiar escolhido pelo custo, com intervalo de confiança, e o teste contrafactual (borrar e comprimir imagens normais para medir se o modelo passa a apontar defeitos nelas).

## Reprodução

Treino no Google Colab com GPU, seguindo `notebooks/04_treino_colab.ipynb`: clonar o repositório, descompactar `data/processed` a partir do Drive, reescrever `cplid.yaml` com o caminho local e rodar

```bash
python src/train/treinar.py configs/exp01_baseline.yaml
```