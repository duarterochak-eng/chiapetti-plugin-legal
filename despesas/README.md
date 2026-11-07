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
    python3 -I despesas/app.py parcelas                         # parceladas em curso e saldo a vencer

## Categorias (`categorias.py`)
Casa (Luz, Diarista, Mercado, Lavanderia, Internet, Condomínio, Material de limpeza/Mercado Livre),
Carro (Lavador, Combustível, Oficina/Toyota, IPVA/Licenciamento, Seguro), Loja maçônica,
Farmácia, Unimed, Bar e restaurante, Kart, Mensalidades (um item por serviço, total no grupo),
Extraordinárias (limpeza de ar-condicionado, obra do novo escritório). O que não casar é perguntado.
`config --esperado "Categoria|Nome|VALOR[|AAAA-MM]"` avisa quando um valor fixo mensal (ex.: prestação) não aparece;
com `AAAA-MM` acumula a dívida (meses devidos x valor - o que já foi pago).
`parcelas` lista compras parceladas em curso e o saldo a vencer; o resumo mostra o total por categoria.
Explicar uma parcela (ex.: como Obra) vale para todas as parcelas, passadas e futuras.
`explicar ... --valor-exato` cria regra só para aquele valor (ex.: R$ 2.509 ao mesmo favorecido de um repasse menor).

## Onde ficam os dados (Google Drive do titular)
- Pasta `Despesas/Enviar`: extratos e faturas novos (CSV; PDF quando o banco só gera PDF).
- Pasta `Despesas/Dados`: cópia de segurança em texto (`snapshot-salvar` / `snapshot-restaurar`):
  `lancamentos.csv`, `importacoes.csv`, `regras.json`, `config.json`.
- Cada sessão começa restaurando a cópia e termina salvando a nova. O conector do Drive cria e lê arquivos,
  mas não sobrescreve conteúdo: para atualizar, grava-se versão nova e a antiga vai para a lixeira.
- A cópia contém dados financeiros: nunca vai para o git (`despesas/dados/` e `*.csv` estão no `.gitignore`).

## Fora do normal
Para lugares já conhecidos (2+ meses de histórico), o app avisa quando o total do mês passa de 2x a média
e de R$ 150 acima dela, e pergunta "o que foi?". Com o tempo, os lugares recorrentes ficam conhecidos.

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
