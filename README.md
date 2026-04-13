# 汐语翻译工具 (XiYuTranslator)

强大的文本翻译工具，支持基于 LLM 的智能翻译和简繁体转换。

## ✨ 特性

- 🤖 **LLM 智能翻译**: 基于大语言模型的高质量翻译
- 🔄 **主备模型自动切换**: 支持配置主备模型，自动故障转移
- 📦 **批量翻译**: 高效的批量文本处理，自动分片优化
- 🌐 **多风格支持**: 推特、新闻、学术、标题等多种翻译风格
- 🈶 **简繁转换**: 支持简体中文与繁体中文互转
- 🔍 **语言检测**: 自动识别简体中文、繁体中文及多种语言
- 🔒 **隐私保护**: 本地部署，完全控制数据

## 📦 安装

### 从 Git 仓库安装

```bash
git clone https://github.com/SummerChris/xiyu-translator.git
cd XiYuTranslator
pip install .
```

### 依赖项

安装时会自动安装以下依赖：
- `openai>=1.0.0` - OpenAI API 客户端
- `opencc>=1.1.0` - 中文简繁转换
- `lingua-language-detector>=2.0.0` - 多语言检测
- `python-dotenv>=1.0.0` - 环境变量管理

## ⚙️ 配置

在使用前，需要配置 LLM API 参数。有两种方式：

### 方式 1: 使用 `.env` 文件（推荐）

在项目根目录创建 `.env` 文件：

```env
# 主模型配置
LLM_API_KEY=your_api_key_here
LLM_API_URL=http://your-api-endpoint.com/v1
LLM_MT_MODEL=your_translation_model

# 备用模型配置（可选）
LLM_API_KEY_BACKUP=your_backup_api_key
LLM_API_URL_BACKUP=https://backup-api-endpoint.com/v1
LLM_MT_MODEL_BACKUP=backup_model_name
```

**配置说明：**
- 主模型和备用模型可以独立配置
- 当主模型失败时，系统会自动切换到备用模型
- 备用模型配置为可选项，如不配置则仅使用主模型

### 方式 2: 设置环境变量

```bash
# Linux/macOS
export LLM_API_KEY=your_api_key_here
export LLM_API_URL=http://your-api-endpoint.com/v1
export LLM_MT_MODEL=your_translation_model

# Windows PowerShell
$env:LLM_API_KEY="your_api_key_here"
$env:LLM_API_URL="http://your-api-endpoint.com/v1"
$env:LLM_MT_MODEL="your_translation_model"
```

## 🚀 快速开始

### 基本使用

#### 1. 单条文本翻译

```python
from xiyu_translator import llm_translate

# 推特风格翻译
text = "Breaking news: New technology breakthrough!"
result = llm_translate('twitter', text, target_lang='ZH')
print(result)

# 新闻风格翻译
result = llm_translate('news', 'The summit concluded today.', target_lang='ZH')
print(result)

# 学术风格翻译
result = llm_translate('academic', 'The hypothesis was validated.', target_lang='ZH')
print(result)
```

#### 2. 批量翻译

```python
from xiyu_translator import llm_translate_batch

texts = [
    "Good morning!",
    "How are you?",
    "Have a nice day!"
]

results = llm_translate_batch(texts, context='general', target_lang='ZH')
for orig, trans in zip(texts, results):
    print(f"{orig} -> {trans}")
```

#### 3. 社交媒体文本（保留@用户名和#标签）

```python
from xiyu_translator import llm_translate_batch

tweets = [
    "@elonmusk Great news! #SpaceX",
    "Check out @NASA's mission. #Mars"
]

results = llm_translate_batch(tweets, context='twitter', target_lang='ZH')
```

#### 4. 简繁体转换

```python
from xiyu_translator import translate_to_simple_chinese

# 繁体转简体
traditional = "這是一個測試"
simplified = translate_to_simple_chinese(traditional, 't2s')
print(simplified)  # 这是一个测试

# 简体转繁体
simplified = "这是一个测试"
traditional = translate_to_simple_chinese(simplified, 's2t')
print(traditional)  # 這是一個測試
```

#### 5. 语言检测

```python
from xiyu_translator import language_classify

texts = [
    "这是简体中文",      # zh-Hans
    "這是繁體中文",      # zh-Hant
    "This is English"   # ''
]

for text in texts:
    lang = language_classify(text)
    print(f"{text}: {lang}")
```

## 📖 API 文档

### `llm_translate(expert, text, context='', source_lang='auto', target_lang='ZH', max_tokens=30000)`

单条文本翻译函数，支持主备模型自动切换。

**参数：**
- `expert` (str): AI 专家类型
  - `'twitter'`: 社交媒体风格
  - `'news'`: 新闻风格
  - `'academic'`: 学术风格
  - `'title'`: 标题风格
  - `''`: 通用翻译
- `text` (str): 需要翻译的文本
- `context` (str): 上下文信息（当 expert 为空时使用）
- `source_lang` (str): 源语言（默认自动检测）
- `target_lang` (str): 目标语言
  - `'ZH'`: 简体中文
  - `'EN'`: 英文
- `max_tokens` (int): 最大 token 数（默认 30000）

**返回：**
- str: 翻译后的文本

**特性：**
- 自动重试机制（最多 3 次）
- 主备模型无缝切换
- 指数退避重试策略

---

### `llm_translate_batch(text_list, context='', source_lang='auto', target_lang='ZH')`

批量翻译函数。

**参数：**
- `text_list` (list): 待翻译的文本列表
- `context` (str): 翻译上下文
- `source_lang` (str): 源语言
- `target_lang` (str): 目标语言（'ZH' 或 'EN'）

**返回：**
- list: 翻译后的文本列表

**特性：**
- 自动过滤 None 值和空字符串
- 智能分批处理大文本量
- 错误降级处理（批量失败时转为单条翻译）

---

### `opencc_translate(text, param='t2s')`

简繁体转换函数。

**参数：**
- `text` (str): 需要转换的文本
- `param` (str): 转换模式
  - `'t2s'`: 繁体转简体
  - `'s2t'`: 简体转繁体

**返回：**
- str: 转换后的文本

---

### `language_classify(text)`

语言检测函数。

**参数：**
- `text` (str): 待检测的文本

**返回：**
- str: 检测结果
  - `'zh-Hans'`: 简体中文
  - `'zh-Hant'`: 繁体中文
  - `''`: 非中文或其他语言

## 📝 示例代码

更多示例请查看 `examples/usage_examples.py` 文件。

运行示例：

```bash
python examples/usage_examples.py
```

## 🧪 测试

运行测试套件：

```bash
# 运行功能测试
python tests/test_translator.py

# 运行导入测试
python tests/test_import.py
```

## 📁 项目结构

```
XiYuTranslator/
├── xiyu_translator/       # 包源代码
│   ├── __init__.py        # 包入口和公共 API
│   └── core.py            # 核心翻译功能（含简繁转换、语言检测）
├── examples/              # 示例代码
│   └── usage_examples.py
├── tests/                 # 测试文件
│   ├── test_translator.py
│   └── test_import.py
├── pyproject.toml         # 项目配置文件
├── setup.py               # 安装脚本
├── README.md              # 项目说明文档
├── .env                   # 环境变量配置（需自行创建）
└── .env.example           # 环境变量示例
```

## 🛠️ 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 代码格式化

```bash
black xiyu_translator/
flake8 xiyu_translator/
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📬 联系方式

- Email: xiyu@example.com
- GitHub: https://github.com/yourusername/xiyu-translator

---

**注意**: 本工具需要配置有效的 LLM API 才能正常使用翻译功能。