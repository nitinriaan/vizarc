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

    def diagnose(self) -> Dict[str, any]:
        """
        Deep codebase diagnostic scan (Archify diagnose spec):
        - Discovers internal module dependencies
        - Detects circular dependencies / import cycles
        - Identifies architectural coupling hotspots (fan-in / fan-out)
        - Recommends the optimal diagram archetype
        """
        import re
        import importlib

        module_deps: Dict[str, Set[str]] = {}
        all_modules: Set[str] = set()
        file_counts: Dict[str, int] = {}
        
        # Regex matchers for multi-language imports
        py_import_re = re.compile(r"^(?:from\s+([a-zA-Z0-9_\.]+)\s+import|import\s+([a-zA-Z0-9_\.]+))", re.MULTILINE)
        js_import_re = re.compile(r"(?:import\s+.*?from\s+['\"]([^'\"]+)['\"]|require\(['\"]([^'\"]+)['\"]\))")
        go_import_re = re.compile(r"import\s+(?:\(\s*([^)]+)\s*\)|['\"]([^'\"]+)['\"])")

        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            rel_dir = os.path.relpath(root, self.root_path)
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext not in (".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java"):
                    continue

                rel_file = os.path.normpath(os.path.join(rel_dir, file)).replace("\\", "/")
                mod_name = os.path.splitext(rel_file)[0]
                all_modules.add(mod_name)
                module_deps.setdefault(mod_name, set())
                file_counts[ext] = file_counts.get(ext, 0) + 1

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    if ext == ".py":
                        for m1, m2 in py_import_re.findall(content):
                            imported = (m1 or m2).split(".")[0]
                            module_deps[mod_name].add(imported)
                    elif ext in (".js", ".ts", ".jsx", ".tsx"):
                        for m1, m2 in js_import_re.findall(content):
                            target = m1 or m2
                            if target.startswith("."):
                                norm_target = os.path.normpath(os.path.join(os.path.dirname(rel_file), target)).replace("\\", "/")
                                module_deps[mod_name].add(norm_target)
                            else:
                                module_deps[mod_name].add(target)
                    elif ext == ".go":
                        # go imports
                        for block, single in go_import_re.findall(content):
                            txt = block or single
                            for line in txt.splitlines():
                                clean = line.strip().strip('"')
                                if clean:
                                    module_deps[mod_name].add(clean.split("/")[-1])
                except Exception:
                    pass

        # Filter dependencies to internal modules
        internal_adj: Dict[str, Set[str]] = {m: set() for m in all_modules}
        fan_in: Dict[str, int] = {m: 0 for m in all_modules}
        fan_out: Dict[str, int] = {m: 0 for m in all_modules}

        for src, targets in module_deps.items():
            for tgt in targets:
                # Check if matches any internal module prefix
                matching = [m for m in all_modules if m == tgt or m.endswith(f"/{tgt}") or tgt.endswith(f"/{m}")]
                for m in matching:
                    if m != src:
                        internal_adj[src].add(m)

        for src, targets in internal_adj.items():
            fan_out[src] = len(targets)
            for tgt in targets:
                fan_in[tgt] = fan_in.get(tgt, 0) + 1

        # Cycle detection across internal modules
        cycles = []
        visited = {}
        rec_stack = {}

        def find_cycle(u, path):
            visited[u] = True
            rec_stack[u] = True
            for v in internal_adj.get(u, []):
                if not visited.get(v, False):
                    find_cycle(v, path + [v])
                elif rec_stack.get(v, False):
                    cycle_subpath = path[path.index(v):] + [v]
                    cycles.append(" -> ".join(cycle_subpath))
            rec_stack[u] = False

        for mod in all_modules:
            if not visited.get(mod, False):
                find_cycle(mod, [mod])

        # Coupling hotspots
        hotspots = sorted(
            [{"module": m, "fan_in": fan_in[m], "fan_out": fan_out[m], "total": fan_in[m] + fan_out[m]} for m in all_modules],
            key=lambda x: x["total"],
            reverse=True
        )[:5]

        # Determine recommended archetype
        recommended_archetype = "architecture"
        if any(kw in str(all_modules).lower() for kw in ["workflow", "pipeline", "etl", "task"]):
            recommended_archetype = "workflow"
        elif any(kw in str(all_modules).lower() for kw in ["stream", "event", "kafka", "queue"]):
            recommended_archetype = "dataflow"
        elif any(kw in str(all_modules).lower() for kw in ["models", "schema", "entities", "db"]):
            recommended_archetype = "erd"

        return {
            "root_name": self.root_path.name,
            "total_modules": len(all_modules),
            "file_types": file_counts,
            "circular_dependencies": cycles[:5],
            "has_cycles": len(cycles) > 0,
            "coupling_hotspots": hotspots,
            "recommended_archetype": recommended_archetype,
            "summary": (
                f"Analyzed {len(all_modules)} modules in {self.root_path.name}. "
                f"Found {len(cycles)} circular dependencies. "
                f"Top hotspot: {hotspots[0]['module'] if hotspots else 'None'}."
            )
        }
