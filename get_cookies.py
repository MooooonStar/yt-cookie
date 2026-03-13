import os
import json
import subprocess
from git import Repo
from datetime import datetime

def get_youtube_cookies():
    """使用 yt-dlp 从 Chrome 导出 YouTube cookie 为 Netscape 格式"""
    cookie_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies.txt')

    try:
        result = subprocess.run(
            ['yt-dlp', '--cookies-from-browser', 'chrome',
             '--cookies', cookie_file,
             '--skip-download', '--flat-playlist',
             '--playlist-items', '0',
             'https://www.youtube.com'],
            capture_output=True, text=True, timeout=30
        )

        if os.path.exists(cookie_file) and os.path.getsize(cookie_file) > 0:
            # 只保留 youtube 相关的 cookie
            with open(cookie_file, 'r') as f:
                lines = f.readlines()
            filtered = [l for l in lines if l.startswith('#') or l.strip() == '' or '.youtube.com' in l]
            with open(cookie_file, 'w') as f:
                f.writelines(filtered)
            print(f"成功导出 YouTube cookie 到 {cookie_file}")
            return True
        else:
            print(f"导出失败: {result.stderr}")
            return False

    except Exception as e:
        print(f"获取 cookie 失败: {str(e)}")
        return False

def get_bilibili_cookies():
    """获取 Bilibili 的 cookie 并保存为 biliup 所需的 JSON 格式"""
    url = 'https://www.bilibili.com'
    
    try:
        # 从 Chrome 获取 cookie
        cookies = chrome_cookies(url)
        
        # 转换为 biliup 所需的 JSON 格式 (参考 cookies.json)
        cookie_data = {
            "cookie_info": {
                "cookies": [],
                "domains": [
                    ".bilibili.com",
                    ".biligame.com", 
                    ".bigfun.cn",
                    ".bigfunapp.cn",
                    ".dreamcast.hk"
                ]
            },
            "sso": [
                "https://passport.bilibili.com/api/v2/sso",
                "https://passport.biligame.com/api/v2/sso",
                "https://passport.bigfunapp.cn/api/v2/sso"
            ],
            "token_info": {
                "access_token": "",
                "expires_in": 15552000,
                "mid": 0,
                "refresh_token": ""
            },
            "platform": "BiliTV"
        }
        print(cookies.items())
        # 添加 cookie 信息
        for name, value in cookies.items():
            cookie_data["cookie_info"]["cookies"].append({
                "expires": 0,
                "http_only": 0,
                "name": name,
                "secure": 0,
                "value": value
            })
        
        # 保存到文件
        with open('cookies.json', 'w', encoding='utf-8') as f:
            json.dump(cookie_data, f, ensure_ascii=False, indent=2)
            
        print(f"成功获取 {len(cookies)} 个 Bilibili cookie")
        return True
    
    except Exception as e:
        print(f"获取 Bilibili cookie 失败: {str(e)}")
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
    if get_youtube_cookies() :
        git_commit_and_push()