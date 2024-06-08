from english.utilities import RegexDict


def main():
    for value in RegexDict("ear").find():
        print(value)


if __name__ == "__main__":
    main()
