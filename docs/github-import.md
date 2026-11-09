# GitHub 이력 가져오기 기록

2026-11-09, 공개 저장소 https://github.com/sopa3344/python-game-quiz 에 업로드했습니다.

GitHub 연결 API로 로컬 원본의 기능별 변경 내용과 부모 관계를 가져왔습니다. 커밋 ID와 작성 시간은 새 값이며 날짜를 소급하지 않았습니다. 첫 원격 커밋은 저장소 초기화용이고, 아래 17개 원본 기록을 이어 붙였습니다. 최종 공개 문서 갱신은 별도 커밋입니다.

개인 이메일, 작성자 설정값과 PC 폴더 경로는 공개 로그에서 제외했습니다. 그 외 프로그램과 테스트 소스는 원본과 동일합니다. 증거 수집 도구에는 개인 경로를 제외하는 처리를 추가했습니다. CLI push, clone, pull을 성공 실행한 것으로 표시하지 않습니다.

| 로컬 원본 커밋 | GitHub 가져온 커밋 | 변경 요약 |
| --- | --- | --- |
| 4798126797911b37c278afd50d86cb42936e9d77 | 25e6fd998189f85c32644929a844563136303a60 | Chore: Python 퀴즈 프로젝트와 Git 기본 설정 |
| f2d1990bc3ed8c6cb06e4fb184103bd6ce83c392 | a87fde8438ff2dd469f2ddb4f61340ea751c00c8 | Feat: 메뉴 반복과 숫자 입력 재시도 구현 |
| d940907f3cf8e34673fa202277a2832b9e808101 | ac6a1ead708930b8ea22196f82ea4be45d135f9b | Feat: Quiz 클래스와 문제 데이터 검증 구현 |
| 2f2b3571619f71336b3a9227d659df7afcca78a3 | a29d33b30e00ee0c33ca95027203aebdd4c2ad3a | Feat: 게임 개발 기초 기본 퀴즈 여섯 개 작성 |
| 958f0eda4a98c271e6b6df707d169f6ab84fcfc3 | 1bbdfc960a91a17893c2aa0b2dfbfbb050cfa66b | Feat: 별도 브랜치에서 퀴즈 출제와 정답 판정 구현 |
| 0a8003e574ecfeb871cfcbd5fc00f14bdf8d7426 | 746b2159de524281988e6711b4dcd57071183176 | Merge: 퀴즈 플레이 기능을 main에 병합 |
| 01f1725844dad0217b2b70ad3d1a0f19ea4df3eb | 7867442c8812d1fff2c197d398f6de80b2d52e68 | Feat: UTF-8 JSON 저장과 손상 파일 복구 구현 |
| 8980fd1e5ee1789a9c8f494dc11d64a342f5553c | 99454cb0fed208855cefaf8f44aa14b968553280 | Feat: 입력 검증을 포함한 퀴즈 등록과 즉시 저장 |
| e38fe77cf8552ccccb78bca63ddc50c99b7191d6 | 575db0acb3604deebd6c760075c932aec1a499f5 | Feat: 퀴즈 목록과 빈 목록 안내 구현 |
| 28e5bf77f056539fecbec46dfa95953ff3d5528d | 3a0db5a1174fe36d894fc4090ea49056add88c81 | Feat: 정답 비율로 최고 점수 비교와 영구 저장 |
| 864264e67b648318075f8073ae4bf4acb5a3cca4 | 7db2afe694ed1d645cd273ed0395593e4e9fa846 | Fix: Ctrl+C와 EOF 종료 시 완료한 데이터 보존 |
| 5859d9dbb73b849653ef69e45425252bc4e361ea | 6f6dfc290d3c9cb3a90e1288d5bcf0c9d99663f3 | Refactor: QuizGame 메뉴 선택 처리와 반복 분리 |
| 347ccc994cffeffcb2ba6faeb2af1412eeb2261f | bf0b9a2a6c34ac026238fa5a183594340c574fe2 | Test: 입력 예외와 저장 복구 및 재시작 23개 검증 |
| 1e03c7af83a5d84cfd6af126adf93073969ce362 | dfb76bacf265e6c6ca821f2f129a2df020ca1468 | Docs: 실행 방법과 데이터 구조 및 복습 가이드 작성 |
| 7899b6418c5c18a65b66a887054fb9e60499dae4 | 85ad181592d147fd2a6afe42c4d74bb49eda54f5 | Test: 실제 콘솔 실행과 재시작 증거 수집 도구 추가 |
| 322550ff23b2649ecf441a4e2eabb3a0073e1a26 | 295b44312f5c9d1c1a05f7e117b5d30feb45b5db | Docs: 검증 원문과 제출 상태 및 GitHub 마무리 절차 정리 |
| 81dd239bc6dd417aa15073f288897509c840df96 | 63dc0a23ab4578b3ece790105fc456b6342a1a0f | Fix: GitHub 실습 로그를 완성한 뒤 스테이징하도록 수정 |

GitHub feature/quiz-play 브랜치는 플레이 기능 커밋을 가리킵니다. 병합 커밋은 main의 기본 문제 커밋과 플레이 커밋을 두 부모로 연결합니다. 로컬 원본 저장소는 그대로 보관했습니다. 이후 작업은 GitHub 저장소를 새 폴더에 clone해서 진행합니다.

