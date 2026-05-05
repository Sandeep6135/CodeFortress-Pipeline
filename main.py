import argparse
import sys
import colorama
from colorama import Fore, Style
from cli.scanner import scan_directory

colorama.init(autoreset=True)

def main():
    parser = argparse.ArgumentParser(description="CodeFortress - Minimal DevSecOps CLI Scanner")
    parser.add_argument("path", help="Directory path to scan for secrets")
    
    args = parser.parse_args()
    
    print(f"{Fore.CYAN}[+] Initializing CodeFortress Scanner...")
    print(f"{Fore.CYAN}[+] Target: {args.path}\n")
    
    findings = scan_directory(args.path)
    
    print("==================================================")
    print("[*] CodeFortress Security Report")
    print("==================================================")
    
    if findings:
        print(f"Status: {Fore.RED}[X] FAILED ({len(findings)} issues detected)\n")
        
        for idx, finding in enumerate(findings, 1):
            # Normalizing path for display
            display_path = finding['file'].replace('\\', '/')
            print(f"{idx}. [{Fore.YELLOW}{finding['type']}{Style.RESET_ALL}] found in {display_path} (Line {finding['line']})")
        
        print(f"\n{Fore.RED}[!] Please remove these secrets before committing.")
        sys.exit(1)
    else:
        print(f"Status: {Fore.GREEN}[v] PASSED (0 secrets found)")
        sys.exit(0)

if __name__ == "__main__":
    main()
