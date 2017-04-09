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

        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        save_menu = filemenu.Append(wx.ID_SAVE, 'Salvar', 'Salvar estado atual')
        exit_menu = filemenu.Append(wx.ID_EXIT, 'Sair', 'Sair da aplicação')
        menubar.Append(filemenu, '&Menu')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, exit_menu)
        self.current_cron()
        self.Show()

    def current_cron(self):
        """ Checando apenas tarefas do usuário root """
        try:
            tasks = check_output(['ls', '-l', '/var/spool/cron/crontabs'])
            tasks = int(tasks.replace('total ', '')) if 'total' in tasks else None
            return tasks
        except CalledProcessError:
            return None

    def OnQuit(self, e):
        self.Close()

if __name__ == '__main__':
    if geteuid() == 0:
        info("Rodando como usuário root")
        app = wx.App()
        MainWindow(None, title='Grontab')
        app.MainLoop()
    else:
        info("Rode como usuário root")
