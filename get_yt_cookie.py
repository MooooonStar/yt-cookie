import os
import json
import subprocess
from git import Repo
from datetime import datetime
from pycookiecheat import chrome_cookies

def get_youtube_cookies():
    """获取 YouTube 的 cookie 并保存为 Netscape 格式"""
    url = 'https://www.youtube.com'
    
    try:
        # 从 Chrome 获取 cookie
        cookies = chrome_cookies(url)
        
        # 转换为 Netscape 格式
        cookie_lines = []
        for name, value in cookies.items():
            # 构建 Netscape 格式的 cookie 行
            # 格式: domain flag path secure expiration name value
            cookie_lines.append(
                f".youtube.com\tTRUE\t/\tTRUE\t0\t{name}\t{value}"
            )
        
        # 添加文件头
        content = "# Netscape HTTP Cookie File\n" + "\n".join(cookie_lines)
        
        # 保存到文件
        with open('cookies.txt', 'w') as f:
            f.write(content)
            
        print(f"成功获取 {len(cookies)} 个 YouTube cookie")
        return True
    
    except Exception as e:
        print(f"获取 cookie 失败: {str(e)}")
        return False

def git_commit_and_push():
    """提交并推送更改到 GitHub"""
    try:
        repo = Repo(os.getcwd())
        repo.git.add('cookies.txt')
        
        # 配置 Git 用户信息 (如果尚未配置)
        if not repo.config_reader().has_option('user', 'name'):
            repo.config_writer().set_value('user', 'name', 'CookieBot').release()
        if not repo.config_reader().has_option('user', 'email'):
            repo.config_writer().set_value('user', 'email', 'cookiebot@example.com').release()
        
        # 提交更改
        commit_message = f"更新 YouTube cookie: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        repo.index.commit(commit_message)
        
        # 推送到远程仓库
        origin = repo.remote(name='origin')
        origin.push()
        
        print("成功推送 cookie 到 GitHub")
        return True
    
    except Exception as e:
        print(f"GitHub 推送失败: {str(e)}")
        return False

if __name__ == "__main__":
    if get_youtube_cookies():
        git_commit_and_push()