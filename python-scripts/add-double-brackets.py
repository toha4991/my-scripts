#########################################################################################################################################
# A script that adds double brackets of user's choice to a string.
# 
# Example:
#     input: "Ethernet, ARP, PPP, Frame Relay"
#     output: "[[Ethernet]], [[ARP]], [[PPP]], [[Frame]], [[Relay]]"
#########################################################################################################################################
# Usage:
#       python add-double-brackets.py "TLS, SSL, MIME, ASCII"          
# Output:
#       [[TLS]], [[SSL]], [[MIME]], [[ASCII]]
#########################################################################################################################################
# TODO: allow users to choose the bracket type
#########################################################################################################################################

import re               # to work with patterns in strings
import argparse         # to pass arguments like in a CLI tool

def add_brackets(input_string):
    # Split on &nbsp; while preserving it in the output
    parts = re.split(r'(&nbsp;)', input_string)
    bracketed_parts = []

    for part in parts:
        if part == '&nbsp;':
            bracketed_parts.append(part)
        else:
            # Split further on commas and spaces
            tokens = re.split(r'[,\s]+', part)
            tokens = [f'[[{token}]]' for token in tokens if token]
            bracketed_parts.append(', '.join(tokens))

    return ''.join(bracketed_parts)

def main():
    parser = argparse.ArgumentParser(description="Wrap words in double brackets, handling HTML entities like &nbsp;.")
    parser.add_argument("text", type=str, help="Input string to process")
    args = parser.parse_args()

    result = add_brackets(args.text)
    print(result)

if __name__ == "__main__":
    main()
