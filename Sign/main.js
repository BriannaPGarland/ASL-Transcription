const { BrowserWindow, app } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width:1200,
        height:850,
        backgroundColor: "#FFFFFF",
        icon:'./signIcon.ico',
        webPreferences: {
            nodeIntegration: false,
            worldSafeExecuteJavaScript: true,
            contextIsolation: true
        }
        
    })

    win.loadFile('index.html')
}

require('electron-reload')(__dirname, {
    electron: path.join(__dirname,'node_modules', '.bin', 'electron')
})



app.whenReady().then(createWindow)
