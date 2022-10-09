from random import randint

# Constantes
N_PISTAS = 3
N_PISTAS_EMERGENCIA = 1
N_PRATELEIRAS = 2
ITERACOES = 20

# Aeroporto
avioes = {}
pistas = []
prateleiras = []
filas_decolagem = []

# Contadores
id_aterrissagem = -1
id_decolagem = 0

count_emergencias = 0

# Cria a quantidade de pistas dinamicamente
def init_aeroporto():
    for i in range(N_PISTAS):
        pistas.append(None)
        filas_decolagem.append([])
    for i in range(N_PISTAS-N_PISTAS_EMERGENCIA):
        prateleiras.append([])
        for j in range(N_PRATELEIRAS):
            prateleiras[i].append([])

# Gera o proximo ID
def proximo_id(decolagem=False):
    # Global serve para ter acesso à variável fora do escopo da função
    global id_aterrissagem
    global id_decolagem
    if decolagem:
        id_decolagem += 2
        return id_decolagem
    id_aterrissagem += 2
    return id_aterrissagem

# Procura pela menor fila de decolagem
def menor_fila_decolagem():
    global filas_decolagem
    # [0] -> Indice, [1] -> Valor
    menor = [0, len(filas_decolagem[0])]
    for i in range(1, len(filas_decolagem)):
        if len(filas_decolagem[i]) < menor[1]:
            menor[0] = i
            menor[1] = len(filas_decolagem[i])
    return menor[0]

# Procura pela menor prateleira de aterrissagem
def menor_fila_aterrissgem():
    # [0] -> Pista, [1] -> Prateleira, [2] -> Valor
    menor = [0, 0, len(prateleiras[0][0])]
    for i in range(0, len(prateleiras)):
        for j in range(0, len(prateleiras[i])):
            if len(prateleiras[i][j]) < menor[2]:
                menor[0] = i
                menor[1] = j
                menor[2] = len(prateleiras[i][j])
    return menor[:2]

# A cada tempo, gasta 1 unidade de combustivel
def decrementar_combustivel():
    global prateleiras
    for i in range(len(prateleiras)):
        for j in range(len(prateleiras[i])):
            for k in range(len(prateleiras[i][j])):
                if prateleiras[i][j][k][1] == 0:
                    raise Exception(
                        f"Avião {prateleiras[i][j][k][0]} caiu por falta de combustível!")
                prateleiras[i][j][k][1] -= 1

# Insere o aviao na menor fila
def inserir_aviao(decolagem=False):
    global prateleiras
    global filas_decolagem

    id = proximo_id(decolagem)
    combustivel = randint(1, 20)
    aviao = [id, combustivel, 0, decolagem]
    avioes[id] = aviao

    if decolagem:
        menor = menor_fila_decolagem()
        filas_decolagem[menor].append(aviao)
    else:
        menor = menor_fila_aterrissgem()
        prateleiras[menor[0]][menor[1]].append(aviao)

# Gera os aviões novos
def chegada():
    n_aterrissagem = randint(0, 3)
    n_decolagem = randint(0, 3)

    for i in range(n_aterrissagem):
        inserir_aviao()

    for i in range(n_decolagem):
        inserir_aviao(decolagem=True)

# Procura por um aviao sem combustivel
def aviao_sem_combustivel():
    global prateleiras
    for i in range(len(prateleiras)):
        for j in range(len(prateleiras[i])):
            for k in range(len(prateleiras[i][j])):
                if prateleiras[i][j][k][1] == 0:
                    return [i, j, k]
    return False

# Gerencia os pousos de emergencia
def pouso_emergencia():
    global prateleiras
    global count_emergencias
    sem_combustivel = aviao_sem_combustivel()
    while sem_combustivel:
        i, j, k = sem_combustivel
        aviao = prateleiras[i][j].pop(k)
        n_achou = True
        for pista in range(N_PISTAS-1, -1, -1):
            if not pistas[pista]:
                count_emergencias += 1
                pistas[pista] = aviao
                n_achou = False
                break
        if n_achou:
            raise Exception(
                f"Avião {aviao[0]} caiu por falta de pista para pouso!")
        sem_combustivel = aviao_sem_combustivel()

# Remove os aviões da pista
def limpar_pistas():
    for i in range(len(pistas)):
        pistas[i] = None

# Incrementa o tempo de espera dos aviões
def incrementar_tempo():
    for i in range(len(prateleiras)):
        for j in range(len(prateleiras[i])):
            for k in range(len(prateleiras[i][j])):
                avioes[prateleiras[i][j][k][0]][2] += 1
    for i in range(len(filas_decolagem)):
        for j in range(len(filas_decolagem[i])):
            avioes[filas_decolagem[i][j][0]][2] += 1

# [0] -> Decolagem, [1] -> aterrissagem

# calcula a média de espera
def media():
    soma_decolagem = 0
    count_decolagem = 0
    soma_aterrissagem = 0
    count_aterrissagem = 0
    for i in avioes:
        if avioes[i][3]:
            soma_decolagem += avioes[i][2]
            count_decolagem += 1
        else:
            soma_aterrissagem += avioes[i][2]
            count_aterrissagem += 1
    return [
        soma_decolagem/count_decolagem if count_decolagem > 0 else 0,
        soma_aterrissagem/count_aterrissagem if count_aterrissagem > 0 else 0
    ]


# Main Loop
init_aeroporto()

print(f"Tempo: 0/{ITERACOES}")
print("Pistas")
print(pistas)
print("Decolagem")
print(filas_decolagem)
print("Aterrissagem")
print(prateleiras)
print("")
for tempo in range(1, ITERACOES+1):
    print(f"Tempo: {tempo}/{ITERACOES}")

    chegada()

    print("Pistas")
    print(pistas)
    print("Decolagem")
    print(filas_decolagem)
    print("Aterrissagem")
    print(prateleiras)
    m_decolagem, m_aterrissagem = media()
    print(f"Espera de decolagem média: {m_decolagem}")
    print(f"Espera de aterrissagem média: {m_aterrissagem}")
    print(f"Pousos de emergência: {count_emergencias}")
    print("")

    limpar_pistas()
    decrementar_combustivel()
    incrementar_tempo()

    # Emergencias
    pouso_emergencia()
    # Quem pode aterrissar
    for pista in range(len(prateleiras)):
        if not pistas[pista]:
            maior = [0, len(prateleiras[pista][0])]
            for j in range(0, len(prateleiras[pista])):
                if len(prateleiras[pista][j]) > maior[1]:
                    maior[0] = j
                    maior[1] = len(prateleiras[pista][j])
            if maior[1] > 0:
                pistas[pista] = prateleiras[pista][maior[0]].pop(0)
    # Quem pode decolar
    for pista in range(len(pistas)):
        if not pistas[pista] and len(filas_decolagem[pista]):
            pistas[pista] = filas_decolagem[pista].pop(0)
