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
- Outros negativos (`Credito Anuidade Cartao`, estornos): créditos.
- Encargos/tarifas: anuidade, IOF (inclusive adicional sobre saldo financiado), multa, juros de mora.
- Exterior: coluna "Valor em Dólar" vem **vazia**; distingue-se pelo estabelecimento (`EXTERIOR_HINTS`).
  O IOF de compra internacional pode vir em data diferente da compra.
- Parcela presente = parcela em curso, não gasto novo. Parcela `n/n` = última, sem saldo restante.

## Convenção real do resumo Sicredi (observada em duas faturas)
- Anuidade, IOF, multa e juros de mora ficam **dentro de "Débitos no Brasil"**.
- Crédito de anuidade fica em **"Pagamentos / Créditos"**.
- **"Encargos"** do resumo pode trazer valor não itemizado nos lançamentos (ex.: juros do saldo financiado).
  Isso gera **aviso** no topo do relatório, não bloqueio.
- "Pagamento Mínimo" é do cabeçalho e não se confunde com "Pagamentos / Créditos".
- Cabeçalho: vencimento, valor total (conferido contra o total do resumo) e pagamento mínimo.
  `saldo financiado se pagar só o mínimo = total - mínimo`.

## Validação obrigatória
`fatura anterior + pagamentos/créditos + encargos + débitos Brasil + débitos exterior = total da fatura`;
total do cabeçalho = total do resumo; soma dos negativos = pagamentos/créditos; soma dos positivos =
Brasil + exterior (ou + encargos, se itemizados). Divergência: reportar a diferença e **parar** (erro).
Diferença exatamente igual a "Encargos" não itemizados: **aviso** visível, análise segue.
A divisão Brasil/exterior é por estabelecimento e só gera aviso.

## Privacidade
- Não imprimir número de cartão, conta ou cooperativa em saída, log ou commit.
- CSV de fatura nunca é versionado (`.gitignore`). Processamento local.

## Saída padrão
Tabela por categoria com total; parcelas em curso (atual/total e saldo restante); itens que parecem
profissionais, sempre marcados "a confirmar".
