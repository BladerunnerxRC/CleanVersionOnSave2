#!/usr/bin/env python3
import os
import sys
import json
import argparse

try:
    import jsonschema
except ImportError:
    sys.stderr.write("Please install jsonschema: pip install jsonschema\n")
    sys.exit(1)


# Schema for manifest.json
MANIFEST_SCHEMA = {
    "type": "object",
    "required": [
        "autodeskProduct", "type", "id", "author",
        "description", "version", "runOnStartup", "main"
    ],
    "properties": {
        "autodeskProduct": {"type": "string"},
        "type": {"enum": ["addin"]},
        "id": {"type": "string"},
        "author": {"type": "string"},
        "description": {"type": "string"},
        "version": {"type": "string"},
        "runOnStartup": {"type": "boolean"},
        "main": {"type": "string"}
    },
    "additionalProperties": False
}


# Schema for data/config.json
CONFIG_SCHEMA = {
    "type": "object",
    "required": [
        "addInId", "autoRunOnStartup",
        "versionControl", "autoRename",
        "notifications", "logging"
    ],
    "properties": {
        "addInId": {"type": "string"},
        "autoRunOnStartup": {"type": "boolean"},
        "versionControl": {
            "type": "object",
            "required": ["versionFile", "versionPattern", "defaultIncrement"],
            "properties": {
                "versionFile": {"type": "string"},
                "versionPattern": {"type": "string"},
                "defaultIncrement": {
                    "enum": ["major", "minor", "patch"]
                }
            },
            "additionalProperties": False
        },
        "autoRename": {
            "type": "object",
            "required": ["enabled", "historyFile"],
            "properties": {
                "enabled": {"type": "boolean"},
                "historyFile": {"type": "string"}
            },
            "additionalProperties": False
        },
        "notifications": {
            "type": "object",
            "required": ["enabled", "showSuccess", "showError"],
            "properties": {
                "enabled": {"type": "boolean"},
                "showSuccess": {"type": "boolean"},
                "showError": {"type": "boolean"}
            },
            "additionalProperties": False
        },
        "logging": {
            "type": "object",
            "required": ["level", "logFile"],
            "properties": {
                "level": {
                    "enum": ["DEBUG", "INFO", "WARN", "ERROR"]
                },
                "logFile": {"type": "string"}
            },
            "additionalProperties": False
        }
    },
    "additionalProperties": False
}


def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to read or parse JSON at '{path}': {e}")


def validate(instance, schema, path):
    try:
        jsonschema.validate(instance=instance, schema=schema)
        print(f"✅  {path} is valid")
        return True
    except jsonschema.ValidationError as ve:
        print(f"❌  Schema validation error in '{path}':\n{ve.message}")
        return False
    except Exception as e:
        print(f"❌  Unexpected error validating '{path}': {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate manifest.json and data/config.json against their schemas."
    )
    parser.add_argument(
        '--manifest', '-m',
        default='manifest.json',
        help='Path to manifest.json'
    )
    parser.add_argument(
        '--config', '-c',
        default=os.path.join('data', 'config.json'),
        help='Path to data/config.json'
    )
    args = parser.parse_args()

    overall_ok = True

    # Validate manifest.json
    try:
        manifest = load_json(args.manifest)
        ok = validate(manifest, MANIFEST_SCHEMA, args.manifest)
        overall_ok = overall_ok and ok
    except RuntimeError as e:
        print(f"❌  {e}")
        overall_ok = False

    # Validate data/config.json
    try:
        cfg = load_json(args.config)
        ok = validate(cfg, CONFIG_SCHEMA, args.config)
        overall_ok = overall_ok and ok
    except RuntimeError as e:
        print(f"❌  {e}")
        overall_ok = False

    sys.exit(0 if overall_ok else 1)


if __name__ == '__main__':
    main()
