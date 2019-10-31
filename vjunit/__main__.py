import argparse
from vjunit.vjunit import VJunit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="the path of the xml file")
    parser.add_argument(
        "-o", "--output", type=str, help="the path of the generated html file"
    )
    args = parser.parse_args()
    vjunit = VJunit()
    vjunit.convert(args.file, args.output)


if __name__ == "__main__":
    main()
