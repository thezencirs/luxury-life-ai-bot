param(
    [string]$Category = "otomatik",
    [switch]$SetupBot = $true
)

$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"
$env:TELEGRAM_BOT_TOKEN = "9244899175:AAGEkK0KD_sMxMB_wJaS_4Mlrjh8IGLgr7c"
$env:TELEGRAM_CHAT_ID = "995164733"
$env:PYTHONPATH = "C:\Users\zenci\.gemini\antigravity\scratch\luxury-life-ai-bot\src;$env:PYTHONPATH"
$env:PATH = "C:\Users\zenci\.gemini\antigravity\scratch\tools\python\tools\Lib\site-packages\imageio_ffmpeg\binaries;$env:PATH"

$PYTHON_EXE = "C:\Users\zenci\.gemini\antigravity\scratch\tools\python\tools\python.exe"
$BOT_DIR = "C:\Users\zenci\.gemini\antigravity\scratch\luxury-life-ai-bot"

Set-Location $BOT_DIR

$argsList = @("src/main.py", "--category", $Category, "--output", "output/luxury_reel_final.mp4")
if ($SetupBot) {
    $argsList += "--setup-bot"
}

& $PYTHON_EXE @argsList
