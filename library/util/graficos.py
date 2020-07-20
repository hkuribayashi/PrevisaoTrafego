import matplotlib.pyplot as plt
import numpy as np


def tco_simples(cenarios, tipo_grafico, path):

    global nome_aglomerado, id_aglomerado

    capex = list()
    opex = list()
    rotulos = list()

    for key in cenarios:
        capex_macro = cenarios[key].capex_macro[tipo_grafico]
        capex_hetnet = cenarios[key].capex_hetnet[tipo_grafico]
        opex_macro = cenarios[key].opex_macro[tipo_grafico]
        opex_hetnet = cenarios[key].opex_hetnet[tipo_grafico]
        tempo_analise = cenarios[key].tempo_analise

        capex_m = np.zeros(tempo_analise)
        capex_m += capex_macro['infraestrutura']
        capex_m += capex_macro['equipamentos']
        capex_m += capex_macro['instalacao']

        capex_h = np.zeros(tempo_analise)
        capex_h += capex_hetnet['infraestrutura']
        capex_h += capex_hetnet['equipamentos']
        capex_h += capex_hetnet['instalacao']

        opex_m = np.zeros(tempo_analise)
        opex_m += opex_macro['energia']
        opex_m += opex_macro['manutencao']
        opex_m += opex_macro['aluguel']
        opex_m += opex_macro['falhas']

        opex_h = np.zeros(tempo_analise)
        opex_h += opex_hetnet['energia']
        opex_h += opex_hetnet['manutencao']
        opex_h += opex_hetnet['aluguel']
        opex_h += opex_hetnet['falhas']

        capex.append(capex_m.sum())
        capex.append(capex_h.sum())
        opex.append(opex_m.sum())
        opex.append(opex_h.sum())

        rotulos.append('Macro-C' + str(cenarios[key].id))
        rotulos.append('Hetnet-C' + str(cenarios[key].id))

        if cenarios[key].tipo_cenario == 'Original':
            nome_aglomerado = cenarios[key].tipo_aglomerado
            id_aglomerado = cenarios[key].id

    # Posição das Barras no eixo X
    posicao = list()
    if len(cenarios) <= 2:
        separacao = 2.5
        plt.figure()
        bar_width = 1.0
    else:
        separacao = 3.8
        plt.figure(figsize=(9.0, 5.5))
        bar_width = 2.0
    for i in range(2 * len(cenarios)):
        posicao.append(i * separacao)

    # Legendas e Largura das Barras
    legenda = ['CAPEX '.format(tipo_grafico), 'OPEX {}'.format(tipo_grafico)]

    line_width = 0.5

    plt.bar(posicao, capex, color='#4f82bd', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
    plt.bar(posicao, opex, bottom=capex, color='#cf4d4f', edgecolor='black', width=bar_width, zorder=3,
            linewidth=line_width)

    # Alterações nas propriedades dos Eixos X e Y
    plt.xticks(posicao, rotulos)
    plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
    plt.legend(legenda, loc='best')
    plt.ylabel('TCO (Unidades Monetárias $)')
    plt.title('Comparação TCO {}: Aglomerado {}'.format(tipo_grafico, nome_aglomerado))

    plt.savefig('{}TCO-Simples-{}-{}.eps'.format(path, tipo_grafico, id_aglomerado), dpi=600, bbox_inches='tight')


def composicao_tco(cenarios, tipo_grafico, path):

    global nome_aglomerado, id_aglomerado

    infraestrutura = list()
    equipamentos = list()
    instalacao = list()
    energia = list()
    manutencao = list()
    aluguel = list()
    falhas = list()
    rotulos = list()

    line_width = 0.5

    if tipo_grafico == 'Radio':
        legenda = ['Infra.', 'Equip.', 'Inst.', 'Energ.', 'Manut.', 'Alug.', 'Falhas']
    else:
        legenda = ['Infra.', 'Equip.', 'Inst.', 'Energ.', 'Manut.', 'Espec.', 'Falhas']

    for key in cenarios:
        capex_macro = cenarios[key].capex_macro[tipo_grafico]
        capex_hetnet = cenarios[key].capex_hetnet[tipo_grafico]
        opex_macro = cenarios[key].opex_macro[tipo_grafico]
        opex_hetnet = cenarios[key].opex_hetnet[tipo_grafico]

        infraestrutura.append(capex_macro['infraestrutura'].sum())
        infraestrutura.append(capex_hetnet['infraestrutura'].sum())

        equipamentos.append(capex_macro['equipamentos'].sum())
        equipamentos.append(capex_hetnet['equipamentos'].sum())

        instalacao.append(capex_macro['instalacao'].sum())
        instalacao.append(capex_hetnet['instalacao'].sum())

        energia.append(opex_macro['energia'].sum())
        energia.append(opex_hetnet['energia'].sum())

        manutencao.append(opex_macro['manutencao'].sum())
        manutencao.append(opex_hetnet['manutencao'].sum())

        aluguel.append(opex_macro['aluguel'].sum())
        aluguel.append(opex_hetnet['aluguel'].sum())

        falhas.append(opex_macro['falhas'].sum())
        falhas.append(opex_hetnet['falhas'].sum())

        rotulos.append('Macro-C' + str(cenarios[key].id))
        rotulos.append('Hetnet-C' + str(cenarios[key].id))

        if cenarios[key].tipo_cenario == 'Original':
            nome_aglomerado = cenarios[key].tipo_aglomerado
            id_aglomerado = cenarios[key].id

    # Posição das Barras no eixo X
    posicao = list()
    if len(cenarios) <= 2:
        separacao = 2.5
        plt.figure(figsize=(8.0, 5.5))
        bar_width = 1.0
    else:
        separacao = 3.8
        plt.figure(figsize=(9.0, 5.5))
        bar_width = 2.0

    for i in range(2 * len(cenarios)):
        posicao.append(i * separacao)

    plt.bar(posicao, infraestrutura, color='#4f82bd', edgecolor='black', width=bar_width, zorder=3,
            linewidth=line_width)

    plt.bar(posicao, equipamentos, bottom=infraestrutura, color='#cf4d4f', edgecolor='black', width=bar_width,
            zorder=3, linewidth=line_width)

    plt.bar(posicao, instalacao, bottom=[i + j for i, j in zip(infraestrutura, equipamentos)], color='#88a54f',
            edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)

    plt.bar(posicao, energia, bottom=[i + j + k for i, j, k in zip(infraestrutura, equipamentos, instalacao)],
            color='#72578f',
            edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)

    plt.bar(posicao, manutencao,
            bottom=[i + j + k + l for i, j, k, l in zip(infraestrutura, equipamentos, instalacao, energia)],
            color='#4298ae', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)

    plt.bar(posicao, aluguel, bottom=[i + j + k + l + m for i, j, k, l, m in
                                      zip(infraestrutura, equipamentos, instalacao, energia, manutencao)],
            color='#da8436', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
    plt.bar(posicao, falhas, bottom=[i + j + k + l + m + n for i, j, k, l, m, n in
                                     zip(infraestrutura, equipamentos, instalacao, energia, manutencao, aluguel)],
            color='#93a9cf', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)

    # Custom X an Y axis
    plt.xticks(posicao, rotulos)
    plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
    plt.legend(legenda, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=7)
    plt.title('Composição TCO {} Aglomerado {}'.format(tipo_grafico, nome_aglomerado))
    plt.ylabel('Composição do TCO (Unidades Monetárias $)')

    plt.savefig('{}TCO-{}-{}.eps'.format(path, tipo_grafico, id_aglomerado), dpi=600, bbox_inches='tight')


def composicao_tco_porcentagem(cenarios, tipo_grafico, path):

    global nome_aglomerado, id_aglomerado

    infraestrutura = list()
    equipamentos = list()
    instalacao = list()
    energia = list()
    manutencao = list()
    aluguel = list()
    falhas = list()
    rotulos = list()

    # Cores dos Gráficos
    a, b = [plt.cm.Blues, plt.cm.Reds]

    for key in cenarios:
        capex_macro = cenarios[key].capex_macro[tipo_grafico]
        capex_hetnet = cenarios[key].capex_hetnet[tipo_grafico]
        opex_macro = cenarios[key].opex_macro[tipo_grafico]
        opex_hetnet = cenarios[key].opex_hetnet[tipo_grafico]

        infraestrutura.append(capex_macro['infraestrutura'].sum())
        infraestrutura.append(capex_hetnet['infraestrutura'].sum())

        equipamentos.append(capex_macro['equipamentos'].sum())
        equipamentos.append(capex_hetnet['equipamentos'].sum())

        instalacao.append(capex_macro['instalacao'].sum())
        instalacao.append(capex_hetnet['instalacao'].sum())

        energia.append(opex_macro['energia'].sum())
        energia.append(opex_hetnet['energia'].sum())

        manutencao.append(opex_macro['manutencao'].sum())
        manutencao.append(opex_hetnet['manutencao'].sum())

        aluguel.append(opex_macro['aluguel'].sum())
        aluguel.append(opex_hetnet['aluguel'].sum())

        falhas.append(opex_macro['falhas'].sum())
        falhas.append(opex_hetnet['falhas'].sum())

        rotulos.append('Macro-C' + str(cenarios[key].id))
        rotulos.append('Hetnet-C' + str(cenarios[key].id))

        if cenarios[key].tipo_cenario == 'Original':
            nome_aglomerado = cenarios[key].tipo_aglomerado
            id_aglomerado = cenarios[key].id

    for index in range(len(infraestrutura)):
        soma = infraestrutura[index] + equipamentos[index] + instalacao[index] + energia[index] + \
               manutencao[index] + aluguel[index] + falhas[index]
        infraestrutura[index] = (infraestrutura[index] / soma) * 100
        equipamentos[index] = (equipamentos[index] / soma) * 100
        instalacao[index] = (instalacao[index] / soma) * 100
        energia[index] = (energia[index] / soma) * 100
        manutencao[index] = (manutencao[index] / soma) * 100
        aluguel[index] = (aluguel[index] / soma) * 100
        falhas[index] = (falhas[index] / soma) * 100

    plt.title('Composição TCO Aglomerado {}'.format(nome_aglomerado))
    fig, axes = plt.subplots(2, len(cenarios), figsize = (12, 8))

    global mypie2
    global ax

    group_names = ['CAPEX', 'OPEX']
    if tipo_grafico == 'Radio':
        subgroup_names = ['Equip.', 'Inst.', 'Infra.', 'Manut.', 'Aluguel', 'Falhas', 'Energ.']
    else:
        subgroup_names = ['Equip.', 'Inst.', 'Infra.', 'Manut.', 'Espec.', 'Falhas', 'Energ.']

    for i, ax in enumerate(axes.flatten()):

        group_size = [infraestrutura[i] + equipamentos[i] + instalacao[i], energia[i] + manutencao[i] + aluguel[i] + falhas[i]]
        subgroup_size = [equipamentos[i], instalacao[i], infraestrutura[i], manutencao[i], aluguel[i], falhas[i], energia[i]]

        ax.axis('equal')
        mypie, _ = ax.pie(group_size, radius=1.3, labels=group_names, colors=[a(0.8), b(0.8)], startangle=90)
        plt.setp(mypie, width=0.5, edgecolor='white')

        mypie2, plt_labels, junk = ax.pie(subgroup_size, radius=1.3 - 0.3, autopct='%1.1f%%', labeldistance=0.9, colors=[a(0.65), a(0.5), a(0.3), b(0.65), b(0.5), b(0.3), b(0.1)], startangle=90)
        plt.setp(mypie2, width=0.7, edgecolor='white')
        plt.margins(50, 50)
        ax.set_title(rotulos[i])
        plt.setp(junk, size=8, weight='bold')

    plt.legend(mypie2, subgroup_names, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

    plt.savefig('{}TCO-{}-Porcentagem-{}.eps'.format(path, tipo_grafico, id_aglomerado), dpi=600, bbox_inches='tight')


def evolucao_tco(cenarios, tipo_grafico, tipo_rede_radio, path):

    global id_aglomerado

    # Legendas
    names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    legenda = list()

    posicao_macro = np.arange(0, 90, step=6)
    posicao_hetnet = posicao_macro + 2.3
    posicao_legenda = (posicao_macro + posicao_hetnet)/2

    bar_width = 2.0
    line_width = 0.6

    # Cores dos Gráficos
    a, b = [plt.cm.Blues, plt.cm.Reds]

    for key in cenarios:
        plt.figure(figsize=(8.0, 5.5))
        for tipo in tipo_rede_radio:
            if tipo == 'Macro':
                posicao = posicao_macro
                cor_capex = a(0.6)
                cor_opex = b(0.6)
                capex = cenarios[key].capex_macro[tipo_grafico]
                opex = cenarios[key].opex_macro[tipo_grafico]
            else:
                posicao = posicao_hetnet
                cor_capex = a(0.3)
                cor_opex = b(0.3)
                capex = cenarios[key].capex_hetnet[tipo_grafico]
                opex = cenarios[key].opex_hetnet[tipo_grafico]

            legenda.append('CAPEX {}'.format(tipo))
            legenda.append('OPEX {}'.format(tipo))

            tempo_analise = cenarios[key].tempo_analise
            capex_ = np.zeros(tempo_analise)
            capex_ += capex['infraestrutura']
            capex_ += capex['equipamentos']
            capex_ += capex['instalacao']

            opex_ = np.zeros(tempo_analise)
            opex_ += opex['energia']
            opex_ += opex['manutencao']
            opex_ += opex['aluguel']
            opex_ += opex['falhas']

            plt.bar(posicao, capex_, color=cor_capex, width=bar_width, zorder=3, linewidth=line_width, edgecolor='black')
            plt.bar(posicao, opex_, bottom=capex_, color=cor_opex, width=bar_width, zorder=3, linewidth=line_width, edgecolor='black')

            id_aglomerado = cenarios[key].id

        # Custom X axis
        plt.xticks(posicao_legenda, names)
        plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
        plt.legend(legenda, loc='best')
        plt.ylabel('TCO (Unidades Monetárias $)')
        plt.xlabel('Unidade de Tempo (t)')
        plt.title('Evolução do TCO - {}: Aglomerado C{}'.format(tipo_grafico, id_aglomerado))

        plt.savefig('{}TCO-{}-Evolucao-{}.eps'.format(path, tipo_grafico, id_aglomerado), dpi=600, bbox_inches='tight')
