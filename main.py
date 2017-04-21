# coding:utf-8
import wx
from logging import basicConfig, info, INFO
from subprocess import check_output, CalledProcessError
from os import geteuid, system

basicConfig(level=INFO)

class MainWindow(wx.Frame):
    def __init__(self, parent, title,  size=None):
        super(MainWindow, self).__init__(parent, title=title, style=wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX)
        self.Centre()
        self.SetMinSize((550, 250))
        self.SetMaxSize((551, 251))
        wsize = self.GetSize()[1]
        ID_ANOTHER = 0
        ico = wx.IconLocation(r'/usr/share/icons/tasks.png')
        default_font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.SetIcon(wx.IconFromLocation(ico))
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        create_menu = filemenu.Append(ID_ANOTHER, 'Criar\tCTRL+C', 'Criar uma nova tarefa')
        exit_menu = filemenu.Append(wx.ID_EXIT, 'Sair', 'Sair da aplicação')
        helpmenu = wx.Menu()
        credits_menu = helpmenu.Append(ID_ANOTHER+1, 'Créditos', 'Ver créditos')
        menubar.Append(filemenu, '&Arquivo')
        menubar.Append(helpmenu, '&Ajuda')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.on_quit, exit_menu)
        self.Bind(wx.EVT_MENU, self.create_task, create_menu)
        self.Bind(wx.EVT_MENU, self.show_credits, credits_menu)
        self.current_crons = self.current_cron()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_one = wx.BoxSizer(wx.VERTICAL)
        sizer_two = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSizer(sizer_one)
        sizer.AddSizer(sizer_two)
        if self.current_crons > 0:
            msg = "\t\t\t\t\tVocê tem tarefa(s) já feita(s)\n"
            self.txt = wx.StaticText(self, label="%s" % (msg))
            self.txt.SetFont(default_font)
            sizer_one.Add(self.txt, 0, wx.ALIGN_CENTER, 0)
        else:
            msg = "\t\t\tVocê ainda não tem tarefa(s). Faça alguma!\n"
            self.txt = wx.StaticText(self, label="%s" % (msg))
            self.txt.SetFont(default_font)
            sizer_one.Add(self.txt, 0, wx.ALIGN_CENTER , 0)
        h = wx.StaticText(self, label="Hora")
        self.hora_escolha = wx.SpinCtrl(self, value='0', min=0, max=24)
        sizer_two.Add(h, 0, wx.CENTER, 1)
        sizer_two.Add(self.hora_escolha, 0, wx.CENTER, 2)
        m = wx.StaticText(self, label="Minuto")
        self.min_escolha = wx.SpinCtrl(self, value='0', min=0, max=60)
        sizer_two.Add(m, 0, wx.CENTER, 2)
        sizer_two.Add(self.min_escolha, 0, wx.CENTER, 2)
        d = wx.StaticText(self, label="Dia")
        self.dia_escolha = wx.SpinCtrl(self, value='1', min=1, max=31)
        sizer_two.Add(d, 0, wx.CENTER, 3)
        sizer_two.Add(self.dia_escolha, 0, wx.CENTER, 3)
        mes = wx.StaticText(self, label="Mês")
        self.mes_escolha = wx.SpinCtrl(self, value='1', min=1, max=12)
        sizer_two.Add(mes, 0, wx.CENTER, 3)
        sizer_two.Add(self.mes_escolha, 0, wx.CENTER, 3)
        dia_semana = wx.StaticText(self, label="Dia da semana")
        self.dia_semana_escolha = wx.SpinCtrl(self, value='1', min=1, max=7)
        sizer.Add(dia_semana, 0, wx.CENTER, 4)
        sizer.Add(self.dia_semana_escolha,0, wx.CENTER, 4)
        scp = wx.StaticText(self, label="Script/comando")
        self.scp_cmd = wx.TextCtrl(self, size=(wsize-25, 30))
        sizer.Add(scp, 0, wx.CENTER, 4)
        sizer.Add(self.scp_cmd, 0, wx.CENTER, 4)
        self.tornar = wx.CheckBox(self, label="Tornar executável")
        sizer.Add(self.tornar, 0, wx.CENTER, 5)
        btn = wx.Button(self, label="Criar tarefa")
        self.Bind(wx.EVT_BUTTON, self.make_executable, btn)
        self.Bind(wx.EVT_BUTTON, self.create_task, btn)
        sizer.Add(btn, 0, wx.CENTER, 5)
        self.SetSizer(sizer)
        self.Show()

    def current_cron(self):
        """ Checando apenas tarefas do usuário root """
        try:
            tasks = check_output(['ls', '-l', '/var/spool/cron/crontabs'])
            tasks = tasks[:tasks.find('-'):]
            tasks = int(tasks.replace('total ', '')) if 'total' in tasks else None
            return tasks
        except CalledProcessError:
            return None

    def create_task(self, e):
        cmd = 'sudo echo "%s %s %s %s %s %s" > /var/spool/cron/crontabs/root' % (self.min_escolha.GetValue(), 
                self.hora_escolha.GetValue(), self.dia_escolha.GetValue(), self.mes_escolha.GetValue(), self.dia_semana_escolha.GetValue(),
                self.scp_cmd.GetValue())
        execution = system(cmd)
        if execution == 0:
            print("Tarefa criada")
            self.update_status()

    def make_executable(self, e):
        valor = self.tornar.GetValue()
        cmd = self.scp_cmd.GetValue()
        if valor:
            try:
                executable = check_output(['chmod', '+x', cmd])
                info(executable)
            except CalledProcessError:
                wx.MessageDialog(self, "Arquivo não encontrado", "Erro", wx.OK_DEFAULT | wx.ICON_ERROR).ShowModal()

    def update_status(self):
        self.txt.SetLabel("\t\t\t\t\tVocê tem tarefa(s) já feita(s)\n")

    def on_quit(self, e):
        self.Close()

    def show_credits(self, e):
        license = """ Copyright (c) 2017 Reni A. Dantas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. """
        credits_info = wx.AboutDialogInfo()
        credits_info.SetName("Grontab")
        credits_info.SetVersion("0.0.1")
        credits_info.SetDescription("Um programa que visa facilitar o uso da ferramenta cron.")
        credits_info.SetCopyright("(C) 2017")
        credits_info.SetWebSite("github.com/renix1/Grontab")
        credits_info.SetLicense(license)
        credits_info.AddDeveloper("Reni A. Dantas")
        wx.AboutBox(credits_info)

if __name__ == '__main__':
    if geteuid() == 0:
        info("Rodando como usuário root")
        app = wx.App()
        MainWindow(None, title='Automatizador de tarefas')
        app.MainLoop()
    else:
        info("Rode como usuário root")
