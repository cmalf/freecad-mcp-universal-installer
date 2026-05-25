#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');
const readline = require('readline');

// ================= ANSI COLORS =================
const colors = {
    reset: "\x1b[0m",
    bright: "\x1b[1m",
    cyan: "\x1b[36m",
    green: "\x1b[32m",
    yellow: "\x1b[33m",
    red: "\x1b[31m",
    magenta: "\x1b[35m"
};

// ================= TRANSLATIONS =================
const i18n = {
    id: {
        checking: "Memeriksa prasyarat...",
        nodeOld: "Versi Node.js Anda terlalu lama. Butuh v16+. Versi saat ini: ",
        gitMissing: "Git tidak ditemukan di sistem.",
        installGit: "Apakah Anda ingin menginstal Git sekarang? (1: Instal Otomatis, 2: Instal Manual, 3: Keluar): ",
        sudoReq: "Meminta akses Sudo jika diperlukan. Masukkan password jika diminta.",
        closeWarn: "PERINGATAN: Disarankan UNTUK menutup program/aplikasi FreeCAD sebelum melanjutkan.",
        aiWarn: "PENTING: Pastikan Anda sudah menginstal salah satu AI di list (Gemini, Claude, Goose, atau Aider).",
        continue: "Lanjutkan? (Y/N): ",
        menuOS: "\n=== Pilih Sistem Operasi Anda ===",
        menu1: "1. MacOS",
        menu2: "2. Linux",
        menu3: "3. Windows",
        menu9: "9. Keluar",
        select: "Pilih menu: ",
        menuAI: "\n=== Pilih AI Anda ===",
        ai1: "1. Gemini CLI",
        ai2: "2. Claude Desktop & Claude Code CLI",
        ai3: "3. Goose CLI",
        ai4: "4. Aider CLI",
        ai9: "9. Kembali ke Menu OS",
        subMenu: "\n=== Sub Menu Konfigurasi ===",
        sub3: "3. Setup [AI] Setting (Save Token / Text Feedback only)",
        sub4: "4. Setup [AI] Setting (Normal Mode)",
        sub5: "5. Install FreeCAD-MCP by neka-nat",
        sub9: "9. Kembali ke Menu AI",
        success: "Proses selesai dengan sukses!",
        failed: "Proses gagal: ",
        pressAnyKey: "Tekan Enter untuk melanjutkan...",
        exit: "Keluar dari program. Sampai jumpa!"
    },
    en: {
        checking: "Checking prerequisites...",
        nodeOld: "Your Node.js version is too old. Requires v16+. Current: ",
        gitMissing: "Git is not installed on this system.",
        installGit: "Do you want to install Git now? (1: Auto Install, 2: Manual Install, 3: Quit): ",
        sudoReq: "Requesting Sudo access if needed. Enter password if prompted.",
        closeWarn: "WARNING: It is recommended TO close the FreeCAD application before proceeding.",
        aiWarn: "IMPORTANT: Make sure you have installed at least one AI in the list (Gemini, Claude, Goose, or Aider).",
        continue: "Continue? (Y/N): ",
        menuOS: "\n=== Choose Your Operating System ===",
        menu1: "1. MacOS",
        menu2: "2. Linux",
        menu3: "3. Windows",
        menu9: "9. Quit",
        select: "Select menu: ",
        menuAI: "\n=== Choose Your AI ===",
        ai1: "1. Gemini CLI",
        ai2: "2. Claude Desktop & Claude Code CLI",
        ai3: "3. Goose CLI",
        ai4: "4. Aider CLI",
        ai9: "9. Back to OS Menu",
        subMenu: "\n=== Configuration Sub Menu ===",
        sub3: "3. Setup [AI] Setting (Save Token / Text Feedback only)",
        sub4: "4. Setup [AI] Setting (Normal Mode)",
        sub5: "5. Install FreeCAD-MCP by neka-nat",
        sub9: "9. Back To AI Menu",
        success: "Process completed successfully!",
        failed: "Process failed: ",
        pressAnyKey: "Press Enter to continue...",
        exit: "Exiting program. Goodbye!"
    },
    zh: {
        checking: "检查先决条件...",
        nodeOld: "您的 Node.js 版本太旧。 需要 v16+。 当前版本: ",
        gitMissing: "系统中未找到 Git。",
        installGit: "您现在要安装 Git 吗？ (1: 自动安装, 2: 手动安装, 3: 退出): ",
        sudoReq: "如果需要，请求 Sudo 访问权限。 提示时输入密码。",
        closeWarn: "警告：建议在继续之前关闭 FreeCAD 应用程序。",
        aiWarn: "重要提示：请确保您已安装列表中的至少一种 AI（Gemini、Claude、Goose 或 Aider）。",
        continue: "继续吗？(Y/N): ",
        menuOS: "\n=== 选择您的操作系统 ===",
        menu1: "1. MacOS",
        menu2: "2. Linux",
        menu3: "3. Windows",
        menu9: "9. 退出",
        select: "选择菜单: ",
        menuAI: "\n=== 选择您的 AI ===",
        ai1: "1. Gemini CLI",
        ai2: "2. Claude Desktop & Claude Code CLI",
        ai3: "3. Goose CLI",
        ai4: "4. Aider CLI",
        ai9: "9. 返回系统菜单",
        subMenu: "\n=== 配置子菜单 ===",
        sub3: "3. 设置 [AI] (仅文本反馈/省Token)",
        sub4: "4. 设置 [AI] (普通模式)",
        sub5: "5. 安装 FreeCAD-MCP (by neka-nat)",
        sub9: "9. 返回 AI 菜单",
        success: "过程成功完成！",
        failed: "过程失败: ",
        pressAnyKey: "按 Enter 键继续...",
        exit: "退出程序。 再见！"
    },
    th: {
        checking: "กำลังตรวจสอบข้อกำหนดเบื้องต้น...",
        nodeOld: "เวอร์ชัน Node.js ของคุณเก่าเกินไป ต้องใช้ v16+ ปัจจุบัน: ",
        gitMissing: "ไม่พบ Git ในระบบ",
        installGit: "คุณต้องการติดตั้ง Git ทันทีหรือไม่? (1: ติดตั้งอัตโนมัติ, 2: ติดตั้งด้วยตนเอง, 3: ออก): ",
        sudoReq: "ร้องขอสิทธิ์ Sudo หากจำเป็น กรุณาป้อนรหัสผ่านเมื่อได้รับแจ้ง",
        closeWarn: "คำเตือน: ขอแนะนำให้ปิดโปรแกรม FreeCAD ก่อนดำเนินการต่อ",
        aiWarn: "สำคัญ: ตรวจสอบให้แน่ใจว่าคุณได้ติดตั้ง AI อย่างน้อยหนึ่งตัวในรายการ (Gemini, Claude, Goose หรือ Aider)",
        continue: "ดำเนินการต่อหรือไม่? (Y/N): ",
        menuOS: "\n=== เลือกระบบปฏิบัติการของคุณ ===",
        menu1: "1. MacOS",
        menu2: "2. Linux",
        menu3: "3. Windows",
        menu9: "9. ออก",
        select: "เลือกเมนู: ",
        menuAI: "\n=== เลือก AI ของคุณ ===",
        ai1: "1. Gemini CLI",
        ai2: "2. Claude Desktop & Claude Code CLI",
        ai3: "3. Goose CLI",
        ai4: "4. Aider CLI",
        ai9: "9. กลับไปที่เมนูระบบปฏิบัติการ",
        subMenu: "\n=== เมนูย่อยการตั้งค่า ===",
        sub3: "3. ตั้งค่า [AI] (ประหยัด Token / ส่งข้อมูลเฉพาะข้อความ)",
        sub4: "4. ตั้งค่า [AI] (โหมดปกติ)",
        sub5: "5. ติดตั้ง FreeCAD-MCP by neka-nat",
        sub9: "9. กลับไปที่เมนู AI",
        success: "กระบวนการเสร็จสมบูรณ์!",
        failed: "กระบวนการล้มเหลว: ",
        pressAnyKey: "กด Enter เพื่อดำเนินการต่อ...",
        exit: "ออกจากโปรแกรม ลาก่อน!"
    }
};

let lang = 'id';
let t = i18n[lang];

// ================= UTILS =================
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const ask = (query) => new Promise((resolve) => rl.question(query, resolve));
const print = (msg, color = colors.reset) => console.log(`${color}${msg}${colors.reset}`);

// ================= BANNER =================
function showBanner() {
    console.clear();
    print("=========================================================", colors.cyan);
    print("     A U T O   I N S T A L L E R  FREECAD-MCP +          ", colors.bright + colors.yellow);
    print("     Gemini,Claude,Goose,Aider                           ", colors.bright + colors.green);
    print("     Github.com/cmalf                                    ", colors.reset);
    print("=========================================================", colors.cyan);
}

// ================= PREREQUISITES =================
async function checkPrerequisites() {
    print(`\n[*] ${t.checking}`, colors.yellow);
    
    const nodeVer = parseInt(process.version.replace('v', '').split('.')[0]);
    if (nodeVer < 16) {
        print(`${t.nodeOld}${process.version}`, colors.red);
        process.exit(1);
    }

    if (os.platform() !== 'win32') {
        print(`\n[*] ${t.sudoReq}`, colors.yellow);
        try {
            execSync('sudo -v', { stdio: 'inherit' });
        } catch (e) {
            print(t.failed + " Sudo auth failed.", colors.red);
        }
    }

    try {
        execSync('git --version', { stdio: 'ignore' });
    } catch (e) {
        print(`\n[!] ${t.gitMissing}`, colors.red);
        const choice = await ask(t.installGit);
        if (choice === '1') {
            try {
                if (os.platform() === 'win32') {
                    execSync('winget install --id Git.Git -e --source winget', { stdio: 'inherit' });
                } else if (os.platform() === 'darwin') {
                    execSync('brew install git', { stdio: 'inherit' });
                } else {
                    execSync('sudo apt-get update && sudo apt-get install -y git', { stdio: 'inherit' });
                }
            } catch (err) {
                print(t.failed + " Git installation failed.", colors.red);
                process.exit(1);
            }
        } else {
            process.exit(0);
        }
    }
}

// ================= CONFIG ENGINE =================
function writeConfig(selectedOS, aiType, onlyTextFeedback) {
    const home = os.homedir();
    const appData = process.env.APPDATA || path.join(home, 'AppData', 'Roaming');
    let filePath = '';
    let content = '';

    try {
        if (aiType === 'Gemini') {
            filePath = path.join(home, '.gemini', 'settings.json');
            const geminiJson = {
                "security": { "auth": { "selectedType": "oauth-personal" } },
                "mcp": { "allowed": ["freecad"] },
                "mcpServers": {
                    "freecad": {
                        "command": "uvx",
                        "args": onlyTextFeedback ? ["freecad-mcp", "--only-text-feedback"] : ["freecad-mcp"],
                        "timeout": 60000
                    }
                },
                "tools": { "shell": { "enableInteractiveShell": true } }
            };
            content = JSON.stringify(geminiJson, null, 2);

        } else if (aiType === 'Claude') {
            if (selectedOS === 'Windows') filePath = path.join(appData, 'Claude', 'claude_desktop_config.json');
            else if (selectedOS === 'MacOS') filePath = path.join(home, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
            else filePath = path.join(home, '.config', 'Claude', 'claude_desktop_config.json');

            const claudeJson = {
                "mcpServers": {
                    "freecad": {
                        "command": "uvx",
                        "args": onlyTextFeedback ? ["freecad-mcp", "--only-text-feedback"] : ["freecad-mcp"]
                    }
                }
            };
            content = JSON.stringify(claudeJson, null, 2);

        } else if (aiType === 'Goose') {
            if (selectedOS === 'Windows') filePath = path.join(appData, 'Block', 'goose', 'config.yaml');
            else if (selectedOS === 'MacOS') filePath = path.join(home, '.config', 'block', 'goose', 'config.yaml'); // fallback standard path
            else filePath = path.join(home, '.config', 'block', 'goose', 'config.yaml');

            content = `extensions:\n  freecad:\n    command: "uvx"\n    args:\n      - "freecad-mcp"\n${onlyTextFeedback ? '      - "--only-text-feedback"\n' : ''}`;

        } else if (aiType === 'Aider') {
            filePath = path.join(home, '.aider.conf.yml');
            content = `mcp-output: true\nmcp-servers:\n  - "uvx freecad-mcp${onlyTextFeedback ? ' --only-text-feedback' : ''}"\n`;
        }

        // Create Directory if not exist and write file
        fs.mkdirSync(path.dirname(filePath), { recursive: true });
        fs.writeFileSync(filePath, content, 'utf-8');
        print(`[OK] Configuration written successfully to:\n-> ${filePath}`, colors.green);
    } catch (err) {
        print(`[ERROR] Failed to write configuration: ${err.message}`, colors.red);
    }
}

// ================= FREE CAD INSTALLATION =================
function installFreeCADMCP(selectedOS) {
    print(`\n>>> Cloning & Preparing FreeCAD-MCP Addon...`, colors.cyan);
    const cloneDir = path.join(process.cwd(), 'freecad-mcp');
    
    try {
        if (!fs.existsSync(cloneDir)) {
            execSync('git clone https://github.com/neka-nat/freecad-mcp.git', { stdio: 'inherit' });
        }
        
        const sourceAddon = path.join(cloneDir, 'addon', 'FreeCADMCP');
        const home = os.homedir();
        const targetPaths = [];

        if (selectedOS === 'Windows') {
            const appData = process.env.APPDATA || path.join(home, 'AppData', 'Roaming');
            targetPaths.push(path.join(appData, 'FreeCAD', 'Mod', 'FreeCADMCP'));
        } else if (selectedOS === 'MacOS') {
            targetPaths.push(path.join(home, 'Library', 'Application Support', 'FreeCAD', 'v1-1', 'Mod', 'FreeCADMCP'));
            targetPaths.push(path.join(home, 'Library', 'Application Support', 'FreeCAD', 'v1-0', 'Mod', 'FreeCADMCP'));
        } else if (selectedOS === 'Linux') {
            targetPaths.push(path.join(home, '.FreeCAD', 'Mod', 'FreeCADMCP'));
            targetPaths.push(path.join(home, '.local', 'share', 'FreeCAD', 'v1-1', 'Mod', 'FreeCADMCP'));
            targetPaths.push(path.join(home, 'snap', 'freecad', 'common', 'Mod', 'FreeCADMCP'));
        }

        let copied = false;
        for (const target of targetPaths) {
            try {
                fs.mkdirSync(path.dirname(target), { recursive: true });
                fs.cpSync(sourceAddon, target, { recursive: true, force: true });
                print(`[OK] Copied addon to: ${target}`, colors.green);
                copied = true;
            } catch (e) {}
        }

        if (!copied) print(`[WARN] Could not automatically inject to default FreeCAD folders. Copy manually from ./freecad-mcp/addon/FreeCADMCP`, colors.yellow);
    } catch (err) {
        print(`[ERROR] ${t.failed}${err.message}`, colors.red);
    }
}

// ================= INTERACTIVE MENUS =================
async function startActionMenu(selectedOS, aiType) {
    let loop = true;
    while (loop) {
        showBanner();
        print(`\nOS: ${selectedOS} | AI: ${aiType}`, colors.magenta);
        print(t.subMenu, colors.bright + colors.cyan);
        print(t.sub3.replace('[AI]', aiType), colors.yellow);
        print(t.sub4.replace('[AI]', aiType));
        print(t.sub5);
        print(t.sub9, colors.red);

        const choice = await ask(t.select);
        switch (choice) {
            case '3':
                writeConfig(selectedOS, aiType, true);
                await ask(`\n${t.pressAnyKey}`);
                break;
            case '4':
                writeConfig(selectedOS, aiType, false);
                await ask(`\n${t.pressAnyKey}`);
                break;
            case '5':
                installFreeCADMCP(selectedOS);
                await ask(`\n${t.pressAnyKey}`);
                break;
            case '9':
                loop = false;
                break;
            default:
                print("Invalid choice!", colors.red);
                await ask(`\n${t.pressAnyKey}`);
        }
    }
}

async function startAIMenu(selectedOS) {
    let loop = true;
    while (loop) {
        showBanner();
        print(`\nOS Terpilih: ${selectedOS}`, colors.magenta);
        print(t.menuAI, colors.bright + colors.cyan);
        print(t.ai1);
        print(t.ai2);
        print(t.ai3);
        print(t.ai4);
        print(t.ai9, colors.red);

        const choice = await ask(t.select);
        switch (choice) {
            case '1': await startActionMenu(selectedOS, 'Gemini'); break;
            case '2': await startActionMenu(selectedOS, 'Claude'); break;
            case '3': await startActionMenu(selectedOS, 'Goose'); break;
            case '4': await startActionMenu(selectedOS, 'Aider'); break;
            case '9': loop = false; break;
            default:
                print("Invalid choice!", colors.red);
                await ask(`\n${t.pressAnyKey}`);
        }
    }
}

async function startMainMenu() {
    let loop = true;
    while (loop) {
        showBanner();
        print(t.menuOS, colors.bright + colors.cyan);
        print(t.menu1);
        print(t.menu2);
        print(t.menu3);
        print(t.menu9, colors.red);

        const choice = await ask(t.select);
        switch (choice) {
            case '1': await startAIMenu('MacOS'); break;
            case '2': await startAIMenu('Linux'); break;
            case '3': await startAIMenu('Windows'); break;
            case '9':
                print(t.exit, colors.green);
                rl.close();
                process.exit(0);
            default:
                print("Invalid choice!", colors.red);
                await ask(`\n${t.pressAnyKey}`);
        }
    }
}

// ================= INITIALIZATION =================
async function init() {
    showBanner();
    print("\nSelect Language / Pilih Bahasa:");
    print("1. English  2. Indonesia (Default)  3. 中文 (Mandarin)  4. ภาษาไทย (Thai)");
    const lChoice = await ask("Language [1-4]: ");
    
    if (lChoice === '1') lang = 'en';
    else if (lChoice === '3') lang = 'zh';
    else if (lChoice === '4') lang = 'th';
    else lang = 'id';
    t = i18n[lang];

    showBanner();
    // Prompt Close FreeCAD Warn
    print(`\n${t.closeWarn}`, colors.bright + colors.red);
    // Prompt AI Pre-installed Warn
    print(`${t.aiWarn}`, colors.bright + colors.yellow);
    
    const cont = await ask(t.continue);
    if (cont.toLowerCase() !== 'y') {
        print(t.exit, colors.green);
        rl.close();
        process.exit(0);
    }

    await checkPrerequisites();
    await startMainMenu();
}

init();
