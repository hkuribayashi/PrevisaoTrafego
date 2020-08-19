import matplotlib.pyplot as plt
import numpy as np

from library.config.param import PARAM


def tco_simples(cenarios, tipo_grafico):

    global id_aglomerado

    plt.figure(figsize=(9.0, 5.5))

    capex = list()
    opex = list()
    rotulos = list()

    # Legendas e Largura das Barras
    legenda_ = ['CAPEX', 'OPEX']
    line_width = 0.5
    bar_width = 1.5

    if tipo_grafico == 'Radio':
        label = 'RAN'
    else:
        label = 'Backhaul'

    for c in cenarios:

        capex_macro = cenarios[c].capex_macro[tipo_grafico]
        capex_hetnet = cenarios[c].capex_hetnet[tipo_grafico]
        opex_macro = cenarios[c].opex_macro[tipo_grafico]
        opex_hetnet = cenarios[c].opex_hetnet[tipo_grafico]
        tempo_analise = cenarios[c].tempo_analise

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

        rotulos.append('Macro')
        rotulos.append('\n{}'.format(c))
        rotulos.append('Hetnet')

        if cenarios[c].tipo_cenario == 'Original':
            id_aglomerado = cenarios[c].id

    # Posicao das Barras
    posicao = np.array([0.0, 1.8, 4.3, 6.1, 8.6, 10.4, 12.9, 14.7])
    posicao_rotulo = np.array([0.0, 0.9, 1.8, 4.3, 5.2, 6.1, 8.6, 9.5, 10.4, 12.9, 13.8, 14.7])

    plt.bar(posicao, capex, color='#4f82bd', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)
    plt.bar(posicao, opex, bottom=capex, color='#cf4d4f', edgecolor='black', width=bar_width, zorder=3, linewidth=line_width)

    # Alterações nas propriedades dos Eixos X e Y
    plt.xticks(posicao_rotulo, rotulos)
    plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
    plt.legend(legenda_, loc='best')
    plt.ylabel('{} TCO - Monetary Units ($)'.format(label))

    plt.savefig('{}TCO-{}-Simples-{}.eps'.format(PARAM.DIRETORIO_IMAGEM.valor, tipo_grafico, id_aglomerado), dpi=PARAM.RESOLUCAO_IMAGEM.valor, bbox_inches='tight')
    plt.close()


def composicao_tco(cenarios, tipo_grafico):

    global id_aglomerado

    plt.figure(figsize=(9.0, 5.5))

    infraestrutura = list()
    equipamentos = list()
    instalacao = list()
    energia = list()
    manutencao = list()
    aluguel = list()
    falhas = list()
    rotulos = list()

    # Legendas e Largura das Barras
    line_width = 0.5
    bar_width = 1.5

    if tipo_grafico == 'Radio':
        legenda = ['Infra.', 'Equip.', 'Inst.', 'Energ.', 'Manut.', 'Alug.', 'Falhas']
        label = 'RAN'
    else:
        legenda = ['Infra.', 'Equip.', 'Inst.', 'Energ.', 'Manut.', 'Espec.', 'Falhas']
        label = 'Backhaul'

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

        rotulos.append('Macro')
        rotulos.append('\n{}'.format(key))
        rotulos.append('Hetnet')

        if cenarios[key].tipo_cenario == 'Original':
            id_aglomerado = cenarios[key].id

    # Posicao das Barras
    posicao = np.array([0.0, 1.8, 4.3, 6.1, 8.6, 10.4, 12.9, 14.7])
    posicao_rotulo = np.array([0.0, 0.9, 1.8, 4.3, 5.2, 6.1, 8.6, 9.5, 10.4, 12.9, 13.8, 14.7])

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
    plt.xticks(posicao_rotulo, rotulos)
    plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
    plt.legend(legenda, loc='upper center', bbox_to_anchor=(0.5, 1.09), fancybox=True, shadow=True, ncol=7)
    plt.ylabel('{} TCO - Monetary Units ($)'.format(label))

    plt.savefig('{}TCO-{}-Composicao-{}.eps'.format(PARAM.DIRETORIO_IMAGEM.valor, tipo_grafico, id_aglomerado), dpi=PARAM.RESOLUCAO_IMAGEM.valor, bbox_inches='tight')
    plt.close()


def composicao_tco_porcentagem(cenarios, tipo_grafico):

    global ax, id_aglomerado, mypie2

    fig, axes = plt.subplots(2, len(cenarios), figsize=(12, 8))

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

    # Grupos
    group_names = ['CAPEX', 'OPEX']

    # Subgrupos
    if tipo_grafico == 'Radio':
        subgroup_names = ['Equip.', 'Inst.', 'Infra.', 'Manut.', 'Aluguel', 'Falhas', 'Energ.']
        label = 'RAN'
    else:
        subgroup_names = ['Equip.', 'Inst.', 'Infra.', 'Manut.', 'Espec.', 'Falhas', 'Energ.']
        label = 'Backhaul'

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

    for i, ax in enumerate(axes.flatten()):

        group_size = [infraestrutura[i] + equipamentos[i] + instalacao[i], energia[i] + manutencao[i] + aluguel[i] + falhas[i]]
        subgroup_size = [equipamentos[i], instalacao[i], infraestrutura[i], manutencao[i], aluguel[i], falhas[i], energia[i]]

        ax.axis('equal')
        mypie, _ = ax.pie(group_size, radius=1.3, labels=group_names, colors=[a(0.8), b(0.8)], startangle=180)
        plt.setp(mypie, width=0.5, edgecolor='white')

        mypie2, plt_labels, junk = ax.pie(subgroup_size, radius=1.3 - 0.3, autopct='%1.1f%%', labeldistance=0.9, colors=[a(0.65), a(0.5), a(0.3), b(0.65), b(0.5), b(0.3), b(0.1)], startangle=180)
        plt.setp(mypie2, width=0.7, edgecolor='white')
        plt.margins(50, 50)
        ax.set_title(rotulos[i])
        plt.setp(junk, size=8, weight='bold')

    plt.legend(mypie2, subgroup_names, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

    plt.savefig('{}TCO-{}-Porcentagem-{}.eps'.format(PARAM.DIRETORIO_IMAGEM.valor, tipo_grafico, id_aglomerado), dpi=PARAM.RESOLUCAO_IMAGEM.valor, bbox_inches='tight')
    plt.close()


def evolucao_tco(cenarios, tipo_grafico):

    global id_aglomerado

    chave_primeiro = list(cenarios)[0]
    tempo_analise = cenarios[chave_primeiro].tempo_analise
    tipo_rede_radio = ['Macro', 'Hetnet']

    # Legendas
    rotulos = np.arange(tempo_analise)
    legenda = list()

    posicao_macro = np.arange(0, tempo_analise*6, step=6)
    posicao_hetnet = posicao_macro + 2.3
    posicao_rotulos = (posicao_macro + posicao_hetnet)/2

    bar_width = 2.0
    line_width = 0.6

    # Cores dos Gráficos
    a, b = [plt.cm.Blues, plt.cm.Reds]

    if tipo_grafico == 'Radio':
        label = 'RAN'
    else:
        label = 'Backhaul'

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
        plt.xticks(posicao_rotulos, rotulos)
        plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
        plt.legend(legenda, loc='best')
        plt.ylabel('{} TCO - Monetary Units ($)'.format(label))
        plt.xlabel('Units of Time (t)')

        plt.savefig('{}TCO-Evolucao-{}-{}.eps'.format(PARAM.DIRETORIO_IMAGEM.valor, tipo_grafico, id_aglomerado), dpi=PARAM.RESOLUCAO_IMAGEM.valor, bbox_inches='tight')
        plt.close()


def fluxo_caixa_municipio(municipios):

    # Legendas
    names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    legenda = list()

    chave_primeiro = list(municipios)[0]
    tempo_analise = municipios[chave_primeiro].tempo_analise

    posicao_macro = np.arange(0, tempo_analise*6, step=6)
    posicao_hetnet = posicao_macro + 2.3
    posicao_legenda = (posicao_macro + posicao_hetnet)/2

    bar_width = 2.0
    line_width = 0.6

    # Cores dos Gráficos
    a, b = [plt.cm.Blues, plt.cm.Reds]

    for m in municipios:
        plt.figure(figsize=(8.0, 5.5))

        for key in municipios[m].cf:

            if key == 'Macro':
                posicao = posicao_macro
                cor = a(0.6)
            else:
                posicao = posicao_hetnet
                cor = b(0.6)

            legenda.append('{}'.format(key))

            plt.bar(posicao, municipios[m].cf[key], color=cor, width=bar_width, zorder=3, linewidth=line_width, edgecolor='black')

        # Custom X axis
        plt.xticks(posicao_legenda, names)
        plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
        plt.legend(legenda, loc='best')
        plt.ylabel('Monetary Units $')
        plt.xlabel('Units od Time (t)')

        plt.savefig('{}CF-{}.eps'.format(PARAM.DIRETORIO_IMAGEM.valor, m), dpi=PARAM.RESOLUCAO_IMAGEM.valor, bbox_inches='tight')
        plt.close()


def npv_municipio(municipios):

    global legenda

    # Inicialização
    names = list()
    valores_macro = list()
    valores_hetnet = list()

    # Visual do Gráfico
    bar_width = 1.5
    line_width = 0.6

    # Cores
    a, b = [plt.cm.Blues, plt.cm.Reds]

    # Posicao das Barras
    posicao_macro = np.array([0.0, 3.6, 7.2, 10.8])
    posicao_hetnet = np.array([1.6, 5.2, 8.8, 12.4])
    posicao_legenda = (posicao_macro + posicao_hetnet)/2

    plt.figure()

    for m in municipios:
        valores_macro.append(municipios[m].npv['Macro'].sum())
        valores_hetnet.append(municipios[m].npv['Hetnet'].sum())
        legenda = municipios[m].municipio.tipos_rede_radio
        names.append(m)

    plt.bar(posicao_macro, valores_macro, color=a(0.6), width=bar_width, zorder=3, linewidth=line_width, edgecolor='black')
    plt.bar(posicao_hetnet, valores_hetnet, color=b(0.6), width=bar_width, zorder=3, linewidth=line_width, edgecolor='black')

    # Custom X axis
    plt.xticks(posicao_legenda, names)
    plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
    plt.legend(legenda, loc='best')
    plt.ylabel('NPV (Moneraty Units $)')
    #plt.ylim(0, 18.0)

    plt.savefig('{}NPV.eps'.format(PARAM.DIRETORIO_IMAGEM.valor), dpi=PARAM.RESOLUCAO_IMAGEM.valor, bbox_inches='tight')
    plt.close()


def tco_municipio(municipios):

    global legenda

    # Inicialização
    names = list()
    valores_macro = list()
    valores_hetnet = list()

    # Visual do Gráfico
    bar_width = 1.5
    line_width = 0.6

    # Cores
    a, b = [plt.cm.Blues, plt.cm.Reds]

    # Posicao das Barras
    posicao_macro = np.array([0.0, 3.6, 7.2, 10.8])
    posicao_hetnet = np.array([1.6, 5.2, 8.8, 12.4])
    posicao_legenda = (posicao_macro + posicao_hetnet)/2

    plt.figure()

    for m in municipios:
        valores_macro.append(municipios[m].tco['Macro'].sum())
        valores_hetnet.append(municipios[m].tco['Hetnet'].sum())
        legenda = municipios[m].municipio.tipos_rede_radio
        names.append(m)

    plt.bar(posicao_macro, valores_macro, color=a(0.6), width=bar_width, zorder=3, linewidth=line_width, edgecolor='black')
    plt.bar(posicao_hetnet, valores_hetnet, color=b(0.6), width=bar_width, zorder=3, linewidth=line_width, edgecolor='black')

    # Custom X axis
    plt.xticks(posicao_legenda, names)
    plt.grid(linestyle='-', linewidth=1, zorder=0, axis='y', color='#E5E5E5')
    plt.legend(legenda, loc='best')
    plt.ylabel('TCO (Unidades Monetárias $)')

    plt.savefig('{}TCO.eps'.format(PARAM.DIRETORIO_IMAGEM.valor), dpi=PARAM.RESOLUCAO_IMAGEM.valor, bbox_inches='tight')
    plt.close()
