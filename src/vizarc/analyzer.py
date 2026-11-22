"""
Codebase analyzer: scans local project repositories to extract architecture context.
"""

import os
from pathlib import Path
from typing import Dict, List, Set

IGNORE_DIRS = {
    ".git", ".svn", "node_modules", "venv", ".venv", "env", 
    "__pycache__", "dist", "build", ".next", ".cache", 
    ".idea", ".vscode", "target", "coverage", ".agents"
}

FRAMEWORK_INDICATORS = {
    "package.json": ["express", "next", "react", "vue", "nestjs", "prisma", "mongoose"],
    "requirements.txt": ["fastapi", "django", "flask", "sqlalchemy", "celery", "redis"],
    "go.mod": ["gin-gonic", "fiber", "echo", "gorm"],
    "Cargo.toml": ["axum", "actix-web", "tokio", "diesel", "sqlx"],
    "pom.xml": ["spring-boot", "hibernate"],
}

class CodebaseAnalyzer:
    def __init__(self, root_dir: str):
        self.root_path = Path(root_dir).resolve()

    def analyze(self) -> Dict[str, any]:
        """
        Scans the directory and compiles an architecture summary.
        """
        if not self.root_path.exists():
            raise FileNotFoundError(f"Directory not found: {self.root_path}")

        tree_lines = []
        detected_frameworks = set()
        detected_infra = []
        detected_services = []

        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            rel_dir = os.path.relpath(root, self.root_path)
            depth = rel_dir.count(os.sep)

            # Limit tree depth to 3 levels to avoid context overflow
            if depth < 3:
                indent = "  " * depth
                folder_name = os.path.basename(root)
                if folder_name and folder_name != ".":
                    tree_lines.append(f"{indent}📁 {folder_name}/")

                for file in files:
                    tree_lines.append(f"{indent}  📄 {file}")
                    
                    # Detect infrastructure configs
                    if file in ("Dockerfile", "docker-compose.yml", "docker-compose.yaml"):
                        detected_infra.append(os.path.join(rel_dir, file))
                    
                    # Detect frameworks
                    if file in FRAMEWORK_INDICATORS:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read().lower()
                                for kw in FRAMEWORK_INDICATORS[file]:
                                    if kw in content:
                                        detected_frameworks.add(kw)
                        except Exception:
                            pass

        return {
            "root_name": self.root_path.name,
            "detected_frameworks": sorted(list(detected_frameworks)),
            "detected_infra": detected_infra,
            "directory_tree": "\n".join(tree_lines[:120]),  # capped lines
        }

    def format_summary_for_prompt(self, analysis: Dict[str, any]) -> str:
        """
        Formats analysis results into a prompt context block.
        """
        frameworks_str = ", ".join(analysis["detected_frameworks"]) or "Generic / Custom"
        infra_str = ", ".join(analysis["detected_infra"]) or "None detected"

        return (
            f"PROJECT NAME: {analysis['root_name']}\n"
            f"DETECTED TECH STACK / FRAMEWORKS: {frameworks_str}\n"
            f"INFRASTRUCTURE CONFIGS: {infra_str}\n\n"
            f"DIRECTORY STRUCTURE (Sampled):\n"
            f"{analysis['directory_tree']}\n"
        )
