import argparse

def make_parser():
    parser = argparse.ArgumentParser("Gettext-Markdown")
    parser.add_argument("make", default='pot')
    parser.add_argument("-l", "--language", type=str)
    parser.add_argument("-f", "--folder", type=str)
    parser.add_argument("-c", "--clean", type=bool)
    return parser

args = make_parser().parse_args()
from generate_markdown_generator import GenerateMarkdownGenerator
from clean_py_files import CleanFiles
print(args)
if args.make == 'pot':
    print(args.language.split(','))
    for lang in args.language.split(','):
        GenerateMarkdownGenerator(args.folder, lang).run()
        import generate_pot
        generate_pot.GeneratePot(args.folder, lang).run()
    if args.clean:
        CleanFiles(args.folder).run()
elif args.make == 'md':
    for lang in args.language.split(','):
        GenerateMarkdownGenerator(args.folder, lang).run()
        import generate_markdown
        generate_markdown.GenerateMarkdown(args.folder, lang).run()
    if args.clean:
        CleanFiles(args.folder).run()
elif args.make == 'clean':
    CleanFiles(args.folder).run()
