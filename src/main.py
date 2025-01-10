from textnode import TextNode, TextType


def main():
    textnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(textnode)

if __name__ == "__main__":
    main()