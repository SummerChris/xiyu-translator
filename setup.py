# -*- coding: utf-8 -*-
"""
汐语翻译工具 - 安装脚本
使用 setuptools 进行包安装
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xiyu-translator",
    version="0.0.1",
    author="XiYu Translator Team",
    author_email="xiyu@example.com",
    description="汐语翻译工具 - 强大的文本翻译工具，支持基于 LLM 的智能翻译和简繁体转换",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/xiyu-translator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "opencc>=1.1.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)
