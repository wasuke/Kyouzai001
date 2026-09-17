import random

hands = ["グー", "チョキ", "パー"]
player = input("グー・チョキ・パーのどれかを入力してください：").strip()
if player not in hands:
    print("グー・チョキ・パーのどれかで、もう一度実行してね。")
else:
    computer = random.choice(hands)
    print(f"コンピューター：{computer}")
    if player == computer:
        print("あいこ！")
    elif (hands.index(player) - hands.index(computer)) % 3 == 2:
        print("あなたの勝ち！")
    else:
        print("コンピューターの勝ち！")
