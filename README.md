# Live Wallpaper Remainder on Windows
## Windows动态墙纸（提醒器）

## Readme[English Version]

### 1.Introduction: This is a little tool that can 
### 2.Main features: 
* 1.fnfkerf


## ReadMe[中文版]
### 1.介绍：
由于本人经常忘记做某事，故经常需要将代办事项记录下来，以提醒我及时做重要的事。而常见的备忘录都是记事本的形式，虽然也可以记录信息用于提醒，但是往往在记下备忘录之后忘记打开软件。所以我便想开发一个小工具来以一个更加醒目的方式来提醒我。  于是，这个小工具便诞生了！

这是一个使用Python和Win32api制作的动态墙纸小工具，它可以用于记录并动态显示待办事项。
### 2.主要功能：
* 1.在桌面图标之下显示动态待办事项[√ 现已实现]
* 2.在桌面图标之下显示一段视频[× 尚未实现]
* 3.背景对鼠标和键盘响应[× 尚为实现]

### 3.实现方法：
实现在Windows窗口图标下显示图像依赖 Gerald Degeneve 的[这个方法](https://www.codeproject.com/articles/856020/draw-behind-desktop-icons-in-windows)，通过向'Progman'发送消息分离'SysListView32'窗口，并在新产生的WorkerW窗口内显示自己的窗口。在新产生的窗口内显示内容即可。

* 1).找到Windows Program Manager窗口的句柄
```
hProgMan = win32gui.FindWindow("Progman", None)
```
* 2).向Windows Program Manager发送信息'0x052c'
``` 
win32gui.SendMessage(hProgMan, 0x052C, 0x0000000D, 1, win32con.SMTO_NORMAL) 
```
* 3).找到分离的hWorkerW窗口句柄
``` 
arhWorkerW = []
def GetWorkerWs(hwnd,mouse):
    if win32gui.GetClassName(hwnd) == 'WorkerW' :
        arhWorkerW.append(hwnd)
win32gui.EnumWindows(GetWorkerWs, 0)
```
* 4).建立WorkerW窗口的子窗口(用于在桌面图标下显示的窗口)
```
hwnd = win32gui.CreateWindowEx(
    win32con.WS_EX_NOACTIVATE, BGWNDREG(),
    'my_Python_windows_desktop',
    win32con.WS_MAXIMIZE|win32con.WS_CHILD|win32con.WS_VISIBLE,
    win32con.CW_USEDEFAULT,win32con.CW_USEDEFAULT,
    win32con.CW_USEDEFAULT,win32con.CW_USEDEFAULT,
    parenthwnd,#hWorkerW
    0,0,None)
```
* 5).在新建立的子窗口内绘制图像

### 4.运行截图：
![图片](https://github.com/Wanjpeng/nvrjevnkbklremvklmkekrbemk/blob/master/screenshots/媒体1_Trim.gif)