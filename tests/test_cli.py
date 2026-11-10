"""Unit and contract tests for the Agentic SDLC CLI (`asdlc`)."""

from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from agentic_sdlc.cli import _safe_within, main


class TestAgenticSdlcCli(unittest.TestCase):
    def _run_cli(self, argv: list[str]) -> tuple[int, str, str]:
        out_buf = io.StringIO()
        err_buf = io.StringIO()
        with redirect_stdout(out_buf), redirect_stderr(err_buf):
            code = main(argv)
        return code, out_buf.getvalue(), err_buf.getvalue()

    def test_list_skills_outputs_12_skills_and_4_personas(self) -> None:
        code, out, err = self._run_cli(["list-skills"])
        self.assertEqual(code, 0, err)
        self.assertIn("Bundled Skills (12):", out)
        self.assertIn("Context-Isolated Personas (4):", out)
        for expected in (
            "sdd-constitution",
            "sdd-specify",
            "add-architect",
            "add-eval",
            "sdlc-sync",
            "spec-critic",
            "security-redteam",
            "eval-verifier",
        ):
            self.assertIn(expected, out)

    def test_init_sdd_mode_scaffolds_only_sdd_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "billing-api"
            code, _, err = self._run_cli(
                ["init", str(root), "--mode", "sdd", "--agent", "universal"]
            )
            self.assertEqual(code, 0, err)
            self.assertTrue((root / "docs/sdlc/SPEC.md").is_file())
            self.assertTrue((root / "docs/sdlc/PLAN.md").is_file())
            self.assertFalse((root / "docs/sdlc/AGENT_SPEC.md").exists())
            self.assertTrue((root / "AGENTS.md").is_file())
            self.assertTrue((root / ".agents/skills/sdd-specify/SKILL.md").is_file())

            v_code, _, v_err = self._run_cli(["validate", str(root)])
            self.assertEqual(v_code, 0, v_err)

    def test_init_add_mode_scaffolds_only_add_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "support-agent"
            code, _, err = self._run_cli(
                ["init", str(root), "--mode", "add", "--agent", "claude"]
            )
            self.assertEqual(code, 0, err)
            self.assertTrue((root / "docs/sdlc/AGENT_SPEC.md").is_file())
            self.assertTrue((root / "docs/sdlc/TOOLS_AND_MCP.md").is_file())
            self.assertTrue((root / "docs/sdlc/EVAL_AND_SAFETY.md").is_file())
            self.assertFalse((root / "docs/sdlc/SPEC.md").exists())
            self.assertTrue((root / "CLAUDE.md").is_file())
            self.assertTrue((root / ".claude/commands/add-architect.md").is_file())
            self.assertTrue((root / ".claude/agents/spec-critic.md").is_file())

            v_code, _, v_err = self._run_cli(["validate", str(root)])
            self.assertEqual(v_code, 0, v_err)

    def test_init_full_mode_all_adapters_and_status_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "unified-platform"
            code, _, err = self._run_cli(
                [
                    "init",
                    str(root),
                    "--mode",
                    "full",
                    "--agent",
                    "all",
                    "--llm",
                    "Gemini / Claude / OpenAI / Kimi",
                    "--stack",
                    "Python 3.12, FastAPI, LangGraph",
                ]
            )
            self.assertEqual(code, 0, err)
            for rel in (
                "AGENTS.md",
                "CLAUDE.md",
                ".cursor/rules/agentic-sdlc.mdc",
                ".github/copilot-instructions.md",
                ".github/prompts/add-eval.prompt.md",
                ".windsurfrules",
                "docs/sdlc/SPEC.md",
                "docs/sdlc/AGENT_SPEC.md",
            ):
                self.assertTrue((root / rel).is_file(), f"Missing {rel}")

            s_code, s_out, s_err = self._run_cli(["status", str(root), "--json"])
            self.assertEqual(s_code, 0, s_err)
            payload = json.loads(s_out)
            self.assertEqual(payload["mode"], "full")
            self.assertEqual(payload["total_tasks"], 3)
            self.assertEqual(payload["pending"], 3)

    def test_non_destructive_reinit_vs_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            self._run_cli(["init", str(root)])
            constitution = root / "docs/sdlc/CONSTITUTION.md"
            constitution.write_text("# Custom Team Constitution\n", encoding="utf-8")

            self._run_cli(["init", str(root)])
            self.assertEqual(
                constitution.read_text(encoding="utf-8"),
                "# Custom Team Constitution\n",
            )

            self._run_cli(["init", str(root), "--force"])
            self.assertIn("Project Constitution", constitution.read_text(encoding="utf-8"))

    def test_validate_catches_dependency_cycles_and_bad_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "cycle-proj"
            self._run_cli(["init", str(root), "--mode", "sdd"])
            progress_file = root / "docs/sdlc/TASK_PROGRESS.json"
            data = json.loads(progress_file.read_text(encoding="utf-8"))
            data["tasks"] = [
                {"id": "T-1", "status": "pending", "depends_on": ["T-2"]},
                {"id": "T-2", "status": "pending", "depends_on": ["T-1"]},
            ]
            progress_file.write_text(json.dumps(data), encoding="utf-8")

            v_code, _, v_err = self._run_cli(["validate", str(root)])
            self.assertEqual(v_code, 1)
            self.assertIn("Dependency cycle", v_err)

    def test_safe_within_blocks_traversal_and_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as base_tmp, tempfile.TemporaryDirectory() as outside_tmp:
            base = Path(base_tmp)
            outside = Path(outside_tmp)

            with self.assertRaises(ValueError):
                _safe_within(base, "../escape.txt")

            link_dir = base / "linked_escape"
            os.symlink(outside, link_dir)
            with self.assertRaises(ValueError):
                _safe_within(base, "linked_escape/secret.txt")


if __name__ == "__main__":
    unittest.main()
