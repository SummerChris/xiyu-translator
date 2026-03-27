# -*- coding: utf-8 -*-
"""
汐语翻译工具 (XiYuTranslator)
强大的文本翻译工具，支持基于 LLM 的智能翻译和简繁体转换

主要功能:
- 单条文本翻译 (llm_translate)
- 批量文本翻译 (llm_translate_batch)
- 简繁体转换 (opencc_translate)
- 语言检测 (language_classify)

使用示例:
    from xiyu_translator import llm_translate, llm_translate_batch
    
    # 单条翻译
    result = llm_translate('twitter', 'Hello World!', target_lang='ZH')
    
    # 批量翻译
    texts = ['Hello', 'World', 'Good morning']
    results = llm_translate_batch(texts, context='general', target_lang='ZH')

配置说明:
    需要在环境变量中设置以下参数:
    - LLM_API_KEY: LLM API 密钥
    - LLM_API_URL: LLM API 地址
    - LLM_MODEL: 使用的模型名称
    或者在项目根目录创建 .env 文件配置这些参数
"""

from .core import llm_translate, llm_translate_batch, translate_to_simple_chinese, language_classify

# 公开 API

__version__ = '0.0.1'
__author__ = 'XiYu Translator Team'
__all__ = [
    'llm_translate',
    'llm_translate_batch',
    'translate_to_simple_chinese',
    'language_classify',
]
