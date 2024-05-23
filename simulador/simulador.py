import random

# Classe Página definindo um intervalo de 0 a 100
class Pagina:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.dados = [random.randint(0, 100) for _ in range(tamanho)]

# Classe Memória Física definindo parâmetros de tamanho, páginas, tempo de acesso e falhas da página
class MemoriaFisica:
    def __init__(self, tamanho, tamanho_pagina):
        self.tamanho = tamanho
        self.tamanho_pagina = tamanho_pagina
        self.paginas = {}
        self.tempo_acesso = 0
        self.falhas_pagina = 0

    # Método para alocar página
    def alocar_pagina(self, processo_id, pagina_id):
        if len(self.paginas) >= self.tamanho:
            return False

        pagina = Pagina(self.tamanho_pagina)
        self.paginas[(processo_id, pagina_id)] = pagina
        return True

    # Método para carregar página usando uma estratégia de substituição
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

    # Método para acessar página
    def acessar_pagina(self, processo_id, pagina_id, offset):
        if (processo_id, pagina_id) not in self.paginas:
            return None

        pagina = self.paginas[(processo_id, pagina_id)]
        self.tempo_acesso += 1
        return pagina.dados[offset]

    # Método para obter estatísticas
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
    # Simulando LRU: neste caso estamos apenas retornando a última chave,
    # isso é apenas um exemplo simplificado, LRU real deve manter um registro de acessos.
    return list(paginas.keys())[-1]

# Simulação principal
tamanho_memoria_fisica = 10  # Tamanho da memória física em páginas
tamanho_pagina = 4  # Tamanho de cada página em bytes
numero_processos = 5  # Número de processos

# Inicializar memória física
memoria_fisica = MemoriaFisica(tamanho_memoria_fisica, tamanho_pagina)

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
