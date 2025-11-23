# 模块1 环境检测与自动更新系统
import os
import sys
import json
import time
import requests
import hashlib
import zipfile
import subprocess
from pathlib import Path
import socket
import psutil
import platform

class 环境检测与自动更新系统
    def __init__(self)
        self.系统信息 = {}
        self.网络状态 = False
        self.更新源 = {
            主源 httpsraw.githubusercontent.comnovel-generatormain,
            备用源 httpsgitee.comnovel-generatormainraw
        }
        self.版本文件 = version.json
        self.代码仓库 = httpsgithub.comnovel-generatormainarchiverefsheadsmain.zip
        
    def 全面环境检测(self)
        执行全面的环境检测
        print(🔍 开始全面环境检测...)
        
        # 系统信息
        self.系统信息 = {
            操作系统 platform.system(),
            系统版本 platform.version(),
            系统架构 platform.architecture()[0],
            处理器 platform.processor(),
            内存_GB round(psutil.virtual_memory().total  (10243), 1),
            Python版本 platform.python_version(),
            工作目录 os.getcwd(),
            磁盘空间_GB self.获取磁盘空间()
        }
        
        # 网络检测
        self.网络状态 = self.检测网络连接()
        
        # 依赖检测
        self.依赖状态 = self.检测依赖()
        
        # 权限检测
        self.权限状态 = self.检测权限()
        
        # 输出检测报告
        self.生成检测报告()
        
        return all([self.网络状态, self.依赖状态, self.权限状态])
    
    def 检测网络连接(self)
        检测真实的网络连接状态
        print(🌐 检测网络连接...)
        测试网站 = [
            httpswww.baidu.com,
            httpswww.google.com, 
            httpswww.github.com,
            httpswww.biquge.com.cn
        ]
        
        for 网站 in 测试网站
            try
                响应 = requests.get(网站, timeout=10)
                if 响应.status_code == 200
                    print(f  ✅ 可访问 {网站})
                    self.网络状态 = True
                    return True
            except
                print(f  ❌ 无法访问 {网站})
                continue
        
        print(  ⚠️ 网络连接受限，部分功能可能无法使用)
        return False
    
    def 检测依赖(self)
        检测必要的依赖包
        print(📦 检测依赖包...)
        必要依赖 = [
            requests, beautifulsoup4, lxml, psutil,
            jieba, numpy, pandas, streamlit
        ]
        
        缺失依赖 = []
        for 依赖 in 必要依赖
            try
                __import__(依赖)
                print(f  ✅ {依赖})
            except ImportError
                缺失依赖.append(依赖)
                print(f  ❌ {依赖})
        
        if 缺失依赖
            print(f  🔧 正在安装缺失依赖 {缺失依赖})
            return self.安装依赖(缺失依赖)
        return True
    
    def 安装依赖(self, 依赖列表)
        自动安装缺失依赖
        try
            for 依赖 in 依赖列表
                subprocess.check_call([sys.executable, -m, pip, install, 依赖])
            return True
        except Exception as e
            print(f  ❌ 依赖安装失败 {e})
            return False
    
    def 检测权限(self)
        检测文件系统和网络权限
        print(🔐 检测系统权限...)
        
        # 检测写入权限
        try
            with open(权限测试.txt, w) as f
                f.write(测试)
            os.remove(权限测试.txt)
            print(  ✅ 文件写入权限)
        except
            print(  ❌ 文件写入权限不足)
            return False
        
        # 检测网络权限
        try
            socket.create_connection((www.baidu.com, 80), timeout=5)
            print(  ✅ 网络访问权限)
        except
            print(  ❌ 网络访问权限受限)
            return False
        
        return True
    
    def 获取磁盘空间(self)
        获取可用磁盘空间
        try
            磁盘 = psutil.disk_usage(os.getcwd())
            return round(磁盘.free  (10243), 1)
        except
            return 0
    
    def 生成检测报告(self)
        生成环境检测报告
        print(n + =50)
        print(📊 环境检测报告)
        print(=50)
        
        for 项目, 值 in self.系统信息.items()
            print(f  {项目} {值})
        
        print(f  网络状态 {'✅ 正常' if self.网络状态 else '❌ 异常'})
        print(f  依赖状态 {'✅ 正常' if self.依赖状态 else '❌ 异常'})
        print(f  权限状态 {'✅ 正常' if self.权限状态 else '❌ 异常'})
        print(=50)
    
    def 检查更新(self)
        检查代码更新
        if not self.网络状态
            print(🌐 网络不可用，跳过更新检查)
            return False
        
        print(🔄 检查更新...)
        try
            # 获取远程版本信息
            远程版本 = None
            for 源名称, 源地址 in self.更新源.items()
                try
                    响应 = requests.get(源地址 + self.版本文件, timeout=10)
                    if 响应.status_code == 200
                        远程版本 = 响应.json()
                        print(f  ✅ 从{源名称}获取版本信息)
                        break
                except
                    continue
            
            if not 远程版本
                print(  ❌ 无法获取远程版本信息)
                return False
            
            # 获取本地版本信息
            本地版本 = self.获取本地版本()
            
            if self.比较版本(远程版本[版本号], 本地版本.get(版本号, 0.0.0))
                print(f  🎯 发现新版本 {本地版本.get('版本号', '未知')} - {远程版本['版本号']})
                return self.执行更新(远程版本)
            else
                print(  ✅ 当前已是最新版本)
                return False
                
        except Exception as e
            print(f  ❌ 更新检查失败 {e})
            return False
    
    def 获取本地版本(self)
        获取本地版本信息
        try
            with open(self.版本文件, r, encoding=utf-8) as f
                return json.load(f)
        except
            return {版本号 0.0.0, 更新时间 未知}
    
    def 比较版本(self, 新版本, 旧版本)
        比较版本号
        新版本号 = tuple(map(int, 新版本.split(.)))
        旧版本号 = tuple(map(int, 旧版本.split(.)))
        return 新版本号  旧版本号
    
    def 执行更新(self, 远程版本信息)
        执行自动更新
        print(🚀 开始自动更新...)
        try
            # 下载新代码
            print(  📥 下载更新包...)
            响应 = requests.get(self.代码仓库, timeout=30)
            if 响应.status_code != 200
                print(  ❌ 下载更新包失败)
                return False
            
            # 保存更新包
            更新包路径 = update.zip
            with open(更新包路径, wb) as f
                f.write(响应.content)
            
            # 备份当前代码
            print(  💾 备份当前版本...)
            self.备份当前版本()
            
            # 解压更新包
            print(  📦 解压更新包...)
            with zipfile.ZipFile(更新包路径, 'r') as zip_ref
                zip_ref.extractall(temp_update)
            
            # 替换文件
            print(  🔄 替换文件...)
            self.替换文件(temp_updatemain, .)
            
            # 清理临时文件
            os.remove(更新包路径)
            import shutil
            shutil.rmtree(temp_update)
            
            # 更新版本信息
            with open(self.版本文件, w, encoding=utf-8) as f
                json.dump(远程版本信息, f, ensure_ascii=False, indent=2)
            
            print(  ✅ 更新完成！)
            return True
            
        except Exception as e
            print(f  ❌ 更新失败 {e})
            # 恢复备份
            self.恢复备份()
            return False
    
    def 备份当前版本(self)
        备份当前版本代码
        import datetime
        备份目录 = fbackup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}
        os.makedirs(备份目录, exist_ok=True)
        
        # 复制所有.py文件
        for 文件 in Path(.).glob(.py)
            if 文件.is_file()
                import shutil
                shutil.copy2(文件, 备份目录)
        
        print(f  ✅ 已备份到 {备份目录})
    
    def 恢复备份(self)
        从备份恢复
        备份列表 = list(Path(.).glob(backup_))
        if not 备份列表
            print(  ❌ 没有找到备份)
            return False
        
        最新备份 = max(备份列表, key=os.path.getmtime)
        print(f  🔄 从备份恢复 {最新备份})
        
        # 恢复文件
        for 文件 in 最新备份.glob(.py)
            import shutil
            shutil.copy2(文件, .)
        
        print(  ✅ 恢复完成)
        return True
    
    def 替换文件(self, 源目录, 目标目录)
        替换文件
        for 根目录, 目录列表, 文件列表 in os.walk(源目录)
            for 文件 in 文件列表
                源路径 = os.path.join(根目录, 文件)
                相对路径 = os.path.relpath(源路径, 源目录)
                目标路径 = os.path.join(目标目录, 相对路径)
                
                # 确保目标目录存在
                os.makedirs(os.path.dirname(目标路径), exist_ok=True)
                
                # 复制文件
                import shutil
                shutil.copy2(源路径, 目标路径)
    
    def 启动小白模式(self)
        启动小白友好模式
        print(👶 启动小白模式...)
        
        # 环境检测
        if not self.全面环境检测()
            print(❌ 环境检测失败，请检查上述问题)
            input(按回车键退出...)
            return False
        
        # 自动更新
        if self.网络状态
            if self.检查更新()
                print(🔄 更新完成，请重新运行程序)
                input(按回车键退出...)
                return True
        
        print(✅ 环境准备就绪，启动主系统...)
        return True

# 主启动程序
def main()
    系统 = 环境检测与自动更新系统()
    
    if len(sys.argv)  1 and sys.argv[1] == --小白模式
        if 系统.启动小白模式()
            # 导入并启动主系统
            try
                from 模块2_配置管理 import 配置管理系统
                主系统 = 配置管理系统()
                主系统.启动()
            except ImportError as e
                print(f❌ 启动主系统失败 {e})
                input(按回车键退出...)
    else
        # 标准模式
        print(🚀 启动标准模式...)
        系统.全面环境检测()
        if 系统.网络状态
            系统.检查更新()

if __name__ == __main__
    main()