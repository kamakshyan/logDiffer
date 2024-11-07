from difflib import unified_diff
from termcolor import colored

class ColoredLogComparer:
    def __init__(self):
        self.patterns = {
            'timestamp': r'\b\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}[.,]\d+\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        }

    def compare_logs(self, file1_path, file2_path):
        try:
            with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
                file1_lines = f1.readlines()
                file2_lines = f2.readlines()

                # Check for common content
                common_lines = set(file1_lines) & set(file2_lines)
                if not common_lines:
                    return [colored("No common content found between the two log files.", 'yellow')]

                diff = list(unified_diff(
                    file1_lines,
                    file2_lines,
                    fromfile=file1_path,
                    tofile=file2_path,
                    lineterm=''
                ))

                if not diff:
                    return [colored("Files are identical", 'green')]

                colored_output = []
                for line in diff:
                    if line.startswith('+'):
                        colored_output.append(colored(line, 'red'))
                    elif line.startswith('-'):
                        colored_output.append(colored(line, 'red'))
                    elif line.startswith('@@'):
                        colored_output.append(colored(line, 'cyan'))
                    else:
                        colored_output.append(colored(line, 'green'))

                return colored_output

        except FileNotFoundError as e:
            return [colored(f"Error: {str(e)}", 'red')]
        except Exception as e:
            return [colored(f"An error occurred: {str(e)}", 'red')]

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Compare two log files and highlight differences')
    parser.add_argument('file1', help='Path to the first log file')
    parser.add_argument('file2', help='Path to the second log file')
    args = parser.parse_args()

    comparer = ColoredLogComparer()
    differences = comparer.compare_logs(args.file1, args.file2)
    for line in differences:
        print(line)

if __name__ == "__main__":
    main()
