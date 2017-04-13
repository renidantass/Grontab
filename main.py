# coding:utf-8
import wx
from logging import basicConfig, info, INFO
from subprocess import check_output, CalledProcessError
from os import geteuid

basicConfig(level=INFO)

class MainWindow(wx.Frame):
    def __init__(self, parent, title,  size=None):
        super(MainWindow, self).__init__(parent, title=title, size=(450, 600))
        self.Centre()
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
        if self.current_crons > 0:
            msg = "\nVocê tem tarefa(s) já feita(s)"
            txt = wx.StaticText(self, label="%s" % (msg))
            txt.SetFont(default_font)
            sizer.Add(txt, 0, wx.CENTER, 0)
        else:
            msg = "\nVocê ainda não tem tarefa(s). Faça alguma!"
            txt = wx.StaticText(self, label="%s" % (msg))
            txt.SetFont(default_font)
            sizer.Add(txt, 0, wx.CENTER, 0)
        wsize = self.GetSize()[1]/1.5
        line = wx.StaticLine(self, size=(wsize, 10))
        sizer.Add(line, 0, wx.CENTER, 1)
        self.SetSizer(sizer)
        self.Show()

    def current_cron(self):
        """ Checando apenas tarefas do usuário root """
        try:
            tasks = check_output(['ls', '-l', '/var/spool/cron/crontabs'])
            tasks = int(tasks.replace('total ', '')) if 'total' in tasks else None
            return tasks
        except CalledProcessError:
            return None

    def create_task(self, e):
        pass

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
