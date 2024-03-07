import sys

from book_dir import BookDir


def main():
    dir_path = sys.argv[1]
    BookDir(dir_path).analyze()


if __name__ == "__main__":
    main()
