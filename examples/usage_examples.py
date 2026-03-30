# -*- coding: utf-8 -*-
"""
汐语翻译工具使用示例

本文件展示了如何在不同场景下使用 XiYuTranslator
"""
from xiyu_translator import (
    llm_translate,
    llm_translate_batch,
    translate_to_simple_chinese,
    language_classify,
)


def _print_section(title):
    """打印分隔线和标题"""
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"{title}")
    print(f"{separator}\n")


def _print_result(original, translated, label_orig="原文", label_trans="译文"):
    """打印翻译结果"""
    print(f"{label_orig}: {original}")
    print(f"{label_trans}: {translated}\n")


def example_single_translation():
    """示例 1: 单条文本翻译"""
    _print_section("示例 1: 单条文本翻译")
    
    test_cases = [
        ('twitter', "Breaking news: New technology breakthrough!", "推特风格"),
        ('news', "The international summit concluded yesterday.", "新闻风格"),
        ('academic', "The experimental results support our hypothesis.", "学术风格"),
    ]
    
    for expert, text, style in test_cases:
        result = llm_translate(expert, text, target_lang='ZH')
        print(f"【{style}]")
        _print_result(text, result)


def example_batch_translation():
    """示例 2: 批量翻译"""
    _print_section("示例 2: 批量翻译")
    
    texts = [
        "Good morning!",
        "How are you doing today?",
        "Have a nice day!",
        "See you later!",
    ]
    
    results = llm_translate_batch(texts, context='general', target_lang='ZH')
    
    for orig, trans in zip(texts, results):
        _print_result(orig, trans)


def example_social_media():
    """示例 3: 社交媒体文本（保留@用户名和#标签）"""
    _print_section("示例 3: 社交媒体文本翻译")
    
    tweets = [
        "@elonmusk Great news! #SpaceX launch successful!",
        "Check out @NASA's latest Mars mission. #Science",
        "RT @OpenAI: Exciting new AI model released today!",
    ]
    
    results = llm_translate_batch(tweets, context='twitter', target_lang='ZH')
    
    for orig, trans in zip(tweets, results):
        _print_result(orig, trans)


def example_chinese_conversion():
    """示例 4: 简繁体转换"""
    _print_section("示例 4: 简繁体中文转换")
    
    conversion_cases = [
        ('t2s', "這是一個測試，看看繁體中文轉換效果如何", "繁体", "简体"),
        ('s2t', "这是一个测试，看看简体中文转换效果如何", "简体", "繁体"),
    ]
    
    for mode, text, label_orig, label_trans in conversion_cases:
        result = translate_to_simple_chinese(text, mode)
        _print_result(text, result, label_orig, label_trans)


def example_language_detection():
    """示例 5: 语言检测"""
    _print_section("示例 5: 简繁体中文检测")
    
    texts = [
        "这是简体中文",
        "這是繁體中文",
        "This is English",
        "混合文本：简体和繁體共存",
    ]
    
    lang_names = {
        'zh-Hans': '简体中文',
        'zh-Hant': '繁体中文',
        'en': '英文',
        'ja': '日文',
        'ko': '韩文',
        'fr': '法文',
        'de': '德文',
        'es': '西班牙文',
        'hi': '印地文',
        '': '无法识别或其他语言'
    }
    
    for text in texts:
        lang = language_classify(text)
        lang_name = lang_names.get(lang, '未知')
        print(f"文本：{text}")
        print(f"检测结果：{lang} ({lang_name})\n")


def main():
    """运行所有示例"""
    _print_section("汐语翻译工具 - 使用示例")
    
    examples = [
        example_single_translation,
        example_batch_translation,
        example_social_media,
        example_chinese_conversion,
        example_language_detection,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"运行示例 {example_func.__name__} 时出错：{e}\n")
    
    _print_section("所有示例运行完成！")


if __name__ == '__main__':
    main()
