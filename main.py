import flet as ft
import asyncio
from backend import BancoDados
from plyer import notification
import flet_charts as charts

# Conecta ao banco de dados
db = BancoDados()

async def main(page: ft.Page):
    # --- CONFIGURAÇÕES DA PÁGINA ---
    page.title = "Antiprocrastinador Tech"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 500  
    page.window_height = 900
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # --- COMPONENTES VISUAIS ---
    lbl_timer = ft.Text("00:00", size=70, weight="bold", color=ft.Colors.BLUE_400)
    txt_tarefa = ft.TextField(label="Tarefa", hint_text="Ex: Estudar Listas", expand=True)
    txt_tech = ft.TextField(label="Tecnologia", hint_text="Ex: Python", expand=True)
    txt_minutos = ft.TextField(label="Minutos", value="25", width=100, text_align=ft.TextAlign.CENTER)

    tabela_relatorio = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Tech")),
            ft.DataColumn(ft.Text("Total (Min)"), numeric=True),
        ],
        rows=[]
    )

    grafico = charts.PieChart(
        sections=[],
        sections_space=2,
        center_space_radius=40,
        expand=True,
    )

    cores_lista = [
        ft.Colors.BLUE, ft.Colors.GREEN, ft.Colors.PURPLE, 
        ft.Colors.AMBER, ft.Colors.RED, ft.Colors.CYAN
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
                        ft.DataCell(ft.Text(str(total)))
                    ])
                )
                
                grafico.sections.append(
                    charts.PieChartSection(
                        value=total,
                        title=f"{tech}\n{total}m",
                        title_style=ft.TextStyle(size=10, weight="bold", color=ft.Colors.WHITE),
                        color=cor,
                        radius=50,
                    )
                )
            page.update()
        except Exception as ex:
            print(f"Erro ao atualizar dashboard: {ex}")

    # --- LÓGICA DO TEMPORIZADOR ---
    async def iniciar_foco(e):
        try:
            if not txt_tarefa.value or not txt_tech.value:
                page.snack_bar = ft.SnackBar(ft.Text("Preencha a tarefa e a tecnologia!"))
                page.snack_bar.open = True
                page.update()
                return

            minutos_foco = int(txt_minutos.value)
            segundos = minutos_foco * 60
            
            btn_iniciar.disabled = True
            txt_tarefa.disabled = True
            txt_tech.disabled = True
            txt_minutos.disabled = True
            page.update()

            while segundos > 0:
                mins, secs = divmod(segundos, 60)
                tempo_formatado = f"{mins:02d}:{secs:02d}"
                lbl_timer.value = tempo_formatado
                page.title = f"({tempo_formatado}) Foco: {txt_tech.value}"
                page.update()
                await asyncio.sleep(1)
                segundos -= 1

            db.salvar_progresso(txt_tarefa.value, txt_tech.value, minutos_foco)
            
            try:
                notification.notify(title="Fim do Ciclo!", message=f"Progresso salvo.")
            except: pass
            
            lbl_timer.value = "00:00"
            btn_iniciar.disabled = False
            txt_tarefa.disabled = False
            txt_tech.disabled = False
            txt_minutos.disabled = False
            page.update()
            atualizar_dashboard()

        except ValueError:
            txt_minutos.error_text = "Número inválido"
            page.update()

    # CORREÇÃO 1: ElevatedButton -> Button
    btn_iniciar = ft.Button(
        "INICIAR CICLO FOCO", 
        icon=ft.Icons.PLAY_ARROW_ROUNDED,
        on_click=iniciar_foco,
        style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_700),
        height=50
    )

    # --- MONTAGEM DA INTERFACE ---
    page.add(
        ft.Column([
            ft.Text("Antiprocrastinador 🚀", size=32, weight="bold"),
            ft.Text("Gerencie seu tempo", color=ft.Colors.GREY_400),
            ft.Divider(height=30),
            txt_tarefa,
            ft.Row([txt_tech, txt_minutos], spacing=10),
            
            # CORREÇÃO 2: Sintaxe de alinhamento atualizada
            ft.Container(
                content=lbl_timer, 
                padding=30, 
                alignment=ft.Alignment(0, 0) # Centralizado (x=0, y=0)
            ),
            
            btn_iniciar,
            
            ft.Divider(height=40),
            
            ft.Row([
                ft.Text("Seu Desempenho", size=22, weight="bold"),
                ft.IconButton(ft.Icons.REFRESH, on_click=atualizar_dashboard)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Container(content=grafico, height=250, width=400, bgcolor=ft.Colors.BLACK12, padding=20),
            ft.Container(content=tabela_relatorio)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    atualizar_dashboard()

if __name__ == "__main__":
    # CORREÇÃO 3: Usando run()
    ft.run(main)
