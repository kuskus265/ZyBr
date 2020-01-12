#!/usr/bin/python
import sys, pyzipper, os, time, argparse, multiprocessing, Crunch, threading

Found = False
password = None

def main():    #definování argumentů
    parser = argparse.ArgumentParser(description="Simple tool to bruteforce crack ZIP files.")
    parser.add_argument("-in", "--input", help="Location of ZIP file to crack", dest="input", type=str, required=True) #Input - Vstupní soubor, uživatel uvee jeho celou cestu
    parser.add_argument("-w", "--wordlist", help="use existing wordlist", dest="wordlist", type=str, required=False) #Jáký použijeme wordlist. Zatím je povinným  další verzi pokud uživatel nedefinuje wordlist, použijí se automaticky nejpoužávanější hesla
    parser.add_argument("-q", "--quiet", help="Quiet mode", dest="q", action='store_true') #Tichý režím - krapet rychlejší, ale uživatel nevidí jak daleko program je.
    parser.add_argument("-m", "--nomulti", help="Enable multithreading", dest="m", action='store_true', default=False)
    parser.add_argument("-c", "--crunch", help="Generate Wordlist using crunch", dest="c", action='store_true')
    parser.set_defaults(func=create_processes)
    args = parser.parse_args()
    args.func(args)

class MultiSplit: #třída, která rozdělí wordlist na několik dílo a každé jádro si vezme jeden
    def __init__(self, args):
        self.args = args

    def get_numbers(self, args):
        ncpu = multiprocessing.cpu_count() #počet jader CPU
        in_file = self.args.wordlist
        count = 0
        print("Creating Multithreading wordlist")
        try:
            with open((in_file), 'rb') as file: #Hledání délky souboru
                for line in file:
                    count += 1
        except Exception:
            print("opening input file failed!")
        print("Length of file: %d lines" % count)
        self.splitline = count // ncpu # vydělí se počet řádků počtem jader, tak se zjistí na kterém řádku doubor rozdělit
        return self.splitline

    def split(self):
        """AKTUÁLNĚ NEFUNKČNÍ, BO SOM KOKOT tato funkce vezme délku z přechozí funnkce a začne rozdělovat soubor. Vygeneruje si soubory podle počtu jader(4 jádrový procesor = 4 soubory. 1.txt, 2.txt, atd.
        otevře původní wordlist a začne kopírovat soubory do nových .txt souborů. když bychom měli wordlist o 8 klíčích a 4 jadrový procesor, funkce to rozdělí tak že budou 4 txt soubory se dvěma klíči
        (8/2 že jo) a ta se později přiradí k procesoru tak, že první jádro zkouší 1.txt, 2 jádro zkouší 2.txt. dál to asi nechám být, není to složíté"""
        copy = False
        i = 1
        x = self.get_numbers(self.args)
        defcount = x
        count = 1
        with open(self.args.wordlist, 'rt') as chunk, open(sys.path[0] + "/data/%s.txt" % str(i), 'wt') as output:
            print("Opened")
            print()
            for line in chunk:
                if copy:
                    if count == x:
                        copy = False
                        output.write(line)
                        i += 1
                        x = defcount * i
                        output.close()
                        output = open(sys.path[0] + "/data/%s.txt" % str(i), 'wt')
                    else:
                        output.write(line)
                elif count < x:
                    copy = True
                    output.write(line)
                    print("......", end="", flush=True) #nejvíc husté UI
                count += 1
        print('\n')
        print("Done\n")


class CrunchImplementation:

    def crunch(self):
        Crunch.generate()

class Process:

    def __init__(self, args):
        self.args = args
        self.ncpu = multiprocessing.cpu_count()
        self.pool = multiprocessing.Pool(processes=self.ncpu)

    def quit(self, result):
        if not result:
            self.pool.terminate()
        if result:
            print("tralalalololo")

    def run(self, args):
        if args.c:
            cr = CrunchImplementation()
            cr.crunch()
            self.args.wordlist = sys.path[0] + "/data/cr_wordlist.txt"
            print(self.args.wordlist)
        if self.args.m:
            split = MultiSplit(args)
            split.split()
            print(self.ncpu)
            time.sleep(2)
            p1 = multiprocessing.Process(target=bruteforce(self, args, 1)).start()
            p2 = multiprocessing.Process(target=bruteforce(self, args, 2)).start()
            p3 = multiprocessing.Process(target=bruteforce(self, args, 3)).start()
            p4 = multiprocessing-Process(target=bruteforce(self, args, 4)).start()
            p1.join()
            p2.join()
            p3.join()
            p4.join()
        else:
            time.sleep(2)
            bruteforce(self, args, 0)

def bruteforce(self, args, n):
    in_zip = args.input
    if self.args.m:
        wl = sys.path[0] + ("/data/%d.txt" % n)
    elif n == 0:
        wl = self.args.wordlist
    print(pyzipper.AESZipFile(in_zip))
    found = False
    global password
    with pyzipper.AESZipFile(in_zip) as zf:
        with open(wl) as wordlist:
            for line in wordlist:
                password = line.strip('\n')
                if not found:
                    try:
                        zf.pwd = str.encode(password)
                        zf.extractall('./')
                        print("password found: %s" % password)
                        p = Process(args)
                        p.quit(found)
                        return
                    except Exception:
                        if args.q:
                            pass
                        else:
                            print(password)

def create_processes(args):
    p = Process(args)
    p.run(args)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(time.time() - start_time)