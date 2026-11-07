# Despesas pessoais

Núcleo do app: importa extrato da conta + faturas de cartão, unifica sem duplicar, aprende regras
e devolve "entrou X, gastou X em ...". Dados ficam em `despesas/dados/` (fora do git).

## Uso mensal (tudo fechado, uma vez por mês)
    python3 -I despesas/app.py config --documento SEU_CPF --cartao sicredi-master --cartao azul ...
    python3 -I despesas/app.py importar-extrato extrato.csv
    python3 -I despesas/app.py importar-fatura fatura.csv --cartao sicredi-master
    python3 -I despesas/app.py pendentes                       # o que o app não reconhece
    python3 -I despesas/app.py explicar ID "Categoria" [--tipo renda|despesa|transferencia|pagamento_cartao] [--so-este]
    python3 -I despesas/app.py resumo 2026-10
    python3 -I despesas/app.py recorrencias

## Regras do cálculo
- **Pagamento de fatura, Pix para você mesmo e Pix ao banco do cartão não são gasto**: o gasto está dentro da fatura.
- **Entrada** só é renda quando explicada (ex.: retirada da PJ); entrada desconhecida fica "a confirmar".
- `explicar` congela uma regra (por CPF/CNPJ ou nome) que vale para o passado e para os próximos envios.
  A regra distingue entrada de saída da mesma pessoa.
- Reenviar extrato com período sobreposto não duplica (cada linha é identificada pelo saldo corrente).
- Extrato e fatura que não conciliam não são importados: o app mostra a diferença e para.
- Cartão por **fatura** (mês do vencimento) ou por **compra** (`config --base compra`).
- O resumo avisa quando faltam faturas de algum cartão configurado.

Testes: `python3 -I -m unittest discover -s despesas/tests`. Ver também `regra-faturas-sicredi.md`.
