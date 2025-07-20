"""Utility to execute planning text files.

This script reads plan documents from a directory and performs simple
automation actions based on keywords or embedded Python code snippets.
"""

import os
import re
import subprocess


def extract_python_blocks(text: str) -> list:
    """Return all embedded Python code blocks from the given text."""
    pattern = r"```python\n(.*?)```"
    return re.findall(pattern, text, re.DOTALL)


def execute_plan_actions(plan_text: str, plan_name: str) -> None:
    """Perform simple automation actions based on plan content."""

    print(f"\n🔹 تنفيذ الخطة: {plan_name}")
    print("-" * 60)
    print(plan_text[:300])
    print("\n✅ التحليل ...\n")

    if "إنشاء مجلد" in plan_text or "structure" in plan_text:
        folders = [
            "project_root/src",
            "project_root/assets",
            "project_root/configs",
            "project_root/logs",
            "project_root/ai_agent"
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        print("📁 تم إنشاء هيكل المجلدات.")

    if "README.md" in plan_text:
        with open("project_root/README.md", "w", encoding="utf-8") as f:
            f.write("# مشروع الذكاء الاصطناعي - تم إنشاؤه من الخطة ✅\n")
        print("📄 تم إنشاء README.md.")

    code_blocks = extract_python_blocks(plan_text)
    for i, code in enumerate(code_blocks, 1):
        print(f"⚙️ تنفيذ كود Python رقم {i}...")
        try:
            exec(code, globals())
            print(f"✅ تم تنفيذ كود {i} بنجاح.")
        except Exception as e:
            print(f"❌ خطأ أثناء تنفيذ كود {i}: {e}")


def run_all_plans(folder: str = "plans") -> None:
    """Execute all plan files in the given directory.

    If the directory does not exist but ``plans.zip`` is found, the archive
    will be extracted automatically.
    """

    if not os.path.exists(folder):
        if os.path.exists("plans.zip"):
            subprocess.run(["unzip", "-o", "plans.zip", "-d", folder], check=True)
        else:
            print(f"❌ لم يتم العثور على مجلد الخطط: {folder}")
            return

    def plan_key(name: str) -> int:
        match = re.search(r"(\d+)", name)
        return int(match.group(1)) if match else 0

    files = sorted(
        [f for f in os.listdir(folder) if f.endswith(".txt")],
        key=plan_key
    )

    for file in files:
        path = os.path.join(folder, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            execute_plan_actions(content, file)


if __name__ == "__main__":
    run_all_plans()
