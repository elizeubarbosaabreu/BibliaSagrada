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


# ------------- Imagens--------------------------------------

icon = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAAEgBckRAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAADZBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDQuMi4yLWMwNjMgNTMuMzUyNjI0LCAyMDA4LzA3LzMwLTE4OjA1OjQxICAgICAgICAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6eG1wUmlnaHRzPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvcmlnaHRzLyIKICAgIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIKICAgIHhtbG5zOklwdGM0eG1wQ29yZT0iaHR0cDovL2lwdGMub3JnL3N0ZC9JcHRjNHhtcENvcmUvMS4wL3htbG5zLyIKICAgeG1wUmlnaHRzOldlYlN0YXRlbWVudD0iaHR0cDovL2Jsb2cuYWRkaWN0ZWR0b2NvZmZlZS5kZSIKICAgcGhvdG9zaG9wOkF1dGhvcnNQb3NpdGlvbj0iIj4KICAgPGRjOnJpZ2h0cz4KICAgIDxyZGY6QWx0PgogICAgIDxyZGY6bGkgeG1sOmxhbmc9IngtZGVmYXVsdCI+wqkgICAgICAgICAgICYjeEE7IDIwMDkgYnkgT2xpdmVyIFR3YXJkb3dza2k8L3JkZjpsaT4KICAgIDwvcmRmOkFsdD4KICAgPC9kYzpyaWdodHM+CiAgIDxkYzpjcmVhdG9yPgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaT5PbGl2ZXIgVHdhcmRvd3NraTwvcmRmOmxpPgogICAgPC9yZGY6U2VxPgogICA8L2RjOmNyZWF0b3I+CiAgIDxkYzp0aXRsZT4KICAgIDxyZGY6QWx0PgogICAgIDxyZGY6bGkgeG1sOmxhbmc9IngtZGVmYXVsdCIvPgogICAgPC9yZGY6QWx0PgogICA8L2RjOnRpdGxlPgogICA8eG1wUmlnaHRzOlVzYWdlVGVybXM+CiAgICA8cmRmOkFsdD4KICAgICA8cmRmOmxpIHhtbDpsYW5nPSJ4LWRlZmF1bHQiLz4KICAgIDwvcmRmOkFsdD4KICAgPC94bXBSaWdodHM6VXNhZ2VUZXJtcz4KICAgPElwdGM0eG1wQ29yZTpDcmVhdG9yQ29udGFjdEluZm8KICAgIElwdGM0eG1wQ29yZTpDaUFkckV4dGFkcj0iIgogICAgSXB0YzR4bXBDb3JlOkNpQWRyQ2l0eT0iIgogICAgSXB0YzR4bXBDb3JlOkNpQWRyUmVnaW9uPSIiCiAgICBJcHRjNHhtcENvcmU6Q2lBZHJQY29kZT0iIgogICAgSXB0YzR4bXBDb3JlOkNpQWRyQ3RyeT0iIgogICAgSXB0YzR4bXBDb3JlOkNpVGVsV29yaz0iIgogICAgSXB0YzR4bXBDb3JlOkNpRW1haWxXb3JrPSIiCiAgICBJcHRjNHhtcENvcmU6Q2lVcmxXb3JrPSIiLz4KICA8L3JkZjpEZXNjcmlwdGlvbj4KIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0idyI/PgiL5zQAAAlfSURBVGjevVlZbFTnFTZr8xg84xkvFJtFGAO2zOKFsngBm2IPOzYYHKki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'

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
    [sg.Image(icon),
     sg.Text('Livro:'),
     sg.Combo(livros_da_bilia, default_value='GN', key='-lb-'),     
     sg.Text('Capítulo:'),         
     sg.Combo(['1'] + [x for x in range(2, 151)], default_value='1', key='-cp-', size=(4,1)),     
     sg.Text('Versículo:', font=('Arial', 15)),
     sg.Combo([''] + [x for x in range(1, 180)], default_value='', key='-v-', size=(3,1)),
     sg.Text('Versão:', font=('Arial', 15)),
     sg.Combo(versoes, default_value='NVI', key='-vs-'),
     sg.Button('Ler'),
     sg.Stretch()],
    [sg.Multiline(txt, font=('Arial', 15), size=(400, 150), autoscroll=False, key='-txt-')]
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
        
        if v == '':        
            response = requests.get(f'https://www.bibliaonline.com.br/{vs}/{lb}/{cp}')            
        else:
            response = requests.get(f'https://www.bibliaonline.com.br/{vs}/{lb}/{cp}/{v}')
        soup = BeautifulSoup(response.text, 'html.parser').article.div        
        soup = str(soup.text)
        txt = soup.replace('Compartilhar Criar Imagem', '')
        window['-txt-'].update(txt)
        window['-v-'].update('')
        
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
        sg.popup_timed('CTRL+C CTRL+V', 'Conteúdo Copiado para área de Transferência\nUse CTRL+V para colar one desejar!!!')

# ----------- Fechar tela -------------
    elif event == sg.WINDOW_CLOSED or event == 'Sair':
        break

window.close()
