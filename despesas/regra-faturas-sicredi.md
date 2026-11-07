# Regra: leitura de faturas de cartão Sicredi (CSV)

Especificação implementada em `sicredi_fatura.py`. Fonte: orientação do titular.

## Formato do arquivo
- UTF-8 com BOM (`utf-8-sig`). Separador `;`. Linhas terminam com `;` sobrando (coluna vazia extra).
- Campos com espaços nas pontas: `strip()` em tudo.
- Duas partes: (1) cabeçalho em pares chave;valor e resumo de despesas; (2) tabela de lançamentos, a partir da linha cujo primeiro campo é `Data`.

## Parsing
- Início da tabela: linha que começa com `Data` e tem `Descrição`, `Parcela`, `Valor`. Antes = metadado; depois = lançamento.
- Colunas: Data, Descrição, Parcela, Valor, Valor em Dólar, Adicional, Nome.
- Datas `dd/mm/aaaa`. Valores `"R$ 1.234,56"` / `"R$ -9.014,73"` convertidos com `Decimal` (nunca float). Negativo = crédito/pagamento.
- Parcela `(02/03)` = atual/total; vazio = à vista.
- Adicional = final do cartão adicional; vazio = titular.
- Descrição truncada e com espaços de preenchimento: normalizar.

## Classificação
- `Pag Fat Deb Cc` (negativo): pagamento da fatura anterior, fora dos totais de despesa.
- `Credito Anuidade Cartao`, `Taxa De Anuidade`, `IOF Compra Internacional`: encargos.
- Exterior: lançamentos em USD; o IOF vem em linha separada com a mesma data.
- Parcela presente = parcela em curso, não gasto novo.

## Validação obrigatória
`fatura anterior + pagamentos/créditos + encargos + débitos Brasil + débitos exterior = total da fatura`,
e soma dos lançamentos conferida com os campos do resumo. Divergência: reportar a diferença e **parar**.

## Privacidade
- Não imprimir número de cartão, conta ou cooperativa em saída, log ou commit.
- CSV de fatura nunca é versionado (`.gitignore`). Processamento local.

## Saída padrão
Tabela por categoria com total; parcelas em curso (atual/total e saldo restante); itens que parecem
profissionais, sempre marcados "a confirmar".
