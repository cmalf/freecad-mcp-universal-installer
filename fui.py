#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import json
import platform

# ================= ANSI COLORS =================
class Colors:
    RESET = "\033[0m"
    BRIGHT = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"

# ================= TRANSLATIONS =================
i18n = {
    "id": {
        "checking": "Memeriksa prasyarat...",
        "pyOld": "Versi Python Anda terlalu lama. Butuh v3.8+. Versi saat ini: ",
        "gitMissing": "Git tidak ditemukan di sistem.",
        "installGit": "Apakah Anda ingin menginstal Git sekarang? (1: Instal Otomatis, 2: Instal Manual, 3: Keluar): ",
        "sudoReq": "Meminta akses Sudo jika diperlukan. Masukkan password jika diminta.",
        "closeWarn": "PERINGATAN: Disarankan UNTUK menutup program/aplikasi FreeCAD sebelum melanjutkan.",
        "aiWarn": "PENTING: Pastikan Anda sudah menginstal salah satu AI di list (Gemini, Claude, Goose, atau Aider).",
        "continue": "Lanjutkan? (Y/N): ",
        "menuOS": "\n=== Pilih Sistem Operasi Anda ===",
        "menu1": "1. MacOS",
        "menu2": "2. Linux",
        "menu3": "3. Windows",
        "menu9": "9. Keluar",
        "select": "Pilih menu: ",
        "menuAI": "\n=== Pilih AI Anda ===",
        "ai1": "1. Gemini CLI",
        "ai2": "2. Claude Desktop & Claude Code CLI",
        "ai3": "3. Goose CLI",
        "ai4": "4. Aider CLI",
        "ai9": "9. Kembali ke Menu OS",
        "subMenu": "\n=== Sub Menu Konfigurasi ===",
        "sub3": "3. Setup [AI] Setting (Save Token / Text Feedback only)",
        "sub4": "4. Setup [AI] Setting (Normal Mode)",
        "sub5": "5. Install FreeCAD-MCP by neka-nat",
        "sub9": "9. Kembali ke Menu AI",
        "success": "Proses selesai dengan sukses!",
        "failed": "Proses gagal: ",
        "pressAnyKey": "Tekan Enter untuk melanjutkan...",
        "exit": "Keluar dari program. Sampai jumpa!"
    },
    "en": {
        "checking": "Checking prerequisites...",
        "pyOld": "Your Python version is too old. Requires v3.8+. Current: ",
        "gitMissing": "Git is not installed on this system.",
        "installGit": "Do you want to install Git now? (1: Auto Install, 2: Manual Install, 3: Quit): ",
        "sudoReq": "Requesting Sudo access if needed. Enter password if prompted.",
        "closeWarn": "WARNING: It is recommended TO close the FreeCAD application before proceeding.",
        "aiWarn": "IMPORTANT: Make sure you have installed at least one AI in the list (Gemini, Claude, Goose, or Aider).",
        "continue": "Continue? (Y/N): ",
        "menuOS": "\n=== Choose Your Operating System ===",
        "menu1": "1. MacOS",
        "menu2": "2. Linux",
        "menu3": "3. Windows",
        "menu9": "9. Quit",
        "select": "Select menu: ",
        "menuAI": "\n=== Choose Your AI ===",
        "ai1": "1. Gemini CLI",
        "ai2": "2. Claude Desktop & Claude Code CLI",
        "ai3": "3. Goose CLI",
        "ai4": "4. Aider CLI",
        "ai9": "9. Back to OS Menu",
        "subMenu": "\n=== Configuration Sub Menu ===",
        "sub3": "3. Setup [AI] Setting (Save Token / Text Feedback only)",
        "sub4": "4. Setup [AI] Setting (Normal Mode)",
        "sub5": "5. Install FreeCAD-MCP by neka-nat",
        "sub9": "9. Back To AI Menu",
        "success": "Process completed successfully!",
        "failed": "Process failed: ",
        "pressAnyKey": "Press Enter to continue...",
        "exit": "Exiting program. Goodbye!"
    },
    "zh": {
        "checking": "检查先决条件...",
        "pyOld": "您的 Python 版本太旧。 需要 v3.8+。 当前版本: ",
        "gitMissing": "系统中未找到 Git。",
        "installGit": "您现在要安装 Git 吗？ (1: 自动安装, 2: 手动安装, 3: 退出): ",
        "sudoReq": "如果需要，请求 Sudo 访问权限。 提示时输入密码。",
        "closeWarn": "警告：建议在继续之前关闭 FreeCAD 应用程序。",
        "aiWarn": "重要提示：请确保您已安装列表中的至少一种 AI（Gemini、Claude、Goose 或 Aider）。",
        "continue": "继续吗？(Y/N): ",
        "menuOS": "\n=== 选择您的操作系统 ===",
        "menu1": "1. MacOS",
        "menu2": "2. Linux",
        "menu3": "3. Windows",
        "menu9": "9. 退出",
        "select": "选择菜单: ",
        "menuAI": "\n=== 选择您的 AI ===",
        "ai1": "1. Gemini CLI",
        "ai2": "2. Claude Desktop & Claude Code CLI",
        "ai3": "3. Goose CLI",
        "ai4": "4. Aider CLI",
        "ai9": "9. 返回系统菜单",
        "subMenu": "\n=== 配置子菜单 ===",
        "sub3": "3. 设置 [AI] (仅文本反馈/省Token)",
        "sub4": "4. 设置 [AI] (普通模式)",
        "sub5": "5. 安装 FreeCAD-MCP (by neka-nat)",
        "sub9": "9. 返回 AI 菜单",
        "success": "过程成功完成！",
        "failed": "过程失败: ",
        "pressAnyKey": "按 Enter 键继续...",
        "exit": "退出程序。 再见！"
    },
    "th": {
        "checking": "กำลังตรวจสอบข้อกำหนดเบื้องต้น...",
        "pyOld": "เวอร์ชัน Python ของคุณเก่าเกินไป ต้องใช้ v3.8+ ปัจจุบัน: ",
        "gitMissing": "ไม่พบ Git ในระบบ",
        "installGit": "คุณต้องการติดตั้ง Git ทันทีหรือไม่? (1: ติดตั้งอัตโนมัติ, 2: ติดตั้งด้วยตนเอง, 3: ออก): ",
        "sudoReq": "ร้องขอสิทธิ์ Sudo หากจำเป็น กรุณาป้อนรหัสผ่านเมื่อได้รับแจ้ง",
        "closeWarn": "คำเตือน: ขอแนะนำให้ปิดโปรแกรม FreeCAD ก่อนดำเนินการต่อ",
        "aiWarn": "สำคัญ: ตรวจสอบให้แน่ใจว่าคุณได้ติดตั้ง AI อย่างน้อยหนึ่งตัวในรายการ (Gemini, Claude, Goose หรือ Aider)",
        "continue": "ดำเนินการต่อหรือไม่? (Y/N): ",
        "menuOS": "\n=== เลือกระบบปฏิบัติการของคุณ ===",
        "menu1": "1. MacOS",
        "menu2": "2. Linux",
        "menu3": "3. Windows",
        "menu9": "9. ออก",
        "select": "เลือกเมนู: ",
        "menuAI": "\n=== เลือก AI ของคุณ ===",
        "ai1": "1. Gemini CLI",
        "ai2": "2. Claude Desktop & Claude Code CLI",
        "ai3": "3. Goose CLI",
        "ai4": "4. Aider CLI",
        "ai9": "9. กลับไปที่เมนูระบบปฏิบัติการ",
        "subMenu": "\n=== เมนูย่อยการตั้งค่า ===",
        "sub3": "3. ตั้งค่า [AI] (ประหยัด Token / ส่งข้อมูลเฉพาะข้อความ)",
        "sub4": "4. ตั้งค่า [AI] (โหมดปกติ)",
        "sub5": "5. ติดตั้ง FreeCAD-MCP by neka-nat",
        "sub9": "9. กลับไปที่เมนู AI",
        "success": "กระบวนการเสร็จสมบูรณ์!",
        "failed": "กระบวนการล้มเหลว: ",
        "pressAnyKey": "กด Enter เพื่อดำเนินการต่อ...",
        "exit": "ออกจากโปรแกรม ลาก่อน!"
    }
}

lang = 'id'
t = i18n[lang]

# ================= UTILS =================
def ask(query):
    return input(query)

def print_msg(msg, color=Colors.RESET):
    print(f"{color}{msg}{Colors.RESET}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_cmd(command):
    subprocess.run(command, shell=True, check=True)

# ================= BANNER =================
def show_banner():
    clear_screen()
    print_msg("=========================================================", Colors.CYAN)
    print_msg("     A U T O   I N S T A L L E R  FREECAD-MCP +          ", Colors.BRIGHT + Colors.YELLOW)
    print_msg("     Gemini,Claude,Goose,Aider                           ", Colors.BRIGHT + Colors.GREEN)
    print_msg("     Github.com/cmalf                                    ", Colors.RESET)
    print_msg("=========================================================", Colors.CYAN)

# ================= PREREQUISITES =================
def check_prerequisites():
    print_msg(f"\n[*] {t['checking']}", Colors.YELLOW)
    
    # Check Python version (using 3.8+ for shutil.copytree dirs_exist_ok)
    if sys.version_info < (3, 8):
        print_msg(f"{t['pyOld']}{sys.version.split(' ')[0]}", Colors.RED)
        sys.exit(1)

    if os.name != 'nt':
        print_msg(f"\n[*] {t['sudoReq']}", Colors.YELLOW)
        try:
            subprocess.run(["sudo", "-v"], check=True)
        except subprocess.CalledProcessError:
            print_msg(t['failed'] + " Sudo auth failed.", Colors.RED)

    # Check Git
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except FileNotFoundError:
        print_msg(f"\n[!] {t['gitMissing']}", Colors.RED)
        choice = ask(t['installGit'])
        if choice == '1':
            try:
                if platform.system() == 'Windows':
                    run_cmd('winget install --id Git.Git -e --source winget')
                elif platform.system() == 'Darwin':
                    run_cmd('brew install git')
                else:
                    run_cmd('sudo apt-get update && sudo apt-get install -y git')
            except Exception as err:
                print_msg(t['failed'] + " Git installation failed.", Colors.RED)
                sys.exit(1)
        else:
            sys.exit(0)

# ================= CONFIG ENGINE =================
def write_config(selected_os, ai_type, only_text_feedback):
    home = os.path.expanduser("~")
    app_data = os.environ.get('APPDATA', os.path.join(home, 'AppData', 'Roaming'))
    file_path = ''
    content = ''

    try:
        if ai_type == 'Gemini':
            file_path = os.path.join(home, '.gemini', 'settings.json')
            gemini_json = {
                "security": { "auth": { "selectedType": "oauth-personal" } },
                "mcp": { "allowed": ["freecad"] },
                "mcpServers": {
                    "freecad": {
                        "command": "uvx",
                        "args": ["freecad-mcp", "--only-text-feedback"] if only_text_feedback else ["freecad-mcp"],
                        "timeout": 60000
                    }
                },
                "tools": { "shell": { "enableInteractiveShell": True } }
            }
            content = json.dumps(gemini_json, indent=2)

        elif ai_type == 'Claude':
            if selected_os == 'Windows':
                file_path = os.path.join(app_data, 'Claude', 'claude_desktop_config.json')
            elif selected_os == 'MacOS':
                file_path = os.path.join(home, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json')
            else:
                file_path = os.path.join(home, '.config', 'Claude', 'claude_desktop_config.json')

            claude_json = {
                "mcpServers": {
                    "freecad": {
                        "command": "uvx",
                        "args": ["freecad-mcp", "--only-text-feedback"] if only_text_feedback else ["freecad-mcp"]
                    }
                }
            }
            content = json.dumps(claude_json, indent=2)

        elif ai_type == 'Goose':
            if selected_os == 'Windows':
                file_path = os.path.join(app_data, 'Block', 'goose', 'config.yaml')
            elif selected_os == 'MacOS':
                file_path = os.path.join(home, '.config', 'block', 'goose', 'config.yaml')
            else:
                file_path = os.path.join(home, '.config', 'block', 'goose', 'config.yaml')

            content = "extensions:\n  freecad:\n    command: \"uvx\"\n    args:\n      - \"freecad-mcp\"\n"
            if only_text_feedback:
                content += "      - \"--only-text-feedback\"\n"

        elif ai_type == 'Aider':
            file_path = os.path.join(home, '.aider.conf.yml')
            content = "mcp-output: true\nmcp-servers:\n  - \"uvx freecad-mcp"
            if only_text_feedback:
                content += " --only-text-feedback"
            content += "\"\n"

        # Create Directory if not exist and write file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print_msg(f"[OK] Configuration written successfully to:\n-> {file_path}", Colors.GREEN)
    except Exception as err:
        print_msg(f"[ERROR] Failed to write configuration: {str(err)}", Colors.RED)

# ================= FREE CAD INSTALLATION =================
def install_freecad_mcp(selected_os):
    print_msg(f"\n>>> Cloning & Preparing FreeCAD-MCP Addon...", Colors.CYAN)
    clone_dir = os.path.join(os.getcwd(), 'freecad-mcp')
    
    try:
        if not os.path.exists(clone_dir):
            run_cmd('git clone https://github.com/neka-nat/freecad-mcp.git')
        
        source_addon = os.path.join(clone_dir, 'addon', 'FreeCADMCP')
        home = os.path.expanduser("~")
        target_paths = []

        if selected_os == 'Windows':
            app_data = os.environ.get('APPDATA', os.path.join(home, 'AppData', 'Roaming'))
            target_paths.append(os.path.join(app_data, 'FreeCAD', 'Mod', 'FreeCADMCP'))
        elif selected_os == 'MacOS':
            target_paths.append(os.path.join(home, 'Library', 'Application Support', 'FreeCAD', 'v1-1', 'Mod', 'FreeCADMCP'))
            target_paths.append(os.path.join(home, 'Library', 'Application Support', 'FreeCAD', 'v1-0', 'Mod', 'FreeCADMCP'))
        elif selected_os == 'Linux':
            target_paths.append(os.path.join(home, '.FreeCAD', 'Mod', 'FreeCADMCP'))
            target_paths.append(os.path.join(home, '.local', 'share', 'FreeCAD', 'v1-1', 'Mod', 'FreeCADMCP'))
            target_paths.append(os.path.join(home, 'snap', 'freecad', 'common', 'Mod', 'FreeCADMCP'))

        copied = False
        for target in target_paths:
            try:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                shutil.copytree(source_addon, target, dirs_exist_ok=True)
                print_msg(f"[OK] Copied addon to: {target}", Colors.GREEN)
                copied = True
            except Exception:
                pass

        if not copied:
            print_msg(f"[WARN] Could not automatically inject to default FreeCAD folders. Copy manually from ./freecad-mcp/addon/FreeCADMCP", Colors.YELLOW)
    except Exception as err:
        print_msg(f"[ERROR] {t['failed']}{str(err)}", Colors.RED)

# ================= INTERACTIVE MENUS =================
def start_action_menu(selected_os, ai_type):
    while True:
        show_banner()
        print_msg(f"\nOS: {selected_os} | AI: {ai_type}", Colors.MAGENTA)
        print_msg(t['subMenu'], Colors.BRIGHT + Colors.CYAN)
        print_msg(t['sub3'].replace('[AI]', ai_type), Colors.YELLOW)
        print_msg(t['sub4'].replace('[AI]', ai_type))
        print_msg(t['sub5'])
        print_msg(t['sub9'], Colors.RED)

        choice = ask(t['select'])
        if choice == '3':
            write_config(selected_os, ai_type, True)
            ask(f"\n{t['pressAnyKey']}")
        elif choice == '4':
            write_config(selected_os, ai_type, False)
            ask(f"\n{t['pressAnyKey']}")
        elif choice == '5':
            install_freecad_mcp(selected_os)
            ask(f"\n{t['pressAnyKey']}")
        elif choice == '9':
            break
        else:
            print_msg("Invalid choice!", Colors.RED)
            ask(f"\n{t['pressAnyKey']}")

def start_ai_menu(selected_os):
    while True:
        show_banner()
        print_msg(f"\nOS Terpilih: {selected_os}", Colors.MAGENTA)
        print_msg(t['menuAI'], Colors.BRIGHT + Colors.CYAN)
        print_msg(t['ai1'])
        print_msg(t['ai2'])
        print_msg(t['ai3'])
        print_msg(t['ai4'])
        print_msg(t['ai9'], Colors.RED)

        choice = ask(t['select'])
        if choice == '1':
            start_action_menu(selected_os, 'Gemini')
        elif choice == '2':
            start_action_menu(selected_os, 'Claude')
        elif choice == '3':
            start_action_menu(selected_os, 'Goose')
        elif choice == '4':
            start_action_menu(selected_os, 'Aider')
        elif choice == '9':
            break
        else:
            print_msg("Invalid choice!", Colors.RED)
            ask(f"\n{t['pressAnyKey']}")

def start_main_menu():
    while True:
        show_banner()
        print_msg(t['menuOS'], Colors.BRIGHT + Colors.CYAN)
        print_msg(t['menu1'])
        print_msg(t['menu2'])
        print_msg(t['menu3'])
        print_msg(t['menu9'], Colors.RED)

        choice = ask(t['select'])
        if choice == '1':
            start_ai_menu('MacOS')
        elif choice == '2':
            start_ai_menu('Linux')
        elif choice == '3':
            start_ai_menu('Windows')
        elif choice == '9':
            print_msg(t['exit'], Colors.GREEN)
            sys.exit(0)
        else:
            print_msg("Invalid choice!", Colors.RED)
            ask(f"\n{t['pressAnyKey']}")

# ================= INITIALIZATION =================
def init():
    global t, lang
    show_banner()
    
    print_msg("\nSelect Language / Pilih Bahasa:")
    print_msg("1. English  2. Indonesia (Default)  3. 中文 (Mandarin)  4. ภาษาไทย (Thai)")
    l_choice = ask("Language [1-4]: ")
    
    if l_choice == '1': lang = 'en'
    elif l_choice == '3': lang = 'zh'
    elif l_choice == '4': lang = 'th'
    else: lang = 'id'
    
    t = i18n[lang]

    show_banner()
    print_msg(f"\n{t['closeWarn']}", Colors.BRIGHT + Colors.RED)
    print_msg(f"{t['aiWarn']}", Colors.BRIGHT + Colors.YELLOW)
    
    cont = ask(t['continue'])
    if cont.lower() != 'y':
        print_msg(t['exit'], Colors.GREEN)
        sys.exit(0)

    check_prerequisites()
    start_main_menu()

if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        print_msg(f"\n{t['exit']}", Colors.GREEN)
        sys.exit(0)
