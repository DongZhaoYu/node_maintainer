
from cli import CLIFactory
import json

if __name__ == '__main__':
    parser = CLIFactory.get_parser()
    args = parser.parse_args()
    with open("./config.json", "r") as file:
        cfg = json.load(file)
        args.host = cfg["host"] if not args.host else args.host
        args.user = cfg["user"] if not args.user else args.user
        args.passwrd = cfg["password"] if not args.passwrd else args.passwrd
    args.func(args)
