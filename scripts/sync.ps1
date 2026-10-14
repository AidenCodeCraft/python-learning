<#
.SYNOPSIS
    双机同步：切机器前 pull，收工后 push。

.DESCRIPTION
    公司电脑和家里电脑共用同一个 Git 仓库时用这个脚本，避免忘记 pull/push。

    铁律：
      1. 开工先 pull，收工必 push。
      2. 一次只在一台电脑上写代码。

.EXAMPLE
    .\scripts\sync.ps1 status
    看看当前分支、有没有未提交的改动、远端配的是谁。

.EXAMPLE
    .\scripts\sync.ps1 pull
    在另一台电脑上开工前先跑这个。

.EXAMPLE
    .\scripts\sync.ps1 push -Message "feat(stage1): day01 对象模型练习与错题"
    收工后提交并推送。不传 -Message 会交互式问你。
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('status', 'pull', 'push')]
    [string]$Action = 'status',

    [string]$Message = ''
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

function Write-Step([string]$Title) {
    Write-Host ""
    Write-Host "==> $Title" -ForegroundColor Cyan
}

function Get-Upstream {
    # 用 git config 查上游，比 'git rev-parse @{u}' 干净：
    # 上游不存在时不会往 stderr 吐东西（$ErrorActionPreference='Stop' 下会被当成终止错误）
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    $remote = git config --get "branch.$branch.remote"
    $merge  = git config --get "branch.$branch.merge"
    if (-not $remote -or -not $merge) { return $null }
    $short = $merge -replace '^refs/heads/', ''
    return "$remote/$short"
}

function Assert-Clean([string]$Why) {
    $dirty = git status --porcelain
    if ($dirty) {
        Write-Host "警告：工作区还有未提交的改动，$Why 可能会冲突。" -ForegroundColor Yellow
        $dirty | ForEach-Object { Write-Host "  $_" }
        Write-Host "建议先执行： .\scripts\sync.ps1 push" -ForegroundColor Yellow
        return $false
    }
    return $true
}

# ---------- 虚拟环境提示 ----------
if (-not (Test-Path (Join-Path $root '.venv\Scripts\python.exe'))) {
    Write-Host "提示：还没建虚拟环境，先跑一次 .\scripts\setup_env.ps1" -ForegroundColor Yellow
}

switch ($Action) {
    'status' {
        Write-Step '分支与领先/落后情况'
        git status -sb

        Write-Step '未提交的改动'
        $dirty = git status --porcelain
        if ($dirty) { $dirty } else { Write-Host '干净，可以安全切换电脑。' -ForegroundColor Green }

        Write-Step '最近 5 次提交'
        git log --oneline -n 5

        Write-Step '远端配置'
        git remote -v

        $up = Get-Upstream
        if ($up) {
            Write-Host "当前分支上游：$up" -ForegroundColor Green
        } else {
            Write-Host "当前分支没有上游。首次推送执行：git push -u origin main" -ForegroundColor Yellow
        }
    }

    'pull' {
        $up = Get-Upstream
        if (-not $up) {
            throw "当前分支没有设置上游远端。先执行一次：`n  git push -u origin main"
        }

        [void](Assert-Clean 'pull')

        Write-Step "从 $up 拉取（--rebase，避免产生多余的合并提交）"
        git pull --rebase

        Write-Step '完成，现在可以开工'
        git log --oneline -n 3
    }

    'push' {
        Write-Step '暂存所有改动'
        git add -A

        $staged = git diff --cached --name-only
        if (-not $staged) {
            Write-Host '没有需要提交的改动。' -ForegroundColor Yellow
        }
        else {
            Write-Host '本次要提交的文件：' -ForegroundColor Cyan
            $staged | ForEach-Object { Write-Host "  $_" }

            if (-not $Message) {
                $Message = Read-Host '提交信息（例：feat(stage1): day01 对象模型练习）'
            }
            if (-not $Message.Trim()) { throw '提交信息不能为空。' }

            Write-Step "提交：$Message"
            git commit -m $Message
        }

        $up = Get-Upstream
        Write-Step '推送到远端'
        if ($up) {
            git push
        } else {
            Write-Host '首次推送，设置上游为 origin/main ...' -ForegroundColor Yellow
            git push -u origin main
        }

        Write-Step '完成'
        git log --oneline -n 3
        git status -sb
    }
}
