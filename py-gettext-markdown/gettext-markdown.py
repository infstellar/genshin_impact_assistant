import argparse

def make_parser():
    parser = argparse.ArgumentParser("Gettext-Markdown")
    parser.add_argument("make", default='pot')
    parser.add_argument("-l", "--language", type=str)
    parser.add_argument("-f", "--folder", type=str)
    return parser

args = make_parser().parse_args()
from generate_markdown_generator import GenerateMarkdownGenerator
print(args)
if args.make == 'pot':
    print(args.language.split(','))
    for lang in args.language.split(','):
        GenerateMarkdownGenerator(args.folder, lang).run()
        import generate_pot
        generate_pot.GeneratePot(args.folder, lang).run()
elif args.make == 'md':
    for lang in args.language.split(','):
        GenerateMarkdownGenerator(args.folder, lang).run()
        import generate_markdown
        generate_markdown.GenerateMarkdown(args.folder, lang).run()
