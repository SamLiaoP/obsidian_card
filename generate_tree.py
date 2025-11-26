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
        '.DS_Store', 'generate_tree.py', 'tree.json',
        'index.html', 'README.md', 'SNAPSHOT.md'
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


def main():
    # 獲取當前目錄
    base_path = Path(__file__).parent.resolve()
    
    # GitHub Pages 的基礎 URL（需要根據實際倉庫名稱修改）
    # 格式: https://{username}.github.io/{repo-name}
    # 如果是用戶主頁則是: https://{username}.github.io
    base_url = "https://SamLiaoP.github.io/obsidian_card"  # 請修改為實際的 URL
    
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
    
    # 寫入 JSON 檔案
    output_path = base_path / 'tree.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功生成 tree.json")
    print(f"📁 共找到 {len(flat_list)} 個 Markdown 檔案")
    print(f"📍 輸出位置: {output_path}")


if __name__ == "__main__":
    main()

