import os
from openai import OpenAI
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    """AI论文解读服务 - 支持多种AI服务提供商"""
    
    def __init__(self, api_key: str = None, provider: str = None, base_url: str = None, model: str = None):
        """
        初始化AI服务
        
        Args:
            api_key: API密钥，如果不提供则从环境变量读取
            provider: AI服务提供商 (openai/qwen/deepseek/moonshot/custom)
            base_url: 自定义API端点
            model: 模型名称
        """
        # 读取配置
        self.provider = provider or os.getenv("AI_PROVIDER", "openai").lower()
        self.api_key = api_key or os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("AI_BASE_URL")
        self.model = model or os.getenv("AI_MODEL")
        
        # 根据provider设置默认值
        if not self.model:
            self.model = self._get_default_model()
        
        if not self.base_url:
            self.base_url = self._get_default_base_url()
        
        # 初始化客户端
        if not self.api_key:
            logger.warning(f"AI_API_KEY not found. AI service will not work.")
            self.client = None
        else:
            try:
                if self.base_url:
                    self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
                    logger.info(f"✓ AI服务已初始化: {self.provider} ({self.model}) at {self.base_url}")
                else:
                    self.client = OpenAI(api_key=self.api_key)
                    logger.info(f"✓ AI服务已初始化: {self.provider} ({self.model})")
            except Exception as e:
                logger.error(f"Failed to initialize AI client: {e}")
                self.client = None
    
    def _get_default_model(self) -> str:
        """根据provider获取默认模型"""
        models = {
            "openai": "gpt-4o-mini",
            "qwen": "qwen-plus",  # 通义千问
            "deepseek": "deepseek-chat",
            "moonshot": "moonshot-v1-8k",
            "glm": "glm-4",  # 智谱AI
            "custom": "gpt-3.5-turbo"
        }
        return models.get(self.provider, "gpt-4o-mini")
    
    def _get_default_base_url(self) -> str:
        """根据provider获取默认API端点"""
        base_urls = {
            "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "deepseek": "https://api.deepseek.com/v1",
            "moonshot": "https://api.moonshot.cn/v1",
            "glm": "https://open.bigmodel.cn/api/paas/v4",
        }
        return base_urls.get(self.provider)
    
    def categorize_paper(self, title: str, abstract: str) -> str:
        """
        对论文进行分类
        
        Args:
            title: 论文标题
            abstract: 论文摘要
            
        Returns:
            分类名称
        """
        if not self.client:
            return "未分类"
        
        try:
            prompt = f"""请根据以下AB测试论文的标题和摘要，将其归类到以下类别之一：
- 统计方法
- 实验平台
- 因果推断
- 多臂老虎机
- 顺序测试
- 实验设计
- 效应估计
- 其他

只返回类别名称，不要其他内容。

标题：{title}

摘要：{abstract[:500]}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的AB测试和实验设计领域的专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            category = response.choices[0].message.content.strip()
            logger.info(f"Paper categorized as: {category}")
            return category
            
        except Exception as e:
            logger.error(f"Error categorizing paper: {e}")
            return "其他"
    
    def translate_title(self, title: str) -> str:
        """
        翻译论文标题为中文
        
        Args:
            title: 英文标题
            
        Returns:
            中文标题
        """
        if not self.client:
            return title
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术翻译专家。"},
                    {"role": "user", "content": f"请将以下论文标题翻译成中文，保持专业性和准确性：\n\n{title}"}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            title_cn = response.choices[0].message.content.strip()
            logger.info(f"Title translated: {title[:50]}... -> {title_cn[:50]}...")
            return title_cn
            
        except Exception as e:
            logger.error(f"Error translating title: {e}")
            return title
    
    def generate_summary_and_interpretation(self, title: str, abstract: str, authors: str) -> Dict[str, str]:
        """
        生成中文摘要和解读（保留兼容）
        
        Args:
            title: 论文标题
            abstract: 论文摘要
            authors: 作者
            
        Returns:
            包含summary_cn和interpretation的字典
        """
        if not self.client:
            return {
                "summary_cn": "AI服务未配置，无法生成摘要",
                "interpretation": "AI服务未配置，无法生成解读"
            }
        
        try:
            prompt = f"""请对以下AB测试相关的学术论文进行深度解读：

标题：{title}

作者：{authors}

摘要：{abstract}

请提供：
1. 中文摘要（200-300字）：用通俗易懂的中文总结论文的主要内容
2. 详细解读（500-800字）：包括以下方面
   - 研究背景和动机
   - 主要创新点和贡献
   - 核心方法和技术
   - 实验结果和发现
   - 实际应用价值
   - 局限性和未来方向

请用JSON格式返回，格式如下：
{{
  "summary_cn": "中文摘要内容",
  "interpretation": "详细解读内容"
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的AB测试和实验设计领域的专家，擅长用中文解读英文学术论文。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            logger.info(f"Generated summary and interpretation")
            
            # 解析JSON
            import json
            parsed_result = json.loads(result)
            return {
                "summary_cn": parsed_result.get("summary_cn", ""),
                "interpretation": parsed_result.get("interpretation", "")
            }
            
        except Exception as e:
            logger.error(f"Error generating summary and interpretation: {e}")
            return {
                "summary_cn": f"生成摘要时出错：{str(e)}",
                "interpretation": f"生成解读时出错：{str(e)}"
            }
    
    def generate_structured_interpretation(self, title: str, abstract: str, authors: str) -> Dict:
        """
        生成结构化论文解读
        
        Returns:
            JSON格式的结构化解读，包含：conclusion, innovations, experimental_data, methods等
        """
        if not self.client:
            return None
        
        try:
            prompt = f"""请对以下AB测试相关论文进行结构化解读：

标题：{title}
作者：{authors}
摘要：{abstract}

请按以下结构进行分析（每部分150-200字）：

1. 论文主要结论：核心发现和结论
2. 主要创新点：相比现有方法的创新之处
3. 实验数据：使用的数据集、数据规模、实验场景
4. 实验方法：核心算法、技术路线、实现方式
5. 应用场景：适用的业务场景和实际应用价值
6. 局限性：存在的局限和待解决问题

请返回JSON格式：
{{
  "conclusion": "主要结论内容",
  "innovations": "创新点内容",
  "experimental_data": "实验数据内容",
  "methods": "实验方法内容",
  "applications": "应用场景内容",
  "limitations": "局限性内容"
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是AB测试和实验设计领域的专家，擅长结构化分析论文。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2500,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Generated structured interpretation")
            return result
            
        except Exception as e:
            logger.error(f"Error generating structured interpretation: {e}")
            return None
    
    def generate_mindmap(self, title: str, abstract: str) -> Dict:
        """
        生成思维导图数据
        
        Returns:
            思维导图的JSON数据（适用于前端渲染）
        """
        if not self.client:
            return None
        
        try:
            prompt = f"""请为以下论文生成思维导图结构：

标题：{title}
摘要：{abstract}

请生成一个树状结构的思维导图，包含：
- 中心主题（论文核心）
- 3-5个一级分支（主要方面）
- 每个一级分支下2-4个二级分支（具体内容）

返回JSON格式：
{{
  "name": "论文核心主题（简短）",
  "children": [
    {{
      "name": "一级分支1",
      "children": [
        {{"name": "二级内容1"}},
        {{"name": "二级内容2"}}
      ]
    }},
    ...
  ]
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术知识结构化专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Generated mindmap")
            return result
            
        except Exception as e:
            logger.error(f"Error generating mindmap: {e}")
            return None
    
    def evaluate_platform_value(self, title: str, abstract: str) -> Dict:
        """
        评估论文对实验平台建设的价值
        
        Returns:
            JSON格式：{"has_value": bool, "score": int, "value_points": [...], "reasoning": "..."}
        """
        if not self.client:
            return None
        
        try:
            prompt = f"""作为AB实验平台的技术专家，请评估以下论文对实验平台建设的价值：

标题：{title}
摘要：{abstract}

请从以下维度评估：
1. 是否可以直接应用到实验平台
2. 是否提供了新的统计方法或算法
3. 是否解决了实际工程问题
4. 是否有助于提升实验效率或准确性

请返回JSON格式：
{{
  "has_value": true/false,
  "score": 0-100分,
  "value_points": [
    "价值点1：具体说明",
    "价值点2：具体说明"
  ],
  "reasoning": "综合评价（100-150字）"
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是AB实验平台建设的资深专家，擅长评估学术研究的工程价值。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Generated platform value evaluation: score={result.get('score', 0)}")
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating platform value: {e}")
            return None
    
    def process_paper(self, paper_data: Dict) -> Dict:
        """
        处理论文：生成所有AI内容（v2.1优化版）
        从6次API调用优化到3次，提升50%速度
        
        Args:
            paper_data: 包含title, abstract, authors的字典
            
        Returns:
            包含所有AI生成内容的字典
        """
        title = paper_data.get('title', '')
        abstract = paper_data.get('abstract', '')
        authors = paper_data.get('authors', '')
        
        logger.info(f"Processing paper (v2.1 optimized): {title[:100]}...")
        
        import json
        
        # 第1次合并调用：标题翻译 + 摘要 + 基础解读
        first_result = self._combined_call_1(title, abstract, authors)
        
        # 第2次合并调用：结构化解读 + 思维导图 + 平台价值
        second_result = self._combined_call_2(title, abstract, authors)
        
        # 第3次调用：分类
        category = self.categorize_paper(title, abstract)
        
        logger.info(f"✓ Paper processed successfully (3 API calls)")
        
        return {
            "title_cn": first_result.get("title_cn"),
            "summary_cn": first_result.get("summary_cn"),
            "interpretation": first_result.get("interpretation"),
            "structured_interpretation": second_result.get("structured_interpretation"),
            "mindmap": second_result.get("mindmap"),
            "platform_value": second_result.get("platform_value"),
            "category": category
        }
    
    def _combined_call_1(self, title: str, abstract: str, authors: str) -> Dict:
        """
        第1次合并调用：标题翻译 + 摘要 + 基础解读
        将原来的3次调用合并为1次
        """
        if not self.client:
            return {
                "title_cn": title,
                "summary_cn": "AI服务未配置",
                "interpretation": "AI服务未配置"
            }
        
        try:
            prompt = f"""请对以下AB测试相关的学术论文进行分析：

标题：{title}
作者：{authors}
摘要：{abstract}

请提供以下内容，以JSON格式返回：

1. title_cn: 将英文标题翻译为中文（保持专业术语准确，简洁易懂）

2. summary_cn: 中文摘要（200-300字）
   - 用通俗易懂的中文总结论文的主要内容
   - 突出研究问题、方法和主要发现

3. interpretation: 详细解读（500-800字）
   包括以下方面：
   - 研究背景和动机
   - 主要创新点和贡献
   - 核心方法和技术
   - 实验结果和发现
   - 实际应用价值
   - 局限性和未来方向

请严格按照以下JSON格式返回：
{{
  "title_cn": "中文标题",
  "summary_cn": "中文摘要内容",
  "interpretation": "详细解读内容"
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是AB测试和实验领域的专家，擅长解读学术论文。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Combined call 1 completed: title={result.get('title_cn', '')[:30]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error in combined call 1: {e}")
            return {
                "title_cn": title,
                "summary_cn": f"处理出错: {str(e)}",
                "interpretation": f"处理出错: {str(e)}"
            }
    
    def _combined_call_2(self, title: str, abstract: str, authors: str) -> Dict:
        """
        第2次合并调用：结构化解读 + 思维导图 + 平台价值
        将原来的3次调用合并为1次
        """
        if not self.client:
            return {
                "structured_interpretation": None,
                "mindmap": None,
                "platform_value": None
            }
        
        try:
            prompt = f"""请对以下AB测试相关论文进行深度分析：

标题：{title}
摘要：{abstract}

请提供以下三部分内容，以JSON格式返回：

1. structured_interpretation: 结构化解读（6个维度）
{{
  "conclusion": "论文主要结论（100-150字）",
  "innovations": "主要创新点，相比现有方法的突破（100-150字）",
  "experimental_data": "实验数据描述（数据集名称、数据规模、实验场景，100字）",
  "methods": "实验方法（核心算法、技术路线、实现方式，100-150字）",
  "applications": "应用场景（适用的业务场景和实际应用价值，100字）",
  "limitations": "局限性（存在的局限和待解决问题，50-100字）"
}}

2. mindmap: 思维导图树状结构（3层）
{{
  "name": "论文核心主题（简短）",
  "children": [
    {{
      "name": "研究背景",
      "children": [
        {{"name": "背景要点1"}},
        {{"name": "背景要点2"}}
      ]
    }},
    {{
      "name": "核心方法",
      "children": [
        {{"name": "方法要点1"}},
        {{"name": "方法要点2"}}
      ]
    }},
    {{
      "name": "实验结果",
      "children": [
        {{"name": "结果要点1"}},
        {{"name": "结果要点2"}}
      ]
    }},
    {{
      "name": "应用价值",
      "children": [
        {{"name": "价值要点1"}},
        {{"name": "价值要点2"}}
      ]
    }}
  ]
}}

3. platform_value: 平台价值评估
判断这篇论文对AB测试实验平台建设是否有价值：
{{
  "has_value": true或false,
  "score": 0-100的整数评分,
  "value_points": ["价值点1", "价值点2", "价值点3"],
  "reasoning": "综合评价说明（100-200字）"
}}

评分标准：
- 80-100分：直接可应用于平台建设，有明确的技术方案
- 60-79分：提供了有价值的思路和方法参考
- 40-59分：有一定参考价值，但需要大量改造
- 0-39分：理论研究为主，实际应用价值有限

请返回完整JSON对象，包含以上三个字段。
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是AB测试和实验平台领域的专家，擅长评估论文的实际应用价值。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # 转换为字符串格式（数据库存储需要）
            structured_interpretation = result.get("structured_interpretation")
            mindmap = result.get("mindmap")
            platform_value = result.get("platform_value")
            
            logger.info(f"Combined call 2 completed: score={platform_value.get('score', 0) if platform_value else 0}")
            
            return {
                "structured_interpretation": json.dumps(structured_interpretation, ensure_ascii=False) if structured_interpretation else None,
                "mindmap": json.dumps(mindmap, ensure_ascii=False) if mindmap else None,
                "platform_value": json.dumps(platform_value, ensure_ascii=False) if platform_value else None
            }
            
        except Exception as e:
            logger.error(f"Error in combined call 2: {e}")
            return {
                "structured_interpretation": None,
                "mindmap": None,
                "platform_value": None
            }
