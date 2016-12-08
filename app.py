"""
sauda

Usage:
    sauda find <query_string>...
    sauda view <song_id>
    sauda save <song_id>
    sauda clear
    sauda (-i | --interactive)

Help:
    For help using this tool, please open an issue on the Github repository:
    https://github.com/hms91

Options:
    -h --help     Show this screen.
    -i --interactive  Interactive Mode
    -v --version
"""
import cmd
import sys
from docopt import docopt, DocoptExit
from logic import FindLyrics
from prettytable import PrettyTable


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as exit:
            # Thrown when args do not match

            print("You have entered an invalid command!")
            print(exit)
            return

        except SystemExit:
            # Prints the usage for --help

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Interactive (cmd.Cmd):
    prompt = "(sauda)"

    # file = None
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.lyrics_finder = FindLyrics()

    @docopt_cmd
    def do_find(self, args):
        """Usage: find <query_string>..."""
        query = args['<query_string>']
        results = self.lyrics_finder.find(query)

        t = PrettyTable(['ID','Title','Artist'])
        for i in range(len(results)):
            song_id = results[i]['result']['id']
            title = results[i]['result']['title']
            artist = results[i]['result']['primary_artist']['name']

            t.add_row([song_id, title, artist])
        print t

    @docopt_cmd
    def do_view(self, args):
        """Usage: view <song_id>"""
        query = args['<song_id>']
        results = self.lyrics_finder.view_by_id(query)
        print results['song_lyrics']

    @docopt_cmd
    def do_save(self, args):
        """Usage: save <song_id>"""
        query = args['<song_id>']
        self.lyrics_finder.save_song(query)

    @docopt_cmd
    def do_clear(self, arg):
        """Usage: load_people"""
        self.lyrics_finder.clear()

    def do_quit(self, arg):
        """Quits out of the interactive mode"""
        print("Goodbye!")
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt["--interactive"]:
    Interactive().cmdloop()

print(opt)

# if __name__ == '__main__':
#     main()
