#Requires -Version 5.1
<#
.SYNOPSIS
    初始化 G:\python-learning 的 Python + FastAPI 学习环境。

.DESCRIPTION
    请在【你自己的终端】里运行本脚本（不要在 AI 助手的受限沙箱里跑）。
    脚本是幂等的：重复执行不会破坏已有环境。

    1) 校验 Python 3.13
    2) 创建虚拟环境 .venv
    3) 升级 pip / setuptools / wheel，安装 uv 与 pytest
    4) 生成 requirements.lock（锁定版本）
    5) 启动 Docker Desktop 并等待守护进程就绪

.EXAMPLE
    pwsh -File .\scripts\setup_env.ps1

.EXAMPLE
    pwsh -File .\scripts\setup_env.ps1 -SkipDocker
#>
[CmdletBinding()]
param(
    [switch]$SkipDocker,
    [int]$DockerTimeoutSeconds = 180
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
Write-Host "==> 项目根目录: $root" -ForegroundColor Cyan

function Get-DockerServerVersion {
    try {
        $v = docker info --format '{{.ServerVersion}}' 2>$null
        if ($LASTEXITCODE -eq 0 -and $v) { return $v.Trim() }
    } catch { }
    return $null
}

# ---------- 1. Python 3.13 ----------
$pyVersion = $null
try { $pyVersion = (& py -3.13 -c "import platform; print(platform.python_version())" 2>$null) } catch { }
if (-not $pyVersion) {
    throw "没有找到 Python 3.13。请先安装 Python 3.13，并在安装时勾选 'Add python.exe to PATH'。"
}
$pyExe = (& py -3.13 -c "import sys; print(sys.executable)").Trim()
Write-Host "==> 解释器: $pyExe (Python $pyVersion)" -ForegroundColor Green

# ---------- 2. 虚拟环境 ----------
$venvDir = Join-Path $root '.venv'
$venvPy  = Join-Path $venvDir 'Scripts\python.exe'
if (-not (Test-Path $venvPy)) {
    Write-Host "==> 创建虚拟环境 .venv ..."
    & py -3.13 -m venv $venvDir
    if (-not (Test-Path $venvPy)) { throw "虚拟环境创建失败：$venvPy 不存在。" }
} else {
    Write-Host "==> 复用已有虚拟环境 .venv"
}
& $venvPy --version

# ---------- 3. 基础依赖 ----------
Write-Host "==> 升级 pip / setuptools / wheel ..."
& $venvPy -m pip install --disable-pip-version-check --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) { throw "pip 升级失败。" }

Write-Host "==> 安装 uv 与 pytest ..."
& $venvPy -m pip install --disable-pip-version-check uv pytest
if ($LASTEXITCODE -ne 0) { throw "uv / pytest 安装失败。" }

Write-Host "==> 锁定版本到 requirements.lock ..."
& $venvPy -m pip freeze | Set-Content -Encoding utf8 (Join-Path $root 'requirements.lock')

# ---------- 4. Docker ----------
if ($SkipDocker) {
    Write-Host "==> 跳过 Docker 检查（-SkipDocker）" -ForegroundColor Yellow
} else {
    $dockerExe = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
    $serverVersion = Get-DockerServerVersion
    if ($serverVersion) {
        Write-Host "==> Docker 守护进程已在运行 (server $serverVersion)" -ForegroundColor Green
    } elseif (Test-Path $dockerExe) {
        Write-Host "==> 启动 Docker Desktop，最多等待 $DockerTimeoutSeconds 秒 ..."
        Start-Process -FilePath $dockerExe
        $deadline = (Get-Date).AddSeconds($DockerTimeoutSeconds)
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Seconds 5
            $serverVersion = Get-DockerServerVersion
            if ($serverVersion) { break }
        }
        if ($serverVersion) {
            Write-Host "==> Docker 就绪 (server $serverVersion)" -ForegroundColor Green
        } else {
            Write-Warning "Docker 在 $DockerTimeoutSeconds 秒内没有就绪。请手动打开 Docker Desktop，再重跑本脚本。"
        }
    } else {
        Write-Warning "没有找到 Docker Desktop（$dockerExe）。阶段 2 之前需要装好。"
    }
}

# ---------- 5. 自检 ----------
Write-Host "`n==> 版本自检" -ForegroundColor Cyan
& $venvPy --version
& $venvPy -m pip --version
$uvExe = Join-Path $venvDir 'Scripts\uv.exe'
if (Test-Path $uvExe) { & $uvExe --version } else { Write-Warning "uv.exe 未找到" }
$pytestExe = Join-Path $venvDir 'Scripts\pytest.exe'
if (Test-Path $pytestExe) { & $pytestExe --version } else { Write-Warning "pytest.exe 未找到" }
docker --version
git --version

Write-Host "`n完成 ✅" -ForegroundColor Green
Write-Host "以后每次开始学习前，先激活虚拟环境：" -ForegroundColor Green
Write-Host "    .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "如果提示禁止运行脚本，先执行（只需一次）：" -ForegroundColor Green
Write-Host "    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned" -ForegroundColor White
