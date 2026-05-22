#!/bin/bash
set -e

# PR 프리뷰면 Netlify 제공 URL, 아니면 프로덕션 URL 사용
if [ "$CONTEXT" = "deploy-preview" ]; then
  BASE_URL="$DEPLOY_PRIME_URL"
else
  BASE_URL="https://42jerrykim.github.io/"
fi

echo "Context: $CONTEXT"
echo "BaseURL: $BASE_URL"

# Hugo 빌드
hugo --gc --minify --baseURL "$BASE_URL"

# WebP 변환본이 아닌 원본 PNG 제거
find public/post -type f -name '*.png' ! -name '*_hu_*' -delete 2>/dev/null || true
find public/tags -type d -name 'page' -exec rm -rf {} + 2>/dev/null || true
find public/categories -type d -name 'page' -exec rm -rf {} + 2>/dev/null || true

# Pagefind 검색 인덱스 생성
npx pagefind --site public --output-subdir _pagefind --glob "post/**/*.html"
