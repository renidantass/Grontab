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
        self.Bind(wx.EVT_MENU, self.OnQuit, exit_menu)
        self.Bind(wx.EVT_MENU, self.CreateTask, create_menu)
        self.current_crons = self.current_cron()
        sizer = wx.BoxSizer(wx.VERTICAL)
        if self.current_crons > 0:
            txt = wx.StaticText(self, label="Você tem tarefas já feitas")
            txt.SetFont(default_font)
            sizer.Add(txt, 0, wx.CENTER, 0)
        else:
            txt = wx.StaticText(self, label="Você ainda não tem tarefas. Faça alguma!")
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

    def CreateTask(self, e):
        pass

    def OnQuit(self, e):
        self.Close()

if __name__ == '__main__':
    if geteuid() == 0:
        info("Rodando como usuário root")
        app = wx.App()
        MainWindow(None, title='Automatizador de tarefas')
        app.MainLoop()
    else:
        info("Rode como usuário root")
