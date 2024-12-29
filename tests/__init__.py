import sys
from pathlib import Path

# hack for pytest resolver =/
sys.path.append(str(Path(__file__).parent.parent / "src"))
