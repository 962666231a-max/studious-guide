# 模块3: 网络学习引擎
import requests
import time
import random
import json
import re
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from typing import Dict, List, Any, Optional, Set
from pathlib import Path
import urllib.robotparser
from 模块2_配置管理 import 获取配置管理器

class 智能爬虫系统:
    def __init__(self):
        self.配置管理器 = 获取配置管理器()
        self.网络配置 = self.配置管理器.获取网络配置()
        self.日志器 = logging.getLogger('智能爬虫')
        
        # 爬虫状态
        self.爬取队列 = []
        self.已爬取网址 = set()
        self.robots解析器 = {}
        self.会话 = requests.Session()
        self.爬虫锁 = threading.Lock()
        
        # 预设角色库和世界观库
        self.预设角色库 = self.初始化预设角色库()
        self.预设世界观库 = self.初始化预设世界观库()
        
        # 统计信息
        self.统计信息 = {
            "总爬取次数": 0,
            "成功次数": 0,
            "失败次数": 0,
            "总字数": 0,
            "开始时间": time.time()
        }
        
        self.设置会话头()
    
    def 设置会话头(self):
        """设置请求头"""
        self.会话.headers.update({
            'User-Agent': self.网络配置["用户代理"],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def 初始化预设角色库(self) -> Dict[str, Any]:
        """初始化米哈游游戏角色预设库"""
        return {
            "崩坏：星穹铁道": {
                "黑塔": {
                    "姓名": "黑塔",
                    "称号": "天才俱乐部#83",
                    "性别": "女",
                    "阵营": "空间站「黑塔」",
                    "命途": "智识",
                    "属性": "冰",
                    "背景故事": "天才俱乐部#83席，空间站「黑塔」的真正主人。凭借天才的智慧创造了诸多奇迹，如今对收集奇物和研究星神产生了浓厚兴趣。",
                    "性格特点": ["天才", "傲慢", "好奇心强", "务实", "追求效率"],
                    "外貌特征": "粉色双马尾，身着科幻风格的服饰，身边漂浮着代步设备",
                    "特殊能力": ["空间站操控", "奇物研究", "智识命途之力"],
                    "经典台词": [
                        "有意思，太有意思了！",
                        "时间就是金钱，效率就是生命。",
                        "这只是个小小的实验罢了。"
                    ],
                    "人际关系": {
                        "主角": "研究对象兼合作伙伴",
                        "艾丝妲": "空间站代理站长",
                        "其他天才俱乐部成员": "竞争对手"
                    }
                },
                "星": {
                    "姓名": "星",
                    "称号": "开拓者",
                    "性别": "可选",
                    "阵营": "星穹列车",
                    "命途": "毁灭/存护",
                    "属性": "物理/火",
                    "背景故事": "被卡芙卡植入星核而苏醒的神秘存在，登上星穹列车踏上开拓之旅。",
                    "性格特点": ["勇敢", "好奇心强", "正义感", "偶尔脱线"]
                },
                "三月七": {
                    "姓名": "三月七",
                    "称号": "记忆追寻者", 
                    "性别": "女",
                    "阵营": "星穹列车",
                    "命途": "存护",
                    "属性": "冰",
                    "背景故事": "在冰中被发现的神秘少女，失去了所有记忆，只有一张车票和名字「三月七」。"
                }
            },
            "原神": {
                "钟离": {
                    "姓名": "钟离",
                    "称号": "尘世闲游",
                    "性别": "男", 
                    "阵营": "璃月",
                    "元素": "岩",
                    "武器": "长柄武器",
                    "背景故事": "璃月的岩神，如今以凡人之姿体验人间生活。",
                    "性格特点": ["沉稳", "博学", "优雅", "有点缺摩拉"]
                },
                "雷电将军": {
                    "姓名": "雷电将军",
                    "称号": "一心净土",
                    "性别": "女",
                    "阵营": "稻妻",
                    "元素": "雷",
                    "武器": "单手剑",
                    "背景故事": "稻妻的雷神，追求永恒之道。"
                }
            },
            "崩坏3": {
                "琪亚娜·卡斯兰娜": {
                    "姓名": "琪亚娜·卡斯兰娜",
                    "称号": "空之律者",
                    "性别": "女",
                    "阵营": "天命",
                    "属性": "生物",
                    "背景故事": "卡斯兰娜家族的战士，经历重重磨难成长为真正的女武神。"
                },
                "雷电芽衣": {
                    "姓名": "雷电芽衣", 
                    "称号": "雷之律者",
                    "性别": "女",
                    "阵营": "天命",
                    "属性": "异能",
                    "背景故事": "ME社的大小姐，第三律者，琪亚娜的重要伙伴。"
                }
            }
        }
    
    def 初始化预设世界观库(self) -> Dict[str, Any]:
        """初始化米哈游游戏世界观预设库"""
        return {
            "崩坏：星穹铁道": {
                "宇宙结构": {
                    "星神": ["存护克里珀", "智识博识尊", "巡猎岚", "丰饶药师", "毁灭纳努克"],
                    "命途": "星神走过的道路，凡人可以追随命途获得力量",
                    "星穹列车": "穿梭于星系之间的神奇列车，由姬子驾驶",
                    "空间站": "黑塔空间站，收藏各种宇宙奇物"
                },
                "主要势力": {
                    "星际和平公司": "追求商业利益的庞大组织",
                    "反物质军团": "追随毁灭星神的破坏势力", 
                    "天才俱乐部": "宇宙中最聪明的83位天才组成的组织"
                },
                "科技水平": "高度发达的太空文明，具备星际旅行能力",
                "魔法体系": "基于命途的力量体系，追随不同星神获得不同能力",
                "历史背景": "星神开辟命途，文明在星神影响下发展演变"
            },
            "原神": {
                "世界结构": {
                    "提瓦特大陆": "由七个国家组成的主要世界",
                    "天空岛": "神灵居住的地方",
                    "元素": ["火", "水", "风", "雷", "草", "冰", "岩"]
                },
                "主要国家": {
                    "蒙德": "风与自由之城",
                    "璃月": "岩与契约之港", 
                    "稻妻": "雷与永恒之国",
                    "须弥": "草与智慧之都"
                },
                "神之眼": "凡人获得元素力量的凭证",
                "历史背景": "远古时期有七神执政，如今旅行者正在寻找失散的亲人"
            },
            "崩坏3": {
                "世界结构": {
                    "崩坏": "周期性毁灭文明的神秘力量",
                    "律者": "崩坏的使徒，拥有毁灭世界的力量",
                    "天命组织": "对抗崩坏的主要组织",
                    "逆熵": "与天命理念不同的对抗崩坏组织"
                },
                "力量体系": {
                    "女武神": "经过改造能够使用崩坏能的战士",
                    "圣痕": "增强女武神能力的特殊印记",
                    "神之键": "用律者核心制造的强大武器"
                },
                "科技水平": "高度发达的基因工程和机械技术",
                "历史背景": "崩坏不断毁灭文明，人类在抗争中寻找生存之道"
            }
        }
    
    def 检查robots协议(self, url: str) -> bool:
        """检查robots.txt协议"""
        if not self.网络配置["遵守规范"]:
            return True
        
        try:
            解析器 = urllib.robotparser.RobotFileParser()
            基础域名 = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
            robots_url = urljoin(基础域名, "/robots.txt")
            
            if 基础域名 not in self.robots解析器:
                解析器.set_url(robots_url)
                解析器.read()
                self.robots解析器[基础域名] = 解析器
            
            解析器 = self.robots解析器[基础域名]
            return 解析器.can_fetch(self.网络配置["用户代理"], url)
            
        except Exception as e:
            self.日志器.warning(f"Robots协议检查失败 {url}: {e}")
            return True
    
    def 智能请求(self, url: str, 最大重试次数: int = None) -> Optional[requests.Response]:
        """智能请求网页，包含重试机制和延迟"""
        if not self.网络配置["真实爬取"]:
            self.日志器.info(f"模拟爬取: {url}")
            return self.模拟请求(url)
        
        if not self.检查robots协议(url):
            self.日志器.warning(f"被robots.txt禁止访问: {url}")
            return None
        
        # 遵守爬取延迟
        time.sleep(self.网络配置["爬取延迟"] + random.uniform(0, 1))
        
        重试次数 = 最大重试次数 or self.网络配置["重试次数"]
        
        for 尝试 in range(重试次数):
            try:
                响应 = self.会话.get(
                    url, 
                    timeout=self.网络配置["超时时间"],
                    allow_redirects=True
                )
                
                if 响应.status_code == 200:
                    self.统计信息["成功次数"] += 1
                    return 响应
                elif 响应.status_code in [403, 404, 500, 503]:
                    self.日志器.warning(f"HTTP {响应.status_code} 错误: {url}")
                    break
                else:
                    self.日志器.warning(f"HTTP {响应.status_code} 错误，重试 {尝试+1}/{重试次数}: {url}")
                    
            except requests.exceptions.RequestException as e:
                self.日志器.warning(f"请求异常，重试 {尝试+1}/{重试次数}: {url} - {e}")
            
            if 尝试 < 重试次数 - 1:
                time.sleep(2 ** 尝试)  # 指数退避
        
        self.统计信息["失败次数"] += 1
        return None
    
    def 模拟请求(self, url: str) -> Optional[requests.Response]:
        """模拟请求，用于测试或网络受限时"""
        class 模拟响应:
            def __init__(self, url):
                self.url = url
                self.status_code = 200
                self.text = self.生成模拟内容()
                self.encoding = 'utf-8'
            
            def 生成模拟内容(self):
                """生成模拟的网页内容"""
                # 根据URL猜测内容类型
                if "biquge" in self.url or "novel" in self.url:
                    return self.生成小说页面()
                elif "character" in self.url or "角色" in self.url:
                    return self.生成角色页面()
                elif "worldview" in self.url or "世界观" in self.url:
                    return self.生成世界观页面()
                else:
                    return self.生成通用页面()
            
            def 生成小说页面(self):
                return f"""
                <html>
                <head><title>模拟小说页面</title></head>
                <body>
                    <div class="book">
                        <h1>模拟小说标题</h1>
                        <div class="content">
                            <p>这是一个模拟的小说内容页面。在实际运行中，这里会是从真实网站爬取的小说内容。</p>
                            <p>小说内容包含各种情节发展和人物对话，用于训练AI模型。</p>
                        </div>
                    </div>
                </body>
                </html>
                """
            
            def 生成角色页面(self):
                return """
                <html>
                <body>
                    <div class="character">
                        <h1>模拟角色资料</h1>
                        <p>姓名：模拟角色</p>
                        <p>背景：这是一个模拟的角色背景故事</p>
                        <p>性格特点：勇敢、聪明、善良</p>
                    </div>
                </body>
                </html>
                """
            
            def 生成世界观页面(self):
                return """
                <html>
                <body>
                    <div class="worldview">
                        <h1>模拟世界观设定</h1>
                        <p>这是一个模拟的世界观设定页面。</p>
                        <p>包含世界结构、历史背景、力量体系等信息。</p>
                    </div>
                </body>
                </html>
                """
            
            def 生成通用页面(self):
                return f"""
                <html>
                <head><title>模拟页面 - {self.url}</title></head>
                <body>
                    <h1>模拟网页内容</h1>
                    <p>这是URL: {self.url} 的模拟内容</p>
                    <p>在实际网络爬取中，这里会是真实的网页内容。</p>
                </body>
                </html>
                """
        
        return 模拟响应(url)
    
    def 提取小说内容(self, html: str, url: str) -> Dict[str, Any]:
        """从HTML中提取小说内容"""
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # 多种选择器尝试提取标题
            标题 = None
            标题选择器 = ['h1', '.book-title', '#bookname', 'title']
            for 选择器 in 标题选择器:
                元素 = soup.select_one(选择器)
                if 元素:
                    标题 = 元素.get_text().strip()
                    break
            
            # 提取正文内容
            内容 = None
            内容选择器 = ['#content', '.chapter-content', '.novel-content', '[class*="content"]']
            for 选择器 in 内容选择器:
                元素 = soup.select_one(选择器)
                if 元素:
                    # 清理内容
                    for 标签 in 元素.select('script, style, nav, footer, header'):
                        标签.decompose()
                    内容 = 元素.get_text().strip()
                    break
            
            # 提取元数据
            元数据 = {}
            元数据选择器 = ['.book-intro', '.description', '#intro', '.summary']
            for 选择器 in 元数据选择器:
                元素 = soup.select_one(选择器)
                if 元素:
                    元数据["简介"] = 元素.get_text().strip()
                    break
            
            return {
                "标题": 标题 or "未知标题",
                "内容": 内容 or "无法提取内容",
                "元数据": 元数据,
                "网址": url,
                "提取时间": time.time(),
                "字数": len(内容) if 内容 else 0
            }
            
        except Exception as e:
            self.日志器.error(f"内容提取失败 {url}: {e}")
            return {
                "标题": "提取失败",
                "内容": f"内容提取失败: {e}",
                "元数据": {},
                "网址": url,
                "提取时间": time.time(),
                "字数": 0
            }
    
    def 提取角色信息(self, html: str, url: str) -> Dict[str, Any]:
        """从HTML中提取角色信息"""
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # 尝试提取角色名称
            角色名 = None
            名称选择器 = ['h1', '.character-name', '.role-name', '[class*="name"]']
            for 选择器 in 名称选择器:
                元素 = soup.select_one(选择器)
                if 元素:
                    角色名 = 元素.get_text().strip()
                    break
            
            # 提取角色信息
            角色信息 = {"姓名": 角色名 or "未知角色"}
            
            # 常见的信息字段
            信息字段 = {
                "称号": ["称号", "别名", "昵称"],
                "性别": ["性别"],
                "阵营": ["阵营", "势力", "组织"],
                "背景": ["背景", "经历", "故事"],
                "性格": ["性格", "特点", "特征"]
            }
            
            # 尝试提取这些字段
            for 字段, 关键词列表 in 信息字段.items():
                for 关键词 in 关键词列表:
                    # 查找包含关键词的元素
                    元素 = soup.find(lambda tag: tag.name in ['p', 'div', 'span'] and 关键词 in tag.get_text())
                    if 元素:
                        角色信息[字段] = 元素.get_text().strip()
                        break
            
            return 角色信息
            
        except Exception as e:
            self.日志器.error(f"角色信息提取失败 {url}: {e}")
            return {"姓名": "提取失败", "错误": str(e)}
    
    def 爬取指定内容(self, 搜索词: str, 内容类型: str = "自动") -> List[Dict[str, Any]]:
        """爬取指定内容"""
        self.日志器.info(f"开始爬取: {搜索词} ({内容类型})")
        
        结果列表 = []
        
        if 内容类型 == "角色" or 内容类型 == "自动":
            # 先检查预设库
            预设结果 = self.从预设库查询角色(搜索词)
            if 预设结果:
                结果列表.extend(预设结果)
                self.日志器.info(f"从预设库找到角色: {搜索词}")
            
            # 网络爬取
            if self.网络配置["真实爬取"]:
                网络结果 = self.网络爬取角色(搜索词)
                结果列表.extend(网络结果)
        
        if 内容类型 == "世界观" or 内容类型 == "自动":
            # 检查预设库
            预设结果 = self.从预设库查询世界观(搜索词)
            if 预设结果:
                结果列表.extend(预设结果)
            
            # 网络爬取
            if self.网络配置["真实爬取"]:
                网络结果 = self.网络爬取世界观(搜索词)
                结果列表.extend(网络结果)
        
        if 内容类型 == "小说" or 内容类型 == "自动":
            # 网络爬取小说
            if self.网络配置["真实爬取"]:
                网络结果 = self.网络爬取小说(搜索词)
                结果列表.extend(网络结果)
        
        return 结果列表
    
    def 从预设库查询角色(self, 角色名: str) -> List[Dict[str, Any]]:
        """从预设角色库查询"""
        结果 = []
        for 游戏, 角色库 in self.预设角色库.items():
            for 名称, 信息 in 角色库.items():
                if 角色名 in 名称 or 角色名 in 信息.get("称号", ""):
                    结果.append({
                        "类型": "角色",
                        "来源": "预设库",
                        "游戏": 游戏,
                        "数据": 信息,
                        "匹配度": self.计算匹配度(角色名, 名称, 信息.get("称号", ""))
                    })
        return 结果
    
    def 从预设库查询世界观(self, 世界观名: str) -> List[Dict[str, Any]]:
        """从预设世界观库查询"""
        结果 = []
        for 游戏, 世界观 in self.预设世界观库.items():
            if 世界观名 in 游戏:
                结果.append({
                    "类型": "世界观", 
                    "来源": "预设库",
                    "游戏": 游戏,
                    "数据": 世界观,
                    "匹配度": 1.0
                })
        return 结果
    
    def 计算匹配度(self, 搜索词: str, 名称: str, 别名: str) -> float:
        """计算搜索词与名称的匹配度"""
        if 搜索词 == 名称:
            return 1.0
        elif 搜索词 in 名称:
            return 0.8
        elif 搜索词 in 别名:
            return 0.6
        else:
            return 0.3
    
    def 网络爬取角色(self, 角色名: str) -> List[Dict[str, Any]]:
        """从网络爬取角色信息"""
        # 构建搜索URL
        搜索词编码 = requests.utils.quote(角色名)
        搜索URL列表 = [
            f"https://www.baidu.com/s?wd={搜索词编码} 角色 设定",
            f"https://www.google.com/search?q={搜索词编码} character",
            f"https://wiki.biligame.com/ys/{搜索词编码}" if "原神" in 角色名 else None,
            f"https://wiki.biligame.com/sr/{搜索词编码}" if "星穹" in 角色名 else None
        ]
        
        结果列表 = []
        for url in 搜索URL列表:
            if not url:
                continue
            
            响应 = self.智能请求(url)
            if 响应 and 响应.status_code == 200:
                角色信息 = self.提取角色信息(响应.text, url)
                if 角色信息["姓名"] != "提取失败":
                    结果列表.append({
                        "类型": "角色",
                        "来源": "网络爬取",
                        "网址": url,
                        "数据": 角色信息,
                        "匹配度": 0.5  # 网络结果的默认匹配度
                    })
        
        return 结果列表
    
    def 网络爬取世界观(self, 世界观名: str) -> List[Dict[str, Any]]:
        """从网络爬取世界观信息"""
        # 类似角色爬取，但专注于世界观信息
        搜索词编码 = requests.utils.quote(世界观名 + " 世界观 设定")
        搜索URL = f"https://www.baidu.com/s?wd={搜索词编码}"
        
        响应 = self.智能请求(搜索URL)
        if 响应 and 响应.status_code == 200:
            # 这里简化处理，实际应该提取世界观相关信息
            return [{
                "类型": "世界观",
                "来源": "网络爬取", 
                "网址": 搜索URL,
                "数据": {"名称": 世界观名, "描述": "从网络提取的世界观信息"},
                "匹配度": 0.5
            }]
        
        return []
    
    def 网络爬取小说(self, 关键词: str) -> List[Dict[str, Any]]:
        """从网络爬取小说内容"""
        # 构建小说搜索URL
        搜索词编码 = requests.utils.quote(关键词 + " 小说")
        搜索URL = f"https://www.biquge.com.cn/search.php?keyword={搜索词编码}"
        
        响应 = self.智能请求(搜索URL)
        if not 响应 or 响应.status_code != 200:
            return []
        
        # 解析搜索结果，获取小说链接
        soup = BeautifulSoup(响应.text, 'lxml')
        小说链接列表 = []
        
        for 链接 in soup.select('a[href*="book"]'):
            href = 链接.get('href')
            if href and not href.startswith('http'):
                href = urljoin(搜索URL, href)
            小说链接列表.append(href)
        
        # 爬取前几个小说页面
        结果列表 = []
        for 链接 in 小说链接列表[:3]:  # 限制数量
            响应 = self.智能请求(链接)
            if 响应 and 响应.status_code == 200:
                小说内容 = self.提取小说内容(响应.text, 链接)
                结果列表.append({
                    "类型": "小说",
                    "来源": "网络爬取",
                    "网址": 链接,
                    "数据": 小说内容,
                    "匹配度": 0.7
                })
        
        return 结果列表
    
    def 批量爬取(self, 任务列表: List[Dict[str, str]]) -> Dict[str, Any]:
        """批量爬取多个任务"""
        self.日志器.info(f"开始批量爬取 {len(任务列表)} 个任务")
        
        结果汇总 = {}
        
        with ThreadPoolExecutor(max_workers=self.网络配置["并发线程数"]) as 执行器:
            # 提交所有任务
            未来任务 = {}
            for 任务 in 任务列表:
                未来 = 执行器.submit(self.爬取指定内容, 任务["搜索词"], 任务.get("内容类型", "自动"))
                未来任务[未来] = 任务
            
            # 收集结果
            for 未来 in as_completed(未来任务):
                任务 = 未来任务[未来]
                try:
                    结果 = 未来.result()
                    结果汇总[任务["搜索词"]] = 结果
                    self.日志器.info(f"完成爬取: {任务['搜索词']} - 找到 {len(结果)} 个结果")
                except Exception as e:
                    self.日志器.error(f"爬取失败 {任务['搜索词']}: {e}")
                    结果汇总[任务["搜索词"]] = []
        
        return 结果汇总
    
    def 获取统计信息(self) -> Dict[str, Any]:
        """获取爬虫统计信息"""
        运行时间 = time.time() - self.统计信息["开始时间"]
        return {
            **self.统计信息,
            "运行时间_秒": round(运行时间, 2),
            "成功率": self.统计信息["成功次数"] / max(self.统计信息["总爬取次数"], 1),
            "预设角色数": sum(len(角色库) for 角色库 in self.预设角色库.values()),
            "预设世界观数": len(self.预设世界观库)
        }
    
    def 保存学习数据(self, 数据: Dict[str, Any], 文件名: str = None):
        """保存学习到的数据"""
        if not 文件名:
            时间戳 = time.strftime("%Y%m%d_%H%M%S")
            文件名 = f"学习数据_{时间戳}.json"
        
        数据目录 = Path("学习数据")
        数据目录.mkdir(exist_ok=True)
        
        文件路径 = 数据目录 / 文件名
        with open(文件路径, 'w', encoding='utf-8') as f:
            json.dump(数据, f, ensure_ascii=False, indent=2)
        
        self.日志器.info(f"学习数据已保存: {文件路径}")
        return 文件路径
    
    def 加载学习数据(self, 文件名: str) -> Dict[str, Any]:
        """加载之前的学习数据"""
        文件路径 = Path("学习数据") / 文件名
        if 文件路径.exists():
            with open(文件路径, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

class 网络学习引擎:
    def __init__(self):
        self.爬虫系统 = 智能爬虫系统()
        self.配置管理器 = 获取配置管理器()
        self.日志器 = logging.getLogger('网络学习引擎')
        self.学习任务队列 = []
        self.学习结果库 = {}
        
    def 小白模式爬取(self, 用户输入: str) -> Dict[str, Any]:
        """小白模式下的智能爬取"""
        self.日志器.info(f"小白模式爬取: {用户输入}")
        
        # 解析用户输入
        解析结果 = self.解析用户输入(用户输入)
        
        if not 解析结果:
            return {"错误": "无法理解您的输入，请尝试更具体的关键词"}
        
        # 执行爬取
        爬取结果 = self.爬虫系统.爬取指定内容(
            解析结果["搜索词"], 
            解析结果["内容类型"]
        )
        
        # 处理结果
        处理后的结果 = self.处理爬取结果(爬取结果, 解析结果)
        
        # 保存到学习库
        self.学习结果库[用户输入] = 处理后的结果
        
        return 处理后的结果
    
    def 解析用户输入(self, 用户输入: str) -> Optional[Dict[str, str]]:
        """解析用户输入，识别意图"""
        # 关键词映射
        角色关键词 = ["角色", "人物", "角色设定", "人物介绍", "是谁"]
        世界观关键词 = ["世界观", "世界设定", "背景设定", "世界背景"]
        小说关键词 = ["小说", "文章", "故事", "文本"]
        
        内容类型 = "自动"
        搜索词 = 用户输入
        
        # 检测内容类型
        for 关键词 in 角色关键词:
            if 关键词 in 用户输入:
                内容类型 = "角色"
                搜索词 = 用户输入.replace(关键词, "").strip()
                break
        
        for 关键词 in 世界观关键词:
            if 关键词 in 用户输入:
                内容类型 = "世界观" 
                搜索词 = 用户输入.replace(关键词, "").strip()
                break
        
        for 关键词 in 小说关键词:
            if 关键词 in 用户输入:
                内容类型 = "小说"
                搜索词 = 用户输入.replace(关键词, "").strip()
                break
        
        if not 搜索词:
            return None
        
        return {
            "搜索词": 搜索词,
            "内容类型": 内容类型,
            "原始输入": 用户输入
        }
    
    def 处理爬取结果(self, 爬取结果: List[Dict], 解析结果: Dict) -> Dict[str, Any]:
        """处理爬取结果，生成用户友好的输出"""
        if not 爬取结果:
            return {
                "状态": "未找到相关结果",
                "建议": "请尝试使用更具体的关键词，或检查网络连接"
            }
        
        # 按匹配度排序
        排序结果 = sorted(爬取结果, key=lambda x: x.get("匹配度", 0), reverse=True)
        
        # 构建响应
        响应 = {
            "状态": "成功",
            "找到结果数": len(排序结果),
            "搜索词": 解析结果["搜索词"],
            "内容类型": 解析结果["内容类型"],
            "最佳结果": [],
            "所有结果": 排序结果
        }
        
        # 提取最佳结果（匹配度>0.7）
        最佳结果 = [结果 for 结果 in 排序结果 if 结果.get("匹配度", 0) > 0.7]
        if 最佳结果:
            响应["最佳结果"] = 最佳结果[:3]  # 取前3个
        
        return 响应
    
    def 添加学习任务(self, 搜索词: str, 内容类型: str = "自动", 优先级: int = 1):
        """添加学习任务到队列"""
        任务 = {
            "搜索词": 搜索词,
            "内容类型": 内容类型, 
            "优先级": 优先级,
            "添加时间": time.time(),
            "状态": "等待中"
        }
        self.学习任务队列.append(任务)
        self.学习任务队列.sort(key=lambda x: x["优先级"], reverse=True)
    
    def 处理学习任务队列(self):
        """处理学习任务队列"""
        while self.学习任务队列:
            任务 = self.学习任务队列.pop(0)
            任务["状态"] = "处理中"
            
            try:
                结果 = self.爬虫系统.爬取指定内容(任务["搜索词"], 任务["内容类型"])
                任务["状态"] = "完成"
                任务["结果"] = 结果
                任务["完成时间"] = time.time()
                
                # 保存结果
                self.学习结果库[f"{任务['搜索词']}_{任务['内容类型']}"] = 结果
                
                self.日志器.info(f"学习任务完成: {任务['搜索词']} - 找到 {len(结果)} 个结果")
                
            except Exception as e:
                任务["状态"] = "失败"
                任务["错误"] = str(e)
                self.日志器.error(f"学习任务失败 {任务['搜索词']}: {e}")
    
    def 获取学习统计(self) -> Dict[str, Any]:
        """获取学习统计信息"""
        爬虫统计 = self.爬虫系统.获取统计信息()
        return {
            "爬虫统计": 爬虫统计,
            "学习任务数": len(self.学习任务队列),
            "学习结果数": len(self.学习结果库),
            "最近学习": list(self.学习结果库.keys())[-5:] if self.学习结果库 else []
        }

# 网络学习引擎单例
网络学习引擎实例 = None

def 获取网络学习引擎():
    """获取网络学习引擎单例"""
    global 网络学习引擎实例
    if 网络学习引擎实例 is None:
        网络学习引擎实例 = 网络学习引擎()
    return 网络学习引擎实例

if __name__ == "__main__":
    # 测试网络学习引擎
    学习引擎 = 网络学习引擎()
    
    # 测试小白模式
    结果 = 学习引擎.小白模式爬取("崩坏星铁的黑塔这个角色")
    print("爬取结果:", json.dumps(结果, ensure_ascii=False, indent=2))
    
    # 显示统计信息
    统计 = 学习引擎.获取学习统计()
    print("学习统计:", json.dumps(统计, ensure_ascii=False, indent=2))