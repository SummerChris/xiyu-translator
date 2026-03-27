# 测试 __init__.py
import xiyu_translator
from xiyu_translator import (
    llm_translate,
    llm_translate_batch,
    translate_to_simple_chinese,
    language_classify,
)

print("✓ 所有模块导入成功")
print(f"✓ 版本号：{xiyu_translator.__version__}")
