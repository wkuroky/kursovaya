import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # task_manager_app
SRC = ROOT / "src"
TESTS = ROOT / "tests"

sys.path.insert(0, str(SRC))    # чтобы работали core/storage/ui/...
sys.path.insert(0, str(TESTS))  # чтобы работал импорт tests.fakes
