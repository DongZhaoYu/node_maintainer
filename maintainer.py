
if __name__ == '__main__':
    parser = CLIFactory.get_parser()
    args = parser.parse_args()
    args.func(args)