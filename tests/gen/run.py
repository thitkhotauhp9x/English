import tokenize


def extract_comments(file_path):
    comments = []
    with open(file_path, 'r') as file:
        tokens = tokenize.generate_tokens(file.readline)
        for token_type, token_string, _, _, _ in tokens:
            if token_type == tokenize.COMMENT:
                comments.append(token_string)
    return comments


comments = extract_comments('do_something.py')
for comment in comments:
    print(comment)
