
from collections import namedtuple
import argparse

Arg = namedtuple(
    "Arg", ["flags", "help", "action", "default", "nargs", "type", "choices", "metavar"]
)
Arg.__new__.__defaults__ = (None, None, None, None, None, None, None)


def clean(args):
    print("clean with %s" % str(args))
    pass


class CLIFactory(object):
    args = {
        "host_name": Arg(("-u, --host",), "the name of the host", type=str, default="localhost"),
        "user_name": Arg(("-u, --user",), "the name of the user", type=str, default="root"),
        "password": Arg(("-p, --pwd",), "the password of the host", type=str)
    }

    subparsers = (
        {
            "func": clean,
            "help": "clean the obsoleted data on the host.",
            "args": ("host_name", "user_name", "password")
        },
    )
    subparsers_dict = {sp["func"].__name__: sp for sp in subparsers}

    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help="sub-command help", dest="subcommand")
        subparsers.required = True

        for sub_k, sub_v in cls.subparsers_dict.items():
            sub = subparsers.add_parser(sub_k, help=sub_v["help"])
            for arg in sub_v["args"]:
                arg = cls.args[arg]
                kwargs = {
                    f: getattr(arg, f) for f in arg._fields if f != "flags" and getattr(arg, f)
                }
                sub.add_argument(*arg.flags, **kwargs)
            sub.set_defaults(func=sub_v["func"])
        return parser


def get_parser():
    return CLIFactory.get_parser()
