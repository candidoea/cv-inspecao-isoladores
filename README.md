# cv-inspecao-isoladores

Detecção de isoladores e de defeitos em isoladores em imagens de drone de linhas de transmissão.

Projeto educativo: o objetivo é percorrer, fase por fase, o ciclo completo de um modelo de visão computacional, da definição do problema ao monitoramento. Cada fase termina com um commit e uma tag.

- Arquitetura: [docs/ARQUITETURA.md](docs/ARQUITETURA.md)

## Status

| Fase | Status |
|---|---|
| 0. Ambiente | em andamento |
| 1. Problema | pendente |
| 2. Auditoria dos dados | pendente |
| 3. Divisão sem vazamento | pendente |
| 4. Baseline | pendente |
| 5. Avaliação | pendente |
| 6. Análise de erros | pendente |
| 7. Melhorias | pendente |
| 8. Produção e drift | pendente |

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
python -m pip install -r requirements.txt
yolo checks
```

## Decisões

Preenchidas na Fase 1.

- Classes:
- Erro mais caro:
- Meta de precision mínima para a classe `defeito`:
- Justificativa:

## Dados

Os dados não fazem parte do repositório. A origem, a licença e a versão usadas ficam registradas aqui na Fase 2.

## Autor

Eduardo Cândido
