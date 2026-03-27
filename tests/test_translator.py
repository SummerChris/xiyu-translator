# -*- coding: utf-8 -*-
"""
汐语翻译工具测试套件
"""
from xiyu_translator import llm_translate_batch


def test_llm_translate_batch():
    """
    llm_translate_batch 函数的测试用例
    """
    print("=" * 60)
    print("开始测试 llm_translate_batch 函数")
    print("=" * 60)
    
    # 测试用例 1: 正常列表翻译
    print("\n【测试 1】正常英文句子列表翻译")
    test_list_1 = [
        "Hello, how are you?",
        "The weather is nice today.",
        "I love programming in Python."
    ]
    result_1 = llm_translate_batch(test_list_1, context='general', source_lang='EN', target_lang='ZH')
    print(f"输入数量：{len(test_list_1)}")
    print(f"输出数量：{len(result_1)}")
    for i, (orig, trans) in enumerate(zip(test_list_1, result_1), 1):
        print(f"  {i}. 原文：{orig}")
        print(f"     译文：{trans}\n")
    
    # 测试用例 2: 空列表
    print("\n【测试 2】空列表测试")
    test_list_2 = []
    result_2 = llm_translate_batch(test_list_2)
    print(f"输入数量：{len(test_list_2)}")
    print(f"输出数量：{len(result_2)}")
    print(f"结果：{'通过' if result_2 == [] else '失败'}")
    
    # 测试用例 3: 包含 None 值和空字符串的混合列表
    print("\n【测试 3】包含 None 和空字符串的混合列表")
    test_list_3 = [
        "First sentence",
        None,
        "",
        "   ",
        "Second sentence",
        "Third sentence"
    ]
    result_3 = llm_translate_batch(test_list_3, context='general', source_lang='EN', target_lang='ZH')
    print(f"输入数量：{len(test_list_3)} (包含 None 和空字符串)")
    print(f"输出数量：{len(result_3)}")
    print(f"过滤后的有效翻译：{result_3}")
    
    # 测试用例 4: 单条目列表
    print("\n【测试 4】单条目列表测试")
    test_list_4 = ["Thank you very much!"]
    result_4 = llm_translate_batch(test_list_4, context='general', source_lang='EN', target_lang='ZH')
    print(f"输入数量：{len(test_list_4)}")
    print(f"输出数量：{len(result_4)}")
    if result_4:
        print(f"原文：{test_list_4[0]}")
        print(f"译文：{result_4[0]}")
    
    # 测试用例 5: 非列表输入（错误处理）
    print("\n【测试 5】非列表输入测试（应该是字符串）")
    test_list_5 = "This is a string, not a list"
    result_5 = llm_translate_batch(test_list_5)
    print(f"输入类型：{type(test_list_5)}")
    print(f"输出：{result_5}")
    print(f"结果：{'通过' if result_5 == [] else '失败'}")
    
    # 测试用例 6: 推特风格文本（包含@用户名和标签）
    print("\n【测试 6】推特风格文本（保留@用户名和#标签）")
    test_list_6 = [
        "@elonmusk Great news! #SpaceX",
        "Check out @NASA's latest mission. #Mars",
        "RT @OpenAI: New model released!"
    ]
    result_6 = llm_translate_batch(test_list_6, context='twitter', source_lang='EN', target_lang='ZH')
    print(f"输入数量：{len(test_list_6)}")
    print(f"输出数量：{len(result_6)}")
    for i, (orig, trans) in enumerate(zip(test_list_6, result_6), 1):
        print(f"  {i}. 原文：{orig}")
        print(f"     译文：{trans}\n")
    
    # 测试用例 7: 短文本边界测试
    print("\n【测试 7】极简短文本测试")
    test_list_7 = ["Bye", "OK", "Yes", "No", "Hi"]
    result_7 = llm_translate_batch(test_list_7, context='general', source_lang='EN', target_lang='ZH')
    print(f"输入数量：{len(test_list_7)}")
    print(f"输出数量：{len(result_7)}")
    for i, (orig, trans) in enumerate(zip(test_list_7, result_7), 1):
        print(f"  {i}. {orig} -> {trans}")
    
    print("\n" + "=" * 60)
    print("所有测试完成")
    print("=" * 60)


if __name__ == '__main__':
    test_llm_translate_batch()
