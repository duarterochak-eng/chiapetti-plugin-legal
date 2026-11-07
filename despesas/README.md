# Despesas pessoais

Núcleo do app: importa extrato da conta + faturas de cartão, unifica sem duplicar, aprende regras
e devolve "entrou X, gastou X em ...". Dados ficam em `despesas/dados/` (fora do git).

## Uso mensal (tudo fechado, uma vez por mês)
    python3 -I despesas/app.py config --documento SEU_CPF --cartao sicredi-master --cartao azul ...
    python3 -I despesas/app.py importar-extrato extrato.csv
    python3 -I despesas/app.py importar-fatura fatura.csv --cartao sicredi-master
    python3 -I despesas/app.py pendentes                       # o que o app não reconhece
    python3 -I despesas/app.py explicar ID "Categoria" [--tipo renda|despesa|transferencia|pagamento_cartao] [--so-este]
    python3 -I despesas/app.py resumo 2026-10                  # entrou/gastou por grupo, com avisos
    python3 -I despesas/app.py acumulado 2026                  # mês a mês e acumulado do ano
    python3 -I despesas/app.py lancar 20/10/2026 100,00 "Bar e restaurante" "churrasco em dinheiro"
    python3 -I despesas/app.py recorrencias

## Categorias (`categorias.py`)
Casa (Luz, Diarista, Mercado, Lavanderia, Internet, Condomínio, Material de limpeza/Mercado Livre),
Carro (Lavador, Combustível, Oficina/Toyota, IPVA/Licenciamento, Ótica, Seguro), Loja maçônica,
Farmácia, Unimed, Bar e restaurante, Kart, Mensalidades (um item por serviço, total no grupo),
Extraordinárias (limpeza de ar-condicionado, obra do novo escritório). O que não casar é perguntado.
`config --esperado "Categoria|Nome|VALOR"` avisa quando um valor fixo mensal (ex.: prestação) não aparece.
`explicar ... --valor-exato` cria regra só para aquele valor (ex.: R$ 2.509 ao mesmo favorecido de um repasse menor).

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
