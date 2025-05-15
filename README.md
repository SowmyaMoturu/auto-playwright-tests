# Playwright Test Generator

A tool to automatically generate Playwright-Cucumber tests from manual test instructions. Designed to work seamlessly within your existing Playwright automation repository.

## Features

- 🤖 Generate Playwright tests from manual instructions
- 📝 Auto-generate feature files, step definitions, and page objects
- 🎭 Optional MFE (Micro Frontend) template integration
- 🏗️ Works directly in your automation repo
- 📊 HAR recording analysis
- 🌳 DOM snapshot processing
- 🎯 data-testid locator preference
- 🔄 Automatic PageObjects.ts updates

## Framework Adaptability

While this generator is optimized for Playwright, it can be adapted for other testing frameworks that use Cucumber. The adaptation process focuses on updating two key prompts:

1. **Step Definition Prompt** (`prompts/step_definition_prompt.md`)
   - Framework-specific action patterns
   - Assertion methods
   - Wait strategies
   - World context setup

2. **Test Generation Prompt** (`prompts/test_generation_prompt.md`)
   - Page object patterns
   - Framework setup code
   - Utility functions
   - Custom commands

The feature file prompt (`prompts/feature_file_prompt.md`) remains unchanged as it's framework-agnostic.

For detailed instructions on adapting these prompts, see [PROMPT_ADAPTATION_GUIDE.md](PROMPT_ADAPTATION_GUIDE.md).

## Prerequisites

- Python 3.8+
- Existing Playwright-Cucumber TypeScript framework
- Optional: MFE React/TypeScript project for template generation

## Installation

1. Copy the generator files to your automation repo:
```bash
cp -r test-generator/* /path/to/your/automation/repo/
```

2. Create and activate a virtual environment:
```bash
cd /path/to/your/automation/repo
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```