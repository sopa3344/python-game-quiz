# Git 실습과 남은 원격 작업

## 실제로 완료한 내용

프로젝트 폴더에서 `git init -b main`, `git add`, 기능별 `git commit`을 실행했습니다. `git checkout -b feature/quiz-play`로 플레이 기능 브랜치를 만들고, `git checkout main` 뒤 `git merge --no-ff feature/quiz-play`로 병합했습니다.

`git log --oneline --graph --all`로 기능별 기록과 병합 부모 둘을 확인할 수 있습니다. `docs/evidence/git-log.txt`는 증거 파일을 커밋하기 전 시점의 출력입니다.

## GitHub 업로드 결과

https://github.com/sopa3344/python-game-quiz 공개 저장소에 코드, 테스트, README, 실제 실행 로그를 업로드했습니다. GitHub 연결 API를 사용해 원본 17개 커밋의 기능별 변경과 두 부모를 가진 병합 구조를 가져왔습니다. 원격의 초기화 커밋과 공개 문서 갱신 커밋은 추가 기록입니다. 커밋 ID와 작성 시간은 달라졌으며 대응표는 github-import.md에 있습니다.

공개본의 실행 로그에서는 이메일과 개인 PC 경로를 제외했습니다. 로컬 원본 이력을 지우거나 날짜를 소급하지 않았습니다. 이것은 CLI push 또는 clone/pull을 성공 실행한 기록이 아닙니다.

## 완료하지 못한 내용

CLI 최초 push, GitHub clone, 복제본 수정과 push, 원래 폴더에서 pull은 미완료입니다. 업로드 전에 다음 오류를 실제로 확인했습니다.

| 시도 | 결과 |
| --- | --- |
| GitHub CLI 인증 확인 | 인증 실패 응답. 네트워크 제한이 있어 자격 증명 만료 여부는 확정할 수 없음 |
| 기존 공개 저장소 git ls-remote | Could not resolve host: github.com |
| 로컬 bare 저장소에 git push | Git for Windows의 sh 실행 중 0xC0000022 접근 거부 |
| git clone --local | 동일한 sh 실행 제한으로 실패 |
| 브라우저의 sopa3344 계정 선택 | 비밀번호 재입력 화면으로 이동, 사용자 로그인 필요 |

로컬 bare 저장소를 이용한 대체 실습도 성공했다고 기록하지 않았습니다. 실패한 명령은 `docs/evidence/git-local-rehearsal.txt`에 있습니다. 제한을 해제하거나 자격 증명을 변경하지 않았습니다.

## 연결이 가능한 환경에서 마무리하기

GitHub 계정으로 CLI 로그인을 완료한 뒤, GitHub의 저장소를 새 폴더에 clone해서 그 폴더에서 아래 스크립트를 실행합니다. 가져오기 전의 로컬 원본은 원격과 커밋 ID가 달라 직접 push하면 이력이 갈라집니다. 원본 이력은 보관하고 강제 push하지 않습니다. 스크립트는 push, 별도 clone, 복제본 변경과 push, 원본 pull, 두 HEAD 비교를 순서대로 수행합니다.

```powershell
pwsh -File scripts/finish_github.ps1
```

기본 대상은 이미 생성된 `sopa3344/python-game-quiz`입니다. 스크립트는 로그인 계정이 다르면 중단하고, 기존 origin이 다른 곳이면 변경하지 않습니다. 강제 push를 하지 않습니다. 실행 결과가 확인되기 전까지 명령어 실습을 완료로 표시하지 않습니다.

첫 커밋 직후 push 조건은 당시 실행하지 못했습니다. 나중에 전체 이력을 올려도 이 시간상의 순서를 소급해서 수행한 것으로 기록하지 않습니다.

## 손으로 연습할 때의 순서

1. 현재 GitHub 저장소를 새 폴더로 clone하고 그 폴더에서 진행합니다.
2. `git push -u origin main`과 `git push origin feature/quiz-play`로 이력을 올립니다.
3. 프로젝트 바깥에서 `git clone 저장소URL quiz-game-clone`을 실행합니다.
4. 복제 폴더의 README를 한 줄 고친 뒤 add, commit, push합니다.
5. 원래 폴더에서 `git pull --ff-only origin main`을 실행합니다.
6. 원본과 복제본에서 `git rev-parse HEAD`를 비교하고 README 문구도 확인합니다.

`clone`과 `pull`은 보통 새 커밋을 만들지 않으므로 커밋 그래프만으로 실행 사실이 증명되지 않습니다. 명령과 출력, 작업 폴더를 함께 남깁니다.
