*This project has been created as part of the 42 curriculum by ecallisa, eguedes-.*

# A-MAZE-ING

## Descrição
O A-maze-ing é um projeto para a criação de labirintos aleatórios de acordo com especificações predeterminadas pelo usuário no arquivo config.txt.
Utilizamos o algoritmo Kruskal para a execução do projeto conforme será melhor descrito.
Este código é aberto para ser utilizado por qualquer pessoa e servirá de base para o projeto "Pac-man" da escola 42.

## Algoritmos e Escolhas Técnicas

**Maze Generation Algorithm: Randomized Kruskal**

Este projeto utiliza o algoritmo Randomized Kruskal (Kruskal Aleatorizado) aliado a uma estrutura de dados de Conjuntos Disjuntos (Union-Find) para gerar os labirintos. A lógica foi encapsulada de forma a permitir tanto a geração de labirintos perfeitos quanto tabuleiros abertos e sem finais mortos.

**Como o Labirinto Perfeito é Gerado (`kruskal_perfect`):**
* Inicialmente, cada célula do labirinto é tratada como um conjunto isolado (`rank = 0` e `parent = self`).
* Todas as arestas possíveis (paredes compartilhadas entre células vizinhas) são mapeadas e embaralhadas aleatoriamente.
* O algoritmo itera sobre essa lista de arestas. Se as duas células separadas pela parede pertencerem a conjuntos diferentes (verificado via `find_set` com compressão de caminho), a parede é derrubada utilizando operações *bitwise* subtraindo o valor direcional (1, 2, 4 ou 8) do atributo `wall`.
* As células são então unidas no mesmo conjunto (`union` por *rank*), garantindo que não haja ciclos e criando um caminho único entre quaisquer dois pontos.
* O padrão fixo "42" fixado através de uma flag (`fix`), impedindo que o algoritmo destrua suas paredes estruturais.

**Adaptação para Tabuleiros de Pac-Man (`kruskal_imperfect`):**
* Para gerar o modo de jogo (onde becos sem saída não são permitidos), o gerador roda o algoritmo perfeito primeiro.
* Em seguida, uma varredura identifica todos os becos sem saída checando se a célula possui exatamente 3 paredes (`wall.bit_count() == 3`).
* Uma parede vizinha válida é escolhida aleatoriamente e derrubada. O processo se repete dinamicamente até a função `verify` confirmar que não restam mais becos no mapa, resultando em um labirinto totalmente trançado (Braided Maze).

**Por que o Kruskal foi escolhido?**
A escolha do Kruskal baseou-se em sua eficiência e previsibilidade estrutural. Diferente do *Recursive Backtracker*, que gera corredores longos e tortuosos e pode estourar o limite de recursão do Python em mapas massivos, o Kruskal aleatorizado cria labirintos com caminhos curtos, altamente ramificados e muitos becos sem saída. Essa característica é ideal para ser posteriormente "trançada" no modo imperfeito, gerando dezenas de rotas circulares interdependentes perfeitas para um clone de Pac-Man. Além disso, a implementação via Union-Find isola a lógica matemática da matriz, facilitando a modularização e o reúso do código.

**Algoritmo para o caminho mais curto: Breadth-First Search (BFS)**
Para solucionar o labirinto e encontrar o caminho mais curto entre a entrada e a saída, o projeto implementa o algoritmo de Busca em Largura (Breadth-First Search - BFS).
A escolha deste algoritmo deve-se à sua garantia matemática de sempre encontrar a rota mais curta em grafos não ponderados (onde o custo de mover-se de uma célula para outra é sempre igual a 1).
A lógica foi isolada na classe Bfs utilizando o decorador @staticmethod, tornando-a uma ferramenta modular e independente que não exige a instanciação de um objeto para ser utilizada.

**Como o BFS opera no labirinto:** O algoritmo recebe as coordenadas Cartesianas (x, y) do arquivo de configuração e as traduz dinamicamente para o padrão matricial do Python [y][x] para acessar os nós (maze[entry[1]][entry[0]]).
* `queue`: Utiliza uma fila (FIFO - First In, First Out) para explorar o labirinto em "camadas" ou níveis de profundidade. A fila armazena não apenas o nó atual, mas também a lista do caminho percorrido até chegar a ele.
* `visited`: Um conjunto (set) rastreia os nós já visitados. Sendo uma estrutura de dados de tempo constante $O(1)$ para buscas, o set impede que o algoritmo entre em loops infinitos ou explore a mesma célula duas vezes, otimizando o processamento.
* `detecção de paredes`: Para saber se um caminho está livre, o BFS lê o atributo wall do nó atual. Através de operações lógicas AND (& 1, & 2, & 4, & 8), o algoritmo verifica instantaneamente se as paredes Norte, Leste, Sul ou Oeste estão abertas (valor == 0) e se a célula vizinha respeita os limites da matriz.
* `Termination`: Assim que o nó atual corresponde às coordenadas de saída, o algoritmo interrompe a busca e retorna o trajeto completo. Se a fila esvaziar e a saída não for encontrada (o que não deve ocorrer devido à validação do Kruskal), ele retorna uma lista vazia de forma segura.

**Minilibx ou MLX**
A interface gráfica foi isolada na classe `Render`, de modo que não interfira no gerador matemático. O módulo traduz os dados estruturados em pixels na tela.
* `start` inicializa a janela com o tamanho correto e as instruções de uso para o usuário
* `select_color` cria 4 padrões de cores fixas armazenadas como lista encadeada circular, que podem ser selecionadas em ordem sequencial
* `paint_block` cria é a função reponsável para "pintar" blocos de pixels em tamanho predeterminado
* `put_block_pixel` "pinta" blocos conforme o tamanho das paredes desejado e chama a função `paint_block` para isso
* `put_entry_exit` insere os blocos que representam a entrada e a saída do labirinto
* `render_path` gera um caminho de cor fixa de acordo com as coordenadas geradas pela função `short_path`
* `render_maze` gera a imagem completa do labirinto
* `gere_key` faz o gerenciamento das teclas apertadas pelo usuário. Cada tecla tem um número de acordo com o sistema operacional e a função fica esperando a entrada do usuário para que ele interaja conforme necessário.

## Instruções

### Arquivo 'config.txt'

O arquivo `config.txt` deverá conter as informações necessárias para a geração do labirinto, de modo que cada valor deve ser colocado de forma exata para evitar erros.

`WIDTH`: é a largura do labirinto, expressa em número inteiro de 4 a 499 para limitar o tamanho total

`HEIGHT`: é a altura do labirinto, expressa em número inteiro de 4 a 499 para limitar o tamanho total

`ENTRY`: é a entrada do labirinto, expressa em coordenada no formato <int>,<int> onde o começo do tabuleiro será sempre no topo à esquerda e o final será embaixo à direita.
O primeiro valor se refere ao eixo X largura e sempre deverá ser no mínimo 0 e no máximo o valor de WIDTH.
O segundo valor se refere ao eixo y altura e sempre deverá ser no mínimo 0 e no máximo o valor de HEIGHT

`EXIT`: é a saída do labirinto, expressa em coordenada no formato <int>,<int> onde o começo do tabuleiro será sempre no topo à esquerda e o final será embaixo à direita.
O primeiro valor se refere ao eixo X largura e sempre deverá ser no mínimo 0 e no máximo o valor de WIDTH.
O segundo valor se refere ao eixo y altura e sempre deverá ser no mínimo 0 e no máximo o valor de HEIGHT

`OUTPUT_FILE`: é o nome do arquivo que será gerado com o labirinto no formato hexadecimal, além das coordenadas de entrada e saída e do caminho mais curto para a saída. Sempre devera ser no formato <str>.txt com caracteres válidos para nomear arquivos

`PERFECT`: é um valor booleano que se for `True` determina que o labirinto será perfeito, com um único caminho para a saída, ou se for `False` o labirinto será imperfeito, sem finais mortos e ideal para uso no Pac-man.

`SEED`: este é o único valor opcional. Em regra o parâmetro será fornecido vazio como `SEED=`o que fará com que a geração do labirinto seja completamente aleatória a cada sessão. Se o usuário desejar, ele pode colocar um número inteiro positivo que servirá de base para repetir o mesmo labirinto. Por exemplo `SEED=42`sempre gerará o mesmo labirinto, desde que todas as informações acima também sejam idênticas.



## Fontes

Utilizamos site de pesquisa Google, repositórios no Github, respostas de IA Gemini, Copilot, Claude e ChatGPT como principais fontes de informação.
O uso da IA nos ajudou muito a estruturar o projeto para torna-lo bem otimizado. Também teve uso de IA na descrição deste README.
O algoritmo Kruskal foi baseados no livro Introduction to algorithms 4ed.

## Contribuição pessoal

*ecallisa* foi o principal responsável pela criação dos algoritmos Kruskal para o labirinto perfeito e imperfeito e também foi o principal responsável pelo uso do MLX para a renderização do labirinto e dos botões do programa.
*eguedes-* foi o responsável principalmente pela organização do projeto e otimização das funções criadas, adequação às normas flake8 e mypy.

Conseguimos nos organizar de modo que aproximadamente metade do projeto foi feito por nós dois através de diálogo direto, de modo que usávamos apenas 1 pc codando, mas nós dois conversando.
