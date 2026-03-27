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


def example_single_translation():
    """示例 1: 单条文本翻译"""
    print("=" * 60)
    print("示例 1: 单条文本翻译")
    print("=" * 60)
    
    # 推特风格翻译
    text = "Breaking news: New technology breakthrough!"
    result = llm_translate('twitter', text, target_lang='ZH')
    print(f"原文：{text}")
    print(f"译文：{result}\n")
    
    # 新闻风格翻译
    text = "The international summit concluded yesterday."
    result = llm_translate('news', text, target_lang='ZH')
    print(f"原文：{text}")
    print(f"译文：{result}\n")
    
    # 学术风格翻译
    text = "The experimental results support our hypothesis."
    result = llm_translate('academic', text, target_lang='ZH')
    print(f"原文：{text}")
    print(f"译文：{result}\n")


def example_batch_translation():
    """示例 2: 批量翻译"""
    print("=" * 60)
    print("示例 2: 批量翻译")
    print("=" * 60)
    
    texts = [
        "Good morning!",
        "How are you doing today?",
        "Have a nice day!",
        "See you later!",
    ]
    
    results = llm_translate_batch(texts, context='general', target_lang='ZH')
    
    for orig, trans in zip(texts, results):
        print(f"原文：{orig}")
        print(f"译文：{trans}\n")


def example_social_media():
    """示例 3: 社交媒体文本（保留@用户名和#标签）"""
    print("=" * 60)
    print("示例 3: 社交媒体文本翻译")
    print("=" * 60)
    
    tweets = [
        "@elonmusk Great news! #SpaceX launch successful!",
        "Check out @NASA's latest Mars mission. #Science",
        "RT @OpenAI: Exciting new AI model released today!",
    ]
    
    results = llm_translate_batch(tweets, context='twitter', target_lang='ZH')
    
    for orig, trans in zip(tweets, results):
        print(f"原文：{orig}")
        print(f"译文：{trans}\n")


def example_chinese_conversion():
    """示例 4: 简繁体转换"""
    print("=" * 60)
    print("示例 4: 简繁体中文转换")
    print("=" * 60)
    
    # 繁体转简体
    traditional_text = "這是一個測試，看看繁體中文轉換效果如何"
    simplified = translate_to_simple_chinese(traditional_text, 't2s')
    print(f"繁体：{traditional_text}")
    print(f"简体：{simplified}\n")
    
    # 简体转繁体
    simplified_text = "这是一个测试，看看简体中文转换效果如何"
    traditional = translate_to_simple_chinese(simplified_text, 's2t')
    print(f"简体：{simplified_text}")
    print(f"繁体：{traditional}\n")


def example_language_detection():
    """示例 5: 语言检测"""
    print("=" * 60)
    print("示例 5: 简繁体中文检测")
    print("=" * 60)
    
    texts = [
        "这是简体中文",
        "這是繁體中文",
        "This is English",
        "混合文本：简体和繁體共存",
    ]
    
    for text in texts:
        lang = language_classify(text)
        lang_name = {
            'zh-Hans': '简体中文',
            'zh-Hant': '繁体中文',
            '': '非中文或其他语言'
        }.get(lang, '未知')
        print(f"文本：{text}")
        print(f"检测结果：{lang} ({lang_name})\n")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("汐语翻译工具 - 使用示例")
    print("=" * 60 + "\n")
    
    # 运行示例
    example_single_translation()
    example_batch_translation()
    example_social_media()
    example_chinese_conversion()
    example_language_detection()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
