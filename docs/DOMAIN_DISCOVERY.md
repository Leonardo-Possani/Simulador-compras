# DOMAIN DISCOVERY

Este documento centraliza conhecimento de domínio que costuma ficar espalhado no código, em conversas ou em decisões implícitas.

## Entidades

1. Produto
- Item vendável com identidade (`produto_id`), nome, preço e estoque.

2. Estoque
- Conjunto de produtos disponíveis para venda.

3. ItemCarrinho
- Intenção de compra de um produto com quantidade e preço no momento da adição.

4. Carrinho
- Agrupador de itens da compra em andamento.

5. Venda
- Transação fechada com totais, método de pagamento e dados de quitação.

6. ItemVendaFechada
- Snapshot imutável dos itens no fechamento da venda.

7. ItemVendido
- Representação mínima (`produto_id`, `qtd`) para baixa de estoque.

8. ResultadoVenda
- Resultado final do checkout: `venda` processada + `estoque_atualizado`.

9. Método de Pagamento
- Enum das formas aceitas: `credito`, `debito`, `dinheiro`.

## Regras de Venda

1. Fechamento
- Não permite fechar venda com carrinho vazio.
- Não permite `produto_id` duplicado no carrinho.
- Total bruto é calculado a partir dos itens do carrinho.

2. Desconto e taxa
- Desconto deve estar entre `0` e `100`.
- Taxa não pode ser negativa.
- Aplicar taxa exige `total_com_desconto` calculado.

3. Sequência obrigatória
- Registrar pagamento exige `total_final` calculado.
- Processar pagamento exige `total_final` calculado e método válido.

4. Validação no fechamento
- Antes da baixa, itens vendidos passam por validação de estoque (quantidade, existência, disponibilidade).

## Regras de Estoque

1. Identidade de produto
- `produto_id` não pode ser negativo.
- `produto_id` deve existir no estoque quando referenciado.

2. Integridade do produto
- Nome não pode ser vazio.
- Preço deve ser maior que zero.
- Estoque base deve ser maior que zero para produto vendável.

3. Limites de quantidade
- Não permite baixa com `qtd <= 0`.
- Não permite soma de quantidade no carrinho acima do disponível.
- Não permite venda acima do estoque disponível.

4. Atualização de estoque
- A baixa ocorre item a item.
- O fluxo retorna uma nova estrutura de estoque (sem mutar a referência original de entrada).

## Regras de Pagamento

1. Método
- Método não pode ser ausente no processamento.
- Método deve ser um dos aceitos (`credito`, `debito`, `dinheiro`).

2. Dinheiro
- `valor_pago` deve ser maior ou igual ao `total_final`.
- Se maior, calcula troco.
- Se menor, bloqueia com erro.

3. Débito e crédito
- `valor_pago` deve ser exatamente igual ao `total_final`.
- Divergência entre valor pago e total final bloqueia operação.

## Invariantes

1. Produto referenciado em carrinho/venda deve existir no estoque.
2. Carrinho válido não possui `produto_id` duplicado.
3. Quantidades de itens em carrinho/venda são sempre maiores que zero.
4. Venda só avança respeitando a ordem: total -> desconto -> taxa -> método -> quitação.
5. Venda finalizada deve manter consistência entre itens vendidos e estoque baixado.
6. Resultado do checkout sempre combina venda processada e estoque atualizado coerente.

## Fluxos Críticos

1. Fluxo completo da venda
1. Recebe entrada (`carrinho`, `estoque`, `desconto`, `taxa`, `pagamento`, `valor_pago`).
2. Fecha venda com carrinho válido e gera snapshot imutável.
3. Aplica desconto.
4. Aplica taxa e define `total_final`.
5. Valida e registra método de pagamento.
6. Processa quitação conforme método.
7. Extrai itens vendidos.
8. Valida estoque para venda.
9. Baixa estoque.
10. Retorna `ResultadoVenda`.

2. Fluxo de atualização de estoque
1. Valida `produto_id`.
2. Controla limite preventivo no carrinho.
3. Revalida itens no fechamento.
4. Baixa quantidades item a item.
5. Retorna `estoque_atualizado`.

3. Fluxo de cancelamento (estado atual)
- Não implementado no domínio atual.
- Implicação: venda finalizada é tratada como definitiva no escopo congelado.

## Inconsistências Encontradas

1. Precisão monetária usa `float`, sem política explícita de arredondamento.
2. Não há validação explícita para `NaN`, `Infinity` e tipos inesperados em campos numéricos.
3. Não há limites superiores para preço, quantidade, taxa e valor pago.
4. Não há validação explícita para `produto_id` duplicado dentro do estoque.
5. Em dinheiro exato, `valor_pago` não é registrado explicitamente na venda (assimetria com débito/crédito).
6. Fluxo de cancelamento/estorno não existe.

## Possíveis Melhorias Arquiteturais

1. Padronizar valores monetários com `Decimal` e regra formal de arredondamento.
2. Criar validações de tipo/faixa para entradas de domínio.
3. Definir e validar unicidade de `produto_id` no estoque.
4. Padronizar contrato de quitação para sempre registrar `valor_pago`.
5. Introduzir fluxo formal de cancelamento (estorno + reposição de estoque + auditoria).
6. Preparar abstrações de persistência/interface (ports/adapters) mantendo o domínio puro.
7. Definir estratégia de concorrência para atualização de estoque em cenário multiusuário.
