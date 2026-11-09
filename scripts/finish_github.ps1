param(
    [string]$Owner = 'sopa3344',
    [string]$Repository = 'python-game-quiz'
)
$ErrorActionPreference = 'Stop'
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$clonePath = Join-Path (Split-Path $projectRoot -Parent) "quiz-game-clone-$stamp"
$remoteUrl = "https://github.com/$Owner/$Repository.git"
$evidenceDir = Join-Path $projectRoot 'docs/evidence'
$logPath = Join-Path $evidenceDir "github-sync-$stamp.txt"

function Invoke-Git {
    param([string[]]$Arguments)
    $result = & git @Arguments 2>&1
    $code = $LASTEXITCODE
    $record = "`nDIRECTORY: $(Get-Location)`nCOMMAND: git $($Arguments -join ' ')`n$($result -join "`n")`nEXIT CODE: $code"
    Add-Content -LiteralPath $logPath -Value $record -Encoding utf8
    Write-Host ($result -join "`n")
    if ($code -ne 0) { throw 'Git 작업이 실패했습니다. 기록을 확인하세요.' }
}

Push-Location $projectRoot
try {
    $login = & gh api user --jq .login
    if ($LASTEXITCODE -ne 0) { throw '먼저 gh auth login으로 GitHub 로그인을 완료하세요.' }
    if ($login.Trim() -ne $Owner) { throw "로그인 계정이 $Owner 계정과 다릅니다." }
    $dirty = & git status --porcelain
    if ($dirty) { throw '진행 전 변경 파일을 확인하고 커밋하세요. 기존 작업을 자동으로 덮어쓰지 않습니다.' }
    if (Test-Path -LiteralPath $clonePath) { throw '복제 대상 폴더가 이미 있습니다.' }
    & gh repo view "$Owner/$Repository" --json name *> $null
    if ($LASTEXITCODE -ne 0) {
        & gh repo create "$Owner/$Repository" --public --description 'Python 콘솔 퀴즈 게임과 Git 입문 실습'
        if ($LASTEXITCODE -ne 0) { throw '새 저장소를 생성하지 못했습니다.' }
    }
    New-Item -ItemType Directory -Force -Path $evidenceDir | Out-Null
    $existingOrigin = & git remote get-url origin 2>$null
    if ($LASTEXITCODE -eq 0) {
        if ($existingOrigin.Trim() -ne $remoteUrl) { throw 'origin이 다른 저장소를 가리킵니다. 직접 확인하세요.' }
    } else {
        Invoke-Git -Arguments @('remote', 'add', 'origin', $remoteUrl)
    }
    Invoke-Git -Arguments @('push', '-u', 'origin', 'main')
    Invoke-Git -Arguments @('push', 'origin', 'feature/quiz-play')
    Invoke-Git -Arguments @('clone', $remoteUrl, $clonePath)
    Push-Location $clonePath
    try {
        Add-Content -LiteralPath 'README.md' -Encoding utf8 -Value "`nGitHub 동기화 실습: $stamp 별도 복제 폴더에서 수정했습니다. 원본 폴더의 pull 검증 결과는 실행 로그를 확인합니다."
        Invoke-Git -Arguments @('add', 'README.md')
        Invoke-Git -Arguments @('commit', '-m', 'Docs: GitHub 복제 폴더에서 동기화 실습 문구 추가')
        Invoke-Git -Arguments @('push', 'origin', 'main')
        $cloneHead = & git rev-parse HEAD
    } finally { Pop-Location }
    Invoke-Git -Arguments @('pull', '--ff-only', 'origin', 'main')
    $originalHead = & git rev-parse HEAD
    if ($originalHead -ne $cloneHead) { throw '원본과 복제본 커밋이 일치하지 않습니다.' }
    $readme = Get-Content -LiteralPath 'README.md' -Raw -Encoding utf8
    if (-not $readme.Contains("GitHub 동기화 실습: $stamp")) { throw 'README 반영을 확인하지 못했습니다.' }
    Add-Content -LiteralPath $logPath -Encoding utf8 -Value "`nVERIFY: HEAD와 README 일치 확인 완료. $originalHead"
    Invoke-Git -Arguments @('add', '--', "docs/evidence/github-sync-$stamp.txt")
    # 커밋 이후에는 로그 파일을 수정하지 않아 작업 폴더를 깨끗하게 유지한다.
    & git commit -m 'Docs: GitHub clone과 push 및 pull 실행 증거 저장'
    if ($LASTEXITCODE -ne 0) { throw '증거 커밋에 실패했습니다.' }
    & git push origin main
    if ($LASTEXITCODE -ne 0) { throw '증거 업로드에 실패했습니다.' }
    Write-Host "완료: https://github.com/$Owner/$Repository"
    Write-Host '이 성공 결과를 확인한 뒤 제출 체크리스트를 갱신하세요.'
} finally { Pop-Location }
