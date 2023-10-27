def judge_open(input_guess, num_player, player_list, need_output=False):
    """

    :param need_output:
    :param input_guess:
    :param num_player:
    :param player_list:
    :return:
    """
    total_dice = 0
    for i in range(num_player):
        # Fei
        if input_guess[1] != 1 and not input_guess[2]:
            total_dice = int(player_list[i].dice_dict[input_guess[1] - 1]) + player_list[i].dice_dict[0] + total_dice
        else:
            total_dice = int(player_list[i].dice_dict[input_guess[1] - 1]) + total_dice
    if total_dice < input_guess[0]:
        if need_output:
            print('开成功')
        return True
    else:
        if need_output:
            print('开失败')
        return False


def judge_legal_guess(last_guess, this_state, num_player):
    """
    Judge if a this_guess is legal
    :param num_player:
    :param last_guess: last this_guess made by previous player
    :param this_state: this this_guess made by this player
    :return: Bool value. True means legal.
    """
    # Is open or stater
    if this_state[0] <= 0:
        if last_guess[0] == -1:
            return False
        else:
            return True
    # Illegal face
    if this_state[1] < 1 or this_state[1] > 6:
        return False
    # Is Zhai but 1
    if this_state[2] and this_state[1] == 1:
        return False
    # Zhai or 1 but too small
    if (this_state[2] or this_state[1] == 1) and this_state[0] < num_player:
        return False
    # Fei but too small
    if (not this_state[2] and this_state[1] != 1) and this_state[0] <= num_player:
        return False
    # Too big
    if this_state[0] > 5 * num_player:
        return False
    # Both guesses are same Zhai or fei
    if (not last_guess[2] and not this_state[2] and last_guess[1] != 1 and this_state[1] != 1) \
            or (last_guess[2] and this_state[2]) \
            or (last_guess[2] and this_state[1] == 1) \
            or (last_guess[1] == 1 and this_state[2])\
            or (last_guess[1] == 1 and this_state[1] == 1):
        if last_guess[0] < this_state[0]:
            return True
        if last_guess[0] == this_state[0] and last_guess[1] < this_state[1]:
            return True
        else:
            return False
    # Last guess zhai or 1, this guess fei
    if (last_guess[2] or last_guess[1] == 1) and (not this_state[2] and this_state[1] != 1):
        if 2 * last_guess[0] > this_state[0]:
            return False
        else:
            return True
    # Last guess fei, this guess zhai or 1
    if (not last_guess[2] and last_guess[1] != 1) and (this_state[2] or this_state[1] == 1):
        if last_guess[0] // 2 >= this_state[0]:
            return False
        else:
            return True
