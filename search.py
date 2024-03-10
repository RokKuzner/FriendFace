import database as db

def find_closest_char(str:str, char:str, start_index:int):
    closes_char = 0
    pointer = start_index
    found = False

    while pointer < len(str):
        if char == str[pointer]:
            found = True
            break
        else:
            closes_char += 1
            pointer += 1

    if found:
        return closes_char
    else:
        return False

def common_char_sequences(str1:str, str2:str):
    pointer_1 = 0
    pointer_2 = 0

    common_char_sequences = 0

    while pointer_1 < len(str1) and pointer_2 < len(str2):
        if str1[pointer_1] == str2[pointer_2]:
            pointer_1 += 1
            pointer_2 += 1

            common_char_sequences += 1
        else:
            closest_to_next_same_char_in_str2 = find_closest_char(str2, str1[pointer_1], pointer_2)
            closest_to_next_same_char_in_str1 = find_closest_char(str1, str2[pointer_2], pointer_1)

            if closest_to_next_same_char_in_str2 and closest_to_next_same_char_in_str1:
                if closest_to_next_same_char_in_str2 < closest_to_next_same_char_in_str1:
                    pointer_2 += closest_to_next_same_char_in_str2
                else:
                    pointer_1 += closest_to_next_same_char_in_str1
            elif closest_to_next_same_char_in_str2:
                pointer_2 += closest_to_next_same_char_in_str2
            elif closest_to_next_same_char_in_str1:
                pointer_1 += closest_to_next_same_char_in_str1
            elif len(str1) > len(str2):
                pointer_1 += 1
            else:
                pointer_2 += 1


    return common_char_sequences

def search(query:str):
    query = query.lower()
    #Get keywords in database that match the query
    keywords = db.get_all_keywords()
    matching_keywords = []
    for keyword in keywords:
        keyword_possibilities = [keyword] + keyword.split()

        for possibility in keyword_possibilities:
            min_chars_for_match = len(possibility)-1 if len(possibility) >= 5 else len(possibility)

            if common_char_sequences(query, possibility) >= min_chars_for_match:
                matching_keywords.append(keyword)
                break

    #Grade posts by keyword count
    posts = {}
    for keyword in matching_keywords:
        for post in db.get_posts_by_keyword(keyword):
            try:
                posts[post] += 1
            except KeyError:
                posts[post] = 1

    posts_by_keyword_count = {}
    for post in posts:
        try:
            posts_by_keyword_count[posts[post]].append(post)
        except KeyError:
            posts_by_keyword_count[posts[post]] = [post]

    sorted_keys = list(posts_by_keyword_count.keys())
    sorted_keys.sort(reverse=True)

    sorted_posts = []
    for key in sorted_keys:
        sorted_posts += posts_by_keyword_count[key]

    return sorted_posts