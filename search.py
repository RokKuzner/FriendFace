def find_closes_char(str:str, char:str, start_index:int):
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
            closest_to_next_same_char_in_str2 = find_closes_char(str2, str1[pointer_1], pointer_2)
            closest_to_next_same_char_in_str1 = find_closes_char(str1, str2[pointer_2], pointer_1)

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

#print(common_char_sequences("The new iPhone 15 pro max".lower(), "iPhone pro max".lower()))