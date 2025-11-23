# 模块2: 配置管理系统
import json
import os
import threading
import time
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, Any, List, Optional
import copy

class 配置管理系统:
    def __init__(self):
        self.配置锁 = threading.RLock()
        self.配置路径 = "系统配置.json"
        self.默认配置 = self.生成默认配置()
        self.当前配置 = {}
        self.配置历史 = []
        self.环境配置 = {}
        self.日志器 = self.初始化日志()
        
        # 加载配置
        self.加载配置()
        
    def 初始化日志(self):
        """初始化日志系统"""
        日志格式 = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        日志器 = logging.getLogger('配置管理')
        日志器.setLevel(logging.INFO)
        
        # 文件处理器
        文件处理器 = logging.FileHandler('系统日志.log', encoding='utf-8')
        文件处理器.setFormatter(日志格式)
        日志器.addHandler(文件处理器)
        
        # 控制台处理器
        控制台处理器 = logging.StreamHandler()
        控制台处理器.setFormatter(日志格式)
        日志器.addHandler(控制台处理器)
        
        return 日志器
    
    def 生成默认配置(self) -> Dict[str, Any]:
        """生成完整的默认配置"""
        return {
            "系统设置": {
                "版本号": "2.0.0",
                "自动更新": True,
                "自动备份": True,
                "日志级别": "INFO",
                "最大备份数": 10,
                "语言": "zh-CN"
            },
            "网络设置": {
                "真实爬取": True,
                "遵守爬虫规范": True,
                "爬取延迟": 2.0,
                "超时时间": 30,
                "重试次数": 3,
                "并发线程数": 5,
                "用户代理": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "代理设置": None,
                "白名单网站": [
                    "https://www.biquge.com.cn",
                    "https://www.xbiquge.la",
                    "https://www.x23us.com",
                    "https://www.qidian.com",
                    "https://www.zongheng.com"
                ],
                "黑名单网站": [],
                "自动学习间隔": "24.0.0"  # 24小时
            },
            "安全设置": {
                "审核模式": "开启",  # 开启/关闭/自定义
                "自定义关键词": [],
                "风险等级阈值": 0.7,
                "内容扫描深度": "全面",
                "实时风险监控": True,
                "敏感词库": self.生成默认敏感词库(),
                "自动屏蔽": True,
                "审核日志": True
            },
            "生成设置": {
                "默认每章字数": 3000,
                "字数浮动": 0.2,
                "整本字数范围": [50000, 5000000],
                "自动分卷": True,
                "每卷章节数": 50,
                "默认风格": "热血战斗风",
                "质量阈值": 0.8,
                "最大生成次数": 3,
                "自动保存间隔": 5
            },
            "风格设置": {
                "风格库路径": "风格库/",
                "自动学习风格": True,
                "风格融合度": 0.5,
                "自定义风格": {},
                "热门风格权重": True,
                "风格预览字数": 500
            },
            "工作流设置": {
                "自动项目管理": True,
                "版本历史数量": 50,
                "自动灵感捕捉": True,
                "实时数据统计": True,
                "协作模式": False,
                "自动导出格式": ["txt", "json"],
                "备份路径": "备份/",
                "云同步": False
            },
            "内容提炼设置": {
                "自动角色提炼": True,
                "自动世界观提炼": True,
                "跨平台识别": True,
                "文学化重构": True,
                "结构化输出": True,
                "术语规范化": True,
                "批量处理数量": 10
            },
            "界面设置": {
                "主题": "深色",
                "字体大小": 14,
                "自动保存布局": True,
                "实时预览": True,
                "动画效果": True,
                "语音提示": False,
                "简化模式": False
            },
            "高级设置": {
                "调试模式": False,
                "性能监控": True,
                "内存优化": True,
                "缓存大小_MB": 500,
                "API限流": True,
                "插件路径": "插件/",
                "自定义脚本": [],
                "实验性功能": False
            }
        }
    
    def 生成默认敏感词库(self) -> List[str]:
        """生成默认敏感词库"""
        return [
            # 政治敏感
            "国家领导人", "政府", "政党", "政治", "民主", "自由", "人权",
            # 暴力
            "杀人", "暴力", "血腥", "恐怖", "爆炸", "枪支",
            # 色情
            "色情", "淫秽", "性爱", "裸体", "强奸",
            # 违法
            "毒品", "赌博", "诈骗", "黑客",
            # 歧视
            "种族歧视", "性别歧视", "地域歧视",
            # 其他
            "自杀", "自残", "虐待"
        ]
    
    def 加载配置(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.配置路径):
                with open(self.配置路径, 'r', encoding='utf-8') as f:
                    文件配置 = json.load(f)
                
                # 深度合并配置
                self.当前配置 = self.深度合并配置(copy.deepcopy(self.默认配置), 文件配置)
                self.日志器.info("配置加载成功")
            else:
                self.当前配置 = copy.deepcopy(self.默认配置)
                self.保存配置()
                self.日志器.info("创建默认配置")
                
        except Exception as e:
            self.日志器.error(f"配置加载失败: {e}")
            self.当前配置 = copy.deepcopy(self.默认配置)
    
    def 深度合并配置(self, 目标配置: Dict, 源配置: Dict) -> Dict:
        """深度合并两个配置字典"""
        for 键, 值 in 源配置.items():
            if 键 in 目标配置 and isinstance(目标配置[键], dict) and isinstance(值, dict):
                self.深度合并配置(目标配置[键], 值)
            else:
                目标配置[键] = 值
        return 目标配置
    
    def 保存配置(self):
        """保存配置到文件"""
        with self.配置锁:
            try:
                # 创建配置历史
                历史记录 = {
                    "时间": datetime.now().isoformat(),
                    "配置": copy.deepcopy(self.当前配置)
                }
                self.配置历史.append(历史记录)
                
                # 限制历史记录数量
                if len(self.配置历史) > self.当前配置["系统设置"]["最大备份数"]:
                    self.配置历史.pop(0)
                
                # 保存到文件
                with open(self.配置路径, 'w', encoding='utf-8') as f:
                    json.dump(self.当前配置, f, ensure_ascii=False, indent=2)
                
                # 备份配置
                if self.当前配置["系统设置"]["自动备份"]:
                    self.备份配置()
                
                self.日志器.info("配置保存成功")
                return True
                
            except Exception as e:
                self.日志器.error(f"配置保存失败: {e}")
                return False
    
    def 备份配置(self):
        """备份配置文件"""
        try:
            备份目录 = Path("配置备份")
            备份目录.mkdir(exist_ok=True)
            
            时间戳 = datetime.now().strftime("%Y%m%d_%H%M%S")
            备份路径 = 备份目录 / f"配置备份_{时间戳}.json"
            
            with open(备份路径, 'w', encoding='utf-8') as f:
                json.dump(self.当前配置, f, ensure_ascii=False, indent=2)
                
            self.日志器.info(f"配置备份成功: {备份路径}")
            
        except Exception as e:
            self.日志器.error(f"配置备份失败: {e}")
    
    def 获取配置(self, 配置路径: str = None, 默认值=None):
        """获取配置值"""
        with self.配置锁:
            try:
                if not 配置路径:
                    return self.当前配置
                
                配置项 = self.当前配置
                for 部分 in 配置路径.split('.'):
                    配置项 = 配置项.get(部分, {})
                
                return 配置项 if 配置项 != {} else 默认值
                
            except (KeyError, AttributeError):
                return 默认值
    
    def 设置配置(self, 配置路径: str, 值: Any, 立即保存: bool = True):
        """设置配置值"""
        with self.配置锁:
            try:
                配置项 = self.当前配置
                路径部分 = 配置路径.split('.')
                
                # 导航到父级
                for 部分 in 路径部分[:-1]:
                    if 部分 not in 配置项:
                        配置项[部分] = {}
                    配置项 = 配置项[部分]
                
                # 设置值
                配置项[路径部分[-1]] = 值
                
                if 立即保存:
                    self.保存配置()
                
                self.日志器.info(f"配置已更新: {配置路径} = {值}")
                return True
                
            except Exception as e:
                self.日志器.error(f"配置设置失败: {配置路径} - {e}")
                return False
    
    def 重置配置(self, 配置节: str = None):
        """重置配置到默认值"""
        with self.配置锁:
            try:
                if 配置节:
                    # 重置特定节
                    if 配置节 in self.默认配置:
                        self.当前配置[配置节] = copy.deepcopy(self.默认配置[配置节])
                else:
                    # 重置全部配置
                    self.当前配置 = copy.deepcopy(self.默认配置)
                
                self.保存配置()
                self.日志器.info(f"配置已重置: {配置节 or '全部'}")
                return True
                
            except Exception as e:
                self.日志器.error(f"配置重置失败: {e}")
                return False
    
    def 导入配置(self, 文件路径: str):
        """从文件导入配置"""
        try:
            with open(文件路径, 'r', encoding='utf-8') as f:
                导入配置 = json.load(f)
            
            # 验证配置结构
            if not self.验证配置(导入配置):
                raise ValueError("配置文件格式无效")
            
            self.当前配置 = self.深度合并配置(copy.deepcopy(self.默认配置), 导入配置)
            self.保存配置()
            
            self.日志器.info(f"配置导入成功: {文件路径}")
            return True
            
        except Exception as e:
            self.日志器.error(f"配置导入失败: {e}")
            return False
    
    def 导出配置(self, 文件路径: str):
        """导出配置到文件"""
        try:
            with open(文件路径, 'w', encoding='utf-8') as f:
                json.dump(self.当前配置, f, ensure_ascii=False, indent=2)
            
            self.日志器.info(f"配置导出成功: {文件路径}")
            return True
            
        except Exception as e:
            self.日志器.error(f"配置导出失败: {e}")
            return False
    
    def 验证配置(self, 配置: Dict) -> bool:
        """验证配置有效性"""
        try:
            # 检查必需字段
            必需字段 = ["系统设置", "网络设置", "安全设置", "生成设置"]
            for 字段 in 必需字段:
                if 字段 not in 配置:
                    return False
            
            # 验证网络设置
            网络设置 = 配置["网络设置"]
            if not isinstance(网络设置.get("真实爬取", True), bool):
                return False
            
            if not isinstance(网络设置.get("爬取延迟", 2.0), (int, float)):
                return False
            
            # 验证安全设置
            安全设置 = 配置["安全设置"]
            if 安全设置.get("审核模式") not in ["开启", "关闭", "自定义"]:
                return False
            
            return True
            
        except Exception:
            return False
    
    def 获取配置摘要(self) -> Dict[str, Any]:
        """获取配置摘要信息"""
        return {
            "版本": self.获取配置("系统设置.版本号"),
            "网络模式": "真实爬取" if self.获取配置("网络设置.真实爬取") else "模拟爬取",
            "安全模式": self.获取配置("安全设置.审核模式"),
            "默认风格": self.获取配置("生成设置.默认风格"),
            "总配置项数": self.计算配置项数(self.当前配置),
            "最后保存": datetime.now().isoformat()
        }
    
    def 计算配置项数(self, 配置: Dict) -> int:
        """计算配置项总数"""
        数量 = 0
        for 值 in 配置.values():
            if isinstance(值, dict):
                数量 += self.计算配置项数(值)
            else:
                数量 += 1
        return 数量
    
    def 环境检测配置(self) -> Dict[str, Any]:
        """根据环境检测结果调整配置"""
        # 检测网络状况
        try:
            import requests
            响应 = requests.get("https://www.baidu.com", timeout=5)
            网络良好 = 响应.status_code == 200
        except:
            网络良好 = False
        
        # 检测系统资源
        import psutil
        内存使用率 = psutil.virtual_memory().percent
        磁盘空间 = psutil.disk_usage('.').free / (1024**3)  # GB
        
        # 根据环境调整配置
        self.环境配置 = {
            "网络状况": "良好" if 网络良好 else "受限",
            "内存使用率": 内存使用率,
            "磁盘空间_GB": round(磁盘空间, 1),
            "推荐并发数": min(5, max(1, int((100 - 内存使用率) / 20))),
            "推荐缓存大小": min(200, max(50, int(磁盘空间 * 0.1)))  # MB
        }
        
        # 自动优化配置
        if not 网络良好:
            self.设置配置("网络设置.真实爬取", False, False)
            self.设置配置("网络设置.并发线程数", 1, False)
        
        if 内存使用率 > 80:
            self.设置配置("高级设置.缓存大小_MB", 100, False)
            self.设置配置("网络设置.并发线程数", 2, False)
        
        self.日志器.info(f"环境检测配置完成: {self.环境配置}")
        return self.环境配置
    
    def 获取网络配置(self) -> Dict[str, Any]:
        """获取网络相关配置"""
        return {
            "真实爬取": self.获取配置("网络设置.真实爬取"),
            "遵守规范": self.获取配置("网络设置.遵守爬虫规范"),
            "爬取延迟": self.获取配置("网络设置.爬取延迟"),
            "超时时间": self.获取配置("网络设置.超时时间"),
            "并发线程数": self.获取配置("网络设置.并发线程数"),
            "用户代理": self.获取配置("网络设置.用户代理"),
            "代理设置": self.获取配置("网络设置.代理设置"),
            "白名单": self.获取配置("网络设置.白名单网站"),
            "黑名单": self.获取配置("网络设置.黑名单网站")
        }
    
    def 获取安全配置(self) -> Dict[str, Any]:
        """获取安全相关配置"""
        return {
            "审核模式": self.获取配置("安全设置.审核模式"),
            "自定义关键词": self.获取配置("安全设置.自定义关键词"),
            "风险阈值": self.获取配置("安全设置.风险等级阈值"),
            "扫描深度": self.获取配置("安全设置.内容扫描深度"),
            "实时监控": self.获取配置("安全设置.实时风险监控"),
            "敏感词库": self.获取配置("安全设置.敏感词库"),
            "自动屏蔽": self.获取配置("安全设置.自动屏蔽"),
            "审核日志": self.获取配置("安全设置.审核日志")
        }
    
    def 添加自定义关键词(self, 关键词: str):
        """添加自定义安全关键词"""
        当前关键词 = self.获取配置("安全设置.自定义关键词", [])
        if 关键词 not in 当前关键词:
            当前关键词.append(关键词)
            self.设置配置("安全设置.自定义关键词", 当前关键词)
            self.日志器.info(f"添加自定义关键词: {关键词}")
    
    def 移除自定义关键词(self, 关键词: str):
        """移除自定义安全关键词"""
        当前关键词 = self.获取配置("安全设置.自定义关键词", [])
        if 关键词 in 当前关键词:
            当前关键词.remove(关键词)
            self.设置配置("安全设置.自定义关键词", 当前关键词)
            self.日志器.info(f"移除自定义关键词: {关键词}")
    
    def 设置审核模式(self, 模式: str, 自定义关键词: List[str] = None):
        """设置审核模式"""
        有效模式 = ["开启", "关闭", "自定义"]
        if 模式 not in 有效模式:
            raise ValueError(f"审核模式必须是: {有效模式}")
        
        self.设置配置("安全设置.审核模式", 模式)
        
        if 模式 == "自定义" and 自定义关键词:
            self.设置配置("安全设置.自定义关键词", 自定义关键词)
        
        self.日志器.info(f"审核模式设置为: {模式}")
    
    def 设置网络模式(self, 真实爬取: bool, 遵守规范: bool = True):
        """设置网络爬取模式"""
        self.设置配置("网络设置.真实爬取", 真实爬取)
        self.设置配置("网络设置.遵守爬虫规范", 遵守规范)
        
        模式描述 = "真实爬取" if 真实爬取 else "模拟爬取"
        规范描述 = "遵守规范" if 遵守规范 else "自由爬取"
        self.日志器.info(f"网络模式: {模式描述}, {规范描述}")
    
    def 启动(self):
        """启动配置管理系统"""
        self.日志器.info("配置管理系统启动")
        
        # 环境检测配置
        self.环境检测配置()
        
        # 确保必要目录存在
        必要目录 = [
            "风格库",
            "备份", 
            "配置备份",
            "插件",
            "日志"
        ]
        
        for 目录 in 必要目录:
            Path(目录).mkdir(exist_ok=True)
        
        # 显示配置摘要
        摘要 = self.获取配置摘要()
        self.日志器.info(f"配置摘要: {摘要}")
        
        return True

# 配置管理器单例
配置管理器 = None

def 获取配置管理器():
    """获取配置管理器单例"""
    global 配置管理器
    if 配置管理器 is None:
        配置管理器 = 配置管理系统()
        配置管理器.启动()
    return 配置管理器

if __name__ == "__main__":
    # 测试配置管理系统
    配置系统 = 配置管理系统()
    配置系统.启动()
    
    # 测试配置操作
    配置系统.设置审核模式("自定义", ["测试关键词"])
    配置系统.设置网络模式(真实爬取=True, 遵守规范=True)
    
    print("配置测试完成")
    print("配置摘要:", 配置系统.获取配置摘要())
    print("环境配置:", 配置系统.环境配置)