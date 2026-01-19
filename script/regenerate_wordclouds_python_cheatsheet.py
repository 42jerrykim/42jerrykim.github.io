import os
import sys

from wordcloud_generator import create_wordcloud_image


def iter_bundle_dirs(collection_root: str) -> list[str]:
    bundle_dirs: list[str] = []
    for name in sorted(os.listdir(collection_root)):
        full_path = os.path.join(collection_root, name)
        if not os.path.isdir(full_path):
            continue
        index_md = os.path.join(full_path, "index.md")
        if os.path.isfile(index_md):
            bundle_dirs.append(full_path)
    return bundle_dirs


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    collection_root = os.path.join(
        repo_root, "content", "collection", "python-cheatsheet"
    )

    if not os.path.isdir(collection_root):
        print(f"오류: python-cheatsheet 컬렉션을 찾을 수 없습니다: {collection_root}")
        return 1

    bundle_dirs = iter_bundle_dirs(collection_root)
    if not bundle_dirs:
        print(f"오류: 번들 디렉토리를 찾지 못했습니다: {collection_root}")
        return 1

    total = len(bundle_dirs)
    print(f"대상 번들 수: {total}")

    failures: list[tuple[str, str]] = []
    for i, bundle_dir in enumerate(bundle_dirs, start=1):
        index_md = os.path.join(bundle_dir, "index.md")
        output_png = os.path.join(bundle_dir, "wordcloud.png")
        rel_dir = os.path.relpath(bundle_dir, repo_root)

        try:
            print(f"[{i}/{total}] 생성: {rel_dir}")
            create_wordcloud_image(index_md, output_png, mandatory_text="")
        except Exception as e:
            failures.append((rel_dir, repr(e)))
            print(f"[{i}/{total}] 실패: {rel_dir} ({e})")

    print(f"완료: 성공 {total - len(failures)} / 실패 {len(failures)}")
    if failures:
        print("\n실패 목록:")
        for rel_dir, err in failures:
            print(f"- {rel_dir}: {err}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
