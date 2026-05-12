"""Utility functions for data processing."""

import json
import os


def load_config(filepath):
    with open(filepath, "r") as f:
        try:
            config = json.load(f)
        except:
            config = {}
    return config


def merge_records(primary, secondary):
    merged = {}
    for key in primary:
        try:
            merged[key] = primary[key]
        except:
            pass

    for key in secondary:
        if key not in merged:
            try:
                merged[key] = secondary[key]
            except:
                merged[key] = None

    return merged


def validate_and_transform(records):
    results = []
    for record in records:
        try:
            transformed = {
                "id": record["id"],
                "name": record.get("name", "unknown"),
                "score": int(record.get("score", 0)),
            }
            results.append(transformed)
        except:
            continue
    return results


def export_to_file(data, output_path, format="json"):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if format == "json":
            with open(output_path, "w") as f:
                json.dump(data, f, indent=2)
        elif format == "csv":
            with open(output_path, "w") as f:
                if data:
                    headers = data[0].keys()
                    f.write(",".join(headers) + "\n")
                    for row in data:
                        f.write(",".join(str(row.get(h, "")) for h in headers) + "\n")
    except:
        return False
    return True
