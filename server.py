#!/usr/bin/env python3
"""
Text Inspector MCP Server
------------------------
خادم MCP بسيط يقدم أداة لتحليل النصوص وإرجاع إحصائيات تفصيلية عنها.
تم تطويره باستخدام مكتبة FastMCP الرسمية.
"""

import re
from collections import Counter
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

# 1. إنشاء كائن خادم MCP باسم "Text Inspector MCP"
mcp = FastMCP("Text Inspector MCP")

# 2. تعريف أداة تحليل النصوص (MCP Tool)
@mcp.tool()
def analyze_text(text: str) -> Dict[str, Any]:
    """
    تحليل النص المداخل وإرجاع إحصائيات تفصيلية عنه.

    Args:
        text (str): النص المراد تحليله.

    Returns:
        Dict[str, Any]: قاموس يحتوي على الإحصائيات (عدد الكلمات، الحروف، الجمل، الخ).
    """
    # التعامل مع النصوص الفارغة
    if not text or not text.strip():
        return {
            "error": "النص المدخل فارغ.",
            "word_count": 0,
            "character_count": 0
        }

    # عدد الحروف الإجمالي (مع المساحات)
    char_count = len(text)
    
    # عدد الحروف بدون المساحات والأسطر الجديدة
    char_count_no_spaces = len(re.sub(r'\s+', '', text))

    # استخراج الكلمات (يدعم اللغات التي تستخدم الأبجدية مثل العربية والإنجليزية)
    words = re.findall(r'\w+', text)
    word_count = len(words)

    # استخراج الجمل (تعتمد على علامات الترقيم . ! ؟ ?)
    sentences = [s.strip() for s in re.split(r'[.!?؟]+', text) if s.strip()]
    sentence_count = len(sentences)

    # عدد الأسطر
    line_count = len(text.splitlines())

    # حساب متوسط طول الكلمة
    avg_word_length = round(sum(len(w) for w in words) / word_count, 2) if word_count > 0 else 0

    # أكثر 5 كلمات تكراراً (مع تحويل الكلمات الإنجليزية لحروف صغيرة لتجنب التكرار)
    normalized_words = [w.lower() for w in words]
    most_common_words = dict(Counter(normalized_words).most_common(5))

    # إرجاع النتيجة بصيغة JSON/Dict
    return {
        "metrics": {
            "character_count_total": char_count,
            "character_count_no_spaces": char_count_no_spaces,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "line_count": line_count,
            "average_word_length": avg_word_length
        },
        "most_common_words": most_common_words
    }

# 3. نقطة التشغيل الرئيسية عبر STDIO (Standard I/O)
if __name__ == "__main__":
    # تشغيل الخادم عبر stdio وهو المعيار المتبع في تطبيقات مثل Claude Desktop
    mcp.run(transport="stdio")