#!/usr/bin/env python3
"""
生成 Markdown 檔案樹狀結構的腳本
用於創建可部署在 GitHub Pages 的靜態 API
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from urllib.parse import quote


def should_ignore(path: Path) -> bool:
    """檢查是否應該忽略此路徑"""
    ignore_patterns = {
        '.git', '.github', 'node_modules', '__pycache__',
        '.DS_Store', 'generate_tree.py', 'tree.json', 'index.json', 'search.json',
        'index.html', 'README.md', 'SNAPSHOT.md', 'DEPLOY_GUIDE.md', '.gitignore'
    }
    
    # 檢查檔名或資料夾名是否在忽略列表中
    if path.name in ignore_patterns:
        return True
    
    # 忽略以點開頭的檔案和資料夾（隱藏檔案）
    if path.name.startswith('.'):
        return True
    
    # 忽略非 .md 和非目錄的檔案
    if path.is_file() and path.suffix != '.md':
        return True
    
    return False


def generate_url(file_path: Path, base_path: Path, base_url: str) -> str:
    """生成檔案的 URL"""
    relative_path = file_path.relative_to(base_path)
    # URL encode 路徑以處理中文和特殊字符
    url_path = '/'.join(quote(part, safe='') for part in relative_path.parts)
    return f"{base_url}/{url_path}"


def build_tree(directory: Path, base_path: Path, base_url: str) -> Dict[str, Any]:
    """遞迴建立檔案樹狀結構"""
    result = {
        "name": directory.name if directory != base_path else "root",
        "type": "directory",
        "path": str(directory.relative_to(base_path)),
        "children": []
    }
    
    try:
        # 獲取所有項目並排序
        items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        
        for item in items:
            if should_ignore(item):
                continue
            
            if item.is_dir():
                # 遞迴處理子目錄
                subtree = build_tree(item, base_path, base_url)
                result["children"].append(subtree)
            elif item.suffix == '.md':
                # 處理 Markdown 檔案
                result["children"].append({
                    "name": item.name,
                    "type": "file",
                    "path": str(item.relative_to(base_path)),
                    "url": generate_url(item, base_path, base_url)
                })
    except PermissionError:
        pass
    
    return result


def generate_flat_list(directory: Path, base_path: Path, base_url: str) -> List[Dict[str, str]]:
    """生成扁平的檔案列表"""
    files = []
    
    for item in directory.rglob('*.md'):
        if should_ignore(item):
            continue
        
        files.append({
            "name": item.name,
            "path": str(item.relative_to(base_path)),
            "url": generate_url(item, base_path, base_url)
        })
    
    return sorted(files, key=lambda x: x['path'])


def generate_lightweight_index(directory: Path, base_path: Path, base_url: str) -> Dict[str, Any]:
    """生成輕量級索引（用於 GPT Actions）- 只包含分類摘要"""
    categories = {}
    
    for item in directory.rglob('*.md'):
        if should_ignore(item):
            continue
        
        relative_path = str(item.relative_to(base_path))
        parts = relative_path.split(os.sep)
        
        # 獲取主分類（第一層目錄）
        if len(parts) > 1:
            category = parts[0]
        else:
            category = "根目錄"
        
        if category not in categories:
            categories[category] = {
                "count": 0,
                "sample_files": []  # 只顯示前 3 個檔案作為範例
            }
        
        categories[category]["count"] += 1
        
        # 只保留前 3 個檔案作為範例
        if len(categories[category]["sample_files"]) < 3:
            categories[category]["sample_files"].append({
                "name": item.name,
                "path": relative_path
            })
    
    # 生成分類摘要
    category_list = []
    for cat, info in sorted(categories.items()):
        category_list.append({
            "category": cat,
            "count": info["count"],
            "sample_files": info["sample_files"]
        })
    
    return {
        "base_url": base_url,
        "total_files": sum(info["count"] for info in categories.values()),
        "categories": category_list,
        "usage": {
            "note": "This is a lightweight index. To get file content, use web browsing to access: base_url + '/' + url_encoded(path)",
            "example": "For path '1. 個人知識管理/file.md', URL is base_url + '/1.%20%E5%80%8B%E4%BA%BA%E7%9F%A5%E8%AD%98%E7%AE%A1%E7%90%86/file.md'",
            "search_tip": "Use search endpoint to find specific files by name or category"
        }
    }


def generate_search_index(directory: Path, base_path: Path, base_url: str) -> Dict[str, Any]:
    """生成可搜索的檔案索引（按分類完整列出）"""
    categories = {}
    
    for item in directory.rglob('*.md'):
        if should_ignore(item):
            continue
        
        relative_path = str(item.relative_to(base_path))
        parts = relative_path.split(os.sep)
        
        # 獲取主分類（第一層目錄）
        if len(parts) > 1:
            category = parts[0]
        else:
            category = "根目錄"
        
        if category not in categories:
            categories[category] = []
        
        categories[category].append({
            "name": item.name,
            "path": relative_path
        })
    
    # 生成分類摘要
    category_data = []
    for cat, files in sorted(categories.items()):
        category_data.append({
            "category": cat,
            "count": len(files),
            "files": files
        })
    
    return {
        "base_url": base_url,
        "total_files": sum(len(files) for files in categories.values()),
        "categories": category_data
    }


def main():
    # 獲取當前目錄
    base_path = Path(__file__).parent.resolve()
    
    # GitHub Pages 的基礎 URL（需要根據實際倉庫名稱修改）
    # 格式: https://{username}.github.io/{repo-name}
    # 如果是用戶主頁則是: https://{username}.github.io
    # 注意：GitHub Pages URL 必須全小寫
    base_url = "https://samliaop.github.io/obsidian_card"  # 請修改為實際的 URL
    
    print("正在掃描 Markdown 檔案...")
    
    # 生成樹狀結構
    tree = build_tree(base_path, base_path, base_url)
    
    # 生成扁平列表
    flat_list = generate_flat_list(base_path, base_path, base_url)
    
    # 組合最終結果
    result = {
        "base_url": base_url,
        "total_files": len(flat_list),
        "generated_at": None,  # 將由前端 JavaScript 填充
        "tree": tree,
        "files": flat_list
    }
    
    # 寫入完整的 tree.json
    output_path = base_path / 'tree.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功生成 tree.json")
    print(f"📁 共找到 {len(flat_list)} 個 Markdown 檔案")
    print(f"📍 輸出位置: {output_path}")
    
    # 生成輕量級索引（用於 GPT Actions - 只有摘要）
    lightweight_index = generate_lightweight_index(base_path, base_path, base_url)
    index_path = base_path / 'index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(lightweight_index, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功生成 index.json (輕量級索引 - 只有分類摘要)")
    print(f"📍 輸出位置: {index_path}")
    
    # 生成可搜索的檔案索引
    search_index = generate_search_index(base_path, base_path, base_url)
    search_path = base_path / 'search.json'
    with open(search_path, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功生成 search.json (完整檔案列表，按分類)")
    print(f"📍 輸出位置: {search_path}")


if __name__ == "__main__":
    main()

