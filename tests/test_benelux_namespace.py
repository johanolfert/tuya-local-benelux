"""Validate the independent install without importing Home Assistant."""

import ast
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
DOMAIN = "tuya_local_benelux"
COMPONENT = ROOT / "custom_components" / DOMAIN


class BeneluxNamespaceTest(unittest.TestCase):
    def test_manifest_and_directory_are_independent(self):
        manifest = json.loads((COMPONENT / "manifest.json").read_text())
        self.assertEqual(manifest["domain"], DOMAIN)
        self.assertEqual(manifest["name"], "Tuya Local Benelux")
        self.assertFalse((ROOT / "custom_components" / "tuya_local").exists())
        const = ast.parse((COMPONENT / "const.py").read_text())
        assignment = next(
            node
            for node in const.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "DOMAIN"
                for target in node.targets
            )
        )
        self.assertEqual(ast.literal_eval(assignment.value), DOMAIN)

    def test_no_imports_from_original_component(self):
        for path in COMPONENT.rglob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules = [node.module]
                for module in modules:
                    self.assertFalse(
                        module == "custom_components.tuya_local"
                        or module.startswith("custom_components.tuya_local."),
                        f"{path}: {module}",
                    )

    def test_service_selector_uses_benelux(self):
        services = (COMPONENT / "services.yaml").read_text()
        self.assertIn("integration: tuya_local_benelux", services)
        self.assertNotIn("integration: tuya_local\n", services)


if __name__ == "__main__":
    unittest.main()
