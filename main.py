import flet as ft
import asyncio
from plyer import notification
import flet_charts as charts

# Importações internas do seu projeto
from database.create_db import criar_tabelas
from database.banco_dados import BancoDados

def inicializar_banco():
    criar_tabelas()

async def main(page: ft.Page):
    # Configura o banco na inicialização do app Flet
    inicializar_banco()
    db = BancoDados()

    # --- CONFIGURAÇÕES DA PÁGINA ---
    page.title = "Antiprocrastinador Tech"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 460
    page.window.height = 800
    page.scroll = ft.ScrollMode.HIDDEN
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.bgcolor = "#0B0E14" # Fundo dark premium
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
    }
    
    # Paleta de cores escolhida (Azul e Roxo)
    cor_primaria = ft.Colors.DEEP_PURPLE_ACCENT_400
    cor_secundaria = ft.Colors.INDIGO_600
    cor_fundo_card = "#161B22"

    # --- COMPONENTES VISUAIS PREMIUM ---
    lbl_timer = ft.Text("00:00", size=85, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE, font_family="RobotoSlab")
    
    txt_tarefa = ft.TextField(
        label="O que você vai estudar/fazer?", 
        hint_text="Ex: Listas em Python", 
        expand=True,
        border_radius=12,
        filled=True,
        bgcolor="#1E232B",
        border_color=cor_secundaria,
        prefix_icon=ft.Icons.TASK_ALT,
        focused_border_width=2,
    )
    
    txt_tech = ft.TextField(
        label="Tecnologia", 
        hint_text="Ex: Python", 
        expand=True,
        border_radius=12,
        filled=True,
        bgcolor="#1E232B",
        border_color=cor_secundaria,
        prefix_icon=ft.Icons.CODE,
        focused_border_width=2,
    )
    
    txt_minutos = ft.TextField(
        label="Minutos", 
        value="25", 
        width=110, 
        text_align=ft.TextAlign.CENTER,
        border_radius=12,
        filled=True,
        bgcolor="#1E232B",
        border_color=cor_secundaria,
        prefix_icon=ft.Icons.TIMER,
        focused_border_width=2,
    )

    tabela_relatorio = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Tecnologia", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Minutos Foco", weight=ft.FontWeight.BOLD), numeric=True),
        ],
        rows=[],
        border=ft.border.all(1, "#2C3440"),
        border_radius=10,
        heading_row_color="#1E232B",
        expand=True,
    )

    grafico = charts.PieChart(
        sections=[],
        sections_space=3,
        center_space_radius=40,
        expand=True,
    )

    cores_lista = [
        cor_primaria, cor_secundaria, ft.Colors.BLUE_400, 
        ft.Colors.CYAN, ft.Colors.PURPLE_300, ft.Colors.AMBER
    ]

    # --- LÓGICA DE ATUALIZAÇÃO ---
    def atualizar_dashboard(e=None):
        try:
            dados = db.obter_relatorio_semanal()
            tabela_relatorio.rows.clear()
            grafico.sections.clear()
            
            if not dados:
                page.update()
                return

            for i, (tech, total) in enumerate(dados):
                cor = cores_lista[i % len(cores_lista)]
                
                tabela_relatorio.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(tech)),
                        ft.DataCell(ft.Text(str(total), weight=ft.FontWeight.BOLD, color=cor))
                    ])
                )
                
                grafico.sections.append(
                    charts.PieChartSection(
                        value=float(total),
                        title=f"{total}m",
                        title_style=ft.TextStyle(size=12, weight="bold", color=ft.Colors.WHITE),
                        color=cor,
                        radius=50,
                        badge=ft.Container(
                            content=ft.Text(tech, size=10, weight="bold"),
                            bgcolor="#1E232B",
                            padding=4,
                            border_radius=5
                        ),
                        badge_position_percentage_offset=1.3,
                    )
                )
            page.update()
        except Exception as ex:
            print(f"Erro ao atualizar dashboard: {ex}")

    # --- LÓGICA DO TEMPORIZADOR ---
    async def iniciar_foco(e):
        try:
            if not txt_tarefa.value or not txt_tech.value:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Preencha a tarefa e a tecnologia para focar!"),
                    bgcolor=ft.Colors.RED_ACCENT_700,
                    behavior=ft.SnackBarBehavior.FLOATING,
                    margin=20,
                )
                page.open(page.snack_bar)
                page.update()
                return

            minutos_foco = int(txt_minutos.value)
            segundos = minutos_foco * 60
            
            btn_iniciar.disabled = True
            txt_tarefa.disabled = True
            txt_tech.disabled = True
            txt_minutos.disabled = True
            
            # Animação do botão e timer ao iniciar
            btn_iniciar.text = "FOCO EM ANDAMENTO"
            btn_iniciar.icon = ft.Icons.HOURGLASS_TOP
            btn_iniciar.style.bgcolor = ft.Colors.RED_ACCENT_400
            
            container_timer.shadow.color = ft.Colors.RED_ACCENT_400
            
            page.update()

            while segundos > 0:
                mins, secs = divmod(segundos, 60)
                tempo_formatado = f"{mins:02d}:{secs:02d}"
                lbl_timer.value = tempo_formatado
                page.title = f"({tempo_formatado}) Foco: {txt_tech.value}"
                page.update()
                await asyncio.sleep(1)
                segundos -= 1

            # Salva o progresso quando bate 00:00
            db.salvar_progresso(txt_tarefa.value, txt_tech.value, minutos_foco)
            
            try:
                notification.notify(
                    title="🚀 Fim do Ciclo de Foco!", 
                    message=f"Você concluiu {minutos_foco} min em {txt_tech.value}.",
                    app_name="Antiprocrastinador"
                )
            except: pass
            
            lbl_timer.value = "00:00"
            btn_iniciar.disabled = False
            txt_tarefa.disabled = False
            txt_tech.disabled = False
            txt_minutos.disabled = False
            
            btn_iniciar.text = "INICIAR CICLO DE FOCO"
            btn_iniciar.icon = ft.Icons.ROCKET_LAUNCH
            btn_iniciar.style.bgcolor = cor_primaria
            
            container_timer.shadow.color = cor_primaria
            
            page.title = "Antiprocrastinador Tech"
            page.update()
            atualizar_dashboard()

        except ValueError:
            txt_minutos.error_text = "!"
            page.update()

    btn_iniciar = ft.ElevatedButton(
        "INICIAR CICLO DE FOCO", 
        icon=ft.Icons.ROCKET_LAUNCH,
        on_click=iniciar_foco,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE, 
            bgcolor=cor_primaria,
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.padding.all(20),
            overlay_color=cor_secundaria
        ),
        width=page.window.width - 60, # Largura quase total
    )

    # --- ESTRUTURAS DE CONTAINERS PREMIUM ---
    
    # 1. Container do Relógio com Neon Glow
    container_timer = ft.Container(
        content=lbl_timer,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[cor_secundaria, ft.Colors.DEEP_PURPLE_800],
        ),
        border_radius=25,
        padding=40,
        alignment=ft.Alignment.CENTER,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=25, color=cor_primaria, offset=ft.Offset(0,0)),
        margin=ft.margin.symmetric(vertical=20)
    )

    # 2. Card de Entrada de Dados (Formulário)
    card_entradas = ft.Container(
        content=ft.Column([
            txt_tarefa,
            ft.Row([txt_tech, txt_minutos], spacing=15),
        ]),
        bgcolor=cor_fundo_card,
        padding=20,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK45, offset=ft.Offset(0,5)),
    )

    # 3. Seção de Desempenho
    card_desempenho = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Seu Desempenho Semanal", size=18, weight="bold", color=ft.Colors.INDIGO_100),
                ft.IconButton(ft.Icons.REFRESH_ROUNDED, icon_color=cor_primaria, on_click=atualizar_dashboard)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color="#2C3440"),
            ft.Container(content=grafico, height=200, padding=10),
            ft.Container(content=tabela_relatorio, padding=ft.padding.only(top=10))
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=cor_fundo_card,
        padding=25,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK45, offset=ft.Offset(0,5)),
        margin=ft.margin.only(bottom=40)
    )

    # Top Bar Header
    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.TIMER, color=cor_primaria, size=30),
            ft.Text("Antiprocrastinador", size=24, weight="bold", color=ft.Colors.WHITE, font_family="RobotoSlab"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.only(top=40, bottom=20, left=20, right=20),
        bgcolor="#07090D",
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK)
    )

    # --- MONTAGEM FINAL DA INTERFACE (SCROLLÁVEL) ---
    conteudo_scroll = ft.ListView(
        controls=[
            ft.Container(
                content=ft.Column([
                    container_timer,
                    btn_iniciar,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Spacing
                    card_entradas,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Spacing
                    card_desempenho
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
            )
        ],
        expand=True,
    )

    # Adiciona tudo à página
    page.add(
        header,
        conteudo_scroll
    )
    
    atualizar_dashboard()

if __name__ == "__main__":
    ft.run(main)