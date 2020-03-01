import time
#from multiprocessing import Pool
#from multiprocessing import freeze_support
from threading import Thread
import numpy as np
import random
import win32gui, win32con

CONFIGFILE = '.\lwp.conf'
class DriftWords:
    def __init__(self):
        self.Words = []
        self.Coors = []
        self.Velocities = []
        self.Accelerations = []
        self.__XMINC = 0
        self.__XMAXC = 3560#1850
        self.__YMINC = 0
        self.__YMAXC = 1400#1000
        
        self.__XINIMINV = 2
        self.__YINIMINV = 2
        self.__XMINV = -3
        self.__XMAXV = 3
        self.__YMINV = -3
        self.__YMAXV = 3
        
    def Initalize(self):
        for word in self.Words:
            self.Coors.append([np.random.randint(self.__XMINC,self.__XMAXC,1)[0], self.__YMINC])
            self.Velocities.append([np.random.randint(self.__XINIMINV, self.__XMAXV,1)[0],
                np.random.randint(self.__YINIMINV, self.__YMAXV,1)[0]])
            self.Accelerations.append([np.random.randn(1)[0], np.random.randn(1)[0]])
        print('DriftWords Initialize Completed...')
    
    def OnChange(self,mode,para=''):
        if mode == 'RandomMove':
            #print('Random Move starting...')
            for i in range(len(self.Words)):
                ## update the coordiante of Words[i]
                    # Update the coordiante's 'x' of word
                #print('words:',self.Words)
                #print('coors:',self.Coors)
                if self.Coors[i][0] <= self.__XMINC :
                    if self.Velocities[i][0] < 0:
                        self.Velocities[i][0] = -self.Velocities[i][0]
                        self.Coors[i][0] = self.Coors[i][0] + int(self.Velocities[i][0])
                    else:
                        self.Coors[i][0] = self.Coors[i][0] + int(self.Velocities[i][0])
                elif self.Coors[i][0] >= self.__XMAXC :
                    if self.Velocities[i][0] >0:
                        self.Velocities[i][0] = -self.Velocities[i][0]
                        self.Coors[i][0] = self.Coors[i][0] + int(self.Velocities[i][0])
                    else:
                        self.Coors[i][0] = self.Coors[i][0] + int(self.Velocities[i][0])
                else:
                    self.Coors[i][0] = self.Coors[i][0] + int(self.Velocities[i][0])
                    # Update the coordiante's 'y' of word
                if self.Coors[i][1] <= self.__YMINC :
                    if self.Velocities[i][1] < 1:
                        self.Velocities[i][1] = -self.Velocities[i][1]
                        self.Coors[i][1] = self.Coors[i][1] + int(self.Velocities[i][1])
                    else:
                        self.Coors[i][1] = self.Coors[i][1] + int(self.Velocities[i][1])
                elif self.Coors[i][1] >= self.__YMAXC :
                    if self.Velocities[i][1] >1:
                        self.Velocities[i][1] = -self.Velocities[i][1]
                        self.Coors[i][1] = self.Coors[i][1] + int(self.Velocities[i][1])
                    else:
                        self.Coors[i][1] = self.Coors[i][1] + int(self.Velocities[i][1])
                else:
                    self.Coors[i][1] = self.Coors[i][1] + int(self.Velocities[i][1])
                ## update the Velocity of Words[i]
                if self.Velocities[i][0] <= self.__XMINV and self.Accelerations[i][0]<0:
                    self.Accelerations[i][0] = -self.Accelerations[i][0]
                    self.Velocities[i][0] = self.Velocities[i][0] + int(self.Accelerations[i][0])
                elif self.Velocities[i][0] >= self.__XMAXV and self.Accelerations[i][0]>0:
                    self.Accelerations[i][0] = -self.Accelerations[i][0]
                    self.Velocities[i][0] = self.Velocities[i][0] + int(self.Accelerations[i][0])
                else:
                    self.Velocities[i][0] = self.Velocities[i][0] + int(self.Accelerations[i][0])
                if self.Velocities[i][1] <= self.__YMINV and self.Accelerations[i][1]<1:
                    self.Accelerations[i][1] = -self.Accelerations[i][1]
                    self.Velocities[i][1] = self.Velocities[i][1] + int(self.Accelerations[i][1])
                elif self.Velocities[i][1] >= self.__YMAXV and self.Accelerations[i][1]>1:
                    self.Accelerations[i][1] = -self.Accelerations[i][1]
                    self.Velocities[i][1] = self.Velocities[i][1] + int(self.Accelerations[i][1])
                else:
                    self.Velocities[i][1] = self.Velocities[i][1] + int(self.Accelerations[i][1])
                ## update the Accelerations of Words[i]
                self.Accelerations[i][0] = np.random.randn(1)[0]/2
                self.Accelerations[i][1] = np.random.randn(1)[0]/2
                #print('word:%13s'%self.Words[i],'cor:',self.Coors[i],
                 #   'V:',self.Velocities[i],'A:',self.Accelerations[i])
            #print('Random Move Completed...')
        elif mode == 'DelWord':
            word_id = int(para)
            if word_id != -1:
                print('Delete Word:\'%s\'! ID:%d'%(self.Words[word_id],word_id))
                del self.Words[word_id]
                del self.Coors[word_id]
                del self.Velocities[word_id]
                del self.Accelerations[word_id]
                return 0
            else:
                return 1 # 无法删除，返回1
        elif mode == 'AddWord':
            print('prepare add word')
            if para == '':
                return 2
            if para in self.Words:
                #win32gui.MessageBox(0,'123','456',win32con.MB_ABORTRETRYIGNORE)
                #print('Word:\'%s\' already exists, so it can\'t be added to show!'%para)
                return 2  # 字符串已有，无法添加，返回2
            print(self.Words)
            print(self.Coors)
            print(self.Velocities)
            print(self.Accelerations)
            self.Words.append(para)
            self.Coors.append([np.random.randint(self.__XMINC,self.__XMAXC,1)[0], self.__YMINC])
            print('Coors appended..')
            self.Velocities.append([np.random.randint(self.__XINIMINV, self.__XMAXV,1)[0], np.random.randint(self.__YINIMINV, self.__YMAXV,1)[0]])
            print('Velocities appended..')
            self.Accelerations.append([np.random.randn(1)[0], np.random.randn(1)[0]])
            print('Accelerations appended..')
            print('Add word:\'%s\'accomplished!'%para)
            return 0
    def ShowWords(self):
        print('Drift Words list:',end='')
        for word in self.Words:
            print(word,end='')
        print('\nDrift Words print finished!')

def GetWorkerWhdwnd():
    # Get the handle of program manager
    hProgMan = win32gui.FindWindow("Progman", None)
    # print("hProgMan:",hProgMan)
    
    # Send a message to program manager to split 'FolderView' and 'SysListView' into WorkerW,
    #    参数为0时,无法工作
    rc,result = win32gui.SendMessageTimeout(hProgMan, 0x052C, 0x0000000D, 1, win32con.SMTO_NORMAL, 1000)
#    rc,result = win32gui.SendMessageTimeout(hProgMan, 0x052C, 0x0000000D, 0, win32con.SMTO_NORMAL, 1000)
#    print('rc,result:',rc,result)
#    print("win32 error:",win32api.GetLastError())
    arhWorkerW = []
    def GetWorkerWs(hwnd,mouse):
        if win32gui.GetClassName(hwnd) == 'WorkerW' :
            arhWorkerW.append(hwnd)
            #print('hwnd:',hex(hwnd),"wdnm:%15s"%win32gui.GetWindowText(hwnd),
            #    'class:%15s'%win32gui.GetClassName(hwnd))
    win32gui.EnumWindows(GetWorkerWs, 0)
    return arhWorkerW[-1]

def GethChildwindow(hParendWND,childWNDclass,childWNDcaption):
    matched_childhWND = win32gui.FindWindowEx(hParendWND,0,childWNDclass,childWNDcaption)
    return matched_childhWND
    
def SendTToBG():
    cnt = 0
    hWorkerW = GetWorkerWhdwnd()
    hBGWND = GethChildwindow(hWorkerW,'Python DeskTop BG On Windows',
            'my_Python_windows_desktop')
    global MoveFlg
    while 1:
        time.sleep(0.014) # 0.016667 为60Hz
        if MoveFlg ==0 :
            #print('send message')
            win32gui.SendMessage(hBGWND, win32con.WM_TIMER, cnt, None)
        elif MoveFlg ==1 :
            pass
        elif MoveFlg ==2 :
            #print('send message quit')
            break
    return 0

class BGWND:
    hdcbuffer = 0
    global DFW
    def BGWndProc(self,hwnd,msg,wParam,lParam):
        if msg == win32con.WM_PAINT:
            #print('BG painting...%d...'%wParam)
            hdc,ps = win32gui.BeginPaint(hwnd)
            rect = win32gui.GetClientRect(hwnd)
    #        win32gui.Rectangle(hdc,min(xc),min(yc),max(xc),max(yc))
    #        win32gui.Ellipse(hdc,300+wParam,550,400+wParam,650)
            DFW.OnChange(mode='RandomMove')
            
            #self.hdcbuffer = win32gui.CreateCompatibleDC(hdc)
            #hBitMap = win32gui.CreateCompatibleBitmap(hdc, 1920, 1080)
            ###win32gui.ReleaseDC(hwnd, hdc)
            #win32gui.SelectObject(self.hdcbuffer, hBitMap)
            #win32gui.PatBlt(self.hdcbuffer, 0, 0, 1920, 1080, win32con.WHITENESS)
            
            #win32gui.SetBkMode(hdc,win32con.TRANSPARENT)
            for index in range(len(DFW.Words)):
                rect = (int(DFW.Coors[index][0]),int(DFW.Coors[index][1]),1920,1080)
                win32gui.DrawText(hdc,'%s,%d'%(DFW.Words[index],wParam),
                    len('%s'%(DFW.Words[index])),rect,win32con.DT_SINGLELINE|win32con.DT_TOP|win32con.DT_LEFT)
            #win32gui.BitBlt(hdc, 0, 0, 1920, 1080, self.hdcbuffer, 0, 0, win32con.SRCCOPY )
            win32gui.EndPaint(hwnd,ps)
        elif msg == win32con.WM_DESTROY:  
            win32gui.PostQuitMessage(0)
        elif msg == win32con.WM_TIMER:
            #print("BG TIMER TRIGGERED",wParam)
            win32gui.InvalidateRect(hwnd,None,True)
            win32gui.UpdateWindow(hwnd)
        else:
            pass
            #print('BG:其他信息:',msg)
        return win32gui.DefWindowProc(hwnd,msg,wParam,lParam)  
    
    def BGWNDRegister(self,parenthwnd):
        def BGWNDREG():
            wc = win32gui.WNDCLASS()  
            wc.hbrBackground = win32con.COLOR_DESKTOP +1
            wc.hCursor = win32gui.LoadCursor(0,win32con.IDI_APPLICATION)  
            wc.lpszClassName = "Python DeskTop BG On Windows"  
            wc.lpfnWndProc = self.BGWndProc  
            reg = win32gui.RegisterClass(wc)
            return reg
        
        hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_NOACTIVATE, BGWNDREG(),
            'my_Python_windows_desktop',
            win32con.WS_MAXIMIZE|win32con.WS_CHILD|win32con.WS_VISIBLE,#WS_OVERLAPPEDWINDOW
            win32con.CW_USEDEFAULT,win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,win32con.CW_USEDEFAULT,
            parenthwnd,#WorkerW
            0,0,None)
        win32gui.ShowWindow(hwnd,win32con.SW_SHOW) 
        win32gui.UpdateWindow(hwnd)  
        win32gui.PumpMessages()
    
    def StartBGWND(self):
        print('starting Background Display Window...')
        hWorkerW = GetWorkerWhdwnd()
        if not hWorkerW:
            print('ERROR OCCURED: Can\'t get handle of WorkerW!')
            return 0
        if not GethChildwindow(hWorkerW,'Python DeskTop BG On Windows','my_Python_windows_desktop'):
            self.BGWNDRegister(hWorkerW) # Background display
        else:
            print('Background Display Window already exists!')

class FGWND:
    ID_BUTTON1 = 0
    ID_BUTTON2 = 0
    ID_BUTTON3 = 0
    ID_LISTBOX1 = 0
    ID_TEXT1 = 0
    def FGWndProc(self,hwnd,msg,wParam,lParam):  
        global MoveFlg
        #global DFW
        if msg == win32con.WM_PAINT:  
            hdc,ps = win32gui.BeginPaint(hwnd)  
            rect = win32gui.GetClientRect(hwnd)  
            #win32gui.DrawText(hdc,'control pannel',len('control pannel'),
            #    rect,win32con.DT_SINGLELINE|win32con.DT_CENTER|win32con.DT_VCENTER)  
            win32gui.EndPaint(hwnd,ps)  
        if msg == win32con.WM_DESTROY:
            MoveFlg = 2
            with open(CONFIGFILE, 'w+', encoding='utf-8')as fo:
                for word in DFW.Words:
                    fo.write(word+'\n')
            print('closing BG window...')
            hWorkerW = GetWorkerWhdwnd()
            if not hWorkerW:
                print('ERROR OCCURED: Can\'t get handle of WorkerW!')
            else:
                hBGWND = GethChildwindow(hWorkerW,'Python DeskTop BG On Windows','my_Python_windows_desktop')
                if hBGWND:
                    win32gui.SendMessageTimeout(hBGWND, win32con.WM_CLOSE, 0, 0, win32con.SMTO_NORMAL, 1000)
                else:
                    print('can\'t find  BG window!')
            print('closing FG window...')
            win32gui.PostQuitMessage(0)
        elif msg == win32con.WM_COMMAND:
            if lParam == self.ID_BUTTON1:
                tempFlg = MoveFlg
                MoveFlg = 1
                # 首先获取文本框内的文本长度
                length = win32gui.SendMessage(self.ID_TEXT1, win32con.WM_GETTEXTLENGTH)+1
                # 生成一个指针用来存放字符串（大小为length）
                buffer = win32gui.PyMakeBuffer(length)
                # 向文本框发送信息获取内容
                win32gui.SendMessage(self.ID_TEXT1, win32con.WM_GETTEXT, length, buffer)
                # 获取字符串地址和长度
                address, length = win32gui.PyGetBufferAddressAndLen(buffer[:-1])
                # 获取指针所指字符串
                text = win32gui.PyGetString(address, length)
                
                #print('Len:%d,'%length,'Text:\'%s\''%text)
                if not DFW.OnChange('AddWord',text):
                    win32gui.SendMessage(self.ID_LISTBOX1, win32con.LB_ADDSTRING,0,text)
                #print('list box 添加完成')
                MoveFlg = tempFlg
            elif lParam == self.ID_BUTTON2:
                tempFlg = MoveFlg
                MoveFlg = 1
                sel_id = win32gui.SendMessage(self.ID_LISTBOX1, win32con.LB_GETCURSEL,0,0)
                # win32con.LB_GETCOUNT 获取listbox内条目总数
                if sel_id != -1:
                    DFW.OnChange('DelWord',str(sel_id))
                    # 删除id为 sel_id 的条目
                    win32gui.SendMessage(self.ID_LISTBOX1, win32con.LB_DELETESTRING,sel_id,0)
                MoveFlg = tempFlg
            elif lParam == self.ID_BUTTON3:
                #print('button 3 clicked: switch the state of words\'s moving')
                if MoveFlg == 0:
                    MoveFlg = 1
                elif MoveFlg ==1:
                    MoveFlg = 0
            else:
                pass
                #print(wParam,lParam)
        else:
            pass
            #print('FG:其他信息',hex(msg),wParam,lParam,'IDs:',self.ID_BUTTON1,self.ID_BUTTON2,self.ID_LISTBOX1,self.ID_TEXT1)
        
        return win32gui.DefWindowProc(hwnd,msg,wParam,lParam) 
    def FGWNDRegister(self):
        global DFW
        def FGWNDREG():
            wc = win32gui.WNDCLASS()  
            wc.hbrBackground = win32con.COLOR_BTNFACE + 1  
            wc.hCursor = win32gui.LoadCursor(0,win32con.IDI_APPLICATION)  
            wc.lpszClassName = "Python DeskTop FG On Windows"  
            wc.lpfnWndProc = self.FGWndProc  
            reg = win32gui.RegisterClass(wc)
            return reg
        reg = FGWNDREG()
        hwnd = win32gui.CreateWindowEx(0, reg,
            'Live Wallpaper Control Pannel',
            win32con.WS_DLGFRAME|win32con.WS_SYSMENU|win32con.WS_MINIMIZEBOX,
            win32con.CW_USEDEFAULT,win32con.CW_USEDEFAULT,
            450,430,
            0,#Parent hWnd
            0,0,None)
        self.ID_BUTTON1 = win32gui.CreateWindow("button"  ,'添加信息',win32con.WS_CHILD|win32con.WS_VISIBLE|win32con.BS_PUSHBUTTON,
            330, 330, 85, 30, hwnd, 1, None,None)
        self.ID_BUTTON2 = win32gui.CreateWindow("button"  ,'删除信息',win32con.WS_CHILD|win32con.WS_VISIBLE|win32con.BS_PUSHBUTTON,
            330, 20, 85, 30, hwnd, 2, None,None)
        self.ID_BUTTON3 = win32gui.CreateWindow("button"  ,'启动/停止',win32con.WS_CHILD|win32con.WS_VISIBLE|win32con.BS_PUSHBUTTON,
            330, 150, 85, 30, hwnd, 2, None,None)
        self.ID_LISTBOX1=win32gui.CreateWindow( "listbox", "list box 1",
            win32con.WS_CHILD|win32con.WS_VSCROLL | win32con.WS_TABSTOP | win32con.LBS_HASSTRINGS|win32con.LBS_NOTIFY,
            20, 20, 280, 300, hwnd, 1, None, None )
        self.ID_TEXT1 = win32gui.CreateWindow("edit"  ,'',win32con.WS_CHILD|win32con.WS_VISIBLE|win32con.WS_BORDER|win32con.ES_AUTOVSCROLL|win32con.ES_AUTOHSCROLL,
            20, 330, 280, 30, hwnd, 1, None,None)
        win32gui.ShowWindow(hwnd,win32con.SW_SHOW)
        win32gui.ShowWindow(self.ID_LISTBOX1,win32con.SW_SHOW)
        for word_id in range(len(DFW.Words)):
            win32gui.SendMessage(self.ID_LISTBOX1, win32con.LB_ADDSTRING,0,DFW.Words[word_id])
        #print('L1-2:',win32gui.SendMessage(self.ID_LISTBOX1, win32con.WM_SETREDRAW, 0,None))

        win32gui.UpdateWindow(hwnd)
    #    print('FG Timer',win32api.SetTimer(hwnd,1,1000,None))
        win32gui.PumpMessages()
    def StartFGWND(self):
        print('starting Foreground Control Pannel Window...')
        if not win32gui.FindWindow('Python DeskTop FG On Windows','Live Wallpaper Control Pannel'):
            self.FGWNDRegister() # Foreground display
        else:
            print('Foreground Control Pannel Window already exists!')


if __name__ == '__main__':
#    freeze_support()

    DFW = DriftWords()

    #try:
    fi = open(CONFIGFILE,'r+',encoding='utf-8')
    i = 0
    while 1:
        line = fi.readline()
        line = line.strip()
        #print('--------------line',line)
        if line != '':
            DFW.Words.append(line)
            i = i+1
            #print('line[%d]:\'%s\''%(i,line))
        else:
            break
    #print('Read lines finished.')
    DFW.Initalize()
    fi.close()
    #except:
    #    print('can\'t find the configuration file!\nCreate a new one(%s).'%CONFIGFILE)
        # fi = open(CONFIGFILE,'w',encoding='utf-8')
        # fi.close()
    
    MoveFlg = 1
    
    BG = BGWND()
    FG = FGWND()
    
    t1 = Thread(target=BG.StartBGWND,args=() )
    t2 = Thread(target=FG.StartFGWND,args=() )
    t1.start()
    t2.start()
    time.sleep(1)
    if 1:#input('输入\'y\'来进行窗口刷新,其他键不刷新:') == 'y':
        t3 = Thread(target=SendTToBG,args=() )
        t3.start()
        t3.join()
    t1.join() 
    t2.join() 
