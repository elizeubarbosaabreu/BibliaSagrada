import requests, clipboard, webbrowser
import PySimpleGUI as sg
from bs4 import BeautifulSoup
# 
#      ____  _ _     _ _         ____                            _       
#     | __ )(_) |__ | (_) __ _  / ___|  __ _  __ _ _ __ __ _  __| | __ _ 
#     |  _ \| | '_ \| | |/ _` | \___ \ / _` |/ _` | '__/ _` |/ _` |/ _` |
#     | |_) | | |_) | | | (_| |  ___) | (_| | (_| | | | (_| | (_| | (_| |
#     |____/|_|_.__/|_|_|\__,_| |____/ \__,_|\__, |_|  \__,_|\__,_|\__,_|
#                                            |___/                       
#     Software desenvolvido inteiramente em Python por Elizeu Babrosa Abreu
#     Leia a Bíblia, Ame a Bíblia. Ela é a Palavra de Deus

# -------------- Lista dos Livros da Bíblia -----------------
livros_da_bilia = [
    # Abreviação dos livros do AT
    'GN', 'EX', 'LV', 'NM', 'DT', 'JS', 'JZ', 'RT', '1SM', '2SM', '1RS',
    '2RS', '1CR', '2CR', 'ED', 'NE', 'ET', 'JÓ', 'SL', 'PV', 'EC', 'CT', 'IS', 'JR',
    'LM', 'EZ', 'DN', 'OS', 'JL', 'AM', 'OB', 'JN', 'MQ', 'NA', 'HC', 'SF', 'AG', 'ZC', 'ML',
    # Abreviação dos livros do NT
    'MT', 'MC', 'LC', 'JO', 'AT', 'RM', '1CO', '2CO', 'GL', 'EF', 'FP', 'CL', '1TS', '2TS',
    '1TM', '2TM', 'TT', 'FM', 'HB', 'TG', '1PE', '2PE', '1JO', '2JO', '3JO', 'JD', 'AP']

# ------------- Lista das versões e traduções da Bíblia -----
vs = ['NVI', 'AKJV', 'BHS', 'TB']
versoes = sorted(vs)

# ----------- Gera o texto de João 3 e 16 caso o usuário esteja conectado -----
vs = 'NAA'
lb = 'JO'
cp = '3'
v = '16'

try:
    response = requests.get(f'https://www.bibliaonline.com.br/{vs}/{lb}/{cp}/{v}')
    soup = BeautifulSoup(response.text, 'html.parser').article.div
    soup = str(soup.text)
    txt = soup.replace('Compartilhar Criar Imagem', '')
except:
    txt = f'''{"-=" * 30}
ERRO DE CONEXÃO
{"-=" * 30}
Não foi possível conectar ao servidor, verifique a conexão, feche e abra este software novamente...
'''

# -------- Interface Gráfica via PySimpleGui -----------

sg.theme('SystemDefault')

menu = [
    ['&Arquivo', ['&Salvar', '&Copiar', '&Sair']],    
    ['&Ajuda', [['&Manual'], '&Autor', ['&GitHub', '&Linkedin']]]
    ]

layout = [
    [sg.Menu(menu)],
    [sg.T('Livro:'),
     sg.Combo(livros_da_bilia, default_value='GN', key='-lb-'),
     sg.T('Capítulo:'),
     sg.Input('1', key='-cp-', size=(3,1)),
     sg.T('Versículo:'),
     sg.Input('0', key='-v-', size=(3,1)),
     sg.T('Versão:'),
     sg.Combo(versoes, default_value='NVI', key='-vs-'),
     sg.B('Ler')],
    [sg.Multiline(txt, font=('Arial', 15), size=(400, 150), autoscroll=True, key='-txt-')]
    ]

window = sg.Window('Bíblia Sagrada', layout, size=(640, 400), resizable=True)

while True:
    event, values = window.read()
# ------------ Localizar texto ----------    
    if event == 'Ler':        
        vs = values['-vs-']
        lb = values['-lb-']
        cp = values['-cp-']
        v = values['-v-']
        
        if v == '0':        
            response = requests.get(f'https://www.bibliaonline.com.br/{vs}/{lb}/{cp}')            
        else:
            response = requests.get(f'https://www.bibliaonline.com.br/{vs}/{lb}/{cp}/{v}')
        soup = BeautifulSoup(response.text, 'html.parser').article.div        
        soup = str(soup.text)
        txt = soup.replace('Compartilhar Criar Imagem', '')
        window['-txt-'].update(txt)
        window['-v-'].update('0')
        
# ------------- Abrir Linkedin ----------------        
    elif event == 'Linkedin':
        webbrowser.open_new_tab('https://www.linkedin.com/in/elizeu-barbosa-abreu-69965b218/')
        
# -------------- Abrir GitHub -------------------    
    elif event == 'GitHub':
        webbrowser.open_new_tab('https://github.com/elizeubarbosaabreu')
        
# -------------- Salvar texto Bíblico como txt ----------        
    elif event == 'Salvar':
        conteudo = values['-txt-']
        filename = sg.popup_get_file('Salvar texto',
                                       title='Salvar Arquivo',
                                       file_types=(("texto plano","*.txt"),),
                                       save_as = True,)
        with open(filename, 'w', encoding='utf8') as f:
            f.write(conteudo)

# ------------ Manual -------------------
    elif event == 'Manual':
        conteudo = f'''{"-=" * 30}
MANUAL DA BÍBLIA
{"-=" * 30}
* Esta Bíblia foi escrita inteiramente em python e usa o site <www.bibliaonline.com.br> para realizar as requisições

* Outras versões da Bíblia Sagrada pode ser visualizadas no site...

* Ore e Leia a Bíblia todos os dias. Deus falará com você e fará grande mudanças em sua vida!!!
'''
        window['-txt-'].update(conteudo)
 
# ------------ Copiar texto -------------
    elif event == 'Copiar':
        conteudo = values['-txt-']
        clipboard.copy(conteudo)
        sg.popup_timed('CTRL+C CTRL+V', 'Conteúdo Copiado para área de Transferência')

# ----------- Fechar tela -------------
    elif event == sg.WINDOW_CLOSED or event == 'Sair':
        break

window.close()
