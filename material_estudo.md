# Material de Estudo: Antiprocrastinador Tech 🚀

Este documento resume a arquitetura, estrutura e as tecnologias utilizadas no desenvolvimento do protótipo **Antiprocrastinador Tech**, uma aplicação de produtividade baseada no método Pomodoro.

---

## 1. Visão Geral da Arquitetura

O projeto foi estruturado seguindo uma divisão clara entre **Frontend (Interface)** e **Backend (Banco de Dados)**, resultando em um código mais limpo e profissional.

### Tecnologias Utilizadas:
- **Linguagem:** Python
- **Interface Gráfica:** `flet` (com modernidade e assincronia)
- **Gráficos:** `flet_charts` (para componentes complexos de chart)
- **Banco de Dados:** MySQL (através do `mysql-connector-python`)
- **Notificações:** `plyer` (notificações integradas no Sistema Operacional)

---

## 2. Camada de Banco de Dados (MySQL)

Nós centralizamos a lógica do banco em scripts limpos, garantindo que o banco de dados sempre exista na inicialização.

### A. Estrutura das Tabelas (`create_db.py`)
A modelagem do banco contém duas tabelas com relacionamento direto (Chave Estrangeira):
- `tarefas`: Guarda o ID, Título e o status (`concluida`).
- `sessoes`: Guarda o histórico de tempo. Colunas principais: ID da tarefa de origem, a `tecnologia` ou assunto em que trabalhou, a quantidade de `duracao_minutos` focado e a data/hora atual (log do Sistema).

### B. A Classe de Integração (`banco_dados.py`)
Criamos uma classe `BancoDados` aplicando Orientação a Objetos. Ela permite que a interface converse com o SQL através de métodos intuitivos sem poluir o arquivo visual:
- `salvar_progresso(tarefa, tech, minutos)`: Procura se a tarefa existe; se não, cria. Em seguida, injeta a sessão do pomodoro.
- `obter_relatorio_semanal()`: Busca todas as sessões apenas dos últimos 7 dias, agrupando pelo nome da tecnologia (usando comando `SUM(duracao_minutos)` e `GROUP BY`).

---

## 3. Interface Visual e Lógica (Flet em `main.py`)

A mágica toda se encontra no `main.py` onde chamamos `flet.run(main)`.

### 3.1. Estado Assíncrono (`async`)
Diferente das interfaces antigas como Tkinter, o *Flet* suporta processamento assíncrono. Nós usamos bibliotecas padrão do Python (como `asyncio.sleep(1)`) dentro de `async def iniciar_foco(e)`. 
Por que isso é bom? Porque enquanto o laço (`while`) atualiza o relógio na tela (decrementando os segundos), você ainda poderia clicar e navegar no aplicativo **sem a interface travar**.

### 3.2. Estradas e Painéis (Componentes)
Utilizamos layouts modernos para distribuir elementos na tela:
- **`ft.Row` e `ft.Column`**: Elementos flexíveis para organizar caixas de texto (`TextField`), relógio (`Text`) e botões visuais.
- **Gráfico Pizza (`charts.PieChart`)**: Lê dinamicamente os valores de desempenho (`db.obter_relatorio_semanal`) e pinta setores baseando-se em cores pré-carregadas que alternam a cada nova tecnologia através de índices de array.
- **Tabela de Dados (`ft.DataTable`)**: Preenche linhas geradas na etapa anterior com os valores brutos para quem prefere ler os números exatos.

### 3.3. Retorno de Experiência (UX)
Quando o cronômetro bate `00:00`:
- **`db.salvar_progresso`**: Vai salvar em background sem o usuário perceber.
- **`plyer.notification`**: Envia aquele "bip" ou "pulo na tela" confirmando encerramento.
- **`atualizar_dashboard()`**: Limpa e recarrega instantaneamente as variáveis e gráficos com os dados recém inseridos no MySQL.

---

### Por que esse protótipo ficou excelente do ponto de vista Técnico?
Porque é um código **Escalável**! 
As queries de banco de dados não estão grudadas no Frontend em arquivos gigantes (nós as separamos), nós migramos do Terminal para uma Interface Gráfica real trocando menos de duas dependências e nós pensamos numa tabela (`sessoes`) que cresce de forma estruturada.

Fim do sumário! Ótimos estudos!
