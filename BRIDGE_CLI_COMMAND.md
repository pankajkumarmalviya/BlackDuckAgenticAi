# Bridge CLI Command Reference

## Exact Command Format

The command to execute Bridge CLI is:

```bash
bridge-cli {project_path} --stage polaris --input input.json --out {project_path}/output/output_{UUID}.json --diagnostics
```

## Parameter Breakdown

| Parameter | Description | Example |
|-----------|-------------|---------|
| `{project_path}` | Path to the project being scanned | `/Users/me/myapp` |
| `--stage polaris` | Scan stage (fixed value) | `polaris` |
| `--input input.json` | Input configuration file path | `input.json` |
| `--out` | Output file path with results | `/Users/me/myapp/output/output_550e8400-e29b-41d4-a716-446655440000.json` |
| `--diagnostics` | Enable diagnostic logging | (flag, no value) |

## Variable Replacements at Runtime

```python
# At runtime, replace:
{project_path}  →  /Users/pankajk/myapp
{UUID}          →  550e8400-e29b-41d4-a716-446655440000

# Final command:
bridge-cli /Users/pankajk/myapp --stage polaris --input input.json --out /Users/pankajk/myapp/output/output_550e8400-e29b-41d4-a716-446655440000.json --diagnostics
```

## Python Implementation

```python
import subprocess
import uuid
import os

def execute_bridge_cli(project_path: str) -> str:
    """
    Execute Bridge CLI with the required command
    
    Args:
        project_path: Path to the project directory
        
    Returns:
        Path to output JSON file
    """
    # Generate UUID
    scan_uuid = str(uuid.uuid4())
    
    # Create output directory
    output_dir = os.path.join(project_path, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Build command
    output_file = os.path.join(output_dir, f'output_{scan_uuid}.json')
    
    command = [
        'bridge-cli',
        project_path,
        '--stage', 'polaris',
        '--input', 'input.json',
        '--out', output_file,
        '--diagnostics'
    ]
    
    # Execute
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Bridge CLI failed: {result.stderr}")
    
    return output_file, scan_uuid
```

## Expected Output

- ✅ File created: `/Users/pankajk/myapp/output/output_550e8400-e29b-41d4-a716-446655440000.json`
- ✅ Contains scan results
- ✅ Diagnostic information included

## Key Points

1. **input.json** must exist in current working directory or specified path
2. **output directory** will be created if it doesn't exist
3. **UUID** must be unique for each scan
4. **Diagnostics** flag provides additional logging info
5. **Stage** is always `polaris` for this integration
