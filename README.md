*This project has been created as part of the 42 curriculum by ecallisa, eguedes-.*

# A-MAZE-ING

## Descrição

O A-Maze-ing é um gerador de labirintos aleatórios em Python. Ele lê um arquivo de configuração (`config.txt`), gera um labirinto (perfeito ou imperfeito/jogável), calcula o caminho mais curto entre entrada e saída, grava o resultado em um arquivo em formato hexadecimal e exibe o labirinto graficamente com a MiniLibX (MLX).

Objetivos principais:

* Gerar labirintos reproduzíveis por meio de uma *seed*.
* Suportar o modo **perfeito** (`PERFECT=True`: exatamente um caminho entre entrada e saída) e o modo **imperfeito** (`PERFECT=False`: tabuleiro estilo Pac-Man, totalmente conexo, com rotas alternativas e **sem becos sem saída**).
* Desenhar o padrão "42" no centro do labirinto com células totalmente fechadas (quando o tamanho permite).
* Oferecer um módulo reutilizável (`mazegen`) que poderá ser instalado via `pip` e reaproveitado em projetos futuros, como o "Pac-Man" da 42.

## Instruções

### Requisitos

* Python 3.10 ou superior
* Linux (Ubuntu): a MiniLibX (MLX) para Python usada no projeto é o *wheel* `mlx-2.2/ubuntu/mlx-2.2-py3-none-any.whl`, fornecido no repositório em `mlx-2.2/mlx-2.2.tgz`
* `flake8`, `mypy` e `build` (instalados automaticamente por `make install`)

### Comandos do Makefile

| Regra | O que faz |
|---|---|
| `make all` | Executa `fclean`, `install` e `run` em sequência |
| `make install` | Extrai a MLX (`mlx-2.2.tgz`), cria o ambiente virtual `env` e instala nele a MLX, `build`, `flake8` e `mypy` |
| `make run` | Executa `python3 a_maze_ing.py config.txt` dentro do ambiente virtual |
| `make debug` | Executa o programa com o depurador `pdb` (`python3 -m pdb a_maze_ing.py config.txt`) |
| `make clean` | Remove `__pycache__`, `.mypy_cache`, `build`, `dist` e `*.egg-info` |
| `make fclean` | Executa `clean` e remove também o ambiente virtual `env`, `maze.txt` e os arquivos extraídos da MLX |
| `make lint` | Roda `flake8 .` e `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs` (ignorando `env`, `mlx-2.2`, `build` e `dist`) |
| `make lint-strict` | Roda `flake8 .` e `mypy . --strict` (com as mesmas pastas ignoradas) |

### Execução

```bash
python3 a_maze_ing.py config.txt
```

`config.txt` é o único argumento. Qualquer erro (arquivo inexistente, sintaxe inválida, parâmetros impossíveis) gera uma mensagem de erro clara, sem encerrar o programa de forma inesperada.

### Arquivo `config.txt`

O arquivo contém um par `CHAVE=VALOR` por linha. Linhas iniciadas com `#` são comentários e são ignoradas. Um arquivo de configuração padrão está disponível no repositório.

| Chave | Obrigatória | Descrição | Exemplo |
|---|---|---|---|
| `WIDTH` | Sim | Largura do labirinto (nº de células). Inteiro de 1 a 500 | `WIDTH=20` |
| `HEIGHT` | Sim | Altura do labirinto (nº de células). Inteiro de 1 a 500 | `HEIGHT=15` |
| `ENTRY` | Sim | Coordenadas `x,y` da entrada. Origem (0,0) no canto superior esquerdo | `ENTRY=0,0` |
| `EXIT` | Sim | Coordenadas `x,y` da saída. Deve ser diferente da entrada e estar dentro do labirinto | `EXIT=19,14` |
| `OUTPUT_FILE` | Sim | Nome do arquivo de saída, no formato `<nome>.txt` | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Não | `True` → labirinto perfeito; `False`(Padrão) → labirinto jogável, sem becos sem saída | `PERFECT=True` |
| `SEED` | Não | Inteiro positivo para reproduzir o mesmo labirinto. Vazio (`SEED=`) → geração aleatória a cada execução | `SEED=42` |
| `ALGORITHM` | Não | Algoritmo de geração: `kruskal` (padrão), `prim` ou `bfs` (maiúsculas/minúsculas são aceitas) | `ALGORITHM=prim` |
| `ANIMATION` | Não | `True` → mostra a construção do labirinto passo a passo; `False` (padrão) → exibe o resultado final | `ANIMATION=True` |

Observações:

* As chaves não diferenciam maiúsculas de minúsculas (`width=20` equivale a `WIDTH=20`). Valores vazios são aceitos apenas em `PERFECT`, `SEED`, `ALGORITHM` e `ANIMATION`, que então usam o valor padrão.
* Chaves desconhecidas são ignoradas. Se faltar uma chave obrigatória, se houver uma linha sem `=` ou se um valor for inválido, o programa mostra uma mensagem de erro com o formato esperado e encerra.
* `ENTRY` e `EXIT` precisam estar dentro do labirinto (`0 <= x < WIDTH` e `0 <= y < HEIGHT`) e ser diferentes entre si.
* `ENTRY` e `EXIT` não podem coincidir com as células do padrão "42".
* O padrão "42" só é desenhado quando `WIDTH > 14` e `HEIGHT > 14`. Em labirintos menores ele é omitido.
* Com a mesma `SEED` e as mesmas demais configurações, o labirinto gerado é sempre o mesmo.

Exemplo:

```
# Labirinto padrão
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=
ALGORITHM=kruskal
ANIMATION=False
```

### Formato do arquivo de saída

Cada célula é escrita como **um dígito hexadecimal** que codifica as paredes fechadas (bit = 1 → parede fechada; bit = 0 → parede aberta):

| Bit | Direção |
|---|---|
| 0 (LSB) | Norte (N) |
| 1 | Leste (E) |
| 2 | Sul (S) |
| 3 | Oeste (W) |

* As células são gravadas linha por linha, uma linha do labirinto por linha do arquivo.
* Após uma linha vazia vêm três linhas: coordenadas de entrada, coordenadas de saída e o caminho mais curto usando as letras `N`, `E`, `S`, `W`.
* Todas as linhas terminam com `\n`.
* Paredes vizinhas são sempre coerentes (se uma célula tem parede a leste, a vizinha tem parede a oeste).

### Interface gráfica (MLX)

Durante a execução é possível:

| Tecla | Ação | Descrição |
|---|---|---|
| `1` | Gerar novo labirinto | Sorteia uma nova *seed*, re-gera e exibe um novo labirinto (com animação, se `ANIMATION=True`) |
| `2` | Mostrar/ocultar caminho | Exibe ou esconde o caminho mais curto da entrada até a saída |
| `3` | Trocar cores | Alterna entre 4 paletas de cores (fundo, paredes e padrão "42") |
| `4` | Sair | Fecha a janela e encerra o programa |

Fechar a janela pelo botão da janela também encerra o programa.

A janela mostra paredes, entrada (azul), saída (amarelo), o padrão "42" e o caminho mais curto, além de uma legenda com as teclas na parte inferior. Cada célula ocupa 10 pixels e cada parede 5 pixels.

> Ao regenerar com a tecla `1`, a *seed* é substituída por uma nova, então o novo labirinto não corresponde mais à `SEED` do `config.txt`. A *seed* usada é impressa no terminal e pode ser colocada no arquivo para repetir o labirinto. O arquivo de saída é sobrescrito a cada geração.

## Algoritmos e escolhas técnicas

O projeto implementa três algoritmos de geração (Kruskal, Prim e BFS aleatorizado), selecionáveis pela chave `ALGORITHM`, e usa BFS para encontrar o caminho mais curto. Todos operam sobre uma grade de objetos `Node`, em que cada célula guarda suas paredes em uma máscara de bits (`wall`, valor inicial 15 = todas fechadas) e as coordenadas `cords`. Derrubar uma parede é subtrair o valor da direção (1, 2, 4 ou 8) da máscara das duas células vizinhas. As células do padrão "42" são marcadas com a flag `fix` e nunca têm paredes derrubadas.

### Kruskal aleatorizado (algoritmo padrão)

* Cada célula começa como um conjunto isolado (`rank = 0` e `parent = self`).
* Todas as arestas possíveis (paredes compartilhadas entre células vizinhas) são listadas e embaralhadas.
* O algoritmo percorre a lista. Se as duas células pertencem a conjuntos diferentes (`find_set` com compressão de caminho), a parede entre elas é derrubada e os conjuntos são unidos (`union` por *rank*). Isso garante a ausência de ciclos e um único caminho entre quaisquer dois pontos.
* Células marcadas com `fix` (padrão "42") são ignoradas, preservando o desenho.

### Prim

* Utiliza uma estrutura de dados **heap mínima**. Como o algoritmo se baseia em pesos, cada aresta entre células vizinhas recebe um peso aleatório.
* É construído um dicionário `graph` em que a chave é uma célula e o valor é uma lista de tuplas `(vizinho, peso)`.
* Todas as células começam com chave "infinita" (`10001`) e sem pai; uma célula inicial aleatória recebe chave `0`.
* A cada passo, a célula de menor chave é extraída do heap, a parede entre ela e seu pai é derrubada e as chaves dos vizinhos que ainda estão no heap são atualizadas (`decrease_key`) quando o peso da aresta é menor.

### BFS aleatorizado (geração)

* Parte da célula central do labirinto, adicionada ao conjunto `visited`.
* Os vizinhos não visitados (e que não pertencem ao "42") são guardados na lista `frontier` como pares `(atual, vizinho)`.
* A cada iteração, um par é retirado **aleatoriamente** de `frontier`. Se o vizinho já foi visitado, o par é ignorado; caso contrário, o vizinho é marcado como visitado, a parede entre as células é derrubada e os vizinhos dele entram em `frontier`.
* O processo se repete até `frontier` ficar vazia, resultando em um labirinto perfeito (árvore geradora).

### Modo imperfeito (`PERFECT=False`) — Braided Maze

Para obter um tabuleiro estilo Pac-Man, o gerador executa primeiro o algoritmo perfeito escolhido e depois chama `break_walls_imperfect`:

* Uma varredura identifica os becos sem saída, isto é, células com exatamente 3 paredes (`wall.bit_count() == 3`) que não fazem parte do "42".
* Para cada beco, uma parede vizinha válida é escolhida aleatoriamente e derrubada.
* O processo se repete até que a função `verify` confirme que não restam becos, resultando em um labirinto totalmente "trançado" (sem becos sem saída e com várias rotas independentes).

### Por que Kruskal como algoritmo padrão?

A escolha baseou-se na eficiência e na previsibilidade estrutural. Diferente do *Recursive Backtracker*, que gera corredores longos e tortuosos e pode estourar o limite de recursão do Python em mapas grandes, o Kruskal aleatorizado cria caminhos curtos e muito ramificados, com muitos becos sem saída. Essa característica é ideal para ser "trançada" no modo imperfeito, gerando várias rotas circulares interdependentes, perfeitas para um clone de Pac-Man. Além disso, a implementação com Union-Find isola a lógica matemática da matriz, facilitando a modularização e o reúso do código. Os demais algoritmos (Prim e BFS) foram adicionados como alternativas, oferecendo labirintos com características visuais diferentes.

### Caminho mais curto: Breadth-First Search (BFS)

Para resolver o labirinto, o projeto usa Busca em Largura, que garante o caminho mais curto em grafos não ponderados (custo 1 por movimento). A lógica está isolada na classe `Bfs` com `@staticmethod`, sem necessidade de instanciar objetos.

* O algoritmo recebe as coordenadas cartesianas `(x, y)` do arquivo de configuração e as traduz para o padrão matricial `[y][x]` (`maze[entry[1]][entry[0]]`).
* `queue`: fila (FIFO) que explora o labirinto por camadas e guarda, junto de cada nó, o caminho percorrido até ele.
* `visited`: `set` com busca em tempo O(1), evitando loops e visitas repetidas.
* Detecção de paredes: operações AND bit a bit (`& 1`, `& 2`, `& 4`, `& 8`) verificam se as paredes Norte, Leste, Sul e Oeste estão abertas (valor 0) e se o vizinho está dentro dos limites da matriz.
* Término: ao alcançar a saída, retorna o caminho completo. Se a fila esvaziar sem encontrar a saída, retorna uma lista vazia.
* O caminho (lista de nós) é convertido em uma string com `N`, `E`, `S`, `W`, gravada no arquivo de saída.

### Renderização: MiniLibX (MLX)

A interface gráfica está isolada na classe `Render`, sem interferir no gerador. O módulo traduz a estrutura do labirinto em pixels na tela.

* `start`: cria a janela com o tamanho correto, escreve as instruções de uso e registra os *hooks* de teclado e de fechamento da janela.
* `select_color` / `next_color`: definem 4 paletas de cores fixas (fundo, paredes e padrão "42"), armazenadas em uma lista encadeada circular, e avançam para a próxima paleta.
* `paint_block`: pinta blocos de pixels de tamanho predeterminado.
* `put_block_pixel`: percorre a grade e pinta as paredes de cada célula conforme sua máscara de bits, chamando `paint_block`.
* `put_entry_exit`: desenha os blocos que representam a entrada e a saída.
* `render_path`: desenha, em cor fixa, o caminho calculado por `short_path`.
* `render_maze`: gera a imagem completa do labirinto.
* `init_animation`: executa o gerador `generate_maze()`. Com `ANIMATION=True`, redesenha cada célula alterada (`animate_wall`) a cada parede derrubada; caso contrário, desenha apenas o resultado final. Ao terminar, grava o arquivo de saída e inicia o loop de eventos.
* `gere_key`: trata as teclas `1` a `4` descritas acima.
* `end` / `end_event`: destroem a janela e encerram o loop da MLX.

### Funcionalidades extras

* Três algoritmos de geração (Kruskal, Prim e BFS), selecionáveis via `ALGORITHM`.
* Modo imperfeito sem becos sem saída (labirinto totalmente trançado).
* Animação da geração do labirinto na janela (`ANIMATION=True`), possível porque os algoritmos são geradores (`yield`) que entregam cada parede derrubada.
* Paletas de cores alternáveis em tempo de execução.

### Estrutura do projeto

| Arquivo | Responsabilidade |
|---|---|
| `a_maze_ing.py` | Ponto de entrada: valida a configuração, cria o `MazeGenerator` e inicia a renderização |
| `parse_config.py` | Leitura e validação do `config.txt` (`validate_config`) |
| `render_maze.py` | Classe `Render`: janela MLX, animação, cores e teclas |
| `mazegen/` | Módulo reutilizável: `mazegen.py` (`MazeGenerator`), `kruskal.py`, `prim.py`, `bfs.py` e `maze_utils.py` |

## Código reutilizável: o módulo `mazegen`

A geração do labirinto está encapsulada na classe `MazeGenerator`, em um módulo independente (`mazegen`) que pode ser instalado com `pip` e importado em outros projetos. Os arquivos de geração (`mazegen.py`, `kruskal.py`, `prim.py`, `bfs.py` e `maze_utils.py`) não dependem da interface gráfica nem do parser de configuração.

### Instalação

O pacote (`mazegen-*.whl` ou `mazegen-*.tar.gz`) está na raiz do repositório:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Para reconstruir o pacote a partir do código-fonte, em um ambiente virtual (o `make install` já cria o ambiente `env` com a ferramenta `build`):

```bash
make install
source env/bin/activate
python3 -m build
```

### Exemplo básico

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    height=15,
    width=20,
    entry=(0, 0),            # (x, y)
    exit_maze=(19, 14),      # (x, y)
    output_file="maze.txt",
)
gen.build()                  # gera o labirinto e calcula o caminho
gen.save_file()              # opcional: grava o arquivo no formato hexadecimal
```

### Parâmetros personalizados

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `height` | `int` | — | Altura (nº de linhas) |
| `width` | `int` | — | Largura (nº de colunas) |
| `entry` | `tuple[int, int]` | — | Entrada `(x, y)` |
| `exit_maze` | `tuple[int, int]` | — | Saída `(x, y)` |
| `output_file` | `str` | — | Nome do arquivo de saída (`.txt`) |
| `seed` | `int \| str` | `"random"` | Inteiro para resultados reproduzíveis |
| `perfect` | `bool` | `False` | `True` → labirinto perfeito |
| `algorithm_str` | `str` | `"kruskal"` | `"kruskal"`, `"prim"` ou `"bfs"` |

```python
gen = MazeGenerator(
    height=30, width=40,
    entry=(0, 0), exit_maze=(39, 29),
    output_file="big.txt",
    seed=42, perfect=True, algorithm_str="prim",
)
gen.build()
```

### Acessando a estrutura e a solução

```python
gen.maze        # list[list[Node]]: grade de células, acessada como gen.maze[linha][coluna]
gen.maze[0][0].wall   # máscara de paredes: 1 = N, 2 = E, 4 = S, 8 = W (bit 1 = parede fechada)
gen.path        # list[Node]: células do caminho mais curto, da entrada até a saída
gen.path_str    # str: caminho como sequência de 'N', 'E', 'S', 'W'
```

Para animar a geração passo a passo, use o gerador `generate_maze()`, que produz (`yield`) cada par de células conectadas:

```python
for step in gen.generate_maze():
    ...  # redesenhar a cada parede derrubada
```

> A estrutura exposta pelo módulo (grade de `Node`) não é necessariamente idêntica ao formato do arquivo de saída.

## Gerenciamento de equipe e projeto

### Papéis

* **ecallisa**: principal responsável pelos algoritmos de Kruskal, Prim (labirinto perfeito e imperfeito) e pelo uso da MLX para renderizar o labirinto e os botões do programa.
* **eguedes-**: principal responsável pela organização do projeto, otimização das funções, adequação às normas `flake8` e `mypy`, além dos algoritmos BFS tanto para geração de labirinto quanto a busca do caminho mais curto.

Aproximadamente metade do projeto foi desenvolvida em conjunto, com os dois conversando diretamente enquanto apenas um computador era usado para programar.

### Planejamento
1. **Kruskal e BFS do caminho mais curto:** implementados conforme o plano, junto com a validação do `config.txt` e a gravação do arquivo de saída.
2. **Novos algoritmos de geração:** como o projeto já estava bem modularizado, percebemos que a mesma estrutura podia ser reaproveitada. Adicionar o BFS e o Prim como algoritmos de geração foi simples e virou um extra do projeto.
3. **Geradores (`yield`):** percebemos que os algoritmos podiam entregar, a cada passo, as células em que uma parede foi derrubada. Essas coordenadas são usadas pelo `Render` para atualizar a janela, o que deu origem à animação da geração.
4. **Renderização com a MiniLibX:** escolhemos a MLX em vez de uma saída ASCII no terminal porque achamos que aprenderíamos mais com ela e entenderíamos melhor como funciona o sistema de janelas no Linux.

### O que funcionou bem e o que pode melhorar

* **Funcionou bem:** separação clara entre geração, resolução e renderização; uso de geradores, que facilita animações; diálogo constante entre a dupla.
* **Pode melhorar:** Testes automatizados, desempenho na utilização da minilibx, desempenho dos algoritmos em labirintos muito grandes.

### Ferramentas utilizadas

* Python 3, MiniLibX (MLX), `flake8`, `mypy`, Git/GitHub, Makefile, `build` (empacotamento do módulo).
* vscode, lazyvim

## Resources

### Referências

* CORMEN, T. H. et al. *Introduction to Algorithms*, 4ª ed. (Kruskal, Prim, Union-Find, BFS e heaps).
* Documentação do Python: https://docs.python.org/3/
* PEP 8 / PEP 257 / PEP 484 (estilo, docstrings e type hints).
* Documentação do `flake8` e do `mypy`.
* Jamis Buck, *Maze Generation* — série de artigos sobre algoritmos de geração de labirintos.
* Wikipedia: *Maze generation algorithm*, *Kruskal's algorithm*, *Prim's algorithm*, *Breadth-first search*.
* Documentação da MiniLibX.
* Pesquisas no Google e repositórios públicos do GitHub.

### Uso de IA

Ferramentas de IA (Gemini, Copilot, Claude e ChatGPT) foram usadas como apoio para:

* estruturar o projeto e discutir a organização das classes e dos módulos;
* sugerir otimizações e revisar o código (docstrings, type hints, conformidade com `flake8` e `mypy`);
* ajudar na redação e na revisão deste README.

Todo o código gerado ou sugerido por IA foi revisado, testado e compreendido pela dupla antes de ser incorporado ao projeto. A lógica dos algoritmos (Kruskal, Prim, BFS) e da renderização foi desenvolvida e é explicável pelos próprios integrantes.

## Licença

Este código é aberto e pode ser reutilizado e distribuído por qualquer pessoa, inclusive em projetos futuros da escola 42 (como o "Pac-Man"). Consulte o arquivo `LICENSE.md` na raiz do repositório para os termos completos.
