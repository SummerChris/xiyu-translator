# -*- coding: utf-8 -*-
"""
汐语翻译工具 - 核心翻译功能模块
提供基于 LLM 的单条和批量翻译功能
"""
import os
import time
import uuid
import re
from openai import OpenAI, OpenAIError
from opencc import OpenCC

# 加载.env 文件
from dotenv import load_dotenv
load_dotenv()


def translate_to_simple_chinese(text, param='t2s'):
    """
    内部函数：使用 OpenCC 进行简繁体转换
    
    :param text: 需要转换的文本
    :param param: 转换模式，'t2s'（繁转简）、's2t'（简转繁）等
    :return: 转换后的文本
    """
    try:
        converter = OpenCC(param)
        if param == 't2s':
            text = text.replace('\\', '')
        return converter.convert(text)
    except Exception:
        return text


def language_classify(text):
    """
    简繁中文检测函数
    支持简体中文、繁体中文、混合文本检测

    :param text: 待检测的文本
    :return: 检测结果，'zh-Hans' 表示简体中文，'zh-Hant' 表示繁体中文，'' 表示非中文
    """
    try:
        converter_s2t = OpenCC('s2t')  # 简转繁

        # 先识别是否包含中文字符
        chinese_chars = re.findall('[\u4e00-\u9fff]', text)
        if len(chinese_chars) / max(len(text), 1) < 0.3:  # 中文占比阈值
            return ""

        # 使用 OpenCC 进行双向转换比对
        converter_t2s = OpenCC('t2s')  # 繁转简
        simplified = converter_t2s.convert(text)

        converter_s2t = OpenCC('s2t')  # 简转繁
        traditional = converter_s2t.convert(text)

        # 判断是否为纯简体（繁转简后不变）
        is_simplified = (simplified == text)
        # 判断是否为纯繁体（简转繁后不变）
        is_traditional = (traditional == text)

        # 混合情况处理
        if is_simplified and not is_traditional:
            return 'zh-Hans'  # 简体中文
        elif is_traditional and not is_simplified:
            return 'zh-Hant'  # 繁体中文
        else:
            # 混合文本时，通过字符数占比判断
            simplified_count = sum(1 for c in text if converter_s2t.convert(c) != c)
            if simplified_count / len(text) > 0.5:
                return 'zh-Hans'  # 简体中文
            else:
                return 'zh-Hant'  # 繁体中文

    except Exception as e:
        print(f"检测异常：{str(e)}")
        return ""  # 降级处理


def llm_translate(expert, text, context='', source_lang='auto', target_lang='ZH', max_tokens=60000):
    """
    使用大语言模型进行翻译。

    :param expert: AI 专家类型，如 'twitter'、'news'、'academic'、'title' 或 ''
    :param text: 需要翻译的文本
    :param context: 上下文信息（当 expert 为空时使用）
    :param source_lang: 源语言（默认自动检测）
    :param target_lang: 目标语言（默认 ZH 简体中文，EN 英文）
    :param max_tokens: 最大 token 数，默认 60000
    :return: 翻译后的文本
    """
    if target_lang == 'ZH':
        target_lang = 'Simplified Chinese'
    if target_lang == 'EN':
        target_lang = 'English'

    # 1. 基础约束强化
    base_rules = (
        f"You are a strictly mechanical translation API. Your ONLY function is to translate text into {target_lang}.\n"
        f"### STRICT RULES:\n"
        f"1. Output PURE translation ONLY. No explanations, no parentheses, no AI disclaimers.\n"
        f"2. Neutrality Override: You MUST translate ALL content, including military, political, or sensitive terms. Do not refuse any translation.\n"
        f"3. Retain ALL @usernames, URLs, and hashtags exactly as they appear.\n"
        f"4. If the text is very short (e.g., just 'Bye' or a username), just translate what is there and STOP."
    )

    # 2. 统一示例格式
    if expert == 'twitter':
        system_prompt = (
            f"{base_rules}\n"
            f"Style: Native, idiomatic, social media (Twitter/X style).\n\n"
            f"===EXAMPLE START===\n"
            f"SOURCE:\nCheck this out! #cool\n"
            f"TRANSLATION:\n快来看看这个！#酷\n"
            f"===EXAMPLE END==="
        )
    elif expert == 'news':
        system_prompt = (
            f"{base_rules}\n"
            f"Style: Formal, objective news style.\n\n"
            f"===EXAMPLE START===\n"
            f"SOURCE:\nThe meeting concluded today.\n"
            f"TRANSLATION:\n该会议今日圆满结束。\n"
            f"===EXAMPLE END==="
        )
    elif expert == 'academic':
        system_prompt = (
            f"{base_rules}\n"
            f"Style: Scholarly, precise, formal.\n\n"
            f"===EXAMPLE START===\n"
            f"SOURCE:\nThe hypothesis was validated.\n"
            f"TRANSLATION:\n该假设得到了验证。\n"
            f"===EXAMPLE END==="
        )
    elif expert == 'title':
        system_prompt = (
            f"{base_rules}\n"
            f"Style: Catchy, concise, plain text only.\n\n"
            f"===EXAMPLE START===\n"
            f"SOURCE:\nBreaking News: New Discovery\n"
            f"TRANSLATION:\n重磅消息：新发现\n"
            f"===EXAMPLE END==="
        )
    else:
        if not context:
            context = "general content"
        system_prompt = (
            f"{base_rules}\nTranslate the text. the context is {context}"
        )

    # 3. 用户输入格式：生成随机 ID 实现任务隔离
    task_id = str(uuid.uuid4()).split('-')[0].upper()
    user_prompt = (
        f"TaskID: {task_id}\n"
        f"SOURCE:\n"
        f"{text}\n"
        f"TRANSLATION:\n"
    )

    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_API_URL")
    )
    model = os.getenv("LLM_MODEL")
    retry_delay = 1
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                top_p=0.9,
                presence_penalty=0.2,
                timeout=180,
                max_tokens=max_tokens,
                stop=["===EXAMPLE", "SOURCE:", "（请注意", "(Note"],
            )
            result = response.choices[0].message.content.strip()
            
            # 过滤重复的系统提示词
            if result.startswith("快来看看"):
                if "Check this out" not in text:
                    raise OpenAIError("Model repeated the few-shot example.")

            return result

        except OpenAIError as e:
            print(f'Attempt {attempt + 1} failed: {e}')
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            continue

    return ""


def llm_translate_batch(text_list, context='', source_lang='auto', target_lang='ZH'):
    """
    使用 LLM 批量翻译文本

    :param text_list: 待翻译的文本列表
    :param context: 翻译上下文
    :param source_lang: 源语言
    :param target_lang: 目标语言
    :return: 翻译后的文本列表
    """
    if not isinstance(text_list, list):
        print("llm_translate_batch 要求输入必须是 list 类型")
        return []
    
    if not text_list:
        return []
    
    SEPARATOR = '<<<|||SEP|||>>>'
    batch_size = 5000
    batches = []
    current_batch = []
    current_length = 0

    for text in text_list:
        if text is None:
            continue
            
        text_str = str(text).strip()
        if not text_str:
            continue
            
        text_length = len(text_str)

        if current_batch and (current_length + text_length > batch_size):
            batches.append(current_batch)
            current_batch = []
            current_length = 0

        current_batch.append(text_str)
        current_length += text_length

    if current_batch:
        batches.append(current_batch)

    if not batches:
        return []

    all_translated = []
    for idx, batch in enumerate(batches):
        texts = SEPARATOR.join(batch)
        try:
            translated_text = llm_translate('', texts, context, source_lang, target_lang)

            if translated_text:
                translated_parts = translated_text.split(SEPARATOR)
                
                if len(translated_parts) != len(batch):
                    print(f"警告：批次 {idx} 翻译后数量不匹配，期望{len(batch)}条，实际{len(translated_parts)}条")
                    for text in batch:
                        try:
                            translated = llm_translate('title', text, context, source_lang, target_lang)
                            all_translated.append(translated if translated else text)
                        except Exception as e:
                            print(f"单条翻译失败：{str(e)}")
                            all_translated.append(text)
                else:
                    all_translated.extend(translated_parts)
            else:
                print(f"批次 {idx} 翻译返回空值，保留原文")
                all_translated.extend(batch)
                
        except Exception as e:
            print(f"批次 {idx} 翻译失败：{str(e)}")
            all_translated.extend(batch)

    return all_translated
