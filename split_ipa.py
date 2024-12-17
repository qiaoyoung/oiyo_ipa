#!/usr/bin/env python3
import os
import hashlib
import math

def split_file(file_path, chunk_size_mb=95):
    # 计算 MD5
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5_hash.update(chunk)
    
    file_md5 = md5_hash.hexdigest()
    file_size = os.path.getsize(file_path)
    
    # 分割文件
    chunk_size = chunk_size_mb * 1024 * 1024  # 转换为字节
    total_chunks = math.ceil(file_size / chunk_size)
    
    with open(file_path, 'rb') as f:
        for i in range(total_chunks):
            chunk_data = f.read(chunk_size)
            output_file = f"{file_path}.part{i:03d}"
            with open(output_file, 'wb') as chunk_file:
                chunk_file.write(chunk_data)
    
    # 创建元数据文件
    with open(f"{file_path}.meta", 'w') as meta:
        meta.write(f"MD5:{file_md5}\n")
        meta.write(f"Size:{file_size}\n")
        meta.write(f"Chunks:{total_chunks}\n")
    
    print(f"File split complete!")
    print(f"MD5: {file_md5}")
    print(f"Total chunks: {total_chunks}")
    print(f"Please add MD5 to GitHub Secrets as IPA_MD5")

if __name__ == "__main__":
    split_file("ios/oiyo.ipa")  # 修改这里的路径为你的 IPA 文件路径