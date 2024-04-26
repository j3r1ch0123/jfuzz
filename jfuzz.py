#!/usr/bin/env python3.11
import requests
import sys
import getopt
import threading

banner = """\
     ██╗███████╗██╗   ██╗███████╗███████╗
     ██║██╔════╝██║   ██║╚══███╔╝╚══███╔╝
     ██║█████╗  ██║   ██║  ███╔╝   ███╔╝ 
██   ██║██╔══╝  ██║   ██║ ███╔╝   ███╔╝  
╚█████╔╝██║     ╚██████╔╝███████╗███████╗
 ╚════╝ ╚═╝      ╚═════╝ ╚══════╝╚══════╝
                                                                                         
"""

format = "Format: python3 jfuzz.py -u <url> -w <wordlist> -t <threads> -x <extensions>"

def run(url, wordlist, thread_number, extensions):
    threads = []
    for i in range(int(thread_number)):
        thread = threading.Thread(target=main, args=(url, wordlist, extensions))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main(url, wordlist, extensions):
    for line in wordlist:
        fuzz = url + line.strip() + extensions
        response = requests.get(fuzz)
        if response.status_code == 404:
             continue
        else:
             print(fuzz, response.status_code)

if __name__ == "__main__":
    print(banner)
    url = ""
    wordlist = ""
    thread_number = 1
    extensions = "/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt" # Empty string in case of no extensions

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:w:t:x:", ["url=", "wordlist=", "threads=", "extensions="])
    except getopt.GetoptError:
        print(format)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(format)
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-w", "--wordlist"):
            wordlist = arg
        elif opt in ("-t", "--threads"):
            thread_number = int(arg)
        elif opt in ("-x", "--extensions"):
            extensions = arg


    with open(wordlist, "r") as words:
        wordlist_lines = words.readlines()

    run(url, wordlist_lines, thread_number, extensions)
