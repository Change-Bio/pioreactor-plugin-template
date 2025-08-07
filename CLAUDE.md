# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Plugin Installation and Testing
```bash
# Install plugin for development (from plugin directory)
pip install -e .

# Install plugin on Pioreactor directly
pio install-plugin <plugin-name-with-hyphens>

# Install on all Pioreactors in cluster (run from leader)
pios install-plugin <plugin-name-with-hyphens>

# Run plugin from command line
pio run <PYTHON_FILE_NAME>

# Test plugin functionality
python -m pytest PLUGIN_NAME/TEST_PLUGIN.py
```

### Package Building
```bash
# Build distribution package
python setup.py sdist bdist_wheel

# Check package contents
python -c "from setuptools import find_packages; print(find_packages())"
```

## Architecture Overview

This is a Pioreactor plugin template that provides a structured approach for creating plugins for the Pioreactor bioreactor system. The template demonstrates a relay control plugin as an example.

### Core Plugin Structure

```
PLUGIN_NAME/                    # Main plugin package directory
├── PLUGIN.py                   # Main plugin implementation (BackgroundJobWithDodgingContrib)
├── TEST_PLUGIN.py              # Test suite with example unit tests
├── __init__.py                 # Package imports and entry points
├── additional_config.ini       # Plugin-specific configuration merged with system config
├── additional_sql.sql          # Database schema additions
├── post_install.sh            # Post-installation scripts
├── pre_uninstall.sh           # Pre-uninstall cleanup scripts
├── exportable_datasets/        # Data export configurations
│   └── exportable_dataset.yaml
└── ui/                         # Web UI integration files
    └── contrib/
        ├── jobs/              # Job definition YAML files
        ├── charts/            # Chart configuration for data visualization  
        └── automations/       # Automation definitions
            ├── dosing/        # Dosing automation templates
            ├── led/           # LED control automation templates
            └── temperature/   # Temperature automation templates
```

### Plugin Implementation Pattern

Pioreactor plugins inherit from `BackgroundJobWithDodgingContrib` and follow these key patterns:

1. **Published Settings**: Define user-controllable settings in `published_settings` dict
2. **State Management**: Implement state transitions via `on_*_to_*` methods
3. **Hardware Integration**: Use Pioreactor's PWM and hardware abstractions
4. **MQTT Communication**: Leverage built-in pub/sub for real-time control
5. **OD Dodging**: Implement `action_to_do_before/after_od_reading` for optical density interference

### Configuration System

- `setup.py`: Defines package metadata, dependencies, and entry points
- `additional_config.ini`: Plugin-specific configuration merged with system config
- UI YAML files: Define web interface elements, forms, and charts
- `MANIFEST.in`: Specifies additional files to include in distribution

### Entry Points

Plugins register with Pioreactor via setuptools entry points:
```python
entry_points={
    "pioreactor.plugins": "<PLUGIN_NAME> = <PLUGIN_NAME>"
}
```

### Template Placeholders

When creating new plugins, replace these placeholders:
- `<DISTRIBUTION-NAME>`: Package name with hyphens
- `<PLUGIN_NAME>`: Python package/module name  
- `<VERSION>`, `<DESCRIPTION>`, `<EMAIL>`, `<NAME>`, `<HOMEPAGE>`
- YAML configuration keys and display names

### Testing Framework

The template includes comprehensive test examples covering:
- Plugin initialization with different parameters
- State transitions and hardware control
- MQTT message handling and pub/sub interactions
- OD dodging behavior
- Context manager usage for proper cleanup

## Plugin Development Guide

### Plugin Types

Pioreactor supports three main plugin types:

1. **Background Jobs**: Long-running processes that manage hardware or data collection
2. **Custom Scripts**: One-time execution scripts for specific tasks
3. **Custom Automations**: Rule-based controllers for automated responses

### Plugin Naming Conventions

- **Plugin Name**: Use lowercase with underscores (e.g., `pioreactor_relay_plugin`)
- **Distribution Name**: Use lowercase with hyphens (e.g., `pioreactor-relay-plugin`)
- **File Names**: Use descriptive names matching functionality

### Essential Plugin Metadata

All plugins should include these metadata attributes:
```python
__plugin_summary__ = "Brief description of plugin functionality"
__plugin_version__ = "1.0.0"
__plugin_name__ = "plugin_name"
__plugin_author__ = "Your Name"
__plugin_homepage__ = "https://github.com/your-repo"
```

### Creating a New Plugin from Template

1. **Clone and Rename**: Copy this template directory and rename it
2. **Replace Placeholders**: Update all `<PLACEHOLDER>` values in files:
   - `setup.py`: Update metadata, entry points, dependencies
   - `MANIFEST.in`: Uncomment and update file paths
   - Python files: Replace class names, job names, and functionality
   - YAML files: Update display names, descriptions, and field definitions

3. **Implement Core Logic**: Develop your plugin functionality in `PLUGIN_NAME/PLUGIN.py`
4. **Add Tests**: Create comprehensive tests in `PLUGIN_NAME/TEST_PLUGIN.py`
5. **Configure UI**: Set up YAML files for web interface integration

### UI Integration

#### Background Job YAML Configuration

Create `ui/contrib/jobs/JOB_NAME.yaml`:
```yaml
---
display_name: Human Readable Name
job_name: job_name_as_defined_in_Python
display: true
source: your_plugin_name
description: Description of what your plugin does
published_settings:
  - key: setting_key
    unit: unit_type
    label: Setting Label
    description: Setting description
    type: numeric|boolean|string|json
    default: null
    display: true
```

#### Automation YAML Configuration

Create `ui/contrib/automations/AUTOMATION_NAME.yaml`:
```yaml
---
display_name: Automation Display Name
automation_name: automation_name_as_defined_in_Python
source: your_plugin_name
description: Automation description
fields:
  - key: field_name
    default: default_value
    unit: unit_type
    label: Field Label
    description: Field description
```

#### Chart Configuration

Create `ui/contrib/charts/CHART_KEY.yaml`:
```yaml
---
chart_key: unique_chart_identifier
data_source: sql_table_name
data_source_column: column_to_plot
title: Chart Title
mqtt_topic: truncated/mqtt/topic
y_axis_label: Y-axis Label
fixed_decimals: 2
```

### Development Workflow

1. **Local Development**: Install plugin with `pip install -e .` for development
2. **Test Functionality**: Run tests and manual testing
3. **UI Refresh**: UI updates may take up to 30 seconds to appear
4. **Check Logs**: Monitor `/var/log/pioreactor.log` for errors

### Publishing and Distribution

#### Building Package
```bash
# Install build dependencies
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*
```

#### Publishing to PyPI
```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

#### Community Submission
Submit your plugin to the Pioreactor community plugin repository via GitHub issue or pull request.

### Best Practices

- **Avoid Blocking Code**: Don't use long-running loops or blocking operations
- **Use Context Managers**: Implement proper cleanup with `__enter__` and `__exit__`
- **Error Handling**: Include comprehensive error handling and logging
- **Hardware Safety**: Implement fail-safes for hardware control plugins
- **Configuration Validation**: Validate configuration parameters on startup
- **MQTT Topics**: Follow Pioreactor's MQTT topic naming conventions
- **State Management**: Properly handle plugin state transitions and cleanup