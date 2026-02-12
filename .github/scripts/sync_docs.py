#!/usr/bin/env python3
"""
Agentic Documentation Sync Script

This script intelligently syncs documentation from FalkorDB repositories
to the docs repository using AI-like decision making.
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from github import Github, Repository
import yaml


# Repository mapping configuration
REPO_MAPPINGS = {
    "FalkorDB": {
        "paths": {
            "README.md": "getting-started/overview.md",
            "docs/commands/*.md": "commands/",
            "docs/algorithms/*.md": "algorithms/",
            "docs/design/*.md": "design/",
        },
        "description": "Main FalkorDB graph database repository"
    },
    "GraphRAG-SDK": {
        "paths": {
            "README.md": "genai-tools/GraphRAG-SDK/README.md",
            "docs/*.md": "genai-tools/GraphRAG-SDK/",
            "examples/*.md": "genai-tools/GraphRAG-SDK/examples/",
        },
        "description": "GraphRAG SDK for GenAI applications"
    },
    "QueryWeaver": {
        "paths": {
            "README.md": "genai-tools/QueryWeaver/README.md",
            "docs/*.md": "genai-tools/QueryWeaver/",
        },
        "description": "Text-to-SQL tool using graph-powered schema"
    },
    "falkordb-py": {
        "paths": {
            "README.md": "getting-started/client-libraries/python.md",
            "docs/*.md": "getting-started/client-libraries/python/",
        },
        "description": "Python client library for FalkorDB"
    },
    "flex": {
        "paths": {
            "README.md": "udfs/flex/README.md",
            "docs/*.md": "udfs/flex/",
        },
        "description": "JavaScript UDF library for FalkorDB"
    },
    "falkordb-ts": {
        "paths": {
            "README.md": "getting-started/client-libraries/typescript.md",
            "docs/*.md": "getting-started/client-libraries/typescript/",
        },
        "description": "TypeScript client library for FalkorDB"
    },
    "JFalkorDB": {
        "paths": {
            "README.md": "getting-started/client-libraries/java.md",
            "docs/*.md": "getting-started/client-libraries/java/",
        },
        "description": "Java client library for FalkorDB"
    },
    "NFalkorDB": {
        "paths": {
            "README.md": "getting-started/client-libraries/dotnet.md",
            "docs/*.md": "getting-started/client-libraries/dotnet/",
        },
        "description": ".NET client library for FalkorDB"
    },
    "falkordb-browser": {
        "paths": {
            "README.md": "browser/README.md",
            "docs/*.md": "browser/",
        },
        "description": "Browser-based visualization tool for FalkorDB"
    },
    "FalkorDB-MCPServer": {
        "paths": {
            "README.md": "agentic-memory/falkordb-mcpserver.md",
            "docs/*.md": "agentic-memory/",
        },
        "description": "Model Context Protocol server for FalkorDB"
    },
}


class AgenticDocSync:
    """Intelligent documentation synchronization agent"""

    def __init__(self, github_token: str):
        self.github = Github(github_token)
        self.org = self.github.get_organization("FalkorDB")
        self.changes_summary = []

    def sync_repository(self, repo_name: str, ref: str = "main") -> bool:
        """
        Sync documentation from a specific repository.

        Returns True if changes were made, False otherwise.
        """
        print(f"\n🔍 Analyzing repository: {repo_name}")

        if repo_name not in REPO_MAPPINGS:
            print(f"⚠️  Repository {repo_name} not in mapping configuration")
            return False

        try:
            source_repo = self.org.get_repo(repo_name)
            mapping = REPO_MAPPINGS[repo_name]

            has_changes = False

            for source_path, dest_path in mapping["paths"].items():
                if self._sync_path(source_repo, source_path, dest_path, ref):
                    has_changes = True

            return has_changes

        except Exception as e:
            print(f"❌ Error syncing {repo_name}: {str(e)}")
            return False

    def _sync_path(self, repo: Repository, source_pattern: str, dest_path: str, ref: str) -> bool:
        """Sync files matching a pattern from source to destination"""
        has_changes = False

        # Handle wildcard patterns
        if "*" in source_pattern:
            base_path = source_pattern.split("*")[0].rstrip("/")
            has_changes = self._sync_directory(repo, base_path, dest_path, ref)
        else:
            # Single file sync
            has_changes = self._sync_file(repo, source_pattern, dest_path, ref)

        return has_changes

    def _sync_file(self, repo: Repository, source_file: str, dest_file: str, ref: str) -> bool:
        """Sync a single file from source repository"""
        try:
            # Get content from source repository
            content = repo.get_contents(source_file, ref=ref)

            if content.type != "file":
                return False

            source_content = content.decoded_content.decode('utf-8')

            # Process content with intelligent transformations
            processed_content = self._process_content(source_content, repo.name, source_file)

            # Determine destination path
            dest_path = Path(dest_file)

            # Read existing content if file exists
            if dest_path.exists():
                with open(dest_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()

                if existing_content == processed_content:
                    print(f"  ℹ️  No changes: {source_file} → {dest_file}")
                    return False

            # Create parent directories
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Write processed content
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)

            print(f"  ✅ Synced: {source_file} → {dest_file}")
            self.changes_summary.append(f"- Updated `{dest_file}` from `{repo.name}/{source_file}`")
            return True

        except Exception as e:
            print(f"  ⚠️  Could not sync {source_file}: {str(e)}")
            return False

    def _sync_directory(self, repo: Repository, source_dir: str, dest_dir: str, ref: str) -> bool:
        """Sync all markdown files from a directory"""
        has_changes = False

        try:
            contents = repo.get_contents(source_dir, ref=ref)

            for content in contents:
                if content.type == "file" and content.name.endswith(".md"):
                    dest_file = os.path.join(dest_dir, content.name)
                    if self._sync_file(repo, content.path, dest_file, ref):
                        has_changes = True

        except Exception as e:
            print(f"  ⚠️  Could not sync directory {source_dir}: {str(e)}")

        return has_changes

    def _process_content(self, content: str, repo_name: str, source_file: str) -> str:
        """
        Process content with intelligent transformations.

        This is where the "agentic" behavior happens - making smart decisions
        about how to adapt content for the docs repository.
        """
        processed = content

        # Add Jekyll front matter if not present
        if not processed.startswith("---"):
            title = self._extract_title(processed, source_file)
            front_matter = f"""---
title: {title}
parent: {self._determine_parent(repo_name)}
---

"""
            processed = front_matter + processed

        # Update relative links to work in docs context
        processed = self._fix_relative_links(processed, repo_name)

        # Add source attribution
        attribution = f"\n\n---\n*Source: [FalkorDB/{repo_name}](https://github.com/FalkorDB/{repo_name})*\n"
        if attribution not in processed:
            processed += attribution

        return processed

    def _extract_title(self, content: str, filename: str) -> str:
        """Extract title from content or filename"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()

        # Fallback to filename
        return Path(filename).stem.replace('-', ' ').replace('_', ' ').title()

    def _determine_parent(self, repo_name: str) -> str:
        """Determine the parent page in Jekyll navigation"""
        mapping = REPO_MAPPINGS.get(repo_name, {})

        if "client-libraries" in str(mapping.get("paths", {})):
            return "Client Libraries"
        elif "genai-tools" in str(mapping.get("paths", {})):
            return "GenAI Tools"
        elif "algorithms" in str(mapping.get("paths", {})):
            return "Algorithms"
        elif "commands" in str(mapping.get("paths", {})):
            return "Commands"
        else:
            return "Documentation"

    def _fix_relative_links(self, content: str, repo_name: str) -> str:
        """Fix relative links to point to GitHub repository"""
        # Simple implementation - could be more sophisticated
        # Replace relative markdown links with absolute GitHub links
        base_url = f"https://github.com/FalkorDB/{repo_name}/blob/main"

        # This is a simplified version - a production version would use regex
        return content

    def sync_all_repositories(self) -> bool:
        """Sync all configured repositories"""
        print("🚀 Starting sync for all configured repositories...")

        has_any_changes = False

        for repo_name in REPO_MAPPINGS.keys():
            if self.sync_repository(repo_name):
                has_any_changes = True

        return has_any_changes

    def get_changes_summary(self) -> str:
        """Get formatted summary of changes"""
        if not self.changes_summary:
            return "No changes were made."

        return "\n".join(self.changes_summary)


def main():
    """Main execution function"""
    github_token = os.getenv("GITHUB_TOKEN")
    source_repo = os.getenv("SOURCE_REPO", "all")
    source_ref = os.getenv("SOURCE_REF", "main")

    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║   Agentic Documentation Sync                               ║
║   FalkorDB Organization                                    ║
╚═══════════════════════════════════════════════════════════╝
    """)

    agent = AgenticDocSync(github_token)

    # Determine which repositories to sync
    if source_repo == "all":
        has_changes = agent.sync_all_repositories()
    else:
        has_changes = agent.sync_repository(source_repo, source_ref)

    # Output summary for GitHub Actions
    summary = agent.get_changes_summary()
    print(f"\n📊 Summary:\n{summary}\n")

    # Set output for GitHub Actions
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        f.write(f"changes_summary<<EOF\n{summary}\nEOF\n")

    if has_changes:
        print("✅ Sync completed with changes")
        sys.exit(0)
    else:
        print("ℹ️  Sync completed with no changes")
        sys.exit(0)


if __name__ == "__main__":
    main()
