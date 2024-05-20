import random

# Classe Página definindo um intervalo de 0 a 100
class Pagina:
  def __init__(self, tamanho):
    self.tamanho = tamanho
    self.dados = [random.randint(0, 100) for _ in range(tamanho)]

# Classe Memória Física definindo parâmetros de tamanho, páginas, tempo de acesso e falhas da página
class MemoriaFisica:
  def __init__(self, tamanho):
    self.tamanho = tamanho
    self.paginas = {}
    self.tempo_acesso = 0
    self.falhas_pagina = 0

# Classe Alocar Página definindo seus parâmetros self, processo_id e pagina_id
  def alocar_pagina(self, processo_id, pagina_id):

    # Se o comprimento da quantidade de páginas é maior ou igual ao tamanho
    if len(self.paginas) >= self.tamanho:
      return False

    # 
    pagina = Pagina(self.tamanho_pagina)
    self.paginas[(processo_id, pagina_id)] = pagina
    return True

  def carregar_pagina(self, processo_id, pagina_id, estrategia_substituicao):
    if (processo_id, pagina_id) in self.paginas:
      return True

    if len(self.paginas) >= self.tamanho:
      substituida = estrategia_substituicao(self.paginas)
      del self.paginas[substituida]

    pagina = Pagina(self.tamanho_pagina)
    self.paginas[(processo_id, pagina_id)] = pagina
    self.falhas_pagina += 1
    return True

# Função para acessar páginas usando os parâmetros self, processo_id, pagina_id e offset
  def acessar_pagina(self, processo_id, pagina_id, offset):

    # Se o processo_id e pagina_id não estiver incluído no construtor self.paginas
    if (processo_id, pagina_id) not in self.paginas:
      return None

    pagina = self.paginas[(processo_id, pagina_id)]
    self.tempo_acesso += 1
    return pagina.dados[offset]

# Função criada para obter estatísticas do tempo de acesso, falhas de página e páginas carregadas
  def get_estatisticas(self):
    return {
      "tempo_acesso": self.tempo_acesso,
      "falhas_pagina": self.falhas_pagina,
      "paginas_carregadas": len(self.paginas),
    }

# Funções de estratégia de substituição de página (exemplos)

def fifo(paginas):
  return list(paginas.keys())[0]

def lru(paginas):
  ultima_acessada = max(paginas, key=paginas.get)
  return ultima_acessada

# Simulação principal

tamanho_memoria_fisica = 10  # Tamanho da memória física em páginas
tamanho_pagina = 4  # Tamanho de cada página em bytes
numero_processos = 5  # Número de processos

# Inicializar memória física
memoria_fisica = MemoriaFisica(tamanho_memoria_fisica)
memoria_fisica.tamanho_pagina = tamanho_pagina

# Simular alocação e acesso a páginas
for _ in range(100):
  processo_id = random.randint(0, numero_processos - 1)
  pagina_id = random.randint(0, 10)
  offset = random.randint(0, tamanho_pagina - 1)

  if not memoria_fisica.alocar_pagina(processo_id, pagina_id):
    memoria_fisica.carregar_pagina(processo_id, pagina_id, fifo)

  dado = memoria_fisica.acessar_pagina(processo_id, pagina_id, offset)
  if dado is None:
    print(f"Falha de página para processo {processo_id}, página {pagina_id}")

# Exibir estatísticas
estatisticas = memoria_fisica.get_estatisticas()
print(f"Estatísticas:\n{estatisticas}")