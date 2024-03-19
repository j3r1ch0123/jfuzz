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

format = "Format: python3 jfuzz.py -u <url> -w <wordlist> -t <threads>"

def run(url, wordlist, thread_number):
    threads = []
    for i in range(int(thread_number)):
        thread = threading.Thread(target=main, args=(url, wordlist))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main(url, wordlist):
    for line in wordlist:
        fuzz = url + line.strip()
        response = requests.get(fuzz)
        print(fuzz, response.status_code)

if __name__ == "__main__":
    print(banner)
    url = ''
    wordlist = ''
    thread_number = 5

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:w:t:", ["url=", "wordlist=", "threads="])
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

    with open(wordlist, "r") as words:
        wordlist_lines = words.readlines()

    run(url, wordlist_lines, thread_number)
