# KAILANGAN MO I-RESTART ANG FLASK SERVER! 🔄

## PROBLEMA:
Ang Flask server ay hindi pa naka-load ng bagong API endpoints kaya lumalabas ang 404 error.

## SOLUSYON:

### Option 1: I-restart sa Terminal/Command Prompt

1. **Hanapin ang terminal kung saan tumatakbo ang Flask server**
   - Tingnan kung may nakikita kang "Running on http://127.0.0.1:5000"

2. **I-stop ang server**
   - Press `Ctrl + C` sa terminal

3. **I-start ulit ang server**
   ```bash
   python app.py
   ```

### Option 2: I-restart gamit ang Task Manager

1. **Open Task Manager** (Ctrl + Shift + Esc)

2. **Hanapin ang Python process**
   - Look for "python.exe" or "Python"
   - Right-click → End Task

3. **I-start ulit ang server**
   - Open terminal/command prompt
   - Navigate to project folder:
     ```bash
     cd C:\xampp\htdocs\iClini V.2
     ```
   - Run:
     ```bash
     python app.py
     ```

### Option 3: Gamit ang VS Code Terminal

1. **Open VS Code Terminal** (Ctrl + `)

2. **I-stop ang running process**
   - Click sa terminal
   - Press `Ctrl + C`

3. **I-start ulit**
   ```bash
   python app.py
   ```

## PAANO MALAMAN NA SUCCESSFUL ANG RESTART:

Dapat makita mo sa terminal:
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

## PAGKATAPOS NG RESTART:

1. **Refresh ang browser** (F5 or Ctrl + R)
2. **Try ulit ang Restore button**
3. **Dapat working na!** ✅

## KUNG MAY ERROR PA RIN:

Check sa terminal kung may error messages. Kung may nakita, screenshot mo at ipakita sa akin.

## IMPORTANT NOTE:

**PALAGING I-RESTART ANG FLASK SERVER** kapag may binago sa `app.py` file para ma-load ang bagong code!
