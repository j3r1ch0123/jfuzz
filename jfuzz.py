#!/usr/bin/env python3.11
import requests
import sys
import getopt

def main(argv):
    url = ''
    wordlist = ''

    try:
        opts, args = getopt.getopt(argv, "hu:w:", ["url=", "wordlist="])

    except getopt.GetoptError:
        print("Format: python3 jfuzz.py -u <url> -w <wordlist>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("Format: python3 jfuzz.py -u <url> -w <wordlist>")
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-w", "--wordlist"):
            wordlist = arg

    with open(wordlist, "r") as words:
        for line in words.readlines():
            fuzz = url + line.strip()  # Corrected line: call strip() on line, not words
            response = requests.get(fuzz)
            print(fuzz, response.status_code)

if __name__ == "__main__":
    main(sys.argv[1:])

