import calendar
import platform
from datetime import datetime, date, timedelta
import tkinter as tk
import locale
from tkinter import *
from tkinter import messagebox, ttk, simpledialog
from ponto.models import RegistroPonto
from openpyxl import Workbook
from openpyxl.styles import Alignment
from tkinter import filedialog


class RegistroPontoScreen:
    def __init__(self, root):
        self.root = root
        self.data_atual = datetime.today().replace(day=1)
        self.mes = self.data_atual.month
        self.ano = self.data_atual.year
        self.preencher_saida = tk.BooleanVar(value=True)
        self.registro_selecionado = None

        sistema = platform.system()
        if sistema == 'Windows':
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
        else:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


        self.painel = PanedWindow(self.root, orient=HORIZONTAL, sashrelief=RAISED)
        self.painel.pack(fill=BOTH, expand=True)

        # Frame esquerdo (formulário) — maior verticalmente
        self.frame_formulario = Frame(self.painel, padx=10, pady=10, width=300, height=600)
        self.frame_formulario.pack_propagate(False)  # Impede que o frame encolha para caber o conteúdo
        self.painel.add(self.frame_formulario)

        # Frame direito (lista) — grande para exibir todos os dias
        self.frame_lista = Frame(self.painel, padx=10, pady=10, width=600, height=600)
        self.frame_lista.pack_propagate(False)
        self.painel.add(self.frame_lista)

        self.criar_formulario()
        self.criar_lista()
        self.carregar_lista()



    def criar_formulario(self):
        Label(self.frame_formulario, text="Dia").grid(row=0, column=0, sticky=W)
        self.entry_dia = Entry(self.frame_formulario, width=5)
        self.entry_dia.grid(row=0, column=1)

        Label(self.frame_formulario, text="Mês").grid(row=1, column=0, sticky=W)
        self.entry_mes = Entry(self.frame_formulario, width=5)
        self.entry_mes.grid(row=1, column=1)

        Label(self.frame_formulario, text="Ano").grid(row=2, column=0, sticky=W)
        self.entry_ano = Entry(self.frame_formulario, width=6)
        self.entry_ano.grid(row=2, column=1)

        Label(self.frame_formulario, text="Entrada").grid(row=3, column=0, sticky=W)
        self.entry_entrada = Entry(self.frame_formulario, width=8)
        self.entry_entrada.grid(row=3, column=1)
        self.entry_entrada.bind("<FocusOut>", self.verificar_valor_saida)

        Label(self.frame_formulario, text="Início Intervalo").grid(row=4, column=0, sticky=W)
        self.entry_inicio_intervalo = Entry(self.frame_formulario, width=8)
        self.entry_inicio_intervalo.grid(row=4, column=1)

        Label(self.frame_formulario, text="Fim Intervalo").grid(row=5, column=0, sticky=W)
        self.entry_fim_intervalo = Entry(self.frame_formulario, width=8)
        self.entry_fim_intervalo.grid(row=5, column=1)

        Label(self.frame_formulario, text="Saída").grid(row=6, column=0, sticky=W)
        self.entry_saida = Entry(self.frame_formulario, width=8)
        self.entry_saida.grid(row=6, column=1)

        self.salvarbutton = Button(self.frame_formulario, text="Salvar", command=self.salvar)
        self.salvarbutton.grid(row=7, column=0, columnspan=2, pady=10)
        self.salvarbutton.bind("<Return>", lambda event: self.salvar())

        Button(self.frame_formulario, text="Exportar para Excel", command=self.exportar_excel).grid(row=8, column=0, columnspan=2, pady=5)

        checkbox = tk.Checkbutton(self.frame_formulario, text="Preencher Saída", variable=self.preencher_saida, ).grid(row=9, column=0, columnspan=2, pady=5)

        campos_hora = [
            self.entry_entrada,
            self.entry_inicio_intervalo,
            self.entry_fim_intervalo,
            self.entry_saida
        ]

        for campo in campos_hora:
            campo.bind("<KeyRelease>", lambda e, entry=campo: self.formatar_hora(e, entry))



    def criar_lista(self):
        topo = Frame(self.frame_lista)
        topo.pack()

        Button(topo, text="<", command=self.mes_anterior).pack(side=LEFT)
        self.label_mes = Label(topo, text="")
        self.label_mes.pack(side=LEFT, padx=10)
        Button(topo, text=">", command=self.proximo_mes).pack(side=LEFT)

        self.tree = ttk.Treeview(self.frame_lista,
                                 columns=("dia", "entrada", "inicio_intervalo", "fim_intervalo", "saida"),
                                 show="headings")
        self.tree.heading("dia", text="Dia")
        self.tree.heading("entrada", text="Entrada")
        self.tree.heading("inicio_intervalo", text="Início Intervalo")
        self.tree.heading("fim_intervalo", text="Fim Intervalo")
        self.tree.heading("saida", text="Saída")
        self.tree.pack(padx=5, pady=10, fill=BOTH, expand=True)
        self.tree.column("dia", width=100, stretch=False)
        self.tree.column("entrada", width=100, stretch=False)
        self.tree.column("inicio_intervalo", width=100, stretch=False)
        self.tree.column("fim_intervalo", width=100, stretch=False)
        self.tree.column("saida", width=100, stretch=False)
        self.tree.bind("<Button-3>", self.menu_contexto)

        self.menu = tk.Menu(self.tree, tearoff=0)
        self.menu.add_command(label="Editar", command=self.editar_registro)
        self.menu.add_command(label="Excluir", command=self.excluir_registro)
        self.menu.add_command(label="Marcar Folga/Atestado", command=self.marcar_folga_atestado)



    def carregar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.label_mes.config(text=self.data_atual.strftime("%B/%Y").capitalize())

        dias_uteis = self.get_dias_uteis(self.ano, self.mes)

        for dia in dias_uteis:
            try:
                ponto = RegistroPonto.objects.get(dia=dia.day, mes=dia.month, ano=dia.year)
                if ponto.status == 'normal':
                    self.tree.insert("", "end", values=(
                        dia.day,
                        ponto.entrada.strftime("%H:%M"),
                        ponto.inicio_intervalo.strftime("%H:%M"),
                        ponto.fim_intervalo.strftime("%H:%M"),
                        ponto.saida.strftime("%H:%M")
                    ))
                else:
                    self.tree.insert("", "end", values=(
                        dia.day,
                        ponto.status.capitalize(),
                        ponto.status.capitalize(),
                        ponto.status.capitalize(),
                        ponto.status.capitalize()
                    ))
            except RegistroPonto.DoesNotExist:
                self.tree.insert("", "end", values=(
                    dia.day,
                    "Sem registro",
                    "Sem registro",
                    "Sem registro",
                    "Sem registro"
                ), tags=('sem_registro',))
        #limpar os campos de hora
        self.entry_dia.delete(0, END)
        self.entry_entrada.delete(0, END)
        self.entry_inicio_intervalo.delete(0, END)
        self.entry_fim_intervalo.delete(0, END)
        self.entry_saida.delete(0, END)

        hoje = datetime.today()
        mes_atual = hoje.month
        ano_atual = hoje.year
        if self.entry_mes.get() == "":
            self.entry_mes.insert(0, mes_atual)
            self.mes_atual = mes_atual
        if self.entry_ano.get() == "":
            self.entry_ano.insert(0, ano_atual)
            self.ano_atual = ano_atual

        self.entry_inicio_intervalo.insert(0, "12:00")
        self.entry_fim_intervalo.insert(0, "13:00")



    def salvar(self):
        try:
            dia = int(self.entry_dia.get())
            mes = int(self.entry_mes.get())
            ano = int(self.entry_ano.get())

            if not self.validar_data(dia, mes, ano):
                messagebox.showerror("Erro", "Data inválida (dia, mês ou ano incorretos).")
                return

            entrada = self.entry_entrada.get().strip() or "08:00"
            intervalo_ini = self.entry_inicio_intervalo.get().strip() or "12:00"
            intervalo_fim = self.entry_fim_intervalo.get().strip() or "13:00"
            saida = self.entry_saida.get().strip() or "17:00"

            campos = {
                "Entrada": entrada,
                "Início do Intervalo": intervalo_ini,
                "Fim do Intervalo": intervalo_fim,
                "Saída": saida,
            }

            for nome, valor in campos.items():
                if not self.validar_horario(valor):
                    messagebox.showerror("Erro", f"Campo '{nome}' inválido. Use o formato HH:MM.")
                    return

            registro, _ = RegistroPonto.objects.update_or_create(
                dia=dia, mes=mes, ano=ano,
                defaults={
                    'entrada': entrada,
                    'inicio_intervalo': intervalo_ini,
                    'fim_intervalo': intervalo_fim,
                    'saida': saida
                }
            )
            messagebox.showinfo("Sucesso", "Registro salvo.")
            self.carregar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")



    def get_dias_uteis(self, ano, mes):
        dias = []
        _, num_dias = calendar.monthrange(ano, mes)
        for dia in range(1, num_dias + 1):
            data = date(ano, mes, dia)
            if data.weekday() < 5:
                dias.append(data)
        return dias



    def mes_anterior(self):
        if self.mes == 1:
            self.mes = 12
            self.ano -= 1
        else:
            self.mes -= 1
        self.data_atual = self.data_atual.replace(year=self.ano, month=self.mes)
        self.carregar_lista()



    def proximo_mes(self):
        if self.mes == 12:
            self.mes = 1
            self.ano += 1
        else:
            self.mes += 1
        self.data_atual = self.data_atual.replace(year=self.ano, month=self.mes)
        self.carregar_lista()



    def menu_contexto(self, event):
        try:
            item = self.tree.identify_row(event.y)
            if item:
                self.tree.selection_set(item)
                values = self.tree.item(item, 'values')
                dia = int(values[0])  # O dia está na primeira coluna
                try:
                    self.registro_selecionado = RegistroPonto.objects.get(dia=dia, mes=self.mes, ano=self.ano)
                except RegistroPonto.DoesNotExist:
                    self.registro_selecionado = None
                self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()



    def get_data_selecionada(self, item_id):
        try:
            values = self.tree.item(item_id, 'values')
            dia = int(values[0])  # O primeiro valor da tupla é o dia
            return RegistroPonto.objects.get(dia=dia, mes=self.mes, ano=self.ano)
        except Exception:
            return None



    def editar_registro(self):
        if self.registro_selecionado:
            r = self.registro_selecionado
            self.entry_dia.delete(0, END)
            self.entry_dia.insert(0, r.dia)

            self.entry_mes.delete(0, END)
            self.entry_mes.insert(0, r.mes)

            self.entry_ano.delete(0, END)
            self.entry_ano.insert(0, r.ano)

            self.entry_entrada.delete(0, END)
            self.entry_entrada.insert(0, r.entrada.strftime("%H:%M"))

            self.entry_inicio_intervalo.delete(0, END)
            self.entry_inicio_intervalo.insert(0, r.inicio_intervalo.strftime("%H:%M"))

            self.entry_fim_intervalo.delete(0, END)
            self.entry_fim_intervalo.insert(0, r.fim_intervalo.strftime("%H:%M"))

            self.entry_saida.delete(0, END)
            self.entry_saida.insert(0, r.saida.strftime("%H:%M"))



    def excluir_registro(self):
        if self.registro_selecionado:
            if messagebox.askyesno("Confirmação", "Deseja excluir este registro?"):
                self.registro_selecionado.delete()
                self.carregar_lista()
                messagebox.showinfo("Sucesso", "Registro excluído.")



    def validar_horario(self, texto):
        try:
            partes = texto.strip().split(":")
            if len(partes) != 2:
                return False
            horas, minutos = int(partes[0]), int(partes[1])
            return 0 <= horas <= 23 and 0 <= minutos <= 59
        except:
            return False



    def validar_data(self, dia, mes, ano):
        try:
            date(ano, mes, dia)
            return True
        except ValueError:
            return False

    def exportar_excel(self):
        try:
            mes = self.mes
            ano = self.ano

            registros = RegistroPonto.objects.filter(mes=mes, ano=ano).order_by('dia')

            if not registros.exists():
                messagebox.showwarning("Aviso", "Não há registros para exportar.")
                return

            wb = Workbook()
            ws = wb.active
            ws.title = "Registros"

            titulo = f"Registro para o período de {mes:02d}/{ano}"
            ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=5)
            ws["A1"] = titulo
            ws["A1"].alignment = Alignment(horizontal="center")

            headers = ["Dia", "Entrada", "Início do Intervalo", "Fim do Intervalo", "Saída"]
            ws.append(headers)

            for registro in registros:
                if hasattr(registro, 'status') and registro.status in ['atestado', 'folga']:
                    entrada = "Atestado" if registro.status == 'atestado' else "Folga/Falta"
                    inicio_intervalo = entrada
                    fim_intervalo = entrada
                    saida = entrada
                else:
                    entrada = registro.entrada.strftime("%H:%M") if registro.entrada else "N/A"
                    inicio_intervalo = registro.inicio_intervalo.strftime(
                        "%H:%M") if registro.inicio_intervalo else "N/A"
                    fim_intervalo = registro.fim_intervalo.strftime("%H:%M") if registro.fim_intervalo else "N/A"
                    saida = registro.saida.strftime("%H:%M") if registro.saida else "N/A"

                ws.append([
                    registro.dia,
                    entrada,
                    inicio_intervalo,
                    fim_intervalo,
                    saida,
                ])

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if file_path:
                wb.save(file_path)
                messagebox.showinfo("Sucesso", f"Arquivo exportado para:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")



    def formatar_hora(self, event, entry):
        valor = entry.get().replace(":", "")[:4]

        if not valor.isdigit():
            entry.delete(0, tk.END)
            return

        if len(valor) >= 3:
            valor = valor[:2] + ":" + valor[2:]
        entry.delete(0, tk.END)
        entry.insert(0, valor)



    def marcar_folga_atestado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Nenhum dia selecionado.")
            return

        item = selected[0]
        values = self.tree.item(item, 'values')
        dia = int(values[0])  # O dia está na primeira coluna

        tipo_ausencia = simpledialog.askstring("Marcar Ausência", "Digite 'folga', 'falta', 'feriado' ou 'atestado':", parent=self.root)
        if tipo_ausencia not in ['folga', 'falta', 'feriado', 'atestado']:
            messagebox.showerror("Erro", "Tipo inválido. Use 'folga', 'falta', 'feriado' ou 'atestado'.")
            return

        try:
            registro = RegistroPonto.objects.get(dia=dia, mes=self.mes, ano=self.ano)
            registro.status = tipo_ausencia
            registro.entrada = None
            registro.inicio_intervalo = None
            registro.fim_intervalo = None
            registro.saida = None
            registro.save()
        except RegistroPonto.DoesNotExist:
            registro = RegistroPonto(
                dia=dia,
                mes=self.mes,
                ano=self.ano,
                status=tipo_ausencia
            )
            registro.save()

        self.carregar_lista()



    def verificar_valor_saida(self, event=None):
        try:
            if self.preencher_saida.get():
                valor = self.entry_entrada.get().strip()
                entrada = datetime.strptime(valor, "%H:%M")
                entrada_padrao = datetime.strptime("08:00", "%H:%M")
                saida_padrao = datetime.strptime("17:48", "%H:%M")

                if entrada < entrada_padrao:
                    minutos_adiantado = int((entrada_padrao - entrada).total_seconds() // 60)
                    nova_saida = saida_padrao - timedelta(minutes=minutos_adiantado)
                else:
                    nova_saida = saida_padrao

                self.entry_saida.delete(0, tk.END)
                self.entry_saida.insert(0, nova_saida.strftime("%H:%M"))
        except ValueError:
            messagebox.showerror("Erro", "Formato de hora inválido. Use HH:MM.")
