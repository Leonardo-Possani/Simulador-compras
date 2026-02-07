# 🛒 Simulador de Compras (PDV)

Projeto pessoal para estudos de **backend** com foco em **DDD (Domain-Driven Design)**, **TDD** e regras de negócio de um PDV (ponto de venda). A ideia é manter o domínio simples, bem testado e fácil de evoluir.

---

## 🎯 Objetivos deste repositório

- Praticar **Python** com orientação a domínio.
- Exercitar **TDD** com testes unitários claros e objetivos.
- Modelar regras de negócio de um PDV: carrinho, estoque, venda e checkout.
- Construir um portfólio sólido para buscar estágio em backend.

---

## 🧩 Domínio modelado

O sistema foi dividido em camadas e conceitos do domínio:

- **Carrinho**: itens e quantidades selecionadas.
- **Estoque**: validação de disponibilidade e baixa após a venda.
- **Venda**: descontos, taxas, pagamento e validações.
- **Checkout**: orquestra o fluxo de fechamento da venda.

---

## 🧪 Testes (TDD)

Os testes unitários ficam em `tests/` e cobrem as regras do domínio.  
Para rodar:

```bash
pytest
```

---

## 🧰 Tecnologias Utilizadas

- **Python 3.10+**
- **Pytest** (testes)
- **Ruff** (lint)
- **Pyright** (type hints)

---

## 🗂 Estrutura do projeto

```bash
Simulador-compras
  ├── src/
  │   └── simulador/
  │       ├── application/  # Casos de uso (ex.: checkout)
  │       └── domain/       # Regras de negócio
  ├── tests/                # Testes unitários
  ├── pyproject.toml
  └── README.md
```

---

## ▶️ Como executar localmente

1. **Clone o repositório**
```bash
git clone git@github.com:Leonardo-Possani/Simulador-compras.git
cd Simulador-compras
```

2. **Crie o ambiente e instale dependências**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

3. **Execute os testes**
```bash
pytest
```

---

## 🔧 Próximos passos (roadmap)

- [ ] Interface GUI, CLI
- [ ] Evoluir a modelagem para suportar múltiplos meios de pagamento
- [ ] Criar uma API simples para expor o domínio (FastAPI/Flask)
- [ ] Aumentar cobertura de testes
- [ ] Estoque integrado

---

## 🙋‍♂️ Sobre mim

Sou estudante de programação buscando **estágio em backend**.  
Estou desenvolvendo este projeto como parte do meu aprendizado e portfólio.  
Sugestões e feedbacks são bem-vindos!
