"""Phase 8 follow-up: replace the now-stale '50개 태그 / 영어+한글 쌍' wording
across per-genre writing skills with the 25-tag / merged-tag wording, now that
data/tags.yaml's approved tags use a single 'Tag(태그)' form instead of two
separate approved entries. Each entry is (file, old, new); old must appear
exactly once in the file (asserted) so this can't silently touch unrelated text.
"""
import io

EDITS = [
    (".claude/skills/ai-tools-post-writing/SKILL.md",
     "tags:  # 50개 이상, 영어+한글 쌍",
     "tags:  # 25개 이상, 영/한 병용 개념은 Tag(태그) 형식"),
    (".claude/skills/ai-tools-post-writing/SKILL.md",
     "`data/tags.yaml`의 `ai_and_data`, `devops_and_tools`, `general_topics` 카테고리에서 50개 이상 선정. 도구명(Claude Code, ChatGPT, Cursor)과 개념(Prompt-Engineering/프롬프트엔지니어링, Automation/자동화)을 영어+한글 쌍으로 채운다.",
     "`data/tags.yaml`의 `ai_and_data`, `devops_and_tools`, `general_topics` 카테고리에서 25개 이상 선정. 도구명(Claude Code, ChatGPT, Cursor)과 병기 승인 태그(Prompt-Engineering(프롬프트엔지니어링), Automation(자동화))로 채운다."),
    (".claude/skills/ai-tools-post-writing/SKILL.md",
     "- [ ] tags 50개 이상(영어+한글)인가?",
     "- [ ] tags 25개 이상(`data/tags.yaml` 승인 태그, 병용 개념은 Tag(태그) 형식)인가?"),

    (".claude/skills/algorithm-post-writing/SKILL.md",
     "  코너 케이스 체크리스트, 50개 이상 태그 작성 규칙을 포함한다. content/collection/Algorithm/ 하위",
     "  코너 케이스 체크리스트, 25개 이상 태그 작성 규칙을 포함한다. content/collection/Algorithm/ 하위"),
    (".claude/skills/algorithm-post-writing/SKILL.md",
     "tags:  # 최소 50개 이상 (한글/영어 쌍으로 작성 권장)",
     "tags:  # 최소 25개 이상 (data/tags.yaml 승인 태그, 병용 개념은 Tag(태그) 형식)"),
    (".claude/skills/algorithm-post-writing/SKILL.md",
     "- [ ] Front Matter의 tags가 50개 이상인가? (한글/영어 쌍 활용)",
     "- [ ] Front Matter의 tags가 25개 이상인가? (data/tags.yaml 승인 태그 활용)"),

    (".claude/skills/blog-agent-pipeline/SKILL.md",
     "| 항상 | `data/tags.yaml` | tags 50개 이상 선정 |",
     "| 항상 | `data/tags.yaml` | tags 25개 이상 선정 |"),

    (".claude/skills/dev-programming-post-writing/SKILL.md",
     "tags:  # 50개 이상, 영어+한글 쌍",
     "tags:  # 25개 이상, 영/한 병용 개념은 Tag(태그) 형식"),
    (".claude/skills/dev-programming-post-writing/SKILL.md",
     "`data/tags.yaml`의 `programming_languages`, `code_quality`, `software_engineering`, `data_structures`, `complexity_analysis`, `general_topics` 카테고리에서 50개 이상 선정. 다루는 언어(예: Python, C++)와 개념(예: Recursion/재귀, Compiler/컴파일러)을 영어+한글 쌍으로 채운다.",
     "`data/tags.yaml`의 `programming_languages`, `code_quality`, `software_engineering`, `data_structures`, `complexity_analysis`, `general_topics` 카테고리에서 25개 이상 선정. 다루는 언어(예: Python, C++)와 병기 승인 태그(예: Recursion(재귀), Compiler(컴파일러))로 채운다."),
    (".claude/skills/dev-programming-post-writing/SKILL.md",
     "- [ ] tags 50개 이상(영어+한글)이고 무관한 보일러플레이트 태그가 없는가?",
     "- [ ] tags 25개 이상(`data/tags.yaml` 승인 태그)이고 무관한 보일러플레이트 태그가 없는가?"),

    (".claude/skills/educational-content-writing/SKILL.md",
     "— 태그 50개는 [`blog-post-writing`](../blog-post-writing/SKILL.md)의 단어/의미/도메인 특화 조합으로 채운다.",
     "— 태그 25개는 [`blog-post-writing`](../blog-post-writing/SKILL.md)의 단어/의미/도메인 특화 조합으로 채운다."),

    (".claude/skills/life-knowledge-post-writing/SKILL.md",
     "tags:  # 50개 이상, 영어+한글 쌍",
     "tags:  # 25개 이상, 영/한 병용 개념은 Tag(태그) 형식"),
    (".claude/skills/life-knowledge-post-writing/SKILL.md",
     "`data/tags.yaml`의 `general_topics` 및 주제별 카테고리(역사=`Culture`/역사 관련, 과학=`ai_and_data`/`system_and_low_level`와 무관하면 일반, 기기=하드웨어 관련)에서 50개 이상 선정. 주제 고유명사(제품명, 인물명, 사건명)와 개념어를 영어+한글 쌍으로 채운다.",
     "`data/tags.yaml`의 `general_topics` 및 주제별 카테고리(역사=`Culture`/역사 관련, 과학=`ai_and_data`/`system_and_low_level`와 무관하면 일반, 기기=하드웨어 관련)에서 25개 이상 선정. 주제 고유명사(제품명, 인물명, 사건명)와 병기 승인 태그(Tag(태그) 형식)로 채운다."),
    (".claude/skills/life-knowledge-post-writing/SKILL.md",
     "- [ ] tags 50개 이상(영어+한글)인가?",
     "- [ ] tags 25개 이상(`data/tags.yaml` 승인 태그)인가?"),

    (".claude/skills/movie-review-writing/movies-collection-rules.md",
     "tags:  # 최소 50개 이상(한/영 혼합, 고유명+키워드 권장)",
     "tags:  # 최소 25개 이상(data/tags.yaml 승인 태그, 고유명+키워드 권장)"),
    (".claude/skills/movie-review-writing/movies-collection-rules.md",
     "- [ ] Front Matter의 tags가 50개 이상인가?",
     "- [ ] Front Matter의 tags가 25개 이상인가?"),

    (".claude/skills/movie-review-writing/SKILL.md",
     "4. tags 50개 이상 (영어+한글 쌍)",
     "4. tags 25개 이상 (`data/tags.yaml` 승인 태그, 병용 개념은 Tag(태그) 형식)"),

    (".claude/skills/shell-command-post-writing/SKILL.md",
     "  공통. 플랫폼별 접두어([Bash Shell]/[CMD])·경로·태그 풀, 70자 이하 title, 150자 description, 50개 이상 tags,",
     "  공통. 플랫폼별 접두어([Bash Shell]/[CMD])·경로·태그 풀, 70자 이하 title, 150자 description, 25개 이상 tags,"),
    (".claude/skills/shell-command-post-writing/SKILL.md",
     "- **tags**: 최소 50개 이상(한글·영어 혼합), `data/tags.yaml` 승인 태그 우선.",
     "- **tags**: 최소 25개 이상, `data/tags.yaml` 승인 태그 우선."),
    (".claude/skills/shell-command-post-writing/SKILL.md",
     "- [ ] tags 50개 이상이고, 본문과 무관한 보일러플레이트 태그가 없는가?",
     "- [ ] tags 25개 이상이고, 본문과 무관한 보일러플레이트 태그가 없는가?"),

    (".claude/skills/systems-infra-post-writing/SKILL.md",
     "tags:  # 50개 이상, 영어+한글 쌍",
     "tags:  # 25개 이상, 영/한 병용 개념은 Tag(태그) 형식"),
    (".claude/skills/systems-infra-post-writing/SKILL.md",
     "`data/tags.yaml`의 `devops_and_tools`, `system_and_low_level`, `web_and_backend`, `frameworks_and_platforms`, `general_topics` 카테고리에서 50개 이상 선정. 도구명(Hugo, Docker, GitHub Actions)과 개념(CI-CD/지속통합, Optimization/최적화)을 영어+한글 쌍으로 채운다.",
     "`data/tags.yaml`의 `devops_and_tools`, `system_and_low_level`, `web_and_backend`, `frameworks_and_platforms`, `general_topics` 카테고리에서 25개 이상 선정. 도구명(Hugo, Docker, GitHub Actions)과 병기 승인 태그(CI-CD, Optimization(최적화))로 채운다."),
    (".claude/skills/systems-infra-post-writing/SKILL.md",
     "- [ ] tags 50개 이상(영어+한글)인가?",
     "- [ ] tags 25개 이상(`data/tags.yaml` 승인 태그)인가?"),

    (".claude/skills/tv-series-review-writing/SKILL.md",
     "  분석·숨겨진 내용 분석을 포함하며, 10개 이상 출처 검색·종합, Act 5 구조 분석, 50개 이상 태그·품질",
     "  분석·숨겨진 내용 분석을 포함하며, 10개 이상 출처 검색·종합, Act 5 구조 분석, 25개 이상 태그·품질"),
    (".claude/skills/tv-series-review-writing/SKILL.md",
     "tags:  # 최소 50개 이상(한/영 혼합, 고유명+키워드 권장)",
     "tags:  # 최소 25개 이상(data/tags.yaml 승인 태그, 고유명+키워드 권장)"),
    (".claude/skills/tv-series-review-writing/SKILL.md",
     "- [ ] Front Matter의 tags가 50개 이상인가?",
     "- [ ] Front Matter의 tags가 25개 이상인가?"),

    (".claude/skills/vocabulary-post-writing/SKILL.md",
     "  50개 이상 tags), 폴더명·날짜·워드클라우드 이미지 규칙, EN/KR 예문 구조, 콜로케이션·유의어·문법 포인트·한눈에",
     "  25개 이상 tags), 폴더명·날짜·워드클라우드 이미지 규칙, EN/KR 예문 구조, 콜로케이션·유의어·문법 포인트·한눈에"),
    (".claude/skills/vocabulary-post-writing/SKILL.md",
     "- **개수**: 최소 50개 이상 (영어 + 한글 혼합)",
     "- **개수**: 최소 25개 이상 (`data/tags.yaml` 승인 태그, 병용 개념은 Tag(태그) 형식)"),
    (".claude/skills/vocabulary-post-writing/SKILL.md",
     "- **실행 규칙**: 재사용 가능한 공통 태그 + 단어/품사/도메인 특화 태그를 조합해 50개 이상을 채운다. 한글/영어를 섞어서 검색 노출과 학습 검색성을 동시에 확보한다.",
     "- **실행 규칙**: 재사용 가능한 공통 태그 + 단어/품사/도메인 특화 태그를 조합해 25개 이상을 채운다. 영/한 병용 개념은 `data/tags.yaml`의 Tag(태그) 형식 승인 태그로 검색 노출과 학습 검색성을 동시에 확보한다."),
    (".claude/skills/vocabulary-post-writing/SKILL.md",
     '> 실제 작성 시 `title`, `description`, `tags`는 단어/품사/의미/도메인에 맞게 수정하되, **길이 규칙(70자 이하 title, 150자 내외 description, 50개 이상 tags)**은 반드시 지킨다.',
     '> 실제 작성 시 `title`, `description`, `tags`는 단어/품사/의미/도메인에 맞게 수정하되, **길이 규칙(70자 이하 title, 150자 내외 description, 25개 이상 tags)**은 반드시 지킨다.'),
    (".claude/skills/vocabulary-post-writing/SKILL.md",
     "   - Front Matter: `title`(`[Vocabulary] ...` 70자 이하), `description`(한국어 150자 내외), `tags`(영어/한글 50개 이상), `date`/`lastmod`(폴더명 날짜와 동일), `categories`(`English`, `Vocabulary`), `image`(`\"wordcloud.png\"`)",
     "   - Front Matter: `title`(`[Vocabulary] ...` 70자 이하), `description`(한국어 150자 내외), `tags`(`data/tags.yaml` 승인 태그 25개 이상), `date`/`lastmod`(폴더명 날짜와 동일), `categories`(`English`, `Vocabulary`), `image`(`\"wordcloud.png\"`)"),
    (".claude/skills/vocabulary-post-writing/SKILL.md",
     "- [ ] `tags`가 영어/한국어 포함 50개 이상인가? (단어/품사/도메인/메타 태그 조합)",
     "- [ ] `tags`가 `data/tags.yaml` 승인 태그 25개 이상인가? (단어/품사/도메인/메타 태그 조합)"),
]


def main():
    changed = 0
    for path, old, new in EDITS:
        with io.open(path, encoding="utf-8") as f:
            content = f.read()
        count = content.count(old)
        if count != 1:
            print(f"SKIP (found {count}x, expected 1): {path}: {old[:60]!r}")
            continue
        content = content.replace(old, new)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        changed += 1
    print(f"applied {changed}/{len(EDITS)} edits")


if __name__ == "__main__":
    main()
