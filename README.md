# Simulador de Compras (PDV)

Projeto de estudo backend com foco em domínio e TDD.  
Objetivo atual: levar o sistema ao estado `v1.0-domain-frozen` para ter regras explícitas, testes confiáveis e base pronta para migração futura para Java OO.

## O que este projeto demonstra

- Evolução orientada por regras de negócio explícitas.
- Refatoração incremental guiada por testes.
- Separação clara entre domínio e orquestração de caso de uso.
- Preocupação com estabilidade de contrato antes de migrar de linguagem.

## Objetivo do Frozen

O marco `v1.0-domain-frozen` será atingido quando todos os critérios abaixo forem verdadeiros:

- Todas as regras de negócio estão explícitas.
- Falhas de negócio usam exceções de domínio (sem retorno silencioso).
- Não há `dict`/estruturas ad-hoc como contrato primário do core.
- Operações de domínio estão claras nos módulos de domínio.
- Domínio não depende de I/O ou infraestrutura.
- Há testes para cada regra e comportamento relevante.
- Entidades têm invariantes claras e protegidas.
- Finalização da venda é atômica e imutável.

## Estado Atual

- Camadas separadas em `domain` e `application`.
- Fluxos principais modelados: carrinho, estoque, venda e checkout.
- Evolução atual orientada por TDD e revisão de regras críticas.

## Roadmap Oficial até `v1.0-domain-frozen`

### Bloco A - Regras críticas (P0)

- [x] A1 - Garantir regra de estoque na primeira inclusão no carrinho
- [x] A2 - Formalizar limites numéricos (desconto e taxa)
- [x] A3 - Validar método de pagamento de forma explícita
- [ ] A4 - Definir pré-condições explícitas de sequência da venda

### Bloco B - Imutabilidade e estado (P0)

- [ ] B5 - Garantir imutabilidade real da venda finalizada
- [ ] B6 - Garantir checkout atômico (all-or-nothing)

### Bloco C - Modelo e contratos (P1)

- [ ] C7 - Definir invariantes de entidades
- [ ] C8 - Substituir contratos `dict` por tipos explícitos no domínio
- [ ] C9 - Eliminar dependência de identidade por índice posicional

### Bloco D - Polimento final (P1/P2)

- [ ] D10 - Refinar hierarquia de exceções de domínio
- [ ] D11 - Completar matriz de testes por regra

### Bloco E - Release

- [ ] Atualizar documentação final do domínio
- [ ] Criar tag `v1.0-domain-frozen`

## Estrutura do Projeto

```bash
simulador_compras
  ├── src/
  │   └── simulador/
  │       ├── application/  # Orquestração de casos de uso (checkout)
  │       └── domain/       # Regras e operações de negócio
  ├── tests/                # Testes unitários e de fluxo
  ├── pyproject.toml
  └── README.md
```

## Como Executar Localmente

1. Clonar o repositório

```bash
git clone git@github.com:Leonardo-Possani/Simulador-compras.git
cd Simulador-compras
```

2. Criar ambiente virtual e instalar dependências

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

3. Rodar testes

```bash
./venv/bin/python -m pytest -q
```

## Qualidade de código

Comandos úteis durante a evolução:

```bash
./venv/bin/python -m pytest -q
ruff check .
pyright
```

## Padrão de Commits

Formato oficial:

```text
<type>(<scope>): <imperative short message>

<objective technical description>

- Technical bullet 1
- Technical bullet 2
- Technical bullet 3

Impact:
<architectural/domain impact>
```

Tipos permitidos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `freeze`  
Escopos permitidos: `domain`, `carrinho`, `venda`, `estoque`, `checkout`, `exceptions`, `entities`, `usecase`, `architecture`
